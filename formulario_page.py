import streamlit as st
import os
import pandas as pd

archivo_csv = "data/dataset_inquilinos.csv"

def obtener_ultimo_id():
    if os.path.exists(archivo_csv):
        df = pd.read_csv(archivo_csv)
        if not df.empty:
            return df["id_inquilino"].max()
    return 0

# Obtener el último ID almacenado en el archivo CSV
ultimo_id_global = int(obtener_ultimo_id())

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
    
    # Crear un formulario utilizando HTML personalizado
    with st.form(key='my_form'):
        preguntas_respuestas = {
            "¿Cuál es tu horario de trabajo típico?": ["mañana", "tarde", "noche"],
            "¿Eres madrugador o nocturno?": ["madrugador", "nocturno"],
            "¿Prefieres un sitio animado que uno silencioso?": ["no", "si"],
            "¿Cuál es tu nivel educativo?": ["primaria", "secundaria", "universitaria"],
            "¿Te gusta leer?": ["no", "si"],
            "¿Te gusta el cine?": ["no", "si"],
            "¿Participas en deportes o actividades recreativas?": ["no", "si"],
            "¿Prefieres vivir con mascotas o sin ellas?": ["sin mascotas", "con mascotas"],
            "¿Te gusta cocinar o prefieres pedir comida?": ["cocinar", "pedir comida"],
            "¿Sigues alguna dieta?": ["no", "si"],
            "¿Eres fumador?": ["no", "si"],
            "¿Tienes visitas con frecuencia?": ["no", "si"],
            "¿Eres una persona ordenada o más relajada en ese aspecto?": ["ordenada", "relajada"],
            "¿Qué géneros de música te gustan?": ["pop", "reggaeton", "rock", "clásica"],
            "¿Tienes la costumbre de escuchar música en alto volumen?": ["no", "si"],
            "¿Tu plan perfecto sería tarde en casa viendo series o salir a tomar algo?": ["casa", "salir"],
            "¿Tocas algún instrumento musical?": ["no", "si"]
        }
        
        respuestas_guardadas = {}
        for pregunta, opciones in preguntas_respuestas.items():
            st.write(f"<label for='{pregunta}'>{pregunta}</label>", unsafe_allow_html=True)
            respuesta_seleccionada = st.selectbox("", opciones, key=pregunta)
            respuestas_guardadas[pregunta] = respuesta_seleccionada

        enviar_button = st.form_submit_button("Enviar Respuestas")

    if enviar_button:
        st.success("Respuestas enviadas correctamente.")
        guardar_en_csv(respuestas_guardadas)
