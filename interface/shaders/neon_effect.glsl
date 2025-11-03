// neon_effect.glsl
// Minimal fragment shader for demo purposes.
// Note: Qt ShaderEffect expects a fragment shader string with main()

uniform lowp float qt_Opacity;
varying highp vec2 qt_TexCoord0;

void main() {
    vec2 uv = qt_TexCoord0;
    float t = mod(uv.y * 10.0 + uv.x * 3.0, 1.0);
    float band = smoothstep(0.45, 0.5, sin((uv.x+uv.y*2.0)*10.0 + t*6.2831));
    vec3 color = mix(vec3(0.01,0.02,0.03), vec3(0.0,0.62,0.64), band);
    gl_FragColor = vec4(color, 1.0) * qt_Opacity;
}