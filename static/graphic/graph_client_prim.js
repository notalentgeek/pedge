var pitch_max  = 5000;
var volume_max = 0.1;

// `prim` stands for primary.
var graph_client_prim_array               = [];
var graph_client_prim_degree_target_array = [];
var prim_dimension                        = { height:320,width:320 };
var prim_dimension_smallest               = prim_dimension.height <= prim_dimension.width ? prim_dimension.height : prim_dimension.width;
var prim_padding                          = prim_dimension_smallest/8;
var prim_radius_main                      = prim_dimension_smallest/2 - prim_padding;
var prim_radius_biggest                   = prim_radius_main/6;
var prim_radius_smallest                  = prim_radius_main/12;
var prim_scale_linear_pitch               = d3.scaleLinear().domain([0,pitch_max]).range([0,1]);
var prim_scale_linear_volume              = d3.scaleLinear().domain([0,volume_max]).range([prim_radius_smallest,prim_radius_biggest]);
var prim_translate                        = { x:prim_dimension.width/2,y:prim_dimension.height/2 };

var graph_client_prim_svg = d3.select("#graph_client_prim_svg_container").append("svg")
  .attr("height", prim_dimension.height)
  .attr("id", "graph_client_prim_svg")
  .attr("width", prim_dimension.width);

function init_graph_client (_received_data) {
  if (_received_data !== null) {
    d3.selectAll(".graph_client_prim_circle" ).remove();
    d3.selectAll(".prim_presence_circle").remove();
    d3.selectAll(".prim_presence_line"  ).remove();
    graph_client_prim_array               = [];
    graph_client_prim_degree_target_array = [];
    for (var i = 0; i < _received_data.length; i ++) {
      value_name_client_temp = _received_data[i].name;
      value_face_temp        = _received_data[i].face;
      value_pitch_temp       = _received_data[i].pitch;
      value_presence_temp    = _received_data[i].presence;
      value_volume_temp      = _received_data[i].volume;
      // The client graph needs at least pitch and volume to be available.
      if (
        value_pitch_temp  != null &&
        value_volume_temp != null
      ) {
        value_pitch_temp    = Number(value_pitch_temp);
        value_volume_temp   = Number(value_volume_temp);
        var graph_color     = INTRGB(HashCode(value_name_client_temp))
        new graph_client_prim(value_face_temp, value_name_client_temp, value_pitch_temp, value_presence_temp, value_volume_temp);
      }
    }
    graph_client_prim_auto();
    graph_client_prim_presence();
  }
}

function insert_from_url_dt () {
  var value_dt = String(window.location.href).split("?dt=")[1];
  value_dt = (value_dt === undefined) ? undefined : value_dt.split("?")[0];
  if (value_dt !== undefined) {
    $("#value_dt").val(value_dt);
    $("#dt_go_to").click();
  }
  $("#value_qr").blur();
}



function graph_client_prim (
  _value_face_temp,
  _value_name_client_temp,
  _value_pitch_temp,
  _value_presence_temp,
  _value_volume_temp
) {
  this.value_face_temp        = _value_face_temp;
  this.value_name_client_temp = _value_name_client_temp;
  this.value_pitch_temp       = Number(_value_pitch_temp);
  this.value_presence_temp    = _value_presence_temp;
  this.value_volume_temp      = Number(_value_volume_temp);
  this.graph_color            = INTRGB(HashCode(this.value_name_client_temp));
  this.circle                 = graph_client_prim_svg.append("circle")
    .attr ("class"       , "graph_client_prim_circle")
    .attr ("color"       , this.graph_color)
    .attr ("face"        , this.value_face_temp)
    .attr ("id"          , this.value_name_client_temp)
    .attr ("pitch"       , this.value_pitch_temp)
    .attr ("presence"    , this.value_presence_temp)
    .attr ("r"           , prim_scale_linear_volume(this.value_volume_temp))
    .attr ("transform"   , "translate(" + prim_translate.x + "," + prim_translate.y + ")")
    .attr ("volume"      , this.value_volume_temp)
    .on   ("click"       , function (e) {
      color_temp    = d3.select(this).attr("color")    != "NaN" ? d3.select(this).attr("color")    : "...";
      face_temp     = d3.select(this).attr("face")     != "NaN" ? d3.select(this).attr("face")     : "...";
      id_temp       = d3.select(this).attr("id")       != "NaN" ? d3.select(this).attr("id")       : "...";
      pitch_temp    = d3.select(this).attr("pitch")    != "NaN" ? d3.select(this).attr("pitch")    : "...";
      presence_temp = d3.select(this).attr("presence") != "NaN" ? d3.select(this).attr("presence") : "...";
      volume_temp   = d3.select(this).attr("volume")   != "NaN" ? d3.select(this).attr("volume")   : "...";
      $("#value_color_graph_client_prim"   ).html(color_temp);
      $("#value_face_graph_client_prim"    ).html(face_temp);
      $("#value_name_graph_client_prim"    ).html(id_temp);
      $("#value_pitch_graph_client_prim"   ).html(pitch_temp);
      $("#value_presence_graph_client_prim").html(presence_temp);
      $("#value_volume_graph_client_prim"  ).html(volume_temp);
    })
    .style("fill"        , ShadeRGBColor("rgb(" + HexRGB(this.graph_color).r + ", " + HexRGB(this.graph_color).g + ", " + HexRGB(this.graph_color).b +")", prim_scale_linear_pitch(this.value_pitch_temp)))
    .style("stroke"      , this.graph_color)
    .style("stroke-width", 5);
  graph_client_prim_array.push(this.circle);
}



