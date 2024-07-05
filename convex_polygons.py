#Kiah Johnson
#CS 536

import sys

def read_input(filename):
    polygons = []
    temp_polygon = []

    with open(filename, 'r') as f:
        lines = f.readlines()
        
    for l in lines:
        data = l.strip().split()
        if len(data) == 3 and data[2] == "moveto":
            if temp_polygon:
                polygons.append(temp_polygon)
                temp_polygon = []
            x, y = int(data[0]), int(data[1])
            temp_polygon.append((x, y))
        elif len(data) == 3 and data[2] == "lineto":
            x, y = int(data[0]), int(data[1])
            temp_polygon.append((x, y))
        elif len(data) == 1 and data[0] == "stroke":
            if temp_polygon:
                polygons.append(temp_polygon)
                temp_polygon = []
    if temp_polygon:
        polygons.append(temp_polygon)
    return polygons

def polygon_point(point, polygon):
    x, y = point
    flag = False
    poly_x, poly_y = polygon[0]

    for k in range(1, len(polygon) + 1):
        temp_x, temp_y = polygon[k % len(polygon)]
        if min(poly_y, temp_y) < y <= max(poly_y, temp_y) and x <= max(poly_x, temp_x):
            if poly_y != temp_y:
                x_coord = (y - poly_y) * (temp_x - poly_x) / (temp_y - poly_y) + poly_x
            if poly_x == temp_x or x <= x_coord:
                flag = not flag
        poly_x, poly_y = temp_x, temp_y
    return flag

def intersection_point(x1, x2, x3, x4, y1, y2, y3, y4):
    denominator = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    if denominator == 0:
        return None
    union_a = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denominator
    union_b = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denominator
    if 0 <= union_a <= 1 and 0 <= union_b <= 1:
        x = x1 + union_a * (x2 - x1)
        y = y1 + union_a * (y2 - y1)
        return (int(x), int(y))
    return None

def weiler_atherton(polygon1, polygon2):
    def next_vertex(edge, poly):
        return poly[(poly.index(edge[1]) + 1) % len(poly)]
    
    p0, p1 = polygon1, polygon2
    merged = []

    vertex = None
    for v in p0:
        if not polygon_point(v, p1):
            vertex = v
            break

    if vertex is None:
        print("No vertex found")
        sys.exit(1)

    merged.append(vertex)
    temp_edge = (vertex, next_vertex((vertex, vertex), p0))

    while len(merged) < 2 or merged[0] != merged[-1]:
        intersect = []
        for k in range(len(p1)):
            edge_start = p1[k]
            edge_end = p1[(k + 1) % len(p1)]
            inter = intersection_point(temp_edge[0][0], temp_edge[1][0], edge_start[0], edge_end[0],
                                       temp_edge[0][1], temp_edge[1][1], edge_start[1], edge_end[1])
            if inter:
                intersect.append((inter, (edge_start, edge_end)))

        if not intersect:
            vertex = temp_edge[1]
            if vertex == merged[0]:
                break
            merged.append(vertex)
            temp_edge = (vertex, next_vertex(temp_edge, p0))
        else:
            intersect.sort(key=lambda x: (x[0][0] - temp_edge[0][0]) ** 2 + (x[0][1] - temp_edge[0][1]) ** 2)
            next_intersect, intersect_edge = intersect[0]
            if next_intersect == merged[0]:
                break
            merged.append(next_intersect)
            temp_edge = (next_intersect, next_vertex((next_intersect, intersect_edge[0]), p1))
            merged.append(intersect_edge[1])
            temp_edge = (intersect_edge[1], next_vertex(intersect_edge, p1))
            p0, p1 = p1, p0
    return merged

def output_ps(polygon):
    print("%!PS-Adobe-2.0")
    print("%%%BEGIN")
    if polygon:
        begin = polygon[0]
        print(f"{begin[0]} {begin[1]} moveto")
        for pt in polygon[1:]:
            print(f"{pt[0]} {pt[1]} lineto")
        print(f"{begin[0]} {begin[1]} lineto")
    print("stroke")
    print("%%%END")   

def main():
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        if filename == "filename":
            filename = "HW5_a_in.ps"

    polygons = read_input(filename)
    if len(polygons) != 2:
        print("File must have 2 polygons")
        sys.exit(1)

    polygon1, polygon2 = polygons
    merged_polygon = weiler_atherton(polygon1, polygon2)
    output_ps(merged_polygon)

if __name__ == "__main__":
    main()  