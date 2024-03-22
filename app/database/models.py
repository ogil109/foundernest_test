from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Event(Base):
    __tablename__ = "events"

    # Amplitude event ID?
    amp_id = Column(BigInteger, primary_key=True)

    # Origin
    user_id = Column(BigInteger)
    device_id = Column(String)
    app = Column(Integer)

    # Time attributes
    date = Column(DateTime)
    event_time = Column(BigInteger)
    client_event_time = Column(BigInteger)
    client_upload_time = Column(BigInteger)
    processed_time = Column(BigInteger)
    server_upload_time = Column(BigInteger)
    server_received_time = Column(BigInteger)

    # Location attributes
    country = Column(String)
    region = Column(String)
    city = Column(String)
    language = Column(String)


# Assuming user properties are fixed and not dynamic for every event
class UserProperties(Base):
    __tablename__ = "user_properties"

    # User ID
    user_id = Column(BigInteger, ForeignKey("events.user_id"), primary_key=True)

    # User properties
    admin_dashboard_metabase = Column(Boolean)
    explore = Column(Boolean)
    explore_companies = Column(Boolean)
    explore_prompt_validation = Column(Boolean)
    initial_li_fat_id = Column(String)
    initial_rtd_cid = Column(String)
    subspaces = Column(Boolean)
    user_corporate_id = Column(BigInteger)
    user_corporate_is_demo = Column(Boolean)
    user_corporate_status = Column(String)
    user_role = Column(String)
    user_signup_date = Column(DateTime)
    user_status = Column(String)


class EventMetadata(Base):
    __tablename__ = "event_metadata"

    # Event ID
    amp_id = Column(BigInteger, ForeignKey("events.amp_id"), primary_key=True)

    # Event metadata
    data_type = Column(String)
    event_type = Column(String)

    # Nested data column
    data = Column(JSON)
