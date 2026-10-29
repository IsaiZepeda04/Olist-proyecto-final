from pathlib import Path

import pandas as pd
import streamlit as st


# ----------------------------------------------------
# Configuración
# ----------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

ARCHIVO_SENTIMIENTO = (
    BASE_DIR
    / "data"
    / "sentimiento_muestra.csv"
)


# ----------------------------------------------------
# Cargar datos
# ----------------------------------------------------

@st.cache_data
def cargar_sentimientos():
    return pd.read_csv(
        ARCHIVO_SENTIMIENTO
    )


df = cargar_sentimientos()


# ----------------------------------------------------
# Asegurar tipo booleano en "coincide"
# ----------------------------------------------------

if df["coincide"].dtype == object:

    df["coincide"] = (
        df["coincide"]
        .astype(str)
        .str.lower()
        .map({
            "true": True,
            "false": False
        })
    )


# ----------------------------------------------------
# Título
# ----------------------------------------------------

st.title(
    "💬 Comentarios y sentimiento"
)

st.write(
    """
    Análisis del sentimiento expresado por los clientes
    en sus comentarios y comparación con la calificación
    otorgada en estrellas.
    """
)


# ----------------------------------------------------
# Regla de interpretación de estrellas
# ----------------------------------------------------

st.info(
    """
    **Interpretación de las estrellas:**

    - ⭐ 1–2 estrellas → **Negativo**
    - ⭐ 3 estrellas → **Neutral**
    - ⭐ 4–5 estrellas → **Positivo**
    """
)


# ----------------------------------------------------
# Métricas principales
# ----------------------------------------------------

total_comentarios = len(df)

coincidencias = (
    df["coincide"]
    .sum()
)

porcentaje_coincidencia = (
    coincidencias
    / total_comentarios
    * 100
)

desacuerdos = (
    total_comentarios
    - coincidencias
)


col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Comentarios analizados",
        f"{total_comentarios:,}"
    )

with col2:

    st.metric(
        "Coincidencia",
        f"{porcentaje_coincidencia:.1f}%"
    )

with col3:

    st.metric(
        "Desacuerdos",
        f"{desacuerdos:,}"
    )


st.divider()


# ----------------------------------------------------
# Distribución del sentimiento del modelo
# ----------------------------------------------------

st.subheader(
    "Distribución del sentimiento"
)

distribucion = (
    df["sentimiento_modelo"]
    .value_counts()
    .rename_axis("Sentimiento")
    .reset_index(name="Cantidad")
)

st.bar_chart(
    distribucion,
    x="Sentimiento",
    y="Cantidad"
)


# ----------------------------------------------------
# Tabla cruzada
# ----------------------------------------------------

st.subheader(
    "Estrellas vs. sentimiento del texto"
)

tabla_cruzada = pd.crosstab(
    df["sentimiento_estrellas"],
    df["sentimiento_modelo"]
)

tabla_cruzada.index.name = (
    "Según estrellas"
)

tabla_cruzada.columns.name = (
    "Según modelo"
)

st.dataframe(
    tabla_cruzada,
    use_container_width=True
)


# ----------------------------------------------------
# Tabla porcentual
# ----------------------------------------------------

st.subheader(
    "Porcentaje por categoría"
)

tabla_porcentual = (
    pd.crosstab(
        df["sentimiento_estrellas"],
        df["sentimiento_modelo"],
        normalize="index"
    )
    * 100
).round(2)

tabla_porcentual.index.name = (
    "Según estrellas"
)

tabla_porcentual.columns.name = (
    "Según modelo"
)

st.dataframe(
    tabla_porcentual,
    use_container_width=True
)

st.caption(
    """
    Las reseñas de 3 estrellas presentan la mayor
    confusión, ya que pueden contener opiniones
    positivas y negativas al mismo tiempo.
    """
)


st.divider()


# ----------------------------------------------------
# Explorador de comentarios
# ----------------------------------------------------

st.subheader(
    "Explorar comentarios"
)

opciones = [
    "Todos",
    "Positivos",
    "Neutrales",
    "Negativos",
    "Solo desacuerdos"
]

filtro = st.selectbox(
    "Mostrar",
    opciones
)


df_filtrado = df.copy()


if filtro == "Positivos":

    df_filtrado = df_filtrado[
        df_filtrado[
            "sentimiento_modelo"
        ] == "positivo"
    ]


elif filtro == "Neutrales":

    df_filtrado = df_filtrado[
        df_filtrado[
            "sentimiento_modelo"
        ] == "neutral"
    ]


elif filtro == "Negativos":

    df_filtrado = df_filtrado[
        df_filtrado[
            "sentimiento_modelo"
        ] == "negativo"
    ]


elif filtro == "Solo desacuerdos":

    df_filtrado = df_filtrado[
        df_filtrado["coincide"] == False
    ]


columnas_mostrar = [
    "review_score",
    "review_comment_message",
    "sentimiento_estrellas",
    "sentimiento_modelo",
    "confianza_modelo"
]


st.dataframe(
    df_filtrado[
        columnas_mostrar
    ],
    use_container_width=True,
    hide_index=True
)


# ----------------------------------------------------
# Ejemplos de desacuerdos
# ----------------------------------------------------

st.divider()

st.subheader(
    "Ejemplos de desacuerdos"
)

st.write(
    """
    En estos casos, la categoría obtenida a partir
    de las estrellas no coincide con el sentimiento
    detectado en el texto.
    """
)


df_desacuerdos = (
    df[
        df["coincide"] == False
    ]
    .copy()
)


muestra_desacuerdos = (
    df_desacuerdos
    .sample(
        n=min(
            10,
            len(df_desacuerdos)
        ),
        random_state=42
    )
)


for _, fila in muestra_desacuerdos.iterrows():

    estrellas = int(
        fila["review_score"]
    )

    sentimiento_estrellas = (
        fila["sentimiento_estrellas"]
    )

    sentimiento_modelo = (
        fila["sentimiento_modelo"]
    )

    with st.expander(
        f"⭐ {estrellas} estrellas "
        f"({sentimiento_estrellas}) "
        f"→ Modelo: {sentimiento_modelo}"
    ):

        st.write(
            "**Comentario del cliente:**"
        )

        st.write(
            fila[
                "review_comment_message"
            ]
        )

        col1, col2, col3 = (
            st.columns(3)
        )

        with col1:

            st.write(
                "**Según estrellas**"
            )

            st.write(
                sentimiento_estrellas
            )

        with col2:

            st.write(
                "**Según modelo**"
            )

            st.write(
                sentimiento_modelo
            )

        with col3:

            st.write(
                "**Confianza del modelo**"
            )

            st.write(
                f"{fila['confianza_modelo'] * 100:.1f}%"
            )


# ----------------------------------------------------
# Conclusión
# ----------------------------------------------------

st.divider()

st.subheader(
    "Conclusión"
)

st.info(
    f"""
    El sentimiento detectado en el texto coincide con
    las estrellas en aproximadamente
    **{porcentaje_coincidencia:.1f}%**
    de los comentarios analizados.

    Los desacuerdos muestran que las estrellas y el
    comentario escrito no siempre expresan exactamente
    lo mismo.

    El texto permite conocer detalles que las estrellas
    por sí solas no muestran, como problemas de entrega,
    productos equivocados, calidad del producto o
    experiencias mixtas.
    """
)