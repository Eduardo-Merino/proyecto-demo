# Librerias necesarias
from fastapi.testclient import TestClient
import pytest

# Dependencias internas
from main import app

# Crear el cliente de pruebas para interactuar con la API, esto nos lo proporciona FastAPI
client = TestClient(app)


# Test para el POST con tres escenarios. Usuario nuevo, usuario duplicado y ponderaciones incorrectas
@pytest.mark.parametrize("user_id, portfolio_data, expected_status, expected_response", [
    ("123", {"stocks": {"AAPL": 50, "GOOG": 50}}, 200, {"message": "Portafolio guardado para el usuario 123"}),
    ("123", {"stocks": {"AAPL": 50, "GOOG": 50}}, 400, {"detail": "El usuario 123 ya tiene un portafolio guardado"}),
    ("456", {"stocks": {"AAPL": 60, "GOOG": 30}}, 400, {"detail": "Las ponderaciones deben sumar 100%"}),
])
def test_save_portfolio(user_id: str, portfolio_data: dict, expected_status: int, expected_response: dict):
    # Enviamos la request
    response = client.post(f"/portfolios/{user_id}", json=portfolio_data)

    # Verificamos la respuesta
    assert response.status_code == expected_status, response.text
    assert response.json() == expected_response


# Tests para el PUT (actualizar portafolio)
@pytest.mark.parametrize("user_id, portfolio_data, expected_status, expected_response", [
    ("123", {"stocks": {"AAPL": 40, "GOOG": 60}}, 200, {"message":"Portafolio actualizado para el usuario 123"}),
    ("456", {"stocks": {"AAPL": 60, "GOOG": 30}}, 404, {"detail":"Portafolio no encontrado para este usuario"}),
])
def test_update_portfolio(user_id: str, portfolio_data: dict, expected_status: int, expected_response: dict):    
    response = client.put(f"/portfolios/{user_id}", json=portfolio_data)

    # Verificar que la respuesta sea la esperada
    assert response.status_code == expected_status, response.text
    assert response.json() == expected_response


# Tests para el GET (obtener portafolio)
@pytest.mark.parametrize("user_id, expected_status, expected_response", [
    ("123", 200, {"user_id": "123", "portfolio": {"AAPL": 40, "GOOG": 60}}),
    ("789", 404, {"detail": "Portafolio no encontrado para este usuario"}),
])
def test_get_portfolio(user_id: str, expected_status: int, expected_response: dict):
    # GET request
    response = client.get(f"/portfolios/{user_id}")

    # Verificar que la respuesta sea la esperada
    assert response.status_code == expected_status, response.text
    assert response.json() == expected_response


# Tests para el DELETE (eliminar portafolio)
@pytest.mark.parametrize("user_id, expected_status, expected_response", [
    ("123", 200, {"message": "Portafolio eliminado para el usuario 123"}),
    ("545", 404, {"detail": "Portafolio no encontrado para este usuario"}),
])
def test_delete_portfolio(user_id: str, expected_status: int, expected_response: dict):
    # DELETE request
    response = client.delete(f"/portfolios/{user_id}")

    # Verificar que la respuesta sea la esperada
    assert response.status_code == expected_status, response.text
    assert response.json() == expected_response