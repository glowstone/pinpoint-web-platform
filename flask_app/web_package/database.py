from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base          # Creates a base class for models

from web_package.config.config_secrets import *

dialect = "mysql://"
host = "sql.mit.edu" 
sqlalchemy_database_uri = dialect + username + ":" + password + "@" + host + "/" + db_name

#engine = create_engine(sqlalchemy_database_uri, convert_unicode=True)
engine = create_engine('sqlite:////tmp/test.db', convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import web_package.models
    Base.metadata.drop_all(bind=engine)             # Only drops tables defined in the model
    Base.metadata.create_all(bind=engine)