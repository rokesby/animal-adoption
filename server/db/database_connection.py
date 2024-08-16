from contextlib import contextmanager

from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.engine import URL

@contextmanager
def db_session():

    """ Creates a context with an open SQLAlchemy session.
    """
    url = URL.create(
        drivername="postgresql",
        host="localhost",
        database="adoption"
    )
    engine = create_engine(url)
    connection = engine.connect()
    meta = MetaData()
    meta.reflect(bind=engine)
    Base = declarative_base()

    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
    yield db_session
    db_session.commit()
    db_session.close()
    connection.close()
