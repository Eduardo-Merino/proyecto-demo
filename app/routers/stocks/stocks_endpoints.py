# Importamos las librerias necesarias
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field, EmailStr, constr, validator
from typing import Optional
import yfinance as yf

router = APIRouter(prefix="/stocks", tags=["stocks"])

# Parámetro en la ruta
@router.get("/{symbol}")
def get_stock(symbol: str):
    return {"symbol": symbol, "price": "120 USD"}

# Parámetros de consulta (query)
@router.get("/")
def get_stock_by_query(symbol: str, exchange: str = "NYSE"):
    return {"symbol": symbol, "exchange": exchange, "price": "120 USD"}

@router.get("/{symbol}/price")
def get_stock_price_on_date(symbol: str, date: str):
    """
    Obtiene el precio de la acción en una fecha específica o la fecha hábil más cercana.
    Parámetros:
    - symbol: El símbolo de la acción (ejemplo: AAPL para Apple)
    - date: Fecha en formato YYYY-MM-DD
    
    Retorna:
    - Precio de cierre de la acción en la fecha solicitada o la más cercana disponible.
    """
    try:
        # Convertir la fecha a datetime
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()

        # Descargar los datos de la acción
        stock = yf.Ticker(symbol)
        history = stock.history(start=date_obj - timedelta(days=3), end=date_obj + timedelta(days=3))

        if history.empty:
            raise HTTPException(status_code=404, detail=f"No hay datos disponibles para {symbol} en {date}")

        # Filtrar los datos por la fecha más cercana si no hay datos exactos
        closest_date = min(history.index, key=lambda d: abs(d.date() - date_obj))
        closing_price = history.loc[closest_date]['Close']

        return {
            "symbol": symbol,
            "requested_date": date,
            "closest_date": closest_date.date().isoformat(),
            "closing_price": round(closing_price, 2)
        }

    except ValueError:
        # Manejar error si el formato de la fecha no es válido
        raise HTTPException(status_code=400, detail="El formato de la fecha debe ser YYYY-MM-DD")
    
    except Exception as e:
        # Manejar cualquier otro error
        raise HTTPException(status_code=500, detail=str(e))
    