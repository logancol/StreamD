from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import openai
import os

