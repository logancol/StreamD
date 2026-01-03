from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from openai import OpenAI
from dotenv import load_dotenv
import time
import os


app = FastAPI()
load_dotenv() 

DB_URL = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set or not loaded")

client = OpenAI(
  api_key=OPENAI_API_KEY
)


class QueryRequest(BaseModel):
    question: str

def execute_sql(query: str):
    # NEED TO INCLUDE VALIDATION 
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    try:
        cur.execute(query)
        cols = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        return {"columns": cols, "rows": rows}
    finally:
        cur.close()
        conn.close()


SCHEMA = """
CREATE TABLE Player
(
    player_id INT PRIMARY KEY,
    player_full_name VARCHAR(256),
    player_first_name VARCHAR(256),
    player_last_name VARCHAR(256),
    player_is_active BOOLEAN
);

CREATE TABLE Team
(
    team_id INT PRIMARY KEY,
    team_full_name VARCHAR(256),
    team_abbreviation VARCHAR(256),
    team_nickname VARCHAR(256),
    team_city VARCHAR(256)
);

CREATE TABLE Game
(
    game_id INT PRIMARY KEY,
    season_id INT,
    home_team_id INT REFERENCES Team(team_id),
    away_team_id INT REFERENCES Team(team_id),
    game_date DATE,
    season_type TEXT
);

CREATE TABLE pbp_raw_event_shots (
  game_id            BIGINT NOT NULL REFERENCES Game(game_id),
  event_num          INTEGER NOT NULL,    
  event_type         TEXT NOT NULL,  
  event_subtype      TEXT,     

  -- Game context
  season             INTEGER NOT NULL,
  home_score         INTEGER,
  away_score         INTEGER,
  season_type        TEXT NOT NULL,  
  period             INTEGER NOT NULL,
  clock              INTERVAL NOT NULL, 
  home_team_id       INTEGER REFERENCES Team(team_id),
  away_team_id       INTEGER REFERENCES Team(team_id),
  possession_team_id INTEGER,

  primary_player_id  INTEGER,  

  -- Shot context
  shot_x             INTEGER,                  
  shot_y             INTEGER,
  is_three           BOOLEAN,
  shot_made          BOOLEAN,
  points             INTEGER,

  created_at         TIMESTAMP DEFAULT now(),

  PRIMARY KEY (game_id, event_num)
);
"""

def get_sql_from_question(question: str):
    print("Getting sql from question")
    prompt = f"""
    You are a helpful SQL assistant for a play by play NBA statistics tool. The database schema is:

    {SCHEMA}
    
    ABOVE ALL OTHER PRIORITIES, NEVER ALTER THE DATABASE

    Possible values for event_type: Missed Shot, Made Shot

    Possible values for event_subtype: 

    Floating Jump shot
    Step Back Jump shot
    Running Reverse Dunk Shot
    Running Jump Shot
    Putback Dunk Shot
    Layup Shot
    Reverse Dunk Shot
    Running Alley Oop Dunk Shot
    Fadeaway Bank shot
    Driving Finger Roll Layup Shot
    Cutting Dunk Shot
    Driving Layup Shot
    Driving Reverse Dunk Shot
    Step Back Bank Jump Shot
    Turnaround Fadeaway shot
    Turnaround Hook Shot
    Jump Bank Shot
    Cutting Finger Roll Layup Shot
    Running Reverse Layup Shot
    Driving Bank Hook Shot
    Fadeaway Jump Shot
    Putback Layup Shot
    Running Alley Oop Layup Shot
    Dunk Shot
    Driving Dunk Shot
    Turnaround Bank shot
    Running Finger Roll Layup Shot

    Currently, the database contains play by play data for this season only!

    Generate a valid SQL SELECT query to answer the user question: This query should be immediately runnable
    without removing text or stripping whitespace. Do not elaborate beyond the query, this is detrimental to the
    process

    User Question: "{question}"
    SQL:
    """
    response = client.responses.create(
        model="gpt-5-nano",
        input=prompt,
        store=True
    )
    print("Response Recieved")
    sql = response.output_text.strip()
    sql = sql.split("```")[0].strip()
    time.sleep(10)
    return sql

def interpret_sql_response(response: str, query: str, question: str):
    print('Interpreting SQL Response')
    prompt = f"""
    You are a helpful SQL assistant for a play by play NBA statistics tool: the database schema is:

    {SCHEMA}
    
    This was the user's question: {question}

    This was the generated sql query to answer said question: {query}

    This is the response from the postgres database: {response}

    Based on this, please provide a concise summary of the answer for the user
    """
    completion = client.responses.create(
        model="gpt-5-nano",
        input=prompt
    )

    answer = completion.output_text.strip()
    answer = answer.split("```")[0].strip()
    return answer

@app.get("/")
def root():
    return {"hello": "world"}

@app.get("/query")
def get_answer(question: str) -> str:
    sql = get_sql_from_question(question)
    database_answer = execute_sql(sql)
    formatted_response = interpret_sql_response(response=database_answer, query=sql, question=question)
    return formatted_response