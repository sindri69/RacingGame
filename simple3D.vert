attribute vec3 a_position;
attribute vec3 a_normal;

uniform mat4 u_model_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;

uniform vec4 u_eye_position;
uniform vec4 u_light_position;

varying vec4 norm;
varying vec4 s;
varying vec4 h;

void main(void)
{
	vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
	norm = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);

	position = u_model_matrix * position;
	norm = normalize(u_model_matrix * norm);

	s = normalize(u_light_position - position);

	vec4 v = normalize(u_eye_position - position);
	h = normalize(s + v);

	position = u_projection_matrix * (u_view_matrix * position);
	gl_Position = position;
}