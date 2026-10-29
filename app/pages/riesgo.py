from pathlib import Path

import pandas as pd
import requests
import streamlit as st


# ----------------------------------------------------
# Configuración
# ----------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

ARCHIVO_PEDIDOS = (
    BASE_DIR
    / "data"
    / "pedidos_app.csv"
)

try:
    URL_API = st.secrets["URL_API"]
except Exception:
    URL_API = (
        "https://olist-proyecto-final-ny5r.onrender.com"
    )


# ----------------------------------------------------
# Cargar pedidos
# ----------------------------------------------------

@st.cache_data
def cargar_pedidos():
    return pd.read_csv(
        ARCHIVO_PEDIDOS
    )


pedidos = cargar_pedidos()


# ----------------------------------------------------
# Funciones auxiliares
# ----------------------------------------------------

def valor_texto(valor):
    if pd.isna(valor):
        return ""

    return str(valor)


def valor_numero(valor, defecto=0.0):
    if pd.isna(valor):
        return defecto

    return float(valor)


# ----------------------------------------------------
# Interfaz
# ----------------------------------------------------

st.title(
    "⚠️ Riesgo de mala reseña"
)

st.write(
    """
    Seleccione un pedido, revise sus datos
    y consulte el modelo de riesgo publicado
    mediante la API de FastAPI.
    """
)


# ----------------------------------------------------
# Crear etiquetas amigables para los pedidos
# ----------------------------------------------------

etiquetas_pedidos = {}

for i, fila_pedido in pedidos.iterrows():

    categoria = (
        fila_pedido["categoria"]
        if pd.notna(fila_pedido["categoria"])
        else "Sin categoría"
    )

    precio = (
        fila_pedido["precio_total"]
        if pd.notna(fila_pedido["precio_total"])
        else 0
    )

    etiquetas_pedidos[
        fila_pedido["order_id"]
    ] = (
        f"Pedido {i + 1} · "
        f"{categoria} · "
        f"R$ {precio:.2f}"
    )


# ----------------------------------------------------
# Selección del pedido
# ----------------------------------------------------

order_id = st.selectbox(
    "Seleccione un pedido",
    pedidos["order_id"].tolist(),
    format_func=lambda x:
        etiquetas_pedidos[x]
)


fila = (
    pedidos[
        pedidos["order_id"] == order_id
    ]
    .iloc[0]
)


# ----------------------------------------------------
# Resumen del pedido seleccionado
# ----------------------------------------------------

st.caption(
    f"ID real del pedido: {order_id}"
)


# ----------------------------------------------------
# Formulario
# ----------------------------------------------------

with st.form("formulario_riesgo"):

    st.subheader(
        "Datos del pedido"
    )

    col1, col2 = st.columns(2)

    with col1:

        order_purchase_timestamp = (
            st.text_input(
                "Fecha de compra",
                valor_texto(
                    fila[
                        "order_purchase_timestamp"
                    ]
                )
            )
        )

        order_approved_at = (
            st.text_input(
                "Fecha de aprobación",
                valor_texto(
                    fila[
                        "order_approved_at"
                    ]
                )
            )
        )

        order_delivered_carrier_date = (
            st.text_input(
                "Entrega al transportista",
                valor_texto(
                    fila[
                        "order_delivered_carrier_date"
                    ]
                )
            )
        )

        order_delivered_customer_date = (
            st.text_input(
                "Entrega al cliente",
                valor_texto(
                    fila[
                        "order_delivered_customer_date"
                    ]
                )
            )
        )

        order_estimated_delivery_date = (
            st.text_input(
                "Fecha prometida",
                valor_texto(
                    fila[
                        "order_estimated_delivery_date"
                    ]
                )
            )
        )

        estado_cliente = st.text_input(
            "Estado del cliente",
            valor_texto(
                fila["estado_cliente"]
            )
        )

        n_items = st.number_input(
            "Número de artículos",
            min_value=1,
            value=int(
                fila["n_items"]
            )
        )

        n_vendedores = st.number_input(
            "Número de vendedores",
            min_value=1,
            value=int(
                fila["n_vendedores"]
            )
        )

    with col2:

        precio_total = st.number_input(
            "Precio total",
            min_value=0.01,
            value=valor_numero(
                fila["precio_total"]
            )
        )

        flete_total = st.number_input(
            "Flete total",
            min_value=0.0,
            value=valor_numero(
                fila["flete_total"]
            )
        )

        peso_total_g = st.number_input(
            "Peso total (g)",
            min_value=0.0,
            value=valor_numero(
                fila["peso_total_g"]
            )
        )

        fotos_promedio = st.number_input(
            "Fotos promedio",
            min_value=0.0,
            value=valor_numero(
                fila["fotos_promedio"]
            )
        )

        categoria = st.text_input(
            "Categoría",
            valor_texto(
                fila["categoria"]
            )
        )

        estado_vendedor = st.text_input(
            "Estado del vendedor",
            valor_texto(
                fila["estado_vendedor"]
            )
        )

        tipo_pago = st.text_input(
            "Tipo de pago",
            valor_texto(
                fila["tipo_pago"]
            )
        )

        cuotas_max = st.number_input(
            "Cuotas máximas",
            min_value=0.0,
            value=valor_numero(
                fila["cuotas_max"]
            )
        )

    consultar = st.form_submit_button(
        "Calcular riesgo",
        type="primary"
    )


