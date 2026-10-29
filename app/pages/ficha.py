from pathlib import Path

import pandas as pd
import streamlit as st


# ----------------------------------------------------
# Rutas
# ----------------------------------------------------

APP_DIR = Path(__file__).resolve().parent.parent
PROYECTO_DIR = APP_DIR.parent

ARCHIVO_FICHA = (
    PROYECTO_DIR
    / "ficha_modelo.md"
)


# ----------------------------------------------------
# Título
# ----------------------------------------------------

st.title(
    "📄 Ficha del modelo"
)

st.write(
    """
    Resumen del propósito, desempeño, limitaciones
    y uso recomendado del modelo de riesgo de
    mala reseña.
    """
)


# ----------------------------------------------------
# Métricas principales
# ----------------------------------------------------

st.subheader(
    "Desempeño del modelo"
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Regresión Logística",
        "44.47%"
    )

with col2:
    st.metric(
        "XGBoost",
        "44.25%"
    )

with col3:
    st.metric(
        "Regla de retraso",
        "33.04%"
    )

with col4:
    st.metric(
        "Azar",
        "11.27%"
    )


st.caption(
    """
    La métrica corresponde a la precisión dentro
    del 10% de pedidos con mayor riesgo.
    """
)


st.divider()


# ----------------------------------------------------
# Gráfico comparativo
# ----------------------------------------------------

st.subheader(
    "Comparación de resultados"
)

resultados = pd.DataFrame(
    {
        "Método": [
            "Regresión Logística",
            "XGBoost",
            "Regla de retraso",
            "Azar"
        ],
        "Precisión Top 10 (%)": [
            44.47,
            44.25,
            33.04,
            11.27
        ]
    }
)

st.bar_chart(
    resultados,
    x="Método",
    y="Precisión Top 10 (%)"
)


st.info(
    """
    La Regresión Logística obtuvo el mejor resultado,
    con **44.47%**, superando a la regla basada
    únicamente en retrasos y a la selección al azar.
    """
)


st.divider()


# ----------------------------------------------------
# Información general
# ----------------------------------------------------

st.subheader(
    "Información general"
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Pedidos utilizados",
        "77,304"
    )

with col2:
    st.metric(
        "Umbral de riesgo alto",
        "68.44%"
    )

with col3:
    st.metric(
        "Modelo final",
        "Regresión Logística"
    )


st.divider()


# ----------------------------------------------------
# Secciones resumidas e interactivas
# ----------------------------------------------------

st.subheader(
    "Detalles del modelo"
)


with st.expander(
    "1. ¿Para qué sirve?",
    expanded=True
):

    st.write(
        """
        El modelo estima la probabilidad de que un
        pedido reciba una mala reseña de **1 o 2
        estrellas** después de su entrega.

        Su objetivo es ayudar al equipo de atención
        al cliente a identificar qué pedidos deberían
        recibir atención prioritaria.

        No debe utilizarse para castigar vendedores
        ni para tomar decisiones automáticas sin
        revisión humana.
        """
    )


with st.expander(
    "2. Datos utilizados"
):

    st.write(
        """
        Se utilizaron **77,304 pedidos** entregados
        y con reseña conocida.

        Entre las variables utilizadas se encuentran:

        - Fechas del pedido y entrega.
        - Estado del cliente.
        - Cantidad de artículos.
        - Cantidad de vendedores.
        - Precio y flete.
        - Peso del pedido.
        - Categoría del producto.
        - Estado del vendedor.
        - Tipo de pago.
        - Número de cuotas.

        La información de la reseña no se utilizó
        como entrada del modelo.
        """
    )


with st.expander(
    "3. ¿Qué tan bien funciona?"
):

    st.write(
        """
        La evaluación se realizó utilizando una
        división temporal.

        Los principales resultados fueron:

        - **Regresión Logística: 44.47%**
        - **XGBoost: 44.25%**
        - **Regla de retraso: 33.04%**
        - **Azar: 11.27%**

        En términos sencillos, de cada 10 clientes
        seleccionados entre los pedidos con mayor
        riesgo, aproximadamente **4 terminaron
        dejando una mala reseña** durante el periodo
        de validación.
        """
    )


with st.expander(
    "4. Límites conocidos"
):

    st.write(
        """
        El desempeño puede cambiar cuando las
        condiciones futuras son diferentes a las
        observadas durante el entrenamiento.

        El modelo puede tener menor capacidad de
        discriminación si existen:

        - pocos retrasos;
        - cambios importantes en logística;
        - nuevas categorías;
        - nuevos vendedores;
        - cambios en el comportamiento de los clientes.

        La probabilidad entregada por el modelo no
        debe interpretarse como una certeza.
        """
    )


with st.expander(
    "5. ¿A quién puede afectar un error?"
):

    st.write(
        """
        Un **falso positivo** ocurre cuando un pedido
        es identificado como riesgo alto, pero el
        cliente finalmente no deja una mala reseña.

        Un **falso negativo** ocurre cuando el modelo
        no identifica un pedido como riesgoso, pero
        el cliente posteriormente deja una mala
        reseña.

        El modelo tampoco debe utilizarse para
        penalizar automáticamente a vendedores,
        porque algunos problemas pueden depender
        del transporte u otros factores externos.
        """
    )


with st.expander(
    "6. Recomendación de uso"
):

    st.write(
        """
        El modelo debe utilizarse como una herramienta
        de apoyo para priorizar clientes.

        Se recomienda:

        - mantener supervisión humana;
        - revisar los casos de mayor riesgo;
        - monitorear periódicamente el desempeño;
        - volver a entrenar el modelo cuando cambien
          significativamente los datos o procesos.
        """
    )


st.divider()


# ----------------------------------------------------
# Ficha oficial del proyecto
# ----------------------------------------------------

st.subheader(
    "Ficha oficial"
)

st.write(
    """
    A continuación se muestra el contenido del archivo
    `ficha_modelo.md` que forma parte de la entrega.
    """
)


if ARCHIVO_FICHA.exists():

    contenido = (
        ARCHIVO_FICHA
        .read_text(
            encoding="utf-8"
        )
    )

    with st.expander(
        "Ver ficha_modelo.md completa"
    ):

        st.markdown(
            contenido
        )

else:

    st.error(
        """
        No se encontró `ficha_modelo.md`
        en la raíz del proyecto.
        """
    )


# ----------------------------------------------------
# Cierre
# ----------------------------------------------------

st.divider()

st.caption(
    """
    Proyecto Olist · Modelo de riesgo de mala reseña
    · Uso académico.
    """
)