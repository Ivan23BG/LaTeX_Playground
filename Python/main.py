import numpy as np
from scipy.spatial import Voronoi
from shapely.geometry import Polygon, LineString

# 1. Original points
points = np.array([
    [0.258, 2.49],
    [0.728, 1.735],
    [0.933, 0.801],
    [0.89, 3.219],
    [1.741, 3.415],
    [2.214, 2.355],
    [2.058, 0.765],
    [2.94, 3.481],
    [3.06, 0.885],
    [3.589, 2.078]
])

# Boîte de délimitation [xmin, ymin, xmax, ymax]
bbox = [0, 0, 4, 4]
box_polygon = Polygon([(bbox[0], bbox[1]), (bbox[2], bbox[1]), (bbox[2], bbox[3]), (bbox[0], bbox[3])])

# 2. Ajout de points "miroirs" pour forcer SciPy à fermer les cellules périphériques
# C'est la méthode la plus robuste pour gérer les bords avec SciPy
def reflect_points(points, bbox):
    xmin, ymin, xmax, ymax = bbox
    reflected = [points]
    # Miroir Gauche / Droite
    reflected.append(np.column_stack((2 * xmin - points[:, 0], points[:, 1])))
    reflected.append(np.column_stack((2 * xmax - points[:, 0], points[:, 1])))
    # Miroir Bas / Haut
    reflected.append(np.column_stack((points[:, 0], 2 * ymin - points[:, 1])))
    reflected.append(np.column_stack((points[:, 0], 2 * ymax - points[:, 1])))
    return np.vstack(reflected)

# Calcul du Voronoi sur les points originaux + miroirs
dummy_points = reflect_points(points, bbox)
vor = Voronoi(dummy_points)

# 3. Extraction et intersection des segments avec la boîte de délimitation
segments_tikz = []

for ridge_points in vor.ridge_vertices:
    # Si le segment est complètement défini (pas d'indice -1)
    if -1 not in ridge_points:
        p1 = vor.vertices[ridge_points[0]]
        p2 = vor.vertices[ridge_points[1]]
        
        # Création du segment mathématique
        line = LineString([p1, p2])
        
        # Intersection avec notre carré (0,0) -> (4,4)
        clipped_line = line.intersection(box_polygon)
        
        # Si le segment traverse ou est dans la boîte
        if not clipped_line.is_empty:
            if clipped_line.geom_type == 'LineString':
                coords = list(clipped_line.coords)
                # On évite les segments réduits à un point
                if len(coords) == 2:
                    segments_tikz.append(coords)

# 4. Nettoyage des doublons éventuels et affichage du résultat au format TikZ
unique_segments = []
for seg in segments_tikz:
    # Arrondi pour éviter les résidus de calcul flottant
    pt1 = (round(seg[0][0], 3), round(seg[0][1], 3))
    pt2 = (round(seg[1][0], 3), round(seg[1][1], 3))
    
    # Trie les points pour identifier facilement les doublons
    sorted_seg = sorted([pt1, pt2])
    if sorted_seg not in unique_segments:
        unique_segments.append(sorted_seg)

print(f"% --- SEGMENTS DU DIAGRAMME DE VORONOI ({len(unique_segments)} segments générés) ---")
for seg in unique_segments:
    print(f"\\draw[thin] ({seg[0][0]}, {seg[0][1]}) -- ({seg[1][0]}, {seg[1][1]});")