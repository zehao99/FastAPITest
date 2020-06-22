import models
from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import Stock
import yfinance as yf
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

app = FastAPI()

templates = Jinja2Templates(directory = "template")

models.Base.metadata.create_all(bind=engine)

class StockRequest(BaseModel):
    symbol: str

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def home(request: Request, forward_pe = None, dividend_yield = None, ma50 = None, ma200 = None, db: Session = Depends(get_db)):
    """
    display the stock screener home / homepage
    """

    stocks = db.query(Stock)

    if forward_pe:
        stocks = stocks.filter(Stock.forward_pe < forward_pe)

    if ma50:
        stocks = stocks.filter(Stock.price > Stock.ma50)
    
    if ma50:
        stocks = stocks.filter(Stock.price > Stock.ma50)

    return templates.TemplateResponse("home.html",{
        "request": request,
        "stocks": stocks,
        "forward_pe": forward_pe
    })


def fetch_stock_data(id: int):
    """
        hold the id and after getting data insert it to database
        async in background task
    """
    db = SessionLocal()
    stock = db.query(Stock). filter(Stock.id == id).first()
    
    yahoo_data = yf.Ticker(stock.symbol)

    stock.ma200 = yahoo_data.info['twoHundredDayAverage']
    stock.ma50 = yahoo_data.info['fiftyDayAverage']
    stock.price = yahoo_data.info['previousClose']
    stock.forward_pe = yahoo_data.info['forwardPE']
    stock.forward_EPS = yahoo_data.info['forwardEps']


    db.add(stock)
    db.commit()

@app.post('/stock')
async def create_stock(stock_request: StockRequest,background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    created a stock and stores it in the databse
    if exist bg_task need async keyword 
    """
    # Pydantic, Dependency Injection, and Background Tasks
    stock = Stock()
    stock.symbol = stock_request.symbol

    db.add(stock)
    db.commit()
    # background here

    background_tasks.add_task(fetch_stock_data, stock.id)

    return {
        "code": "success",
        "message": "shit"
    }

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}