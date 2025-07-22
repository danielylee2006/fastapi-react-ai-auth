from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware #Cross-Orgin Resource Sharing

app = FastAPI()

#middleware controls which origins/domains are allowed access the APP.
app.add_middleware(CORSMiddleware,
                   allow_orgins=["*"], #all websites/domains allowed
                   allow_credentials=True, 
                   allow_methods=["*"], #all HTTP methods allowed ('GET', 'POST', 'PUT', etc.)
                   allow_headers=["*"]) #allows requests to include headers (contains data, Ex: Content-Type)

