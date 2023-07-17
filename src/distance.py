import numpy as np
import pandas as pd
import utils as utils

# Coordenadas dos eletrodos
coordenadas = [(296, 276), (153, 95), (222, 106), (223, 58), (247, 161), (199, 161), (153, 154), (108, 142),
               (76, 205), (238, 220), (184, 218), (130, 213), (236, 277), (180, 277), (122, 277), (64, 277),
               (75, 347), (238, 333), (183, 336), (129, 340), (247, 394), (199, 393), (152, 400), (109, 411),
               (63, 445), (221, 448), (159, 463), (223, 495), (295, 565), (294, 506), (294, 449), (294, 392),
               (294, 335), (294, 47), (364, 58), (435, 96), (367, 106), (294, 104), (294, 163), (342, 161),
               (389, 160), (435, 153), (480, 142), (513, 206), (459, 213), (404, 219), (350, 221), (294, 219),
               (351, 277), (408, 277), (467, 277), (523, 277), (513, 348), (459, 340), (404, 336), (351, 334),
               (340, 394), (388, 394), (436, 400), (480, 411), (525, 447), (429, 464), (366, 447), (365, 496)]

# Inicializar matriz de distância
matriz_distancia = np.zeros((64, 64))

# Calcular a distância entre cada par de eletrodos
for i in range(64):
    for j in range(i + 1, 64):
        x1, y1 = coordenadas[i]
        x2, y2 = coordenadas[j]
        distancia = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        matriz_distancia[i, j] = round(distancia,4)
        matriz_distancia[j, i] = round(distancia,4)
        
df = pd.DataFrame(matriz_distancia, index=utils.CHANNELS, columns=utils.CHANNELS)
df.to_csv('distance_matriz.csv', index=True)


