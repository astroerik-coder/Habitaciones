import streamlit as st
import pandas as pd
from logica import *
from pca import *
from ayudantes import *
from knn import *
from formulario_page import mostrar_formulario1
# Configurar la página para utilizar un layout más amplio.

archivo_csv = "data/dataset_inquilinos.csv"

resultado = None
resultado_pca = None 
resultado_knn= None

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
            # PCA
            resultado_pca = inquilinos_compatibles_pca(id_inquilinos, topn)
            # KNN
            resultado_knn = inquilinos_compatibles_knn(id_inquilinos[0], topn)  # Utiliza solo el primer inquilino dado


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
    
# Verificar si 'resultado_pca' contiene un mensaje de error (cadena de texto)
if isinstance(resultado_pca, str):
    st.error(resultado_pca)
# Si no, y si 'resultado_pca' no es None, mostrar el gráfico de barras y la tabla
elif resultado_pca is not None:  # Corrige esta línea
    cols = st.columns((1, 2))  # Divide el layout en 2 columnas
    
    with cols[0]:  # Esto hace que el gráfico y su título aparezcan en la primera columna
        st.write("Nivel de compatibilidad de cada nuevo compañero PCA:")
        fig_grafico = generar_grafico_compatibilidad(resultado_pca[1])
        st.pyplot(fig_grafico)
    
    with cols[1]:  # Esto hace que la tabla y su título aparezcan en la segunda columna
        st.write("Comparativa entre compañeros:")
        fig_tabla = generar_tabla_compatibilidad(resultado_pca)
        st.plotly_chart(fig_tabla, use_container_width=True)

# Verificar si 'resultado_knn' contiene un mensaje de error (cadena de texto)
if isinstance(resultado_knn, str):
    st.error(resultado_knn)
# Si no, y si 'resultado_knn' no es None, mostrar el gráfico de barras y la tabla
elif resultado_knn is not None:
    cols = st.columns((1, 2))  # Divide el layout en 2 columnas
    
    with cols[0]:  # Esto hace que el gráfico y su título aparezcan en la primera columna
        st.write("Nivel de compatibilidad de cada nuevo compañero (KNN):")
        fig_grafico_knn = generar_grafico_compatibilidad(resultado_knn[1])
        st.pyplot(fig_grafico_knn)
    
    with cols[1]:  # Esto hace que la tabla y su título aparezcan en la segunda columna
        st.write("Comparativa entre compañeros (KNN):")
        fig_tabla_knn = generar_tabla_compatibilidad(resultado_knn)
        st.plotly_chart(fig_tabla_knn, use_container_width=True)

#if st.button("Ir al Formulario"):
mostrar_formulario1()
#guardar_mensaje()


    
