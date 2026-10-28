
from pathlib import Path
from datetime import datetime
from typing import Optional
import json

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

# Importante para que joblib encuentre crear_variables
import preparacion


BASE_DIR = Path(__file__).resolve().parent

MODELO_PATH = BASE_DIR / "modelo_riesgo.joblib"
UMBRAL_PATH = BASE_DIR / "umbral_riesgo.json"


# ---------------------------------------------------------
# Cargar modelo y umbral
# ---------------------------------------------------------

modelo = joblib.load(MODELO_PATH)

with open(
    UMBRAL_PATH,
    "r",
    encoding="utf-8"
) as archivo:
    datos_umbral = json.load(archivo)

UMBRAL_RIESGO = float(
    datos_umbral["umbral_top10"]
)


# ---------------------------------------------------------
# Aplicación FastAPI
# ---------------------------------------------------------

app = FastAPI(
    title="API de Riesgo Olist",
    description=(
        "API para estimar la probabilidad de que "
        "un pedido reciba una mala reseña."
    ),
    version="1.0.0"
)


# ---------------------------------------------------------
# Contrato de entrada
# ---------------------------------------------------------

class PedidoEntrada(BaseModel):

    order_id: str

    order_purchase_timestamp: datetime

    order_approved_at: Optional[datetime] = None

    order_delivered_carrier_date: Optional[datetime] = None

    order_delivered_customer_date: datetime

    order_estimated_delivery_date: datetime

    estado_cliente: str

    n_items: int = Field(
        ge=1
    )

    n_vendedores: int = Field(
        ge=1
    )

    precio_total: float = Field(
        gt=0
    )

    flete_total: float = Field(
        ge=0
    )

    peso_total_g: Optional[float] = Field(
        default=None,
        gt=0
    )

    fotos_promedio: Optional[float] = Field(
        default=None,
        ge=0
    )

    categoria: Optional[str] = None

    estado_vendedor: str

    tipo_pago: Optional[str] = None

    cuotas_max: Optional[float] = Field(
        default=None,
        ge=0
    )


# ---------------------------------------------------------
# GET /
# ---------------------------------------------------------

@app.get("/")
def inicio():

    return {
        "estado": "ok",
        "mensaje": "API de riesgo Olist funcionando"
    }


# ---------------------------------------------------------
# POST /riesgo
# ---------------------------------------------------------

@app.post("/riesgo")
def predecir_riesgo(
    pedido: PedidoEntrada
):

    datos = pedido.model_dump()

    # Convertir fechas a texto para conservar
    # el mismo formato utilizado por el contrato
    columnas_fecha = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    for columna in columnas_fecha:

        if datos[columna] is not None:

            datos[columna] = (
                datos[columna]
                .strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )

    entrada = pd.DataFrame(
        [datos]
    )

    probabilidad = float(
        modelo.predict_proba(
            entrada
        )[0, 1]
    )

    riesgo_alto = (
        probabilidad >= UMBRAL_RIESGO
    )

    return {
        "probabilidad": round(
            probabilidad,
            6
        ),
        "riesgo_alto": bool(
            riesgo_alto
        ),
        "umbral": round(
            UMBRAL_RIESGO,
            6
        )
    }
