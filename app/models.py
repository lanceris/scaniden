from sqlalchemy import Column, Integer, String, Date, DateTime

from .database import Base


class Identity(Base):
    __tablename__ = 'identities'

    id = Column(Integer, primary_key=True, nullable=False)
    license_number = Column(String(100), nullable=False)
    full_name = Column(String(200), nullable=False)
    address = Column(String(200))
    expires_at = Column(Date)


class Scan(Base):
    __tablename__ = 'scans'

    id = Column(Integer, primary_key=True, nullable=False)
    identity_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    verdict_value = Column(String(50), nullable=False)

