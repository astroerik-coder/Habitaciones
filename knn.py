# 1. SETUP
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors

# 2. CARGA DE DATOS
df = pd.read_csv('data//dataset_inquilinos.csv', index_col='id_inquilino')

df.columns = ['horario', 'bioritmo', 'nivel_educativo', 'leer', 'animacion', 
              'cine', 'mascotas', 'cocinar', 'deporte', 'dieta', 'fumador',
              'visitas', 'orden', 'musica_tipo', 'musica_alta', 'plan_perfecto', 'instrumento']

# 3. ONE HOT ENCODING
# Realizar el one-hot encoding
encoder = OneHotEncoder(sparse_output=False)
df_encoded = encoder.fit_transform(df)

# 4. FUNCION PARA OBTENER INQUILINOS COMPATIBLES USANDO PCA Y KNN
def inquilinos_compatibles_KNN(id_inquilinos, topn):
    n_components=2
    n_neighbors=5
    # Verificar si todos los ID de inquilinos existen en el DataFrame original
    for id_inquilino in id_inquilinos:
        if id_inquilino not in df.index:
            return 'Al menos uno de los inquilinos no encontrado'

    # Obtener los datos de los inquilinos dados
    datos_inquilinos = df.loc[id_inquilinos]

    # Aplicar PCA
    pca = PCA(n_components=n_components)
    pca_resultados = pca.fit_transform(df_encoded)

    # Aplicar KNN
    knn = NearestNeighbors(n_neighbors=n_neighbors)
    knn.fit(pca_resultados)

    # Encontrar los vecinos más cercanos a los inquilinos de referencia
    _, indices_compatibles = knn.kneighbors(pca.transform(encoder.transform(datos_inquilinos)))

    # Convertir los índices de los vecinos en una lista plana
    indices_compatibles = indices_compatibles.flatten()

    # Excluir los índices de los inquilinos de referencia
    indices_compatibles = np.setdiff1d(indices_compatibles, id_inquilinos)

    # Tomar los topn inquilinos más similares
    topn_indices = indices_compatibles[:topn]

    # Obtener los registros de los inquilinos compatibles
    registros_compatibles = df.iloc[topn_indices]

    # Concatenar los registros de los inquilinos buscados con los registros de los inquilinos compatibles
    resultado = pd.concat([datos_inquilinos.T, registros_compatibles.T], axis=1)

    # Calcular la similitud entre los inquilinos compatibles y los inquilinos de referencia
    similitud_series = pd.Series(data=indices_compatibles[:topn], index=registros_compatibles.index, name='Similitud')

    return (resultado, similitud_series)
