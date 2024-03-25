from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Event(Base):
    __tablename__ = "events"

    # Composite primary key (assuming user cannot produce multiple events concurrently)
    event_time = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, primary_key=True)

    # Origin
    amp_id = Column(BigInteger)
    device_id = Column(String)
    app = Column(Integer)

    # Time attributes
    date = Column(
        Date
    )
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

    @classmethod
    def get_by_event_time_and_user_id(cls, session, event_time, user_id):
        # Class method to fetch an instance by event_time and user_id
        return (
            session.query(cls)
            .filter_by(event_time=event_time, user_id=user_id)
            .one_or_none()
        )


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
    user_signup_date = Column(Date)
    user_status = Column(String)

    @classmethod
    def get_by_user_id(cls, session, user_id):
        # ORM method to get UserProperties instance by user ID using passed in session
        return session.query(cls).filter_by(user_id=user_id).one_or_none()


class EventMetadata(Base):
    __tablename__ = "event_metadata"

    # Event ID
    event_time = Column(BigInteger, ForeignKey("events.event_time"), primary_key=True)
    user_id = Column(BigInteger, ForeignKey("events.user_id"), primary_key=True)

    # Event metadata
    data_type = Column(String)
    event_type = Column(String)

    # Nested data column
    data = Column(JSON)
