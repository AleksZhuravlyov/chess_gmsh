import gmsh
import json


gmsh.initialize()
gmsh.option.setNumber("Mesh.MshFileVersion", 2)
gmsh.model.add("chess_gmsh")

lc = 1e-5

with open('throats_polygons_edited.json') as file:
    model = json.load(file)

inlet_throats = model['inlet_throats']
outlet_throats = model['outlet_throats']
hexahedrons = model['polygons']


hex_n = len(hexahedrons)


for polygon, curve_loops in hexahedrons.items():
    for curve_loop in curve_loops:
        for point in curve_loop:
            gmsh.model.occ.add_point(point[0], point[1], point[2])
            
for i in range(hex_n):
    p0 = 1 + i * 8 + 0
    p1 = 1 + i * 8 + 1
    p2 = 1 + i * 8 + 2
    p3 = 1 + i * 8 + 3
    p4 = 1 + i * 8 + 4
    p5 = 1 + i * 8 + 5
    p6 = 1 + i * 8 + 6
    p7 = 1 + i * 8 + 7    
    
    gmsh.model.occ.add_line(p0, p1) # 0
    gmsh.model.occ.add_line(p1, p3) # 1
    gmsh.model.occ.add_line(p3, p2) # 2
    gmsh.model.occ.add_line(p2, p0) # 3
                    
    gmsh.model.occ.add_line(p4, p5) # 4
    gmsh.model.occ.add_line(p5, p7) # 5
    gmsh.model.occ.add_line(p7, p6) # 6
    gmsh.model.occ.add_line(p6, p4) # 7
    
    gmsh.model.occ.add_line(p0, p6) # 8
    gmsh.model.occ.add_line(p1, p7) # 9
    gmsh.model.occ.add_line(p3, p5) # 10
    gmsh.model.occ.add_line(p2, p4) # 11
    
for i in range(hex_n):
    l0 = 1 + i * 12 + 0
    l1 = 1 + i * 12 + 1
    l2 = 1 + i * 12 + 2
    l3 = 1 + i * 12 + 3
    l4 = 1 + i * 12 + 4
    l5 = 1 + i * 12 + 5
    l6 = 1 + i * 12 + 6
    l7 = 1 + i * 12 + 7
    l8 = 1 + i * 12 + 8
    l9 = 1 + i * 12 + 9
    l10 = 1 + i * 12 + 10
    l11 = 1 + i * 12 + 11    
    
    gmsh.model.occ.add_curve_loop([l0, l1, l2, l3])
    gmsh.model.occ.add_curve_loop([l4, l5, l6, l7])
    gmsh.model.occ.add_curve_loop([-l2, l10, -l4, -l11])
    gmsh.model.occ.add_curve_loop([-l0, l8, -l6, -l9])
    gmsh.model.occ.add_curve_loop([-l1, l9, -l5, -l10])
    gmsh.model.occ.add_curve_loop([l3, l8, l7, -l11])
 
 
for i in range(hex_n):
    ls0 = 1 + i * 6 + 0
    ls1 = 1 + i * 6 + 1
    ls2 = 1 + i * 6 + 2
    ls3 = 1 + i * 6 + 3
    ls4 = 1 + i * 6 + 4
    ls5 = 1 + i * 6 + 5
      
    gmsh.model.occ.add_plane_surface([ls0])
    gmsh.model.occ.add_plane_surface([ls1])
    gmsh.model.occ.add_plane_surface([ls2])
    gmsh.model.occ.add_plane_surface([ls3])
    gmsh.model.occ.add_plane_surface([ls4])
    gmsh.model.occ.add_plane_surface([ls5])
    
    
for i in range(hex_n):
    s0 = 1 + i * 6 + 0
    s1 = 1 + i * 6 + 1
    s2 = 1 + i * 6 + 2
    s3 = 1 + i * 6 + 3
    s4 = 1 + i * 6 + 4
    s5 = 1 + i * 6 + 5
      
    gmsh.model.occ.add_volume([gmsh.model.occ.add_surface_loop([s0, s1, s2, s3, s4, s5])])


gmsh.model.occ.fuse([(3, 1)], [(3, i) for i in range(2, hex_n + 1)])

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

gmsh.model.mesh.generate(3)

gmsh.write('chess_gmsh.vtk')
gmsh.write('chess_gmsh.msh')

gmsh.finalize()