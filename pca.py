# Importar las librerías necesarias
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.decomposition import PCA

# Cargar los datos y realizar el preprocesamiento
df = pd.read_csv('data//datos_transformados.csv', index_col='id_inquilino')

# Realizar one-hot encoding de las variables categóricas
encoder = OneHotEncoder(sparse_output=False)
df_encoded = encoder.fit_transform(df)

# Aplicar PCA
pca = PCA(n_components=0.95)  # Conservar el 95% de la varianza
df_pca = pca.fit_transform(df_encoded)

# Calcular la matriz de similaridad utilizando PCA
matriz_s_pca = np.dot(df_pca, df_pca.T)

# Definir el rango de destino para la reescala
rango_min = -100
rango_max = 100

# Encontrar el mínimo y máximo valor en la matriz de similaridad PCA
min_original_pca = np.min(matriz_s_pca)
max_original_pca = np.max(matriz_s_pca)

# Reescalar la matriz de similaridad PCA
matriz_s_reescalada_pca = ((matriz_s_pca - min_original_pca) / (max_original_pca - min_original_pca)) * (rango_max - rango_min) + rango_min

# Convertir la matriz reescalada a un DataFrame de pandas
df_similaridad_pca = pd.DataFrame(matriz_s_reescalada_pca, index=df.index, columns=df.index)

# Definir la función para buscar inquilinos compatibles utilizando PCA
def inquilinos_compatibles_pca(id_inquilinos, topn):
    # Verificar si todos los ID de inquilinos existen en la matriz de similaridad PCA
    for id_inquilino in id_inquilinos:
        if id_inquilino not in df_similaridad_pca.index:
            return 'Al menos uno de los inquilinos no encontrado en la matriz de similaridad PCA'

    # Obtener las filas correspondientes a los inquilinos dados
    filas_inquilinos_pca = df_similaridad_pca.loc[id_inquilinos]

    # Calcular la similitud promedio entre los inquilinos
    similitud_promedio_pca = filas_inquilinos_pca.mean(axis=0)

    # Ordenar los inquilinos en función de su similitud promedio
    inquilinos_similares_pca = similitud_promedio_pca.sort_values(ascending=False)

    # Excluir los inquilinos de referencia (los que están en la lista)
    inquilinos_similares_pca = inquilinos_similares_pca.drop(id_inquilinos)

    # Tomar los topn inquilinos más similares
    topn_inquilinos_pca = inquilinos_similares_pca.head(topn)

    # Obtener los registros de los inquilinos similares en el conjunto reducido por PCA
    registros_similares_pca = df.loc[topn_inquilinos_pca.index]

    # Obtener los registros de los inquilinos buscados
    registros_buscados_pca = df.loc[id_inquilinos]

    # Concatenar los registros buscados con los registros similares en las columnas
    resultado_pca = pd.concat([registros_buscados_pca.T, registros_similares_pca.T], axis=1)

    # Crear un objeto Series con la similitud de los inquilinos similares encontrados
    similitud_series_pca = pd.Series(data=topn_inquilinos_pca.values, index=topn_inquilinos_pca.index, name='Similitud')

    # Devolver el resultado y el objeto Series
    return (resultado_pca, similitud_series_pca)
