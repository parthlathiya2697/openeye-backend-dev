import enum
from sqlalchemy import String, Column, DateTime, JSON, Integer
from sqlalchemy.sql.sqltypes import Boolean, Enum, Float

from server.db.base_class import Base

class UserRole(enum.Enum):
    super_admin = "super_admin"
    admin = "admin"
    member = "member"

class User(Base):
    
    id = Column(String, primary_key=True, unique=True, nullable=False)
    full_name = Column(String, index=True)
    photo_url = Column(String, nullable=True)
    
    role = Column(Enum(UserRole))
    
    email = Column(String, unique=True)
    email_verified = Column(Boolean)
    
    one_time_credits = Column(Float, default=0)
    recurring_credits = Column(Float, default=0)
    lifetime_deal_credits = Column(Float, default=0)
    
    created_date = Column(DateTime)
    last_signed_date = Column(DateTime)
    last_used_date = Column(DateTime)
    
    dial_number = Column(String)
    dial_number_is_verified = Column(Boolean, default=False)

class UserGenerations(Base):
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String)
    
    input_data = Column(JSON)
    output_data = Column(String)
    
    application = Column(String)
    application_tier = Column(String)
