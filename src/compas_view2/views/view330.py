from OpenGL import GL

from ..shaders import Shader
from ..buffers import make_camera_ubo, update_camera_ubo
from .view120 import View120
import numpy as np


class View330(View120):
    """View widget for OpenGL 3.3 and GLSL 330 and above, with a Core Profile.
    """

    def init(self):
        # create the program
        self.shader = Shader(name="330/mesh")
        self.shader.bind()
        self.shader.uniform1f("opacity", self.opacity)
        self.shader.uniform3f("selection_color", self.selection_color)
        self.shader.release()

        # Create and bind camera uniform buffer object
        self.cam_ubo = make_camera_ubo()
        self.shader.bind_ubo("camera", 0, self.cam_ubo)

        self.grid.init(shader_version="330")
        # init the buffers
        for guid in self.objects:
            obj = self.objects[guid]
            obj.init(shader_version="330")

    def paint(self):
        self.shader.bind()
        update_camera_ubo(self.cam_ubo, self.camera)
        # create object color map
        # if interactive selection is going on
        if self.app.selector.enabled:
            if self.app.selector.select_from == "pixel":
                self.app.selector.instance_map = self.paint_instances()
            if self.app.selector.select_from == "box":
                self.app.selector.instance_map = self.paint_instances(self.app.selector.box_select_coords)
            self.app.selector.enabled = False
            self.clear()
        # create grid uv map
        # if interactive selection on plane is going on
        if self.app.selector.wait_for_selection_on_plane:
            self.shader.uniform1f("opacity", 1)
            self.app.selector.uv_plane_map = self.paint_plane()
            self.shader.uniform1f("opacity", self.opacity)
            self.clear()
        # draw grid
        if self.show_grid:
            self.grid.draw(self.shader)
        # draw all objects
        for guid in self.objects:
            obj = self.objects[guid]
            obj.draw(self.shader, self.mode == "wireframe", self.mode == "lighted")
        # finish
        self.shader.release()
        # draw 2D box for multi-selection
        if self.app.selector.select_from == "box":
            self.shader.draw_2d_box(self.app.selector.box_select_coords, self.app.width, self.app.height)

    def paint_instances(self, cropped_box=None):
        if cropped_box is None:
            x, y, width, height = 0, 0, self.app.width, self.app.height
        else:
            x1, y1, x2, y2 = cropped_box
            x, y = min(x1, x2), self.app.height - max(y1, y2)
            width, height = abs(x1 - x2), abs(y1 - y2)
        for guid in self.objects:
            obj = self.objects[guid]
            if hasattr(obj, "draw_instance"):
                obj.draw_instance(self.shader, self.mode == "wireframe")
        # create map
        r = self.devicePixelRatio()
        instance_buffer = GL.glReadPixels(x*r, y*r, width*r, height*r, GL.GL_RGB, GL.GL_UNSIGNED_BYTE)
        instance_map = np.frombuffer(instance_buffer, dtype=np.uint8).reshape(height*r, width*r, 3)
        instance_map = instance_map[::-r, ::r, :]
        return instance_map
