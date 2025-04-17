# Este es solo un ejemplo rapido xd
import streamlit as st
import os
import tempfile

from app.dfpandas.init_conversation import analizar_inicios

from app.chat_to_df import chat_to_dataframe
from app.dfpandas.cleaning import clean_dataframe

from app.logging_config import configure_logging
import logging

configure_logging()
logger = logging.getLogger(__name__)

def main():
    st.title("DEMO titulo chingo aqui")

    uploaded_file = st.file_uploader("Carga tu archivo weeee", type=["txt"])

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name

        try:
            # Procesar el archivo y mostrar el DataFrame
            df = chat_to_dataframe(temp_file_path)
            df_cleaned = clean_dataframe(df)
            with st.expander("Raw DataFrame"):
                st.dataframe(df_cleaned)
            st.subheader("¿Quién inicia más conversaciones?")
            countprop, inicios = analizar_inicios(df)
            st.dataframe(countprop)
            csv = df_cleaned.to_csv(index=False).encode('utf-8')
            st.success("Pos funcionó :v")
            st.download_button(
                label="📥 Descargar CSV",
                data=csv,
                file_name="chat_convertido.csv",
                mime="text/csv"
            )

        except Exception as e:
            logger.error(f"Error al procesar el archivo: {e}")
            st.error(e)

        # Después de terminar el procesamiento, se elimina el archivo temporal.
        try:
            os.remove(temp_file_path)
            logger.debug("Archivo temporal eliminado exitosamente.")

        except Exception as e:
            logger.warning(f"Error al eliminar el archivo temporal: {e}")

if __name__ == "__main__":
    main()
