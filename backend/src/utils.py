from fastapi import HTTPException
from clerk_backend_api import Clerk, AuthenticateRequestOptions
import os
from dotenv import load_dotenv

load_dotenv()

#Create Clerk SDK instance for JWT token authentication
clerk_sdk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))

#Takes in request sent from React (JWT Token)
def authenticate_and_get_user_details(request): 

#Use method from Clerk SDK to validate user's token
    #1. parses the request
    #2. ensures that the requests came from the origins -> "authorized_parties"
    #3. JWT_KEY is used to verify the frontend token's signature is from clerk.
    #4. returns a request_state object with information about the request.
    try: 
        request_state = clerk_sdk.authenticate_request(
            request, 
            AuthenticateRequestOptions(
                authorized_parties=["http://localhost:5173", "http://localhost:5173"],
                jwt_key=os.getenv("JWT_KEY")
            )
        )
        #if user is actually not logged in, raise 401 Exception.
        if not request_state.is_signed_in:
            raise HTTPException(status_code=401, detail="Invalid token")
        #a 401 exception (Unauthorized Access) is appropriate exception to raise
        #bc user is not signed in meaning that the JWT is missing, invalid, or expired
        
        #request_state.payload = decoded JWT Token
        #"Sub" = standard JWT claim for subject which in Clerk's case is the user_id
        user_id = request_state.payload.get("sub")

        #If everything goes well, we return the user_id to the rest of the app
        #(e.g. to get user specific data)
        return {"user_id" : user_id}

    except Exception as e:
        raise HTTPException(status_code=500, details="Invalid credentials")
    #500 exception (internal server error) is valid here bc it is a general
    # catch-all exception. (this section of code catches all error thrown)