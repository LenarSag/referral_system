from datetime import datetime
import re
from uuid import uuid4

from sqlalchemy import (
    Column,
    ForeignKey,
    func,
    String,
    Table,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    validates,
    backref,
)

from app.models.base import Base
from config import CODE_LENGTH, CODE_REGEX, EMAIL_LENGTH, USERNAME_LENGTH


user_referral = Table(
    'user_referrer',
    Base.metadata,
    Column(
        'user_id',
        ForeignKey('user.id', ondelete='CASCADE'),
        primary_key=True
    ),
    Column(
        'referral_id',
        ForeignKey('user.id', ondelete='CASCADE'),
        primary_key=True
    ),
)


class User(Base):
    __tablename__ = 'user'

    id: Mapped[PG_UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    username: Mapped[str] = mapped_column(
        String(USERNAME_LENGTH), unique=True, nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(
        String(EMAIL_LENGTH), unique=True, nullable=False, index=True
    )
    password: Mapped[str] = mapped_column(nullable=False)

    referral_code: Mapped[list['ReferralCode']] = relationship(
        back_populates='user'
    )
    referrals: Mapped[list['User']] = relationship(
        secondary=user_referral,
        primaryjoin=id == user_referral.c.user_id,
        secondaryjoin=id == user_referral.c.referral_id,
        backref=backref('referred_by', cascade='all, delete'),
    )

    @validates('email')
    def validate_email(self, key, email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            raise ValueError('Invalid email format')
        return email

    @validates('username')
    def validate_username(self, key, first_name):
        username_regex = r'^[\w.@+-]+$'
        if not re.match(username_regex, first_name):
            raise ValueError('First name is invalid')
        return first_name


class ReferralCode(Base):
    __tablename__ = 'referral_code'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[PG_UUID] = mapped_column(
        ForeignKey('user.id', ondelete='CASCADE')
    )
    code: Mapped[str] = mapped_column(
        String(CODE_LENGTH), unique=True, nullable=False, index=True
    )
    expires_at: Mapped[datetime] = mapped_column(nullable=False)

    user: Mapped['User'] = relationship(back_populates='referral_code')

    @validates('code')
    def validate_code(self, key, code):
        if not CODE_REGEX.match(code):
            raise ValueError(
                'Referral code must be at least 12 characters long, '
                'contain at least one uppercase letter, one lowercase letter, '
                'and one digit.'
            )
        return code

    @hybrid_property
    def is_active(self):
        return self.expires_at > datetime.now()

    @is_active.expression
    def is_active(cls):
        return cls.expires_at > func.now()
