from fastapi import FastAPI
import uvicorn
from routers.portfolios.portfolios_endpoints import router as router_portfolios
from routers.stocks.stocks_endpoints import router as router_stocks

app = FastAPI(
    title="DEMO API",
    description="API demo para clase"
    )

@app.get("/")
async def root():
    return {"message": "Bienvenidos a la API"}

app.include_router(router_portfolios)
app.include_router(router_stocks)

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)