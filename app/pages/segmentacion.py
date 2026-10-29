from pathlib import Path

import pandas as pd
import streamlit as st


# ----------------------------------------------------
# Configuración
# ----------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

ARCHIVO_SEGMENTOS = (
    BASE_DIR
    / "data"
    / "segmentacion_vendedores.csv"
)

ARCHIVO_PERFILES = (
    BASE_DIR
    / "data"
    / "perfil_segmentos.csv"
)


# ----------------------------------------------------
# Cargar datos
# ----------------------------------------------------

@st.cache_data
def cargar_datos():

    vendedores = pd.read_csv(
        ARCHIVO_SEGMENTOS
    )

    perfiles = pd.read_csv(
        ARCHIVO_PERFILES
    )

    return vendedores, perfiles


vendedores, perfiles = cargar_datos()


# ----------------------------------------------------
# Preparar índice del perfil
# ----------------------------------------------------

if "segmento" in perfiles.columns:
    perfiles = perfiles.set_index("segmento")

elif "Unnamed: 0" in perfiles.columns:
    perfiles = perfiles.rename(
        columns={
            "Unnamed: 0": "segmento"
        }
    )

    perfiles = perfiles.set_index(
        "segmento"
    )


# ----------------------------------------------------
# Nombres y acciones
# ----------------------------------------------------

nombres_segmentos = {
    0: "Alto valor y operación estable",
    1: "Bajo ticket y alto flete",
    2: "Mayor riesgo de retraso",
    3: "Pedidos más complejos",
    4: "Alto volumen y diversidad"
}


acciones_segmentos = {
    0: (
        "Mantener condiciones favorables y realizar "
        "seguimiento preventivo para conservar su "
        "buen desempeño."
    ),

    1: (
        "Revisar alternativas para reducir el peso "
        "del costo de flete sobre el valor del pedido."
    ),

    2: (
        "Priorizar el seguimiento logístico y revisar "
        "las principales causas de retraso."
    ),

    3: (
        "Optimizar la preparación, empaquetado y "
        "consolidación de pedidos con varios artículos."
    ),

    4: (
        "Ofrecer atención prioritaria y herramientas "
        "para manejar operaciones de mayor escala."
    )
}


# ----------------------------------------------------
# Título
# ----------------------------------------------------

st.title(
    "👥 Segmentación de vendedores"
)

st.write(
    """
    Los vendedores fueron agrupados mediante
    **K-Means** utilizando variables relacionadas
    con ventas, pedidos, flete, retrasos y diversidad
    de categorías.
    """
)


# ----------------------------------------------------
# Información general
# ----------------------------------------------------

total_vendedores = len(
    vendedores
)

numero_segmentos = (
    vendedores["segmento"]
    .nunique()
)


col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Vendedores analizados",
        f"{total_vendedores:,}"
    )

with col2:

    st.metric(
        "Segmentos",
        numero_segmentos
    )

with col3:

    st.metric(
        "K seleccionado",
        5
    )


st.caption(
    """
    Se eligió k = 5 considerando el método del codo,
    el coeficiente de silueta y la utilidad de los
    grupos para el negocio.
    """
)


st.divider()


# ----------------------------------------------------
# Distribución de vendedores
# ----------------------------------------------------

st.subheader(
    "Distribución de vendedores por segmento"
)

distribucion = (
    vendedores
    .groupby("segmento")
    .size()
    .reset_index(
        name="Cantidad"
    )
)

distribucion["Segmento"] = (
    distribucion["segmento"]
    .map(
        nombres_segmentos
    )
)


st.bar_chart(
    distribucion,
    x="Segmento",
    y="Cantidad"
)


st.divider()


# ----------------------------------------------------
# Resumen de perfiles
# ----------------------------------------------------

st.subheader(
    "Perfil general de los segmentos"
)


tabla_perfiles = perfiles.copy()

tabla_perfiles[
    "nombre_segmento"
] = [
    nombres_segmentos.get(
        int(i),
        f"Segmento {i}"
    )
    for i in tabla_perfiles.index
]


columnas_mostrar = [
    "nombre_segmento",
    "n_vendedores",
    "pedidos_entregados",
    "ventas_total",
    "ticket_promedio",
    "flete_relativo",
    "tasa_retraso",
    "categorias_distintas"
]


columnas_existentes = [
    columna
    for columna in columnas_mostrar
    if columna in tabla_perfiles.columns
]


