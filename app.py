import streamlit as st
import pandas as pd
from logica import *
from pca import *
from ayudantes import *
from kmeanspca import *
from formulario import *
from svm import *

# Configurar la página para utilizar un layout más amplio.
st.set_page_config(layout="wide")

resultado = None
resultado_kmeans= None
resultado_svm= None

# Mostrar una gran imagen en la parte superior.
st.image('Media//portada.png', use_column_width=True)

# Insertar un espacio vertical de 60px
st.markdown(f'<div style="margin-top: 60px;"></div>', unsafe_allow_html=True)

# Configurar el sidebar con inputs y un botón.
with st.sidebar:
    st.header("¿Quién está viviendo ya en el piso?")
    inquilino1 = st.text_input("Inquilino 1")
    inquilino2 = st.text_input("Inquilino 2")
    inquilino3 = st.text_input("Inquilino 3")
    
    num_compañeros = st.text_input("¿Cuántos nuevos compañeros quieres buscar?")
    
    if st.button('BUSCAR NUEVOS COMPAÑEROS'):
        # Verifica que el número de compañeros sea un valor válido
        try:
            topn = int(num_compañeros)
        except ValueError:
            st.error("Por favor, ingresa un número válido para el número de compañeros.")
            topn = None
        

        # Obtener los identificadores de inquilinos utilizando la función
        id_inquilinos = obtener_id_inquilinos(inquilino1, inquilino2, inquilino3, topn)

        if id_inquilinos and topn is not None:
            # Llama a la función inquilinos_compatibles con los parámetros correspondientes
            resultado = inquilinos_compatibles(id_inquilinos, topn)
            # Kmenas
            resultado_kmeans = inquilinos_compatibles_kmeans(id_inquilinos, topn)
            #SVM
"""             resultado_svm = inquilinos_compatibles_svm(id_inquilinos, topn)
 """
# Verificar si 'resultado' contiene un mensaje de error (cadena de texto)
if isinstance(resultado, str):
    st.error(resultado)
# Si no, y si 'resultado' no es None, mostrar el gráfico de barras y la tabla
elif resultado is not None:
    cols = st.columns((1, 2))  # Divide el layout en 2 columnas
    
    with cols[0]:  # Esto hace que el gráfico y su título aparezcan en la primera columna
        st.write("Nivel de compatibilidad de cada nuevo compañero:")
        fig_grafico = generar_grafico_compatibilidad(resultado[1])
        st.pyplot(fig_grafico)
    
    with cols[1]:  # Esto hace que la tabla y su título aparezcan en la segunda columna
        st.write("Comparativa entre compañeros:")
        fig_tabla = generar_tabla_compatibilidad(resultado)
        st.plotly_chart(fig_tabla, use_container_width=True)
    
# Mostrar la tabla y su título
if resultado_kmeans is not None:
    cols = st.columns((1, 2))  # Divide el layout en 2 columnas
    
    with cols[0]:  # Esto hace que el gráfico y su título aparezcan en la primera columna
        st.write("Nivel de compatibilidad de cada nuevo compañero KMeans:")
        fig_grafico_kmeans = generar_grafico_compatibilidad(resultado_kmeans[1])
        st.pyplot(fig_grafico_kmeans)
    
    with cols[1]:  # Esto hace que la tabla y su título aparezcan en la segunda columna
        st.write("Comparativa entre compañeros KMeans:")
        fig_tabla_kmeans = generar_tabla_compatibilidad(resultado_kmeans)
        st.plotly_chart(fig_tabla_kmeans, use_container_width=True)
        
""" # Mostrar la tabla y su título
if resultado_kmeans is not None:
    cols = st.columns((1, 2))  # Divide el layout en 2 columnas
    
    with cols[0]:  # Esto hace que el gráfico y su título aparezcan en la primera columna
        st.write("Nivel de compatibilidad de cada nuevo compañero SVM:")
        fig_grafico_svm = generar_grafico_compatibilidad(resultado_svm[1])
        st.pyplot(fig_grafico_svm)
    
    with cols[1]:  # Esto hace que la tabla y su título aparezcan en la segunda columna
        st.write("Comparativa entre compañeros SVM:")
        fig_tabla_svm = generar_tabla_compatibilidad(resultado_svm)
        st.plotly_chart(fig_tabla_svm, use_container_width=True) """