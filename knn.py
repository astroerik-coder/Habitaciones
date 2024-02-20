import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

# 1. SETUP
# Cargar datos
df = pd.read_csv('data//datos_transformados.csv', index_col='id_inquilino')

# 2. Preprocesamiento de los datos para KNN
# Escalar las características
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df)

# 3. Entrenamiento del modelo KNN
knn_model = KNeighborsClassifier(n_neighbors=10)  # Definir el número de vecinos que deseas considerar
knn_model.fit(X_scaled, df.index)  # Utilizar los índices de los inquilinos como etiquetas

# 4. Búsqueda de inquilinos compatibles utilizando KNN
def inquilinos_compatibles_knn(id_inquilino, topn):
    # Escalar las características del inquilino dado
    id_inquilino_scaled = scaler.transform(df.loc[[id_inquilino]])
    
    # Utilizar el modelo KNN para encontrar los vecinos más cercanos
    distances, indices = knn_model.kneighbors(id_inquilino_scaled, n_neighbors=topn+1)
    
    # Obtener los índices de los vecinos más cercanos (excluyendo el inquilino dado)
    neighbors_indices = indices[0][1:]
    
    # Obtener los registros de los inquilinos similares
    registros_similares = df.iloc[neighbors_indices]
    
    # Obtener la similitud de los inquilinos similares
    similitud_series = pd.Series(data=distances[0][1:], index=neighbors_indices, name='Similitud')
    
    # Devolver los registros similares y la similitud
    return registros_similares, similitud_series