# ----------------------------------------------------
# Consultar API
# ----------------------------------------------------

if consultar:

    pedido = {
        "order_id": order_id,

        "order_purchase_timestamp":
            order_purchase_timestamp,

        "order_approved_at":
            order_approved_at or None,

        "order_delivered_carrier_date":
            order_delivered_carrier_date or None,

        "order_delivered_customer_date":
            order_delivered_customer_date,

        "order_estimated_delivery_date":
            order_estimated_delivery_date,

        "estado_cliente":
            estado_cliente,

        "n_items":
            int(n_items),

        "n_vendedores":
            int(n_vendedores),

        "precio_total":
            float(precio_total),

        "flete_total":
            float(flete_total),

        "peso_total_g":
            (
                float(peso_total_g)
                if peso_total_g > 0
                else None
            ),

        "fotos_promedio":
            float(fotos_promedio),

        "categoria":
            categoria or None,

        "estado_vendedor":
            estado_vendedor,

        "tipo_pago":
            tipo_pago or None,

        "cuotas_max":
            float(cuotas_max)
    }

    try:

        with st.spinner(
            "Consultando modelo..."
        ):

            respuesta = requests.post(
                f"{URL_API}/riesgo",
                json=pedido,
                timeout=90
            )

        if respuesta.status_code == 200:

            resultado = respuesta.json()

            probabilidad = (
                resultado["probabilidad"]
            )

            riesgo_alto = (
                resultado["riesgo_alto"]
            )

            umbral = (
                resultado.get(
                    "umbral"
                )
            )

            st.subheader(
                "Resultado"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Probabilidad de mala reseña",
                    f"{probabilidad * 100:.2f}%"
                )

            with col2:

                if riesgo_alto:

                    st.error(
                        "🔴 Riesgo alto"
                    )

                else:

                    st.success(
                        "🟢 Riesgo no alto"
                    )

            st.progress(
                min(
                    max(
                        float(probabilidad),
                        0.0
                    ),
                    1.0
                )
            )

            if umbral is not None:

                st.caption(
                    f"Umbral de riesgo alto: "
                    f"{umbral * 100:.2f}%"
                )

            st.caption(
                "El resultado es generado por "
                "el modelo de riesgo desplegado "
                "en Render."
            )

        elif respuesta.status_code == 422:

            st.error(
                "Los datos enviados no cumplen "
                "con el contrato de la API."
            )

            st.json(
                respuesta.json()
            )

        else:

            st.error(
                "La API respondió con un error."
            )

            st.code(
                respuesta.text
            )

    except requests.exceptions.RequestException:

        st.warning(
            """
            La API no respondió. El servicio gratuito
            de Render puede estar iniciándose.
            Intente nuevamente en unos momentos.
            """
        )