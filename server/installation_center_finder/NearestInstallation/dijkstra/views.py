# Create your views here.
import math
import heapq

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import SolarInstallationCenter
from .serializers import SolarInstallationCenterSerializer

def haversine(lat1, lon1, lat2, lon2):
    """
    Return distance in kilometers between two lat/lon points using Haversine.
    """
    R = 6371.0  # Earth radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def build_graph(centers, source_lat, source_lon):
    """
    Build a fully-connected undirected weighted graph for centers and a source node.
    Nodes 0..n-1 => centers, node n => source (input lat/lon).
    adjacency: dict node -> list of (neighbor_node, weight_km)
    """
    n = len(centers)
    adjacency = {i: [] for i in range(n)}
    # pairwise center distances
    for i in range(n):
        for j in range(i + 1, n):
            d = haversine(centers[i].latitude, centers[i].longitude,
                          centers[j].latitude, centers[j].longitude)
            adjacency[i].append((j, d))
            adjacency[j].append((i, d))
    # source node index = n
    adjacency[n] = []
    for i in range(n):
        d = haversine(source_lat, source_lon, centers[i].latitude, centers[i].longitude)
        adjacency[n].append((i, d))
    return adjacency, n  # return adjacency and source_index

def dijkstra(adjacency, source_index):
    """
    Standard Dijkstra that returns (distances dict, prev dict)
    """
    dist = {node: float('inf') for node in adjacency.keys()}
    prev = {node: None for node in adjacency.keys()}
    dist[source_index] = 0.0
    heap = [(0.0, source_index)]
    while heap:
        d_u, u = heapq.heappop(heap)
        if d_u > dist[u]:
            continue
        for v, w in adjacency.get(u, []):
            alt = d_u + w
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                heapq.heappush(heap, (alt, v))
    return dist, prev

class NearestCentersView(APIView):
    """
    POST JSON: { "latitude": 12.9632, "longitude": 79.9449, "k": 5 }
    Responds with top-k nearest centers (via Dijkstra over haversine weights).
    """
    def post(self, request):
        # Validate input
        try:
            print(request.data)
            lat = float(request.data.get('latitude'))
            lon = float(request.data.get('longitude'))
        except (TypeError, ValueError):
            return Response({'error': 'Please provide numeric "latitude" and "longitude".'}, status=status.HTTP_400_BAD_REQUEST)

        k = request.data.get('k', 5)
        try:
            k = int(k)
        except Exception:
            k = 3

        centers = list(SolarInstallationCenter.objects.all())
        if not centers:
            return Response({'origin': {'latitude': lat, 'longitude': lon}, 'nearest': []})

        adjacency, source_index = build_graph(centers, lat, lon)
        dist, prev = dijkstra(adjacency, source_index)

        results = []
        for i, center in enumerate(centers):
            d_km = dist.get(i, float('inf'))
            if not math.isfinite(d_km):
                continue
            # reconstruct path of center indices (excluding the source node)
            path_idxs = []
            node = i
            while node is not None and node != source_index:
                if node < len(centers):  # center node
                    path_idxs.append(node)
                node = prev.get(node)
            path_idxs.reverse()
            # map to external_ids
            path_external_ids = [centers[idx].external_id for idx in path_idxs]
            results.append({
                'external_id': center.external_id,
                'name': center.name,
                'address': center.address,
                'latitude': center.latitude,
                'longitude': center.longitude,
                'phone': center.phone,
                'distance_km': round(d_km, 4),
                'path_external_ids': path_external_ids
            })

        results_sorted = sorted(results, key=lambda x: x['distance_km'])
        return Response({
            'origin': {'latitude': lat, 'longitude': lon},
            'nearest': results_sorted[:k]
        })
