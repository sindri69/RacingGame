varying vec4 norm;
varying vec4 s;
varying vec4 h;

uniform vec4 u_light_ambiance;
uniform vec4 u_light_diffuse;
uniform vec4 u_light_specular;

uniform vec4 u_material_diffuse;
uniform vec4 u_material_specular;
uniform float u_material_shininess;


void main(void)
{
    float lambert = max(dot(norm, s), 0);
    float phong = max(dot(norm, h), 0);

    gl_FragColor = u_light_ambiance + u_light_diffuse * u_material_diffuse * lambert + u_light_specular * u_material_specular * pow(phong, u_material_shininess);
}