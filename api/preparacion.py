import numpy as np
import pandas as pd

COLUMNAS_CONTRATO = [
    "order_id",
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
    "estado_cliente",
    "n_items",
    "n_vendedores",
    "precio_total",
    "flete_total",
    "peso_total_g",
    "fotos_promedio",
    "categoria",
    "estado_vendedor",
    "tipo_pago",
    "cuotas_max",
]

COLUMNAS_NUMERICAS = [
    "n_items",
    "n_vendedores",
    "precio_total",
    "flete_total",
    "peso_total_g",
    "fotos_promedio",
    "cuotas_max",
    "horas_aprobacion",
    "dias_hasta_transportista",
    "dias_transporte",
    "dias_entrega",
    "dias_prometidos",
    "dias_diferencia_promesa",
    "dias_retraso",
    "dias_anticipacion",
    "precio_por_item",
    "flete_por_item",
    "peso_por_item",
    "flete_relativo",
    "es_multivendedor",
    "es_multiarticulo",
    "dia_semana_compra",
    "hora_compra",
]

COLUMNAS_CATEGORICAS = [
    "estado_cliente",
    "categoria",
    "estado_vendedor",
    "tipo_pago",
]

def _division_segura(numerador, denominador):
    denominador = denominador.replace(0, np.nan)
    resultado = numerador / denominador
    return resultado.replace([np.inf, -np.inf], np.nan)

def crear_variables(df):
    datos = df.copy()

    faltantes = [c for c in COLUMNAS_CONTRATO if c not in datos.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas requeridas por el contrato: {faltantes}")

    columnas_fecha = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    for columna in columnas_fecha:
        datos[columna] = pd.to_datetime(datos[columna], errors="coerce")

    numericas_originales = [
        "n_items",
        "n_vendedores",
        "precio_total",
        "flete_total",
        "peso_total_g",
        "fotos_promedio",
        "cuotas_max",
    ]
    for columna in numericas_originales:
        datos[columna] = pd.to_numeric(datos[columna], errors="coerce")

    datos["horas_aprobacion"] = (
        datos["order_approved_at"] - datos["order_purchase_timestamp"]
    ).dt.total_seconds() / 3600

    datos["dias_hasta_transportista"] = (
        datos["order_delivered_carrier_date"] - datos["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400

    datos["dias_transporte"] = (
        datos["order_delivered_customer_date"] - datos["order_delivered_carrier_date"]
    ).dt.total_seconds() / 86400

    datos["dias_entrega"] = (
        datos["order_delivered_customer_date"] - datos["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400

    datos["dias_prometidos"] = (
        datos["order_estimated_delivery_date"] - datos["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400

    datos["dias_diferencia_promesa"] = (
        datos["order_delivered_customer_date"] - datos["order_estimated_delivery_date"]
    ).dt.total_seconds() / 86400

    datos["dias_retraso"] = datos["dias_diferencia_promesa"].clip(lower=0)
    datos["dias_anticipacion"] = (-datos["dias_diferencia_promesa"]).clip(lower=0)

    datos["precio_por_item"] = _division_segura(datos["precio_total"], datos["n_items"])
    datos["flete_por_item"] = _division_segura(datos["flete_total"], datos["n_items"])
    datos["peso_por_item"] = _division_segura(datos["peso_total_g"], datos["n_items"])
    datos["flete_relativo"] = _division_segura(datos["flete_total"], datos["precio_total"])

    datos["es_multivendedor"] = (datos["n_vendedores"] > 1).astype(int)
    datos["es_multiarticulo"] = (datos["n_items"] > 1).astype(int)

    datos["dia_semana_compra"] = datos["order_purchase_timestamp"].dt.dayofweek
    datos["hora_compra"] = datos["order_purchase_timestamp"].dt.hour

    for columna in COLUMNAS_CATEGORICAS:
        datos[columna] = (
            datos[columna]
            .astype("string")
            .str.strip()
            .replace("", pd.NA)
            .fillna("Desconocido")
        )

    resultado = datos[COLUMNAS_NUMERICAS + COLUMNAS_CATEGORICAS].copy()
    return resultado.replace([np.inf, -np.inf], np.nan)
