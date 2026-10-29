import streamlit as st

st.set_page_config(
    page_title="Olist · Proyecto Final",
    page_icon="📦",
    layout="wide"
)

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

paginas.run()