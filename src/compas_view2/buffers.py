import ctypes as ct
import numpy as np
from OpenGL import GL
from OpenGL.arrays.vbo import VBO


def make_vertex_buffer(data, dynamic=False):
    """Make a vertex buffer from the given data.

    Parameters
    ----------
    data: list[float]
        A flat list of floats.

    Returns
    -------
    int
        Vertex buffer ID.
    """
    access = GL.GL_DYNAMIC_DRAW if dynamic else GL.GL_STATIC_DRAW
    n = len(data)
    size = n * ct.sizeof(ct.c_float)
    vbo = GL.glGenBuffers(1)
    data = (ct.c_float * n)(* data)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, size, data, access)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vbo


def make_index_buffer(data, dynamic=False):
    """Make an element buffer from the given data.

    Parameters
    ----------
    data: list[int]
        A flat list of ints.

    Returns
    -------
    int
        Element buffer ID.
    """
    access = GL.GL_DYNAMIC_DRAW if dynamic else GL.GL_STATIC_DRAW
    n = len(data)
    size = n * ct.sizeof(ct.c_uint)
    vbo = GL.glGenBuffers(1)
    data = (ct.c_int * n)(* data)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, size, data, access)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    return vbo


def make_vao_buffer(data, mode):
    positions, colors, elements = data
    positions = np.array(positions)
    colors = np.array(colors)
    elements = np.array(elements).flatten()
    # Vertices positions and colors are combined and will be loaded into a single vbo
    vertices = np.concatenate((positions, colors), axis=1)

    # Create Vertex Array Object, Vertex Buffer object and Element Buffer Object
    vao = GL.glGenVertexArrays(1)
    vbo = VBO(np.array(vertices, 'f'))
    ebo = VBO(elements, target=GL.GL_ELEMENT_ARRAY_BUFFER)

    # Bind all of them
    GL.glBindVertexArray(vao)
    vbo.bind()
    ebo.bind()

    # Write data to vbo
    GL.glEnableVertexAttribArray(0)
    GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 24, GL.ctypes.c_void_p(0))
    GL.glEnableVertexAttribArray(1)
    GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, 24, GL.ctypes.c_void_p(12))

    # Unbind everthing
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(0)
    GL.glDisableVertexAttribArray(1)
    vbo.unbind()
    ebo.unbind()

    gl_modes = {
        "points": GL.GL_POINTS,
        "lines": GL.GL_LINES,
        "triangles": GL.GL_TRIANGLES
    }

    return {
        "vao": vao,
        "vbo": vbo,
        "ebo": ebo,
        "mode": gl_modes[mode],
        "n": len(elements)
    }


def update_vertex_buffer(data, buffer):
    n = len(data)
    size = n * ct.sizeof(ct.c_float)
    data = (ct.c_float * n)(* data)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, buffer)
    GL.glBufferSubData(GL.GL_ARRAY_BUFFER, 0, size, data)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)


def update_index_buffer(data, buffer):
    n = len(data)
    size = n * ct.sizeof(ct.c_uint)
    data = (ct.c_int * n)(* data)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, buffer)
    GL.glBufferSubData(GL.GL_ELEMENT_ARRAY_BUFFER, 0, size, data)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)


def make_camera_ubo():
    # https://paroj.github.io/gltut/Positioning/Tut07%20Shared%20Uniforms.html
    # https://learnopengl.com/Advanced-OpenGL/Advanced-GLSL
    ubo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_UNIFORM_BUFFER, ubo)
    GL.glBufferData(GL.GL_UNIFORM_BUFFER, 128, None, GL.GL_STREAM_DRAW)
    GL.glBindBuffer(GL.GL_UNIFORM_BUFFER, 0)
    GL.glBindBufferRange(GL.GL_UNIFORM_BUFFER, 0, ubo, 0, 128)
    return ubo


def bind_camera_ubo(shader, ubo):
    ubi = GL.glGetUniformBlockIndex(shader.program, "camera")
    GL.glUniformBlockBinding(shader.program, ubi, 0)
    GL.glBindBufferBase(GL.GL_UNIFORM_BUFFER, 0, ubo)


def update_camera_ubo(ubo, camera):
    GL.glBindBuffer(GL.GL_UNIFORM_BUFFER, ubo)
    projection = np.array(camera.projection(), dtype="f").swapaxes(0, 1)
    GL.glBufferSubData(GL.GL_UNIFORM_BUFFER, 0, 64, projection)
    viewworld = np.array(camera.viewworld(), dtype="f").swapaxes(0, 1)
    GL.glBufferSubData(GL.GL_UNIFORM_BUFFER, 64, 64, viewworld)
    GL.glBindBuffer(GL.GL_UNIFORM_BUFFER, 0)


def make_object_ubo():
    ubo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_UNIFORM_BUFFER, ubo)
    GL.glBufferData(GL.GL_UNIFORM_BUFFER, 72, None, GL.GL_DYNAMIC_DRAW)
    GL.glBindBuffer(GL.GL_UNIFORM_BUFFER, 0)
    return ubo


def update_object_ubo(ubo, matrix, opacity, is_selected):

    GL.glBindBuffer(GL.GL_UNIFORM_BUFFER, ubo)

    matrix = np.array(matrix, dtype="f").swapaxes(0, 1)
    GL.glBufferSubData(GL.GL_UNIFORM_BUFFER, 0, 64, matrix)

    opacity = np.array([opacity], dtype="f")
    GL.glBufferSubData(GL.GL_UNIFORM_BUFFER, 64, 4, opacity)

    GL.glBindBuffer(GL.GL_UNIFORM_BUFFER, 0)