function graph_client_prim_degree_target_determine () {
  graph_client_prim_degree_target_array = [];
  for (var i = 0; i < graph_client_prim_array.length; i ++) {
    var graph_client_prim_degree_target_temp = (i/graph_client_prim_array.length)*360;
    graph_client_prim_degree_target_array.push(graph_client_prim_degree_target_temp);
  }
}



function graph_client_prim_presence () {
  if (graph_client_prim_array.length > 1){
    // Iterate through all active client circle.
    for (var i = 0; i < graph_client_prim_array.length; i ++) {
      if (graph_client_prim_array[i].attr("presence") != null) {
        var value_presence_temp = graph_client_prim_array[i].attr("presence").split(",");
        // Iterate through all name list in the presence list.
        for (var j = 0; j < value_presence_temp.length; j ++) {
          // Search for which client circle is connected.
          for (var k = 0; k < graph_client_prim_array.length; k ++) {
            if (
              graph_client_prim_array[k].attr("id") == value_presence_temp[j] &&
              graph_client_prim_array[i].attr("id") != graph_client_prim_array[k].attr("id")
            ) {
              var c_x_1    = Number(graph_client_prim_array[i].attr("cx"));
              var c_x_2    = Number(graph_client_prim_array[k].attr("cx"));
              var c_y_1    = Number(graph_client_prim_array[i].attr("cy"));
              var c_y_2    = Number(graph_client_prim_array[k].attr("cy"));
              var r_1      = Number(graph_client_prim_array[i].attr("r" ));
              var r_2      = Number(graph_client_prim_array[k].attr("r" ));
              var distance = Math.atan2(c_y_2 - c_y_1, c_x_2 - c_x_1);
              var x_1      = c_x_1 + (r_1*Math.cos(distance));
              var x_2      = c_x_2 - (r_2*Math.cos(distance));
              var y_1      = c_y_1 + (r_1*Math.sin(distance));
              var y_2      = c_y_2 - (r_2*Math.sin(distance));
              graph_client_prim_svg.append("circle")
                .attr("class", "prim_presence_circle")
                .attr("cx", x_2)
                .attr("cy", y_2)
                .attr("r", 10)
                .attr(
                  "transform",
                  "translate(" +
                    prim_translate.x + ", " +
                    prim_translate.y +
                  ")"
                )
                .style("opacity", 1)
                .style("fill", graph_client_prim_array[i].style("stroke"))
                .style("stroke", "no-stroke");
              graph_client_prim_svg.append("line")
                .attr("class", "prim_presence_line")
                .attr("x1", x_1)
                .attr("y1", y_1)
                .attr("x2", x_2)
                .attr("y2", y_2)
                .attr(
                  "transform",
                  "translate(" +
                    prim_translate.x + ", " +
                    prim_translate.y +
                  ")"
                )
                .style("opacity", 0.5)
                .style("stroke", graph_client_prim_array[i].style("stroke"))
                .style("stroke-width", 5);
            }
          }
        }
      }
    }
  }
}



function graph_client_prim_auto () {
  if (graph_client_prim_array.length == 1){
    graph_client_prim_array[0]
      .attr("cx"    , 0)
      .attr("cy"    , 0)
      .attr("degree", 0);
  }
  else{
    graph_client_prim_degree_target_determine();
    for (var i = 0; i < graph_client_prim_array.length; i ++) {
      var graph_client_prim_temp = graph_client_prim_array[i];
      graph_client_prim_array[i]
        .attr("cx"    , prim_radius_main*Math.cos(Math.Radian(graph_client_prim_degree_target_array[0])))
        .attr("cy"    , prim_radius_main*Math.sin(Math.Radian(graph_client_prim_degree_target_array[0])))
        .attr("degree", graph_client_prim_degree_target_array[0]);
      graph_client_prim_degree_target_array.splice(0, 1);
    }
  }
}



function resize_graph_client_prim () {
  prim_dimension                        = { height:$("#graph_client_prim_svg_container").height(),width:$("#graph_client_prim_svg_container").width() };
  prim_dimension_smallest               = prim_dimension.height <= prim_dimension.width ? prim_dimension.height : prim_dimension.width;
  prim_padding                          = prim_dimension_smallest/8;

  // Make sure the resize happens only when there is a change in size.
  if (prim_radius_main != prim_dimension_smallest/2 - prim_padding) {
    prim_radius_main                      = prim_dimension_smallest/2 - prim_padding;
    prim_radius_biggest                   = prim_radius_main/6;
    prim_radius_smallest                  = prim_radius_main/12;
    prim_scale_linear_pitch               = d3.scaleLinear().domain([0,pitch_max]).range([0,1]);
    prim_scale_linear_volume              = d3.scaleLinear().domain([0,volume_max]).range([prim_radius_smallest,prim_radius_biggest]);
    prim_translate                        = { x:prim_dimension.width/2,y:prim_dimension.height/2 };

    graph_client_prim_svg
      .attr("height", prim_dimension.height)
      .attr("id", "graph_client_prim_svg")
      .attr("width", prim_dimension.width);

    init_graph_client(received_data)
  }
}