from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel  #defines the shape of the request data (We want users to send correct data)
from sqlalchemy.orm import Session #Session to interact with DB 
from ..database.db import ( #importing all DB helper functions
    get_challenge_quota,
    create_challenge,
    create_challenge_quota,
    reset_quota_if_needed,
    get_user_challenges
)
from ..utils import authenticate_and_get_user_details
from ..database.models import get_db
import json #handling json data
from datetime import datetime

router = APIRouter() #Modular router to organize routes

#Pydantic is used here for Data Validation for a correct POST request. 
#Breakdown:
    #1.Defining a data model called ChallengeRequest (Subclass of BaseModel for data validation functionality)
    #2.Model is expecting a key called "difficulty" w/ a string value associated with it.
    #3.difficulty:str -> telling pydantic that this field is required for the POST request from the user.
class ChallengeRequest(BaseModel):
    difficulty: str

    #This config class is for swagger documentation generation 
    #Helps API users understand what kind of data to send (POST) to the backend
    class Config:
        json_schema_extra = {"example": {"difficulty" : "easy"}}

@router.post("/generate-challenge") #route decorator
async def generate_challenge(request: ChallengeRequest, db:Session = Depends(get_db)):
    
    try:
        user_details = authenticate_and_get_user_details(request)
        user_id = user_details.get("user_id")

        quota = get_challenge_quota(db, user_id)
        if not quota: 
            create_challenge_quota(db, user_id)
        
        quota = reset_quota_if_needed(db, quota)

        if quota.remaining_quota <= 0: 
            raise HTTPException(status_code=429 , details="Quota exhasted")
        
        challenge_data = None

        quota.quota_remaining -= 1
        db.commit()

        return challenge_data

    except Exception as e:
        raise HTTPException(status_code=400, details=str(e))
                        

#Fetches all the challenges created by the user
@router.get("/my-history")
async def my_history(request: Request, db : Session = Depends(get_db)):
    user_details = authenticate_and_get_user_details(request)
    user_id = user_details.get("user_id")

    challenges = get_user_challenges(db, user_id)
    return {"challenges": challenges} #returns JSON

#Fetches user's quota (quota stores: remaining quotas, last reset time, user id)
@router.get("/quota")
async def get_quota(request: Request, db: Session = Depends(get_db)):
    user_details= authenticate_and_get_user_details(request)
    user_id = user_details.get("user_id")

    quota = get_challenge_quota(db, user_id)

    #if no quota record is found, assume first visit and provide with
    if not quota:
        return {
            "user_id" : user_id,
            "quota_remaning": 0,
            "last_reset_date" : datetime.now()
        }
    quota = reset_quota_if_needed(db, quota)
    return quota


#Notes:

    #1. db: Session = Depends(get_db): 
    # It injects the DB session into the router function automatically.
    # You don't have to open or close the DB manually, FastAPI handles 
    # DB session using Dependency injection. 
    #Depends(get_db) tells fastapi -> "When this router runs, I need a database
    #Session so call the get_db function and give me the result (session)