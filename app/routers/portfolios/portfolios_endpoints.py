# Importamos las librerias necesarias
from datetime import datetime
from fastapi import APIRouter, HTTPException
import yfinance as yf
from models.portfolio import Portfolio

router = APIRouter(prefix="/portfolios", tags=["portfolios"])

# Diccionario para almacenar los portafolios de los usuarios
portfolios_db = {}


@router.post("/{user_id}")
def save_portfolio(user_id: str, portfolio: Portfolio):
    """
    Guarda el portafolio de un usuario.

    Parámetros:
    - user_id: ID único del usuario.
    - portfolio: Diccionario con las acciones y sus ponderaciones.

    Retorna:
    Un mensaje de confirmación.
    """
    # Verificamos si el usuario ya tiene un portafolio guardado
    if user_id in portfolios_db:
        raise HTTPException(status_code=400, detail=f"El usuario {user_id} ya tiene un portafolio guardado")

    # Verificamos que las ponderaciones sumen 100%
    total_weight = sum(portfolio.stocks.values())
    if total_weight != 100:
        raise HTTPException(status_code=400, detail="Las ponderaciones deben sumar 100%")

    # Guardar el portafolio del usuario
    portfolios_db[user_id] = portfolio.stocks
    
    return {"message": f"Portafolio guardado para el usuario {user_id}"}

@router.put("/{user_id}")
def update_portfolio(user_id: str, portfolio: Portfolio):
    """
    Actualiza el portafolio de un usuario.
    Parámetros:
    - user_id: ID único del usuario.
    - portfolio: Diccionario con las acciones y sus nuevas ponderaciones.

    Retorna:
    Un mensaje de confirmación.
    """
    # Verificamos si el usuario ya tiene un portafolio guardado
    if user_id not in portfolios_db:
        raise HTTPException(status_code=404, detail="Portafolio no encontrado para este usuario")

    # Verificamos que las ponderaciones sumen 100%
    total_weight = sum(portfolio.stocks.values())
    if total_weight != 100:
        raise HTTPException(status_code=400, detail="Las ponderaciones deben sumar 100%")

    # Actualizo el portafolio del usuario
    portfolios_db[user_id] = portfolio.stocks
    return {"message": f"Portafolio actualizado para el usuario {user_id}"}

@router.delete("/{user_id}")
def delete_portfolio(user_id: str):
    """
    Elimina el portafolio de un usuario.

    Parámetros:
    - user_id: ID único del usuario.

    Retorna:
    Un mensaje de confirmación.
    """
    if user_id not in portfolios_db:
        raise HTTPException(status_code=404, detail="Portafolio no encontrado para este usuario")

    # Elimino el portafolio del usuario
    del portfolios_db[user_id]
    
    return {"message": f"Portafolio eliminado para el usuario {user_id}"}

@router.get("/{user_id}")
def get_portfolio(user_id: str):
    """
    Obtiene el portafolio de un usuario.
    Parámetros:
    - user_id: ID único del usuario.

    Retorna:
    El portafolio del usuario.
    """
    if user_id not in portfolios_db:
        raise HTTPException(status_code=404, detail="Portafolio no encontrado para este usuario")

    return {"user_id": user_id, "portfolio": portfolios_db[user_id]}


@router.get("/{user_id}/performance")
def get_portfolio_performance(user_id: str, start_date: str, end_date: str):
    """
    Calcula el rendimiento del portafolio de un usuario en un período de tiempo.
    Parámetros:
    - user_id: ID único del usuario.
    - start_date: Fecha de inicio en formato YYYY-MM-DD.
    - end_date: Fecha de fin en formato YYYY-MM-DD.

    Retorna:
    El rendimiento total del portafolio en el período de tiempo seleccionado
    """
    # Verificar si el usuario tiene un portafolio guardado
    if user_id not in portfolios_db:
        raise HTTPException(status_code=404, detail="Portafolio no encontrado para este usuario")

    portfolio = portfolios_db[user_id]

    # Validamos el formato de las fechas
    try:
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido, debe ser YYYY-MM-DD")

    # Obtener los precios históricos de las acciones
    total_return = 0
    for stock, weight in portfolio.items():
        ticker = yf.Ticker(stock)
        history = ticker.history(start=start_date, end=end_date)

        if history.empty:
            raise HTTPException(status_code=404, detail=f"No hay datos disponibles para la acción {stock} en el período seleccionado")

        # Calcular el rendimiento de la acción
        initial_price = history['Close'].iloc[0]
        final_price = history['Close'].iloc[-1]
        stock_return = (final_price - initial_price) / initial_price

        # Ponderar el rendimiento por la ponderación en el portafolio
        weighted_return = stock_return * (weight / 100)
        total_return += weighted_return

    # Pasamos a porcentaje
    total_return = round(total_return * 100, 2)

    return {
        "user_id": user_id,
        "total_return": total_return,
        "start_date": start_date,
        "end_date": end_date
    }