// opengl_effects.glsl
// A compact shader that blends neon glow + subtle wave distortion

#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 u_resolution;
uniform float u_time;
uniform sampler2D source;

vec3 neonC = vec3(0.0, 1.0, 0.97);

void main() {
    vec2 uv = gl_FragCoord.xy / u_resolution.xy;
    uv.x *= u_resolution.x / u_resolution.y;

    float wave = sin(uv.y * 30.0 + u_time * 2.0) * 0.0025;
    uv.x += wave;

    vec3 base = texture2D(source, uv).rgb;

    vec2 center = vec2(0.5 + 0.05*sin(u_time*0.5), 0.5);
    float r = length(uv - center);
    float glow = smoothstep(0.5, 0.0, r) * 0.9;

    vec3 color = mix(base, neonC * glow, 0.75);
    color = pow(color, vec3(0.95));

    gl_FragColor = vec4(color, 1.0);
}