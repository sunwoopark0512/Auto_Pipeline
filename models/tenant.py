from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    api_key = Column(String, unique=True)
    stripe_customer_id = Column(String)
    plan = Column(String, default="free")
    quota = Column(Integer, default=10000)
    used = Column(Integer, default=0)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
