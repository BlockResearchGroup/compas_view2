import random
import math

import compas
from compas.datastructures import Network
from compas.datastructures import Mesh
from compas.geometry import Pointcloud, Box
from compas.geometry import Scale, Rotation, Translation
from compas.utilities import i_to_rgb

from compas_view2 import app

viewer = app.App(version='330')

mesh = Mesh.from_off(compas.get('tubemesh.off'))
viewer.add(mesh, show_vertices=False)

network = Network.from_obj(compas.get('grid_irregular.obj'))
viewer.add(network)

bunny = Mesh.from_ply(compas.get('bunny.ply'))
T = Translation.from_vector([-10, 20, 0])
R = Rotation.from_axis_and_angle([1, 0, 0], math.radians(90))
S = Scale.from_factors([100, 100, 100])
bunny.transform(T * R * S)
viewer.add(bunny, show_vertices=False)

cloud = Pointcloud.from_bounds(10, 5, 3, 100)

R1 = Rotation.from_axis_and_angle([0, 0, 1], math.radians(180))
for point in cloud.transformed(R1):
    size = random.random()
    box = Box((point, [1, 0, 0], [0, 1, 0]), size, size, size)
    color = i_to_rgb(random.random(), normalize=True)
    viewer.add(box, show_vertices=False, color=color, opacity=random.random())

viewer.show()
