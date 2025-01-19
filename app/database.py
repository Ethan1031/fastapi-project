from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
from .config import settings 

# We will not encourage to hardcode our database url here: 
# i. Anyone check the code or access to github will see our password, it's unsecure
# ii. This hardcode url is only works on development or our local machine, 
# we need to make it automatically changes to adapt when we deploy it to production. 
SQLALCHEMY_DATABASE_URL = f'''postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{
    settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'''
print(SQLALCHEMY_DATABASE_URL)


engine =  create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()

# Dependency to get connection or get session with database
# we just keep calling this function everytime we get requests from API endpoints
# perfrom some operations on database like get, update, delete from it
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Optional, not use here, just for reference
# We can choosing using sqlalchemy or psycopg2 to connect with database. 
# while True: 
#     try: 
#         conn = psycopg2.connect(host = 'localhost', database = 'fastAPI', user = 'postgres', 
#         password  = 'e031031e', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection is sucessfull!!")
#     except Exception as error:
#         print("Connection is failed !")
#         print("Error: ", error)
#         time.sleep(2)