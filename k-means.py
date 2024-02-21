from sklearn.cluster import KMeans
import pandas as pd
import numpy as np


# 2. CARGA DE DATOS
df = pd.read_csv('data//dataset_inquilinos.csv', index_col='id_inquilino')

# 3. ONE HOT ENCODING (si es necesario)
# No es necesario realizar One Hot Encoding para K-Means

# 4. ENTRENAMIENTO DEL MODELO K-MEANS
def entrenar_kmeans(df, topn):
    # Inicializar y entrenar el modelo K-Means
    kmeans = KMeans(n_clusters=topn, random_state=42)
    kmeans.fit(df)

    # Asignar cada inquilino a su clúster correspondiente
    labels = kmeans.labels_

    # Obtener los centroides de los clústeres
    centroids = kmeans.cluster_centers_

    # Encontrar los inquilinos más cercanos a cada centroide
    inquilinos_similares = {}
    for i, centroid in enumerate(centroids):
        distances = np.linalg.norm(df - centroid, axis=1)  # Distancia euclidiana
        closest_indices = np.argsort(distances)[:5]  # Obtener los 5 inquilinos más cercanos
        inquilinos_similares[i] = closest_indices

    return inquilinos_similares

# 5. BÚSQUEDA DE INQUILINOS COMPATIBLES
def inquilinos_compatibles_kmeans(id_inquilinos, topn):
    # Verificar si todos los ID de inquilinos existen en el DataFrame
    for id_inquilino in id_inquilinos:
        if id_inquilino not in df.index:
            return 'Al menos uno de los inquilinos no encontrado'

    # Obtener las características de los inquilinos actuales
    inquilinos_actuales = df.loc[id_inquilinos]

    # Entrenar el modelo K-Means
    resultado_kmeans = entrenar_kmeans(df, topn)
    print('Inquilinos actuales :'+inquilinos_actuales)
    print("Resultado Kmeans: "+resultado_kmeans)
    # Obtener los inquilinos similares de los clústeres encontrados
    inquilinos_similares = {}
    for cluster_id, closest_indices in resultado_kmeans.items():
        inquilinos_similares[cluster_id] = df.iloc[closest_indices]

    return (inquilinos_actuales, inquilinos_similares)

