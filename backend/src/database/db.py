from sqlalchemy import Session
from datetime import datetime, timedelta
from . import models

def get_challenge_quota(db: Session, user_id: str):

    return (db.query(models.ChallengeQuota).filter(models.ChallengeQuota.user_id ==  user_id).first())