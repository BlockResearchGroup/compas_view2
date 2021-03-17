from OpenGL import GL

from PySide2 import QtCore, QtWidgets

from ..camera import Camera
from ..mouse import Mouse
from ..objects import GridObject
import time


class View(QtWidgets.QOpenGLWidget):
    """Base OpenGL view widget.

    Parameters
    ----------
    app: :class:`compas_view2.app.App`
        The parent application of the view.
    background_color: tuple[float, float, float, float], optional
        The background or "clear" color of the view.
        Default is ``(1.0, 1.0, 1.0, 1.0)``.
    selection_color: tuple[float, float, float], optional
        The highlight color of selected objects.
        Default is ``(1.0, 1.0, 0.0)``.
    mode: 'shaded' | 'ghosted', optional
        The display mode.
        Default is ``'shaded'``.
    show_grid: bool, optional
        Flag for turning the grid on or off.
        Default is ``True``, which turns the grid on.
    """

    FRONT = 1
    RIGHT = 2
    TOP = 3
    PERSPECTIVE = 4

    def __init__(self,
                 app,
                 background_color=(1, 1, 1, 1),
                 selection_color=(1.0, 1.0, 0.0),
                 mode='shaded',
                 show_grid=True):
        super().__init__()
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self._opacity = 1.0
        self._current = View.PERSPECTIVE
        self.shader_model = None
        self.app = app
        self.color = background_color
        self.mode = mode
        self.selection_color = selection_color
        self.show_grid = show_grid
        self.camera = Camera(self)
        self.mouse = Mouse()
        self.grid = GridObject(1, 10, 10)
        self.objects = {}
        self.keys = {"shift": False, "control": False}
        self._frames = 0
        self._now = time.time()

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        self._mode = mode
        if mode == 'ghosted':
            self._opacity = 0.7
        else:
            self._opacity = 1.0
        if self.shader_model:
            self.shader_model.bind()
            self.shader_model.uniform1f("opacity", self._opacity)
            self.shader_model.release()
            self.update()

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, current):
        self._current = current
        if self.shader_model:
            self.shader_model.bind()
            self.shader_model.uniform4x4("projection", self.camera.projection(self.app.width, self.app.height))
            self.shader_model.release()
            self.update()

    @property
    def opacity(self):
        return self._opacity

    def clear(self):
        """Clear the view."""
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

    def initializeGL(self):
        """Initialize the OpenGL canvas.

        This implements the virtual funtion of the OpenGL widget.
        See the PySide2 docs [1]_ for more info.
        It sets the clear color of the view,
        and enables culling, depth testing, blending, point smoothing, and line smoothing.

        To extend the behaviour of this function,
        you can implement :meth:`~compas_view2.views.View.init`.

        References
        ----------
        .. [1] https://doc.qt.io/qtforpython-5.12/PySide2/QtWidgets/QOpenGLWidget.html#PySide2.QtWidgets.PySide2.QtWidgets.QOpenGLWidget.initializeGL

        """
        GL.glClearColor(* self.color)
        GL.glPolygonOffset(1.0, 1.0)
        GL.glEnable(GL.GL_POLYGON_OFFSET_FILL)
        GL.glEnable(GL.GL_CULL_FACE)
        GL.glCullFace(GL.GL_BACK)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glDepthFunc(GL.GL_LESS)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        # GL.glEnable(GL.GL_POINT_SMOOTH)
        # GL.glEnable(GL.GL_LINE_SMOOTH)
        self.init()

    def init(self):
        pass

    def resizeGL(self, w, h):
        """Resize the OpenGL canvas.

        This implements the virtual funtion of the OpenGL widget.
        See the PySide2 docs [1]_ for more info.

        To extend the behaviour of this function,
        you can implement :meth:`~compas_view2.views.View.resize`.

        Parameters
        ----------
        w: float
            The width of the canvas.
        h: float
            The height of the canvas.

        References
        ----------
        .. [1] https://doc.qt.io/qtforpython-5.12/PySide2/QtWidgets/QOpenGLWidget.html#PySide2.QtWidgets.PySide2.QtWidgets.QOpenGLWidget.resizeGL

        """
        GL.glViewport(0, 0, w, h)
        self.app.width = w
        self.app.height = h
        self.resize(w, h)

    def resize(self, w, h):
        pass

    def paintGL(self):
        """Paint the OpenGL canvas.

        This implements the virtual funtion of the OpenGL widget.
        See the PySide2 docs [1]_ for more info.

        To extend the behaviour of this function,
        you can implement :meth:`~compas_view2.views.View.paint`.

        Notes
        -----
        This method also paints the instance map used by the selector to identify selected objects.
        The instance map is immediately cleared again, after which the real scene objects are drawn.

        References
        ----------
        .. [1] https://doc.qt.io/qtforpython-5.12/PySide2/QtWidgets/QOpenGLWidget.html#PySide2.QtWidgets.PySide2.QtWidgets.QOpenGLWidget.paintGL

        """
        self.clear()
        self.paint()
        self._frames += 1
        if time.time() - self._now > 1:
            self._now = time.time()
            self.app.fps(self._frames)
            self._frames = 0

    def paint(self):
        pass

    def paint_instances(self):
        pass

    def paint_plane(self):
        pass

    def mouseMoveEvent(self, event):
        """Callback for the mouse move event.

        This method registers selections, if the left button is pressed,
        and modifies the view (pan/rotate), if the right button is pressed.
        """
        if not self.isActiveWindow() or not self.underMouse():
            return
        # record mouse position
        self.mouse.pos = event.pos()
        # compute displacement
        dx = self.mouse.dx()
        dy = self.mouse.dy()
        # do a box selection
        # if left button + SHIFT
        if event.buttons() & QtCore.Qt.LeftButton:
            if self.keys["shift"] or self.keys["control"]:
                self.app.selector.perform_box_selection(self.mouse.pos.x(), self.mouse.pos.y())
            # record mouse position
            self.mouse.last_pos = event.pos()
            self.update()
        # change the view
        # if right bottom
        elif event.buttons() & QtCore.Qt.RightButton:
            if self.keys["shift"]:
                self.camera.pan(dx, dy)
            else:
                self.camera.rotate(dx, dy)
            # record mouse position
            self.mouse.last_pos = event.pos()
            self.update()

    def mousePressEvent(self, event):
        if not self.isActiveWindow() or not self.underMouse():
            return
        # start selecting
        # if left button
        if event.buttons() & QtCore.Qt.LeftButton:
            self.mouse.buttons['left'] = True
            if self.keys["shift"] or self.keys["control"]:
                self.app.selector.reset_box_selection(event.pos().x(), event.pos().y())
        # do nothing
        # if right button
        elif event.buttons() & QtCore.Qt.RightButton:
            self.mouse.buttons['right'] = True
        # recod mouse position
        self.mouse.last_pos = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        if not self.isActiveWindow() or not self.underMouse():
            return
        # finalize selecting
        # if left button
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.mouse.buttons['left'] = False
            # select location on grid
            if self.app.selector.wait_for_selection_on_plane:
                self.app.selector.finish_selection_on_plane(event.pos().x(), event.pos().y())
            # trigger object selection
            else:
                self.app.selector.enabled = True
        # do nothing
        # if right button
        elif event.button() == QtCore.Qt.MouseButton.RightButton:
            self.mouse.buttons['right'] = False
        self.update()

    def wheelEvent(self, event):
        if not self.isActiveWindow() or not self.underMouse():
            return
        degrees = event.delta() / 8
        steps = degrees / 15
        self.camera.zoom(steps)
        self.update()

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Return or key == QtCore.Qt.Key_Enter:
            self.app.selector.finish_selection()
        if key == QtCore.Qt.Key_Shift:
            self.app.selector.mode = "multi"
            self.keys["shift"] = True
        if key == QtCore.Qt.Key_Control:
            self.app.selector.mode = "deselect"
            self.keys["control"] = True

    def keyReleaseEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Shift:
            self.app.selector.mode = self.app.selector.overwrite_mode or "single"
            self.keys["shift"] = False
        if key == QtCore.Qt.Key_Control:
            self.app.selector.mode = self.app.selector.overwrite_mode or "single"
            self.keys["control"] = False
