import numpy as np
from scipy.spatial import Voronoi
from shapely.geometry import Polygon

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

bbox = [0, 0, 4, 4]
box_polygon = Polygon([(bbox[0], bbox[1]), (bbox[2], bbox[1]), (bbox[2], bbox[3]), (bbox[0], bbox[3])])

# 2. Reflect points to handle borders correctly
def reflect_points(points, bbox):
    xmin, ymin, xmax, ymax = bbox
    reflected = [points]
    reflected.append(np.column_stack((2 * xmin - points[:, 0], points[:, 1])))
    reflected.append(np.column_stack((2 * xmax - points[:, 0], points[:, 1])))
    reflected.append(np.column_stack((points[:, 0], 2 * ymin - points[:, 1])))
    reflected.append(np.column_stack((points[:, 0], 2 * ymax - points[:, 1])))
    return np.vstack(reflected)

dummy_points = reflect_points(points, bbox)
vor = Voronoi(dummy_points)

print("% --- CENTERS OF VORONOI CELLS ---")
print("% Option A: Original generating points (Input Sites)")
for i, pt in enumerate(points):
    print(f"\\node[circle, fill=black, inner sep=1.5pt, label={{above:{chr(65+i)}}}] at ({round(pt[0], 3)}, {round(pt[1], 3)}) {{}};")

print("\n% Option B: Geometric Centroids of the clipped cells")
# We only iterate over the first len(points) because the rest are dummy mirror points
for i in range(len(points)):
    region_idx = vor.point_region[i]
    region_vertices_indices = vor.regions[region_idx]
    
    # Check if the region is valid (doesn't contain infinity -1)
    if -1 not in region_vertices_indices and len(region_vertices_indices) > 0:
        region_vertices = vor.vertices[region_vertices_indices]
        
        # Create the cell polygon and clip it to our 4x4 box
        cell_poly = Polygon(region_vertices)
        clipped_cell = cell_poly.intersection(box_polygon)
        
        if not clipped_cell.is_empty:
            # Calculate the mathematical centroid of the closed polygon
            centroid = clipped_cell.centroid
            cx, cy = round(centroid.x, 3), round(centroid.y, 3)
            print(f"\\node[circle, fill=red, inner sep=1.2pt, label={{below:\\tiny C_{chr(65+i)}}}] at ({cx}, {cy}) {{}};")