from datetime import date, datetime
from enum import Enum as PyEnum
import re

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    func,
    String,
    Table,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    validates,
    backref,
)

from app.models.base import Base


user_referral = Table(
    'user_referrer',
    Base.metadata,
    Column('user_id', ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    Column(
        'user_referral', ForeignKey('group.id', ondelete='CASCADE'), primary_key=True
    ),
)


class User(Base):
    __tablename__ = 'user'

    id: Mapped[PG_UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
    )
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(150), unique=True, nullable=False, index=True
    )
    password: Mapped[str] = mapped_column(nullable=False)

    referral_code: Mapped[list['ReferralCode']] = relationship(back_populates='user')
    referrals: Mapped[list['User']] = relationship(
        secondary=user_referral,
        primaryjoin=id == user_referral.c.user_id,
        secondaryjoin=id == user_referral.c.referral_id,
        backref=backref('referrals', cascade='all, delete'),
    )

    @validates('email')
    def validate_email(self, key, email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            raise ValueError('Invalid email format')
        return email

    @validates('username')
    def validate_first_name(self, key, first_name):
        username_regex = r'^[\w.@+-]+$'
        if not re.match(username_regex, first_name):
            raise ValueError('First name is invalid')
        return first_name


class ReferralCode(Base):
    __tablename__ = 'referral_code'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[PG_UUID] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    code: Mapped[str] = mapped_column(String(12), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(nullable=False)
    active: Mapped[bool] = mapped_column(nullable=False)

    user: Mapped['User'] = relationship(back_populates='referral_code')

    code_regex = re.compile(
        r'^(?=.*[a-z])'  # At least one lowercase letter
        r'(?=.*[A-Z])'  # At least one uppercase letter
        r'(?=.*\d)'  # At least one digit
        r'[A-Za-z\d]{12,}$'  # Minimum 12 characters (only letters and digits)
    )

    @validates('code')
    def validate_code(self, key, code):
        if not self.code_regex.match(code):
            raise ValueError(
                'Referral code must be at least 12 characters long, '
                'contain at least one uppercase letter, one lowercase letter, and one digit.'
            )
        return code

    @property
    def is_active(self):
        now = datetime.now()
        return self.expires_at > now and self.active

    __table_args__ = (
        UniqueConstraint('user_id', 'active', name='unique_active_referral_code'),
    )
