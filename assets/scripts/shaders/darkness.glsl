#version 330

// Input vertex attributes (from vertex shader)
in vec2 fragTexCoord;
in vec4 fragColor;

uniform vec2 lpos;

// Output fragment color
out vec4 finalColor;

// vec2 screenSize = vec2(320, 180);

void main()
{   
    vec2 pos = vec2(gl_FragCoord.x, -gl_FragCoord.y + 180);
    float alpha = sqrt( 
        pow(lpos.x - pos.x, 2) + pow(lpos.y - pos.y, 2)
     );
    finalColor = vec4(0, 0, 0, alpha / 100);
}
