import osmnx as ox

G = ox.graph_from_place("Taipei, Taiwan", network_type = 'drive')
Gp = ox.project_graph(G)
points = ox.utils_geo.sample_points(ox.get_undirected(Gp), 20) # generate 20 random point
print(points)

# 轉換經緯度