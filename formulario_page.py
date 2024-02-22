import streamlit as st
import os
import pandas as pd

archivo_csv = os.path.join("data", "dataset_inquilinos.csv")

# Función para obtener un nuevo ID autogenerativo
def obtener_nuevo_id():
    current_id = st.session_state.get('current_id', 12000)
    new_id = current_id + 1
    st.session_state['current_id'] = new_id
    return new_id

def mostrar_formulario():
    st.title("Registro de datos del inquilino")
    
    # Obtener un nuevo ID autogenerativo
    nuevo_id = obtener_nuevo_id()

    # Muestra el ID en el formulario (campo de texto deshabilitado)
    st.text_input("ID:", value=nuevo_id, key="id_input", disabled=True)

    # Preguntas y respuestas
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

    # Crear un formulario utilizando st.form
    with st.form(key='my_form'):
        # Iterar sobre las preguntas y agregarlas al formulario
        for pregunta, respuestas in preguntas_respuestas.items():
            respuesta_seleccionada = st.selectbox(pregunta, respuestas)

        # Botón para enviar el formulario
        enviar_button = st.form_submit_button("Enviar Respuestas")

    # Si se hace clic en el botón de enviar, realiza acciones con las respuestas
    if enviar_button:
        # Obtener un nuevo ID autogenerativo
        nuevo_id = obtener_nuevo_id()

        # Almacena las respuestas y el nuevo ID en algún lugar (puedes adaptar esto según tus necesidades)
        respuestas_guardadas = {
            'ID': nuevo_id,
            'Respuestas': {pregunta: respuesta_seleccionada for pregunta, respuesta_seleccionada in preguntas_respuestas.items()}
        }

        # Puedes imprimir o almacenar las respuestas en una base de datos, por ejemplo.
        print(f"Respuestas Guardadas: {respuestas_guardadas}")

        # Guardar los datos en el archivo CSV
        guardar_en_csv(respuestas_guardadas)

        # Agregar más lógica según sea necesario

    # Botón para volver a la página principal
    if st.button("Volver a la Página Principal"):
        st.experimental_rerun()
        
# Función para guardar datos en el archivo CSV
def guardar_en_csv(datos):
    # Crear un DataFrame para los nuevos datos
    df_nuevos_datos = pd.DataFrame([datos])

    # Si el archivo CSV ya existe, cargarlo y agregar los nuevos datos
    if os.path.exists(archivo_csv):
        df_existente = pd.read_csv(archivo_csv)
        df_concatenado = pd.concat([df_existente, df_nuevos_datos], ignore_index=True)
    else:
        df_concatenado = df_nuevos_datos

    # Guardar el DataFrame completo en el archivo CSV
    df_concatenado.to_csv(archivo_csv, index=False)

# Configurar la página principal
st.title("Página Principal")

# Botón para ir al formulario
if st.button("Ir al Formulario", key="formulario_button"):
    mostrar_formulario()
