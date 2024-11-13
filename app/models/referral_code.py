from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    func,
    String,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    validates,
)

from app.models.base import Base
from config import CODE_LENGTH, CODE_REGEX


class ReferralCode(Base):
    __tablename__ = 'referral_code'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[PG_UUID] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    code: Mapped[str] = mapped_column(
        String(CODE_LENGTH), unique=True, nullable=False, index=True
    )
    expires_at: Mapped[datetime] = mapped_column(nullable=False)

    user: Mapped['User'] = relationship('User', back_populates='referral_code')

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
