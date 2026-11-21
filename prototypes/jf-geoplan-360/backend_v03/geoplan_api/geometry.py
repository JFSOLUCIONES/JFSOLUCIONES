"""Geometry is an engineering AID only, not a cadastral or construction certification.

Accepts WGS84 geographic coordinates or an explicitly identified projected metre CRS.
Returns projected analysis coordinates with source and output EPSG recorded.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import floor, isfinite
from pyproj import CRS, Transformer
from shapely.geometry import Polygon

@dataclass(frozen=True)
class GeometryResult:
    source_epsg: int
    projected_epsg: int
    area_m2: float
    perimeter_m: float
    projected_vertices: tuple[tuple[float, float], ...]


def analyze_polygon(vertices: list[list[float]], source_epsg: int) -> GeometryResult:
    if not isinstance(source_epsg, int) or source_epsg < 2000 or source_epsg > 999999:
        raise ValueError('EPSG de origen obligatorio y válido')
    if not isinstance(vertices, list) or not 3 <= len(vertices) <= 1000:
        raise ValueError('Se requieren entre 3 y 1000 vértices')
    points = []
    for xy in vertices:
        if not isinstance(xy, (list, tuple)) or len(xy) != 2:
            raise ValueError('Cada vértice tiene exactamente X,Y')
        try:
            x, y = float(xy[0]), float(xy[1])
        except (TypeError, ValueError):
            raise ValueError('Coordenada no numérica') from None
        if not isfinite(x) or not isfinite(y):
            raise ValueError('Coordenada infinita o NaN')
        points.append((x, y))
    if points[0] == points[-1]:
        points.pop()
    if len(points) < 3 or len(set(points)) < 3:
        raise ValueError('Vértices degenerados')
    try:
        source = CRS.from_epsg(source_epsg)
    except Exception:
        raise ValueError('EPSG no reconocido') from None
    if source.is_geographic:
        if source_epsg != 4326:
            raise ValueError('Solo EPSG:4326 está admitido en coordenadas geográficas de este piloto')
        if any(x < -180 or x > 180 or y < -90 or y > 90 for x, y in points):
            raise ValueError('Longitud/latitud fuera de rango')
        average_lon = sum(x for x, _ in points) / len(points)
        average_lat = sum(y for _, y in points) / len(points)
        zone = max(1, min(60, floor((average_lon+180)/6) + 1))
        projected_epsg = (32600 if average_lat >= 0 else 32700) + zone
        t = Transformer.from_crs(source, CRS.from_epsg(projected_epsg), always_xy=True)
        points = [tuple(map(float, t.transform(x, y))) for x, y in points]
    else:
        axis = source.axis_info
        if not source.is_projected or any(a.unit_name.lower() not in ('metre', 'meter', 'metres', 'meters') for a in axis):
            raise ValueError('Sistema proyectado debe estar expresado en metros')
        projected_epsg = source_epsg
    polygon = Polygon(points)
    if not polygon.is_valid:
        raise ValueError('Polígono inválido: cruces o geometría inconsistente')
    if polygon.area < 0.01:
        raise ValueError('Superficie insuficiente')
    if polygon.length > 1e7 or polygon.area > 1e12:
        raise ValueError('Dimensiones fuera de límites del piloto')
    return GeometryResult(source_epsg, projected_epsg, round(polygon.area, 3),round(polygon.length, 3),tuple(points))


def export_dxf(vertices_projected: tuple[tuple[float, float], ...], projected_epsg: int) -> str:
    import io
    import ezdxf
    if len(vertices_projected) < 3:
        raise ValueError('Mínimo 3 vértices')
    drawing = ezdxf.new('R2010')
    drawing.layers.new('LOTE_CONCEPTUAL', dxfattribs={'color': 5})
    msp = drawing.modelspace()
    msp.add_lwpolyline(vertices_projected, close=True, dxfattribs={'layer': 'LOTE_CONCEPTUAL'})
    origin = vertices_projected[0]
    msp.add_text(f'ANTEPROYECTO - EPSG:{projected_epsg} - NO CERTIFICADO',dxfattribs={'height':0.5,'insert':(origin[0],origin[1]),'layer':'LOTE_CONCEPTUAL'})
    buffer = io.StringIO()
    drawing.write(buffer)
    return buffer.getvalue()
