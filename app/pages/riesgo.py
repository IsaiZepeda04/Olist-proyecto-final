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


# ----------------------------------------------------
# URL de la API
# ----------------------------------------------------

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
    return pd.read_csv(ARCHIVO_PEDIDOS)


pedidos = cargar_pedidos()


# ----------------------------------------------------
# Funciones auxiliares
# ----------------------------------------------------

def texto(valor):
    """
    Convierte valores nulos en texto vacío.
    """
    if pd.isna(valor):
        return ""

    return str(valor)


def numero(valor, defecto=0.0):
    """
    Convierte un valor a float.
    """
    if pd.isna(valor):
        return defecto

    return float(valor)


def entero(valor, defecto=0):
    """
    Convierte un valor a entero.
    """
    if pd.isna(valor):
        return defecto

    return int(valor)


def opcional_texto(valor):
    """
    Convierte texto vacío en None.
    """
    valor = str(valor).strip()

    if valor == "":
        return None

    return valor


# ----------------------------------------------------
# Preparar etiqueta de los pedidos
# ----------------------------------------------------

pedidos[
    "order_delivered_customer_date"
] = pd.to_datetime(
    pedidos[
        "order_delivered_customer_date"
    ],
    errors="coerce"
)

pedidos[
    "order_estimated_delivery_date"
] = pd.to_datetime(
    pedidos[
        "order_estimated_delivery_date"
    ],
    errors="coerce"
)


pedidos["dias_retraso_app"] = (
    pedidos[
        "order_delivered_customer_date"
    ]
    -
    pedidos[
        "order_estimated_delivery_date"
    ]
).dt.days


def etiqueta_pedido(fila):

    order_id = str(
        fila["order_id"]
    )

    id_corto = (
        order_id[:8]
        + "..."
    )

    retraso = (
        fila["dias_retraso_app"]
    )

    if pd.isna(retraso):

        estado = (
            "sin dato de retraso"
        )

    elif retraso > 0:

        estado = (
            f"retraso +{int(retraso)} días"
        )

    elif retraso < 0:

        estado = (
            f"entrega {abs(int(retraso))} días antes"
        )

    else:

        estado = (
            "entrega a tiempo"
        )

    return (
        f"{id_corto} · {estado}"
    )


pedidos[
    "etiqueta_pedido"
] = pedidos.apply(
    etiqueta_pedido,
    axis=1
)


# ----------------------------------------------------
# Título
# ----------------------------------------------------

st.title(
    "⚠️ Riesgo de mala reseña"
)

st.write(
    """
    Seleccione un pedido de ejemplo, revise o modifique
    sus datos y consulte el modelo desplegado en la API
    de Render.
    """
)


# ----------------------------------------------------
# Seleccionar pedido
# ----------------------------------------------------

indice_seleccionado = st.selectbox(
    "Pedido de ejemplo",
    pedidos.index,
    format_func=lambda i: (
        pedidos.loc[
            i,
            "etiqueta_pedido"
        ]
    )
)


pedido = pedidos.loc[
    indice_seleccionado
]


st.caption(
    f"ID completo: {pedido['order_id']}"
)


# ----------------------------------------------------
# Información rápida
# ----------------------------------------------------

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Precio",
        f"R$ {numero(pedido['precio_total']):,.2f}"
    )


with col2:

    st.metric(
        "Flete",
        f"R$ {numero(pedido['flete_total']):,.2f}"
    )


with col3:

    retraso_actual = (
        pedido[
            "dias_retraso_app"
        ]
    )

    if pd.isna(retraso_actual):

        texto_retraso = "Sin dato"

    elif retraso_actual > 0:

        texto_retraso = (
            f"+{int(retraso_actual)} días"
        )

    else:

        texto_retraso = (
            f"{int(retraso_actual)} días"
        )

    st.metric(
        "Diferencia de entrega",
        texto_retraso
    )


st.divider()


# ----------------------------------------------------
# Formulario
# ----------------------------------------------------

st.subheader(
    "Datos del pedido"
)

st.write(
    """
    Puede modificar los valores antes de enviar
    el pedido al modelo.
    """
)


