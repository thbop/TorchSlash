#version 330

// Input vertex attributes (from vertex shader)
// in vec2 fragTexCoord;
// in vec4 fragColor;

uniform vec2 lpos;
uniform vec2 cpos;

// Output fragment color
out vec4 finalColor;

// vec2 screenSize = vec2(320, 180);

void main()
{   
    vec2 pos = vec2(gl_FragCoord.x, -gl_FragCoord.y + 180) + cpos;
    float alpha = distance(pos, lpos);
    finalColor = vec4(0, 0, 0, alpha/70);
}
