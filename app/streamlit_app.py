import requests
import streamlit as st


# ----------------------------------------------------
# Configuración general
# ----------------------------------------------------

st.set_page_config(
    page_title="Olist · Proyecto Final",
    page_icon="📦",
    layout="wide"
)


# ----------------------------------------------------
# URL de la API
# ----------------------------------------------------

try:
    URL_API = st.secrets["URL_API"]
except Exception:
    URL_API = "https://olist-proyecto-final-ny5r.onrender.com"


# ----------------------------------------------------
# Verificar estado de la API
# ----------------------------------------------------

@st.cache_data(ttl=30)
def verificar_api(url):

    try:

        respuesta = requests.get(
            url,
            timeout=10
        )

        if respuesta.status_code == 200:
            return True

        return False

    except requests.exceptions.RequestException:
        return False


# ----------------------------------------------------
# Navegación
# ----------------------------------------------------

paginas = st.navigation(
    [
        st.Page(
            "pages/riesgo.py",
            title="Riesgo de pedido",
            icon="⚠️"
        ),

        st.Page(
            "pages/comentarios.py",
            title="Comentarios",
            icon="💬"
        ),

        st.Page(
            "pages/segmentacion.py",
            title="Segmentación",
            icon="👥"
        ),

        st.Page(
            "pages/ficha.py",
            title="Ficha del modelo",
            icon="📄"
        )
    ]
)


# ----------------------------------------------------
# Información de API en barra lateral
# ----------------------------------------------------

st.sidebar.divider()

st.sidebar.markdown(
    "**URL de la API**"
)

st.sidebar.text_input(
    "URL de la API",
    value=URL_API,
    disabled=True,
    label_visibility="collapsed"
)


# ----------------------------------------------------
# Estado de la API
# ----------------------------------------------------

api_activa = verificar_api(
    URL_API
)


if api_activa:

    st.sidebar.success(
        "🟢 API activa"
    )

else:

    st.sidebar.error(
        "🔴 API no disponible"
    )

    st.sidebar.caption(
        """
        El servicio de Render puede estar
        iniciándose después de un periodo
        de inactividad.
        """
    )


# ----------------------------------------------------
# Botón para volver a comprobar
# ----------------------------------------------------

if st.sidebar.button(
    "🔄 Actualizar estado",
    use_container_width=True
):

    verificar_api.clear()

    st.rerun()


# ----------------------------------------------------
# Ejecutar página seleccionada
# ----------------------------------------------------

paginas.run()