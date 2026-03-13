from fastapi import APIRouter, HTTPException
from api.connection import create_connection

router = APIRouter()
r = create_connection()