#version 150

uniform sampler2D p3d_Texture0;
uniform sampler2D center;
uniform sampler2D edge;
uniform sampler2D corner;
uniform vec2 borderWidth;
uniform float size;

uniform vec4 p3d_ColorScale;

in vec2 texcoord;

out vec4 p3d_FragColor;

void main() {
    vec2 coord = vec2(texcoord.x * (1 + borderWidth.x/size * 2) - borderWidth.x/size,
                      texcoord.y * (1 + borderWidth.y * 2) - borderWidth.y);
    vec4 color = texture(center, coord);
    mat2 rotation = mat2(0, -1, 1, 0);

    //handle edges on vertical sides
    vec2 edgeCoord = vec2(texcoord.x / borderWidth.x * size, texcoord.y / borderWidth.y);
    if (coord.x > 1){
        color = texture(edge, vec2(edgeCoord.x, coord.y) - vec2(size/borderWidth.x, 0));
    } else if (coord.x < 0){
        color = texture(edge, vec2(1 - edgeCoord.x, coord.y));
    } else if (coord.y > 1){  //handle edges on horizontal sides
        color = texture(edge, rotation*vec2(coord.x, edgeCoord.y));
    } else if (coord.y < 0){
        color = texture(edge, rotation*vec2(coord.x, 1 - edgeCoord.y));
    }

    //handle corners
    vec2 cornerCoord = vec2(texcoord.x / borderWidth.x * size,
                            texcoord.y / borderWidth.y);
    if (coord.y > 1 && coord.x > 1){
        color = texture(corner, cornerCoord - vec2(size/borderWidth.x, 0));
    } else if (coord.y > 1 && coord.x < 0){
        color = texture(corner, vec2(1 - cornerCoord.x, cornerCoord.y));
    } else if (coord.y < 0 && coord.x > 1){
        color = texture(corner, vec2(cornerCoord.x, 1 - cornerCoord.y) - vec2(size/borderWidth.x, 0));
    } else if (coord.y < 0 && coord.x < 0){
        color = texture(corner, vec2(1 - cornerCoord.x, 1 - cornerCoord.y));
    }

    p3d_FragColor = color * p3d_ColorScale;
}