with st.form(
    "formulario_riesgo"
):

    col1, col2 = st.columns(2)


    # ------------------------------------------------
    # Columna izquierda
    # ------------------------------------------------

    with col1:

        order_id = st.text_input(
            "Order ID",
            value=texto(
                pedido["order_id"]
            )
        )


        order_purchase_timestamp = st.text_input(
            "Fecha de compra",
            value=texto(
                pedido[
                    "order_purchase_timestamp"
                ]
            )
        )


        order_approved_at = st.text_input(
            "Fecha de aprobación",
            value=texto(
                pedido[
                    "order_approved_at"
                ]
            )
        )


        order_delivered_carrier_date = st.text_input(
            "Fecha entregada al transportista",
            value=texto(
                pedido[
                    "order_delivered_carrier_date"
                ]
            )
        )


        order_delivered_customer_date = st.text_input(
            "Fecha de entrega al cliente",
            value=texto(
                pedido[
                    "order_delivered_customer_date"
                ]
            )
        )


        order_estimated_delivery_date = st.text_input(
            "Fecha estimada de entrega",
            value=texto(
                pedido[
                    "order_estimated_delivery_date"
                ]
            )
        )


        estado_cliente = st.text_input(
            "Estado del cliente",
            value=texto(
                pedido[
                    "estado_cliente"
                ]
            )
        )


        n_items = st.number_input(
            "Número de artículos",
            min_value=1,
            step=1,
            value=max(
                1,
                entero(
                    pedido["n_items"],
                    1
                )
            )
        )


        n_vendedores = st.number_input(
            "Número de vendedores",
            min_value=1,
            step=1,
            value=max(
                1,
                entero(
                    pedido[
                        "n_vendedores"
                    ],
                    1
                )
            )
        )


    # ------------------------------------------------
    # Columna derecha
    # ------------------------------------------------

    with col2:

        precio_total = st.number_input(
            "Precio total (R$)",
            min_value=0.01,
            value=max(
                0.01,
                numero(
                    pedido[
                        "precio_total"
                    ],
                    0.01
                )
            ),
            step=1.0
        )


        flete_total = st.number_input(
            "Flete total (R$)",
            min_value=0.0,
            value=max(
                0.0,
                numero(
                    pedido[
                        "flete_total"
                    ]
                )
            ),
            step=1.0
        )


        peso_total_g = st.number_input(
            "Peso total (g)",
            min_value=0.0,
            value=max(
                0.0,
                numero(
                    pedido[
                        "peso_total_g"
                    ]
                )
            ),
            step=100.0
        )


        fotos_promedio = st.number_input(
            "Fotos promedio",
            min_value=0.0,
            value=max(
                0.0,
                numero(
                    pedido[
                        "fotos_promedio"
                    ]
                )
            ),
            step=1.0
        )


        categoria = st.text_input(
            "Categoría",
            value=texto(
                pedido[
                    "categoria"
                ]
            )
        )


        estado_vendedor = st.text_input(
            "Estado del vendedor",
            value=texto(
                pedido[
                    "estado_vendedor"
                ]
            )
        )


        tipo_pago = st.text_input(
            "Tipo de pago",
            value=texto(
                pedido[
                    "tipo_pago"
                ]
            )
        )


        cuotas_max = st.number_input(
            "Cuotas máximas",
            min_value=0.0,
            value=max(
                0.0,
                numero(
                    pedido[
                        "cuotas_max"
                    ]
                )
            ),
            step=1.0
        )


    enviar = st.form_submit_button(
        "Calcular riesgo",
        type="primary",
        use_container_width=True
    )


# ----------------------------------------------------
# Enviar a la API
# ----------------------------------------------------

if enviar:

    datos = {
        "order_id":
            order_id,

        "order_purchase_timestamp":
            order_purchase_timestamp,

        "order_approved_at":
            opcional_texto(
                order_approved_at
            ),

        "order_delivered_carrier_date":
            opcional_texto(
                order_delivered_carrier_date
            ),

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
                None
                if peso_total_g == 0
                else float(
                    peso_total_g
                )
            ),

        "fotos_promedio":
            float(
                fotos_promedio
            ),

        "categoria":
            opcional_texto(
                categoria
            ),

        "estado_vendedor":
            estado_vendedor,

        "tipo_pago":
            opcional_texto(
                tipo_pago
            ),

        "cuotas_max":
            float(
                cuotas_max
            )
    }


    try:

        with st.spinner(
            "Consultando el modelo..."
        ):

            respuesta = requests.post(
                f"{URL_API}/riesgo",
                json=datos,
                timeout=90
            )


        # --------------------------------------------
        # Respuesta correcta
        # --------------------------------------------

        if respuesta.status_code == 200:

            resultado = (
                respuesta.json()
            )


            probabilidad = float(
                resultado[
                    "probabilidad"
                ]
            )

            riesgo_alto = bool(
                resultado[
                    "riesgo_alto"
                ]
            )

            umbral = float(
                resultado[
                    "umbral"
                ]
            )


            st.divider()

            st.subheader(
                "Resultado de la predicción"
            )


            col1, col2 = st.columns(2)


            with col1:

                st.metric(
                    "Probabilidad de mala reseña",
                    f"{probabilidad * 100:.2f}%"
                )


            with col2:

                st.metric(
                    "Umbral de riesgo alto",
                    f"{umbral * 100:.2f}%"
                )


            st.progress(
                min(
                    max(
                        probabilidad,
                        0.0
                    ),
                    1.0
                )
            )


            if riesgo_alto:

                st.error(
                    """
                    🔴 **Riesgo alto**

                    Este pedido se encuentra dentro
                    del grupo de pedidos que deberían
                    recibir atención prioritaria.
                    """
                )

            else:

                st.success(
                    """
                    🟢 **Riesgo no alto**

                    Este pedido no supera el umbral
                    utilizado para priorizar el 10%
                    de pedidos con mayor riesgo.
                    """
                )


            st.caption(
                f"""
                Umbral utilizado por el modelo:
                {umbral:.6f}
                """
            )


        # --------------------------------------------
        # Error de validación Pydantic
        # --------------------------------------------

        elif respuesta.status_code == 422:

            st.error(
                """
                La API rechazó algunos datos del pedido.
                Revise que los campos obligatorios
                tengan valores válidos.
                """
            )

            with st.expander(
                "Ver detalle del error"
            ):

                st.json(
                    respuesta.json()
                )


        # --------------------------------------------
        # Otro error HTTP
        # --------------------------------------------

        else:

            st.error(
                f"""
                La API respondió con el código
                {respuesta.status_code}.
                """
            )

            with st.expander(
                "Ver respuesta de la API"
            ):

                st.text(
                    respuesta.text
                )


    # ------------------------------------------------
    # API no disponible
    # ------------------------------------------------

    except requests.exceptions.RequestException:

        st.error(
            """
            No fue posible conectarse con la API.

            El servicio gratuito de Render puede
            tardar en activarse después de un periodo
            de inactividad.

            Intente nuevamente en unos momentos.
            """
        )