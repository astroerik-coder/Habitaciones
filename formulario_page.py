import streamlit as st
import os
import pandas as pd

archivo_csv = "data/dataset_inquilinos.csv"

# Inicializar el contador del id_inquilino
ultimo_id_global = 12000

def guardar_en_csv(respuestas):
    global ultimo_id_global

    # Incrementar el contador del último id_inquilino global
    ultimo_id_global += 1

    # Asegurar que la columna id_inquilino sea de tipo entero
    respuestas["id_inquilino"] = ultimo_id_global

    # Crear un DataFrame con las respuestas y un índice (id_inquilino)
    df_respuestas = pd.DataFrame(respuestas, index=[0])

    # Reorganizar las columnas para que "id_inquilino" esté en la primera posición
    columnas_ordenadas = ["id_inquilino"] + [col for col in df_respuestas.columns if col != "id_inquilino"]
    df_respuestas = df_respuestas[columnas_ordenadas]

    # Guardar el DataFrame completo en el archivo CSV
    df_respuestas.to_csv(archivo_csv, mode='a', header=not os.path.exists(archivo_csv), index=False)

    st.success("Respuestas guardadas correctamente.")

def mostrar_formulario1():
    st.title("Registro de datos del inquilino")
    
    # Preguntas y respuestas
    preguntas_respuestas = {
        "variable1": ["mañana", "tarde", "noche"],
        "variable2": ["madrugador", "nocturno"],
        "variable3": ["no", "si"],
        "variable4": ["primaria", "secundaria", "universitaria"],
        "variable5": ["no", "si"],
        "variable6": ["no", "si"],
        "variable7": ["no", "si"],
        "variable8": ["sin mascotas", "con mascotas"],
        "variable9": ["cocinar", "pedir comida"],
        "variable10": ["no", "si"],
        "variable11": ["no", "si"],
        "variable12": ["ordenada", "relajada"],
        "variable13": ["pop", "reggaeton", "rock", "clasica"],
        "variable14": ["no", "si"],
        "variable15": ["casa", "salir"],
        "variable16": ["no", "si"],
        "variable17": ["no", "si"]
    }

    # Crear un formulario utilizando st.form
    with st.form(key='my_form'):
        # Iterar sobre las preguntas y agregarlas al formulario
        respuestas_guardadas = {}
        for pregunta, respuestas in preguntas_respuestas.items():
            respuesta_seleccionada = st.selectbox(pregunta, respuestas)
            respuestas_guardadas[pregunta] = respuesta_seleccionada

        # Botón para enviar el formulario
        enviar_button = st.form_submit_button("Enviar Respuestas")

    # Si se hace clic en el botón de enviar, realiza acciones con las respuestas
    if enviar_button:
        # Aquí puedes realizar acciones adicionales con las respuestas
        st.success("Respuestas enviadas correctamente.")
        guardar_en_csv(respuestas_guardadas)

    # Puedes devolver las respuestas si las necesitas fuera de la función
    return respuestas_guardadas
