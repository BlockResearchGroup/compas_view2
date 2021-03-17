#version 330

in vec3 vertex_color;
out vec4 out_color;

uniform float opacity;

layout (std140) uniform object
{   
    mat4 transform;
    float object_opacity;
    bool is_selected;
};

void main()
{   
    out_color = vec4(vertex_color, opacity * object_opacity);
}
