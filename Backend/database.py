from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Ytrewq6677%25@localhost/e_com"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://admin:Ytrewq6677%@database-1.c8diyq4uc3r9.us-east-1.rds.amazonaws.com:3306/Ecom"

# mysql -h database-1.c8diyq4uc3r9.us-east-1.rds.amazonaws.com:3306 -u Ytrewq6677% -p

engine=create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
)

SessionLocal =sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()