from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base          # Creates a base class for models

from app_pkg import app

engine = create_engine(app.config.get('SQLALCHEMY_DATABASE_URI'), convert_unicode=True)

# CRUD data access for API controller
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


# Base class for models
Base = declarative_base()
Base.query = db_session.query_property()

# Initialize database
def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from app_pkg.blueprints.api import models
    Base.metadata.drop_all(bind=engine)             # Only drops tables defined in the model
    Base.metadata.create_all(bind=engine)