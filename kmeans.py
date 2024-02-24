# 1. SETUP
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# 2. CARGA DE DATOS
df = pd.read_csv('data//dataset_inquilinos.csv', index_col='id_inquilino')

df.columns = ['horario', 'bioritmo', 'nivel_educativo', 'leer', 'animacion', 
              'cine', 'mascotas', 'cocinar', 'deporte', 'dieta', 'fumador',
              'visitas', 'orden', 'musica_tipo', 'musica_alta', 'plan_perfecto', 'instrumento']

# 3. ONE HOT ENCODING
# Realizar el one-hot encoding
encoder = OneHotEncoder(sparse_output=False)
df_encoded = encoder.fit_transform(df)

def inquilinos_compatibles_PCA_Kmeans(id_inquilinos, topn, n_components=5, n_clusters=5):
    # Verificar si todos los ID de inquilinos existen en el DataFrame original
    for id_inquilino in id_inquilinos:
        if id_inquilino not in df.index:
            return 'Al menos uno de los inquilinos no encontrado'

    # Obtener los datos de los inquilinos dados
    datos_inquilinos = df.loc[id_inquilinos]

    # Aplicar PCA
    pca = PCA(n_components=n_components)
    pca_resultados = pca.fit_transform(df_encoded)

    # Aplicar K-means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans_resultados = kmeans.fit_predict(pca_resultados)

    # Obtener el índice del cluster al que pertenece cada inquilino
    clusters_inquilinos = kmeans.predict(pca.transform(encoder.transform(datos_inquilinos)))

    # Obtener el centroide del cluster de los inquilinos de referencia
    centroide_referencia = kmeans.cluster_centers_[clusters_inquilinos[0]]

    # Calcular la distancia euclidiana entre el centroide de referencia y todos los puntos
    distancia_centroide = np.linalg.norm(pca_resultados - centroide_referencia, axis=1)

    # Ordenar los índices por distancia y obtener los topn inquilinos más cercanos
    indices_compatibles = np.argsort(distancia_centroide)[1:topn + 1]

    # Obtener los registros de los inquilinos compatibles
    registros_compatibles = df.iloc[indices_compatibles]

    # Calcular el porcentaje de similitud con los inquilinos de referencia
    porcentaje_similitud = (1 - distancia_centroide[indices_compatibles] / np.max(distancia_centroide)) * 100

    # Crear un objeto Series con los porcentajes de similitud
    similitud_series = pd.Series(data=porcentaje_similitud, index=registros_compatibles.index, name='Similitud')

    return (registros_compatibles, similitud_series)
