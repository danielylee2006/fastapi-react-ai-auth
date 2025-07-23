from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

#determine which type of DB to use (postgres, mysql, etc.)
engine = create_engine('sqlite:///database.db', echo=True)

#Parent class of all tables (ORM mapping)
Base = declarative_base()

class Challenge(Base):
    __tablename__ = 'challenges'

    id = Column(Integer, primary_key=True)
    difficulty = Column(String, nullable=False)
    date_created = Column(DateTime, default=datetime.now)
    created_by = Column(String, nullable=False) #stores user_id
    title = Column(String, nullable=False)
    options = Column(String, nullable=False)
    correct_answer_id = Column(Integer, nullable=False)
    explanation = Column(String, nullable=False)

class ChallengeQuota(Base):
    __tablename__ = 'challenge_quotas'

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False, unique=True)
    quota_remaining = Column(Integer, nullable=False, default=50)
    last_reset_date = Column(DateTime, default=datetime.now)

#Creates Tables in sqlite using the engine
Base.metadata.create_all(engine)

#Session represent a workspace for interacting w/ the DB
#autocommit=false: must explicitly call db.commit() to saves changes in the DB (prevents accidental overwrites)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Ensures a session is closed after use.
#Also prevents creating duplicate sessions for the DB.
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()



