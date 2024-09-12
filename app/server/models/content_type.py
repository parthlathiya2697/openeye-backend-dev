import uuid
from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean, Integer

from app.db.base_class import Base


class ContentType(Base):

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    content_name = Column(String)
    order = Column(Integer, nullable=True)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=True)
    title = Column(JSON, nullable=True)
    description = Column(JSON, nullable=True)
    charge_credits = Column(Integer, nullable=True)
    num_copies = Column(Integer, nullable=True)
    color = Column(String, nullable=True)
    image_src = Column(String, nullable=True)
    is_visible = Column(Boolean, nullable=True, default=True)
    num_free_copies = Column(Integer, nullable=True)
    is_free = Column(Boolean, nullable=True)
    dynamic_num_copies = Column(Boolean, default=True)
    content_type_group_id = Column(
        UUID(as_uuid=True), ForeignKey("content_type_groups.id")
    )
    last_updated = Column(DateTime, default=datetime.utcnow, index=True)
    history_v2 = relationship("HistoryV2", back_populates="content_types")
    credit_histories = relationship("CreditHistory", back_populates="content_types")
    x_credit_histories = relationship("XCreditHistory", back_populates="content_types")
    x_rates = relationship("XRate", back_populates="content_types")
    badges = relationship("Badge")
    content_type_groups = relationship("ContentTypeGroup")
