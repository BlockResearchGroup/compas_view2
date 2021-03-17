#version 330

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 color;


out vec3 vertex_color;

layout (std140) uniform camera
{
    mat4 projection;
    mat4 viewworld;
};

layout (std140) uniform object
{   
    mat4 transform;
    float object_opacity;
    bool is_selected;
};

void main()
{   
    vertex_color = color;
    gl_Position = projection * viewworld * vec4(position, 1.0);
}
