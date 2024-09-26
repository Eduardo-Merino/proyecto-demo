from pydantic import BaseModel
from typing import Dict


# Modelo de datos Pydantic para el portafolio
class Portfolio(BaseModel):
    stocks: Dict[str, float]