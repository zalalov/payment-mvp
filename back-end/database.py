from sqlalchemy.orm import session, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from config import get_configuration

configuration = get_configuration()
Session = session.sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=create_engine(configuration.DB_URI)
)
session = scoped_session(Session)
Base = declarative_base()
