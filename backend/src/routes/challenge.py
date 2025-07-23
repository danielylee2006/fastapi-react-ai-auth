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
from ..ai_generator import generate_challenge_with_ai

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

        if quota.quota_remaining <= 0: 
            raise HTTPException(status_code=429 , details="Quota exhasted")
        
        challenge_data = generate_challenge_with_ai(request.difficulty)

        #adds new Challenge Object to the database via create_challenge helper function
        #stores the new challenge object in the new_challenge to use in JSON that we are going to return to frontend
        new_challenge = create_challenge(
            db=db, 
            difficulty=request.difficulty,
            created_by=user_id,
            **challenge_data #fill in rest of challenge data with challenge_data (obj stored variable)
        )

        #reduces remaining quota by one every time a POST request (/generate-challenge) called
        quota.quota_remaining -= 1

        #this commit updates quota_remaning and the added new challenge in the DB.
        db.commit()

        #return Challenge JSON object to the frontend
        return {

            "id" : new_challenge.id,
            "difficulty": request.difficulty,
            "title" : new_challenge.title,
            "options" : json.loads(new_challenge.options), #in the LLM prompt options are generated as strings, so we convert them to JSON
            "correct_answer_id": new_challenge.correct_answer_id,
            "explanation": new_challenge.explanation,
            "timestamp" : new_challenge.date_created.isoformat()

        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
                        

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