from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import user_router, session_router
from core.db import create_all_tables # Import the function to create tables

# Initialize FastAPI application
app1 = FastAPI(
    title="Chatbot API",
    description="API for managing users and chatbot sessions.",
    version="1.0.0",
)

app1.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (not secure for production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)
# Call this function to create database tables when the application starts
# This will ensure the SQLite database file and tables are set up.
create_all_tables()

# # Include routers
app1.include_router(user_router.router)
app1.include_router(session_router.router)

@app1.get("/", tags=["Root"])
async def read_root():
    """
    Root endpoint for the Chatbot API.
    """
    return {"message": "Welcome to the Chatbot API!"}