attribute vec3 a_position;
attribute vec3 a_normal;

uniform mat4 u_model_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;

uniform vec4 u_eye_position;

uniform vec4 u_light_position;
uniform vec4 u_light_diffuse;
uniform vec4 u_light_specular;
uniform vec4 u_light_ambiance;
uniform vec4 u_material_diffuse;
uniform vec4 u_material_specular;
uniform int u_material_shininess;

uniform vec4 u_light1_position;
uniform vec4 u_light1_diffuse;
uniform vec4 u_light1_specular;
uniform vec4 u_light1_ambiance;

uniform vec4 u_light2_direction;
uniform vec4 u_light2_diffuse;
uniform vec4 u_light2_specular;
uniform vec4 u_light2_ambiance;

const int numberOfLights = 3;

varying vec4 v_color;  //Leave the varying variables alone to begin with
varying vec4 v_color1;
varying vec4 v_color2;

void main(void)
{


	position = u_model_matrix * position;
	normal = normalize(u_model_matrix * normal);

	vec4 s = normalize(u_light_position - position);
	float lambert = max(dot(normal, s), 0);

	vec4 s1 = normalize(u_light1_position - position);
	float lambert1 = max(dot(normal, s1), 0);

	vec4 s2 = u_light2_direction;
	float lambert2 = max(dot(normal, s2), 0);

	vec4 v = normalize(u_eye_position - position);
	vec4 h = normalize(s + v);
	vec4 h1 = normalize(s1 + v);
	vec4 h2 = normalize(s2 + v);

	float phong = max(dot(normal, h), 0);
	float phong1 = max(dot(normal, h1), 0);
	float phong2 = max(dot(normal, h2), 0);
	v_color = (u_light_ambiance + u_light_diffuse * u_material_diffuse * lambert + u_light_specular * u_material_specular * pow(phong, u_material_shininess))
						+ (u_light1_ambiance + u_light1_diffuse * u_material_diffuse * lambert1 + u_light1_specular * u_material_specular * pow(phong1, u_material_shininess))
						+ (u_light2_ambiance + u_light2_diffuse * u_material_diffuse * lambert2 + u_light2_specular * u_material_specular * pow(phong2, u_material_shininess));

	position = u_view_matrix * position;
	position = u_projection_matrix * position;
	gl_Position = position;
}