import sys

import gmsh
import json

gmsh.initialize()
gmsh.option.setNumber("Mesh.MshFileVersion", 2)
gmsh.model.add("chess_gmsh")

lc = 1e-5

file_name = 'throats_polygons_edited'
# file_name = 'throats_polygons_rotated'

with open(file_name + '.json') as file:
    model = json.load(file)

hexahedrons = model['polygons']

hex_n = len(hexahedrons)

for polygon, curve_loops in hexahedrons.items():
    for curve_loop in curve_loops:
        for point in curve_loop:
            gmsh.model.occ.add_point(point[0], point[1], point[2])

add_line = gmsh.model.occ.add_line
for i in range(hex_n):
    start = 1 + i * 8 + 0
    stop = 1 + i * 8 + 7 + 1
    ps = range(start, stop)

    add_line(ps[0], ps[1])  # 0
    add_line(ps[1], ps[3])  # 1
    add_line(ps[3], ps[2])  # 2
    add_line(ps[2], ps[0])  # 3

    add_line(ps[4], ps[5])  # 4
    add_line(ps[5], ps[7])  # 5
    add_line(ps[7], ps[6])  # 6
    add_line(ps[6], ps[4])  # 7

    add_line(ps[0], ps[6])  # 8
    add_line(ps[1], ps[7])  # 9
    add_line(ps[3], ps[5])  # 10
    add_line(ps[2], ps[4])  # 11

    add_line(ps[0], ps[7])  # 12
    add_line(ps[3], ps[4])  # 13
    add_line(ps[1], ps[5])  # 14
    add_line(ps[6], ps[2])  # 15

add_curve_loop = gmsh.model.occ.add_curve_loop
add_plane_surface = gmsh.model.occ.add_plane_surface
for i in range(hex_n):
    start = 1 + i * 16 + 0
    stop = 1 + i * 16 + 15 + 1
    ls = range(start, stop)

    add_plane_surface([add_curve_loop([ls[0], ls[1], ls[2], ls[3]])])  # 0

    add_plane_surface([add_curve_loop([ls[4], ls[5], ls[6], ls[7]])])  # 1

    add_plane_surface([add_curve_loop([ls[12], ls[6], -ls[8]])])  # 2
    add_plane_surface([add_curve_loop([ls[0], ls[9], -ls[12]])])  # 3

    add_plane_surface([add_curve_loop([ls[14], ls[5], -ls[9]])])  # 4
    add_plane_surface([add_curve_loop([ls[1], ls[10], -ls[14]])])  # 5

    add_plane_surface([add_curve_loop([ls[13], ls[4], -ls[10]])])  # 6
    add_plane_surface([add_curve_loop([ls[2], ls[11], -ls[13]])])  # 7

    add_plane_surface([add_curve_loop([ls[15], ls[11], -ls[7]])])  # 8
    add_plane_surface([add_curve_loop([ls[3], ls[8], -ls[15]])])  # 9

add_surface_loop = gmsh.model.occ.add_surface_loop
add_volume = gmsh.model.occ.add_volume
for i in range(hex_n):
    start = 1 + i * 10 + 0
    stop = 1 + i * 10 + 9 + 1
    add_volume([add_surface_loop(range(start, stop))])

print()
print()

entities_store = gmsh.model.occ.get_entities(3)

print('entities_store', entities_store)
outDimTags = [entities_store[0]]
del entities_store[0]

while entities_store:
    print()
    print('=====')
    objectDimTags = entities_store[0:1]
    del entities_store[0]
    print('objectDimTags', objectDimTags)
    print('toolDimTags', outDimTags)
    outDimTags, outDimTagsMap = gmsh.model.occ.fuse(objectDimTags, outDimTags)
    print('-><-')
    print('outDimTags', outDimTags)
    print('outDimTagsMap', outDimTagsMap)
    print('entities', gmsh.model.occ.get_entities(3))
    print('=====')

gmsh.model.occ.synchronize()

s_left = []
for s in gmsh.model.getEntitiesInBoundingBox(-1e-2, -1e-2, -1e-2, 1e-5, 1e-3, 1e-4, 2):
    s_left.append(s[1])

s_right = []
for s in gmsh.model.getEntitiesInBoundingBox(8e-4, -1e-2, -1e-2, 12e-4, 1e-3, 1e-4, 2):
    s_right.append(s[1])

gmsh.model.setPhysicalName(2, gmsh.model.addPhysicalGroup(2, s_left), "left")
gmsh.model.setPhysicalName(2, gmsh.model.addPhysicalGroup(2, s_right), "right")

gmsh.model.setPhysicalName(3, gmsh.model.addPhysicalGroup(3, [e[1] for e in gmsh.model.getEntities(3)]), "volume")

gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc)

# gmsh.option.setNumber("Mesh.SaveAll", 1)

gmsh.model.mesh.generate(3)

gmsh.write('chess_gmsh.vtk')
gmsh.write('chess_gmsh.msh')

print('get_entities', gmsh.model.occ.get_entities(3))

gmsh.finalize()