st.dataframe(
    tabla_perfiles[
        columnas_existentes
    ],
    use_container_width=True
)


st.divider()


# ----------------------------------------------------
# Explorador de segmentos
# ----------------------------------------------------

st.subheader(
    "Explorar un segmento"
)


segmento_seleccionado = st.selectbox(
    "Seleccione un segmento",
    sorted(
        vendedores[
            "segmento"
        ].unique()
    ),
    format_func=lambda x: (
        f"Segmento {x} · "
        f"{nombres_segmentos.get(x, '')}"
    )
)


# ----------------------------------------------------
# Obtener perfil del segmento
# ----------------------------------------------------

fila_perfil = (
    perfiles.loc[
        segmento_seleccionado
    ]
)


st.markdown(
    f"""
    ### Segmento {segmento_seleccionado}
    **{nombres_segmentos[segmento_seleccionado]}**
    """
)


# ----------------------------------------------------
# Métricas del segmento
# ----------------------------------------------------

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Vendedores",
        int(
            fila_perfil[
                "n_vendedores"
            ]
        )
    )


with col2:

    st.metric(
        "Pedidos promedio",
        f"{fila_perfil['pedidos_entregados']:.1f}"
    )


with col3:

    st.metric(
        "Ventas promedio",
        f"R$ {fila_perfil['ventas_total']:,.2f}"
    )


col4, col5, col6 = st.columns(3)


with col4:

    st.metric(
        "Ticket promedio",
        f"R$ {fila_perfil['ticket_promedio']:,.2f}"
    )


with col5:

    st.metric(
        "Tasa de retraso",
        f"{fila_perfil['tasa_retraso'] * 100:.1f}%"
    )


with col6:

    st.metric(
        "Categorías promedio",
        f"{fila_perfil['categorias_distintas']:.2f}"
    )


# ----------------------------------------------------
# Interpretación del segmento
# ----------------------------------------------------

st.subheader(
    "Descripción"
)


if segmento_seleccionado == 0:

    st.write(
        """
        Este grupo reúne vendedores con pedidos de
        mayor valor, bajo costo relativo de flete y
        una tasa de retraso reducida.
        """
    )


elif segmento_seleccionado == 1:

    st.write(
        """
        Este grupo presenta el ticket promedio más
        bajo y el mayor peso relativo del flete sobre
        el valor de las ventas.
        """
    )


elif segmento_seleccionado == 2:

    st.write(
        """
        Este segmento se caracteriza principalmente
        por presentar la tasa de retraso más alta
        entre los cinco grupos.
        """
    )


elif segmento_seleccionado == 3:

    st.write(
        """
        Estos vendedores manejan una mayor cantidad
        de artículos por pedido, lo que puede generar
        una operación logística más compleja.
        """
    )


elif segmento_seleccionado == 4:

    st.write(
        """
        Este grupo concentra vendedores con alto
        volumen de pedidos, mayores ventas y una
        mayor diversidad de categorías.
        """
    )


# ----------------------------------------------------
# Acción recomendada
# ----------------------------------------------------

st.subheader(
    "Acción recomendada"
)

st.info(
    acciones_segmentos[
        segmento_seleccionado
    ]
)


st.divider()


# ----------------------------------------------------
# Mostrar vendedores del segmento
# ----------------------------------------------------

st.subheader(
    "Vendedores del segmento"
)


vendedores_segmento = (
    vendedores[
        vendedores["segmento"]
        == segmento_seleccionado
    ]
    .copy()
)


columnas_vendedores = [
    "seller_id",
    "estado_vendedor",
    "pedidos_entregados",
    "ventas_total",
    "ticket_promedio",
    "flete_relativo",
    "tasa_retraso",
    "categorias_distintas"
]


columnas_vendedores = [
    columna
    for columna in columnas_vendedores
    if columna in vendedores_segmento.columns
]


st.dataframe(
    vendedores_segmento[
        columnas_vendedores
    ],
    use_container_width=True,
    hide_index=True
)


# ----------------------------------------------------
# Conclusión
# ----------------------------------------------------

st.divider()

st.subheader(
    "Conclusión"
)

st.info(
    """
    La segmentación permitió identificar cinco perfiles
    de vendedores con diferencias en volumen de ventas,
    ticket promedio, costos de flete, retrasos y
    diversidad de productos.

    Estos grupos pueden utilizarse para diseñar acciones
    distintas según las necesidades de cada tipo de
    vendedor.
    """
)