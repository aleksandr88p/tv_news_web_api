from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
import os
from urllib.parse import quote
from analize_articles import get_article_groups
from gpt_magic import generate_summary
import datetime
import json
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from some_functions import make_soup_here, find_top_by_platform, platforms_dict
from box_office import connect_to_database, get_last_dates, get_article_by_date, generate_summary_BO

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
encoded_password = quote(db_password, safe='')
db_name = os.getenv('DB_NAME')

table_names = ['deadline_film', 'deadline_tv', 'hollywoodreporter_movies_news',
               'hollywoodreporter_tv_news', 'indiwire_film', 'indiwire_tv',
               'variety_film_news', 'variety_tv_news']

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/news_digest")
async def news_digest(request: Request):
  return templates.TemplateResponse("news_digest.html", {"request": request})

@app.get("/show_tops", response_class=HTMLResponse)
def show_tops(request: Request):
    return templates.TemplateResponse("show_tops.html", {"request": request})

@app.get("/box_office", response_class=HTMLResponse)
async def box_office(request: Request):
    return templates.TemplateResponse("box_office.html", {"request": request})



@app.get("/api/box_office/{date}")
async def get_box_office_summary(date: str):
    # print(date)
    conn = connect_to_database(db_host, db_user, db_password, db_name)

    article = get_article_by_date(conn, date)
    summary = generate_summary_BO(api_key=openai_api_key, article_content=article)
    conn.close()

    return {"summary": summary}

@app.get("/api/box_office/dates/{count}")
async def get_last_article_dates(count: int):
    conn = connect_to_database(db_host, db_user, db_password, db_name)
    last_dates = get_last_dates(count, conn)
    conn.close()
    return {"last_dates": last_dates}

@app.get("/api/top_shows")
def get_top_shows():
    soup = make_soup_here()
    data = find_top_by_platform(platform_dict=platforms_dict, soup=soup)
    print(data)
    return data


@app.post("/news_digest/generate")
async def generate(request: Request):
    form_data = await request.form()
    print("Starting to generate summaries...")
    print(form_data)
    print('**********************')
    days = int(form_data.get("days"))
    query = form_data.get("query")
    article_groups = get_article_groups(days_ago=days, host=db_host,user=db_user, password=encoded_password, database=db_name, table_names=table_names)
    summaries = generate_summary(api_key=openai_api_key, article_groups=article_groups, query=query if query else None)
    return {"summaries": summaries}
