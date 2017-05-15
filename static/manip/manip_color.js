function HashCode(_string){
    var hash = 0;
    for (var i = 0; i < _string.length; i++){

       hash = _string.charCodeAt(i) + ((hash << 5) - hash);

    }

    return hash;
}

function INTRGB(_hash){
    var colorHex = (_hash & 0x00FFFFFF)
        .toString(16)
        .toUpperCase();

    return "00000".substring(0, 6 - colorHex.length) + colorHex;
}

function HexRGB(_hex){

    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(_hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;

}

function ShadeRGBColor(_color, _percent){

    var f = _color.split(",");
    var t = _percent < 0 ? 0 : 255;
    var p =_percent < 0 ? _percent*-1 : _percent;
    var R = parseInt(f[0].slice(4));
    var G = parseInt(f[1]);
    var B = parseInt(f[2]);
    return "rgb(" +
        (Math.round((t - R)*p) + R) + "," +
        (Math.round((t - G)*p) + G) + "," +
        (Math.round((t - B)*p) + B) + ")";

}