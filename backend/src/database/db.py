from sqlalchemy.orm import Session #database interaction 
from datetime import datetime, timedelta
from . import models #Challenge and ChallengeQuota tables from models

#Queries a challenge quota for a specific user
def get_challenge_quota(db: Session, user_id: str):
    return (db.query(models.ChallengeQuota).filter(models.ChallengeQuota.user_id ==  user_id).first())

#add a default challenge quota for the new user.
def create_challenge_quota(db: Session, user_id: str):
    db_quota = models.ChallengeQuota(user_id=user_id) #intializing new row/object
    db.add(db_quota)
    db.commit()
    db.refresh(db_quota) #refresh the object after committing
    return db_quota

def reset_quota_if_needed(db: Session, quota: models.ChallengeQuota):
    now = datetime.now()
    #more than 24 hours have passed since last quota reset date, 
    if now - quota.last_reset_date > timedelta(hours=24):
        quota.quota_remaining = 10
        quota.last_reset_date = now
        db.commit()
        db.refresh(quota)
    
    return quota

def create_challenge(db: Session,  difficulty: str, created_by: str, title: str, options: str, correct_answer_id: int, explanation: str):
    db_challenge = models.Challenge( #new Challenge obj/row
        difficulty = difficulty, 
        created_by = created_by,
        title=title,
        options=options,
        correct_answer_id=correct_answer_id,
        explanation=explanation
    )

    db.add(db_challenge)
    db.commit()
    db.refresh(db_challenge)
    return db_challenge

#quering all challenges created by a specific user.
def get_user_challenges(db: Session, user_id: str):
    return db.query(models.Challenge).filter(models.Challenge.created_by == user_id).all()

#created_by contains user_id.