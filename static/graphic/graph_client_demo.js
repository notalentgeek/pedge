var client_demo_array                     = [];
var client_demo_name_array                = ["carl", "chris", "dennet", "neil", "richard", "sam"];
var client_demo_online_chance_step        = 0.01;
var client_demo_online_count              = 0;
var graph_client_demo_array               = [];
var graph_client_demo_degree_target_array = [];
var demo_dimension                        = { height:320,width:320 };
var demo_dimension_smallest               = demo_dimension.height <= demo_dimension.width ? demo_dimension.height : demo_dimension.width;
var demo_padding                          = demo_dimension_smallest/8;
var demo_radius_main                      = demo_dimension_smallest/2 - demo_padding;
var demo_radius_main_prev                 = demo_radius_main;
var demo_radius_biggest                   = demo_radius_main/6;
var demo_radius_smallest                  = demo_radius_main/12;
var demo_scale_linear_pitch               = d3.scaleLinear().domain([0,pitch_max]).range([0,1]);
var demo_scale_linear_volume              = d3.scaleLinear().domain([0,volume_max]).range([demo_radius_smallest,demo_radius_biggest]);
var demo_translate                        = { x:demo_dimension.width/2,y:demo_dimension.height/2 };

var graph_client_demo_svg = d3.select("#graph_client_demo_svg_container").append("svg")
  .attr("height", demo_dimension.height)
  .attr("id", "graph_client_demo_svg")
  .attr("width", demo_dimension.width);

function client_demo (_name) {
  client_demo_array.push(this);
  client_demo_online_count ++;

  this.name = _name;
  this.graph_color = INTRGB(HashCode(this.name));
  this.latest = {
    face    :0,
    pitch   :0,
    volume  :0,
    online  :true,
    presence:[]
  };
  this.online_chance = 1;

  // Let `this` fully initiated first before creating the corresponding graph.
  this.graph = new graph_client_demo(this, 180);
}
function client_demo_all () {
  d3.selectAll(".demo_presence_circle").remove();
  d3.selectAll(".demo_presence_line"  ).remove();

  client_demo_online();

  var debug_online   = "";
  var debug_pitch    = "";
  var debug_presence = "";
  var debug_volume   = "";

  for (var i = 0; i < client_demo_array.length; i ++) {
    var client_demo_temp = client_demo_array[i];
    client_demo_face(client_demo_temp);
    client_demo_pitch(client_demo_temp);
    client_demo_presence(client_demo_temp);
    client_demo_volume(client_demo_temp);

    debug_online   += client_demo_debug_online(client_demo_temp)   + " ";
    debug_pitch    += client_demo_debug_pitch(client_demo_temp)    + " ";
    debug_volume   += client_demo_debug_volume(client_demo_temp)   + " ";
  }

  graph_client_demo_presence();

  //console.log("=========================");
  //console.log(debug_online);
  //console.log(debug_pitch);
  //console.log(debug_presence);
  //console.log(debug_volume);
  //console.log("=========================");
}
function client_demo_debug_online   (_client_demo) { return _client_demo.name + ":" + _client_demo.latest.online; }
function client_demo_debug_pitch    (_client_demo) { return _client_demo.name + ":" + _client_demo.latest.pitch; }
function client_demo_debug_presence (_client_demo) { return _client_demo.name + ":" + _client_demo.latest.presence.length; }
function client_demo_debug_volume   (_client_demo) { return _client_demo.name + ":" + _client_demo.latest.volume; }
function client_demo_face (_client_demo) {
  if (_client_demo.latest.online) {
    _client_demo.latest.face = Math.ceil(
      Math.random()*client_demo_online_count
    );
  }
}
function client_demo_online () {
  for (var i = 0; i < client_demo_array.length; i ++) {
    var client_demo_temp = client_demo_array[i];
    var random = Math.random();

    if (random < client_demo_temp.online_chance) {
      if (!client_demo_temp.latest.online) {
        client_demo_online_count ++;

        // Remove the graph of online client.
        client_demo_temp.graph = new graph_client_demo(client_demo_temp, 180);
        // Re - position.
        graph_client_demo_rotate_auto();

        client_demo_temp.latest.online = true;
        client_demo_temp.online_chance = 1;
      }
      else {
        client_demo_temp.online_chance -= client_demo_online_chance_step;
      }
    }
    else {
      if (client_demo_temp.latest.online) {
        client_demo_online_count --;

        // Remove the graph of offline client.
        client_demo_temp.graph.circle.remove();
        graph_client_demo_array.splice(graph_client_demo_array.indexOf(client_demo_temp.graph), 1);
        client_demo_temp.graph = null;
        // Re - position.
        graph_client_demo_rotate_auto();

        client_demo_temp.latest.online = false;
        client_demo_temp.online_chance = 0;
      }
      else {
        client_demo_temp.online_chance += client_demo_online_chance_step;
      }
    }
  }
}
function client_demo_pitch (_client_demo) {
  if (_client_demo.latest.online) {
    _client_demo.latest.pitch = (Math.random()*pitch_max).toFixed(3);
    graph_client_demo_pitch(_client_demo.graph);
  }
}
function client_demo_presence (_client_demo) {
  _client_demo.latest.presence = [];
  if (_client_demo.latest.online) {
    for (var i = 0; i < client_demo_array.length; i ++) {
      var client_demo_temp = client_demo_array[i];
      if (
        (client_demo_temp.name  != _client_demo.name) &&
        (client_demo_temp.latest.online) &&
        (Math.random() < 0.8)
      ) {
        _client_demo.latest.presence.push(client_demo_temp);
      }
    }
  }
}
function client_demo_volume (_client_demo) {
  if (_client_demo.latest.online) {
    _client_demo.latest.volume = (Math.random()*volume_max).toFixed(3);
    graph_client_demo_volume(_client_demo.graph);
  }
}
function graph_client_demo (_client, _degree) {
  graph_client_demo_array.push(this);
  this.client       = _client;
  this.client.graph = this;
  this.circle       = graph_client_demo_svg.append("circle")
    .attr ("class"       , "graph_client_demo_circle")
    .attr ("cx"          , demo_radius_main*Math.cos(Math.Radian(_degree)))
    .attr ("cy"          , demo_radius_main*Math.sin(Math.Radian(_degree)))
    .attr ("degree"      , _degree)
    .attr ("id"          , this.client.name)
    .attr ("r"           , demo_radius_biggest)
    .attr ("transform"   , "translate(" + demo_translate.x + "," + demo_translate.y + ")")
    .on   ("click"       , function (e) {
      var presence_temp = print_value_in_array_of_dictionary(_client.latest.presence, "name") ? print_value_in_array_of_dictionary(_client.latest.presence, "name") : "...";
      $("#value_color_graph_client_demo"   ).html(_client.graph_color);
      $("#value_face_graph_client_demo"    ).html(_client.latest.face);
      $("#value_name_graph_client_demo"    ).html(_client.name);
      $("#value_pitch_graph_client_demo"   ).html(_client.latest.pitch);
      $("#value_presence_graph_client_demo").html(presence_temp);
      $("#value_volume_graph_client_demo"  ).html(_client.latest.volume);
    })
    .style("fill"        , this.client.graph_color)
    .style("stroke"      , this.client.graph_color)
    .style("stroke-width", 5);
  graph_client_demo_rotate_auto();
}
function graph_client_demo_degree_target_determine () {
  graph_client_demo_degree_target_array = [];
  for (var i = 0; i < graph_client_demo_array.length; i ++) {
    var graph_client_demo_degree_target_temp = (i/graph_client_demo_array.length)*360;
    graph_client_demo_degree_target_array.push(graph_client_demo_degree_target_temp);
  }
}
function graph_client_demo_pitch (_graph_client_demo) {
  _graph_client_demo.client.latest.pitch = (Math.random()*pitch_max).toFixed(3);
  _graph_client_demo.circle.style(
    "fill",
    ShadeRGBColor(
      "rgb(" +
        HexRGB(_graph_client_demo.client.graph_color).r + ", " +
        HexRGB(_graph_client_demo.client.graph_color).g + ", " +
        HexRGB(_graph_client_demo.client.graph_color).b +
      ")",
      demo_scale_linear_pitch(
        _graph_client_demo.client.latest.pitch
      )
    )
  );
}
function graph_client_demo_presence () {
  for (var i = 0; i < graph_client_demo_array.length; i ++) {
    var graph_client_demo_temp = graph_client_demo_array[i];
    for (var j = 0; j < graph_client_demo_temp.client.latest.presence.length; j ++) {
      var client_demo_temp = graph_client_demo_temp.client.latest.presence[j];
      if (client_demo_temp.latest.online) {
        var c_x_1    = Number(graph_client_demo_temp.circle.attr("cx"));
        var c_x_2    = Number(client_demo_temp.graph.circle.attr("cx"));
        var c_y_1    = Number(graph_client_demo_temp.circle.attr("cy"));
        var c_y_2    = Number(client_demo_temp.graph.circle.attr("cy"));
        var r_1      = Number(graph_client_demo_temp.circle.attr("r" ));
        var r_2      = Number(client_demo_temp.graph.circle.attr("r" ));
        var distance = Math.atan2(c_y_2 - c_y_1, c_x_2 - c_x_1);
        var x_1      = c_x_1 + (r_1*Math.cos(distance));
        var x_2      = c_x_2 - (r_2*Math.cos(distance));
        var y_1      = c_y_1 + (r_1*Math.sin(distance));
        var y_2      = c_y_2 - (r_2*Math.sin(distance));
        graph_client_demo_svg.append("circle")
          .attr("class", "demo_presence_circle")
          .attr("cx", x_2)
          .attr("cy", y_2)
          .attr("r", 10)
          .attr(
            "transform",
            "translate(" +
              demo_translate.x + ", " +
              demo_translate.y +
            ")"
          )
          .style("opacity", 1)
          .style("fill", graph_client_demo_temp.client.graph_color)
          .style("stroke", "no-stroke")
          .style("position", "relative");
        graph_client_demo_svg.append("line")
          .attr("class", "demo_presence_line")
          .attr("x1", x_1)
          .attr("y1", y_1)
          .attr("x2", x_2)
          .attr("y2", y_2)
          .attr(
            "transform",
            "translate(" +
              demo_translate.x + ", " +
              demo_translate.y +
            ")"
          )
          .style("opacity", 0.5)
          .style("stroke", graph_client_demo_temp.client.graph_color)
          .style("stroke-width", 5)
          .style("position", "relative");
      }
    }
  }
}
function graph_client_demo_rotate (_graph_client_demo, _degree) {
  _graph_client_demo.circle
    .attr("cx"    , demo_radius_main*Math.cos(Math.Radian(_degree)))
    .attr("cy"    , demo_radius_main*Math.sin(Math.Radian(_degree)))
    .attr("degree", _degree);
}
function graph_client_demo_rotate_auto () {
  if (graph_client_demo_array.length == 1){
    graph_client_demo_array[0].circle
      .attr("cx"    , 0)
      .attr("cy"    , 0)
      .attr("degree", 0);
  }
  else{
    graph_client_demo_degree_target_determine();
    for (var i = 0; i < graph_client_demo_array.length; i ++) {
      var graph_client_demo_temp = graph_client_demo_array[i];
      graph_client_demo_rotate(graph_client_demo_temp, graph_client_demo_degree_target_array[0])
      graph_client_demo_degree_target_array.splice(0, 1);
    }
  }
}
function graph_client_demo_volume (_graph_client_demo) {
  _graph_client_demo.client.latest.volume = (Math.random()*volume_max).toFixed(3);
  _graph_client_demo.circle.attr("r", demo_scale_linear_volume(_graph_client_demo.client.latest.volume));
}
function init_graph_client_demo () {
  for (var i = 0; i < client_demo_name_array.length; i ++) {
    var client_demo_name_temp = client_demo_name_array[i];
    new client_demo(client_demo_name_temp);
  }
}
function resize_graph_client_demo () {
  demo_dimension                 = { height:$("#graph_client_demo_svg_container").height(),width:$("#graph_client_demo_svg_container").width() };
  demo_dimension_smallest        = demo_dimension.height <= demo_dimension.width ? demo_dimension.height : demo_dimension.width;
  demo_padding                   = demo_dimension_smallest/8;

  // Make sure the resize happens only when there is a change in size.
  if (demo_radius_main != demo_dimension_smallest/2 - demo_padding) {
    d3.selectAll(".demo_presence_circle").remove();
    d3.selectAll(".demo_presence_line"  ).remove();

    demo_radius_main_prev        = demo_radius_main;

    demo_radius_main             = demo_dimension_smallest/2 - demo_padding;
    demo_radius_biggest          = demo_radius_main/6;
    demo_radius_smallest         = demo_radius_main/12;
    demo_scale_linear_pitch      = d3.scaleLinear().domain([0,pitch_max]).range([0,1]);
    demo_scale_linear_volume     = d3.scaleLinear().domain([0,volume_max]).range([demo_radius_smallest,demo_radius_biggest]);
    demo_translate               = { x:demo_dimension.width/2,y:demo_dimension.height/2 };

    graph_client_demo_svg
      .attr("height", demo_dimension.height)
      .attr("width" , demo_dimension.width);

    for (var i = 0; i < graph_client_demo_array.length; i ++) {
      var c_x_temp                     = 0;
      var c_y_temp                     = 0;
      var graph_client_demo_temp       = graph_client_demo_array[i];
      var degree                       = Number(graph_client_demo_temp.circle.attr("degree"));
      var radius_prev                  = Number(graph_client_demo_temp.circle.attr("r"));
      var radius_proportion            = (demo_radius_main/demo_radius_main_prev < 1) ? 1 : (demo_radius_main/demo_radius_main_prev);
      var radius                       = radius_proportion*radius_prev;
      if (graph_client_demo_array.length > 1){
        c_x_temp = demo_radius_main*Math.cos(Math.Radian(degree));
        c_y_temp = demo_radius_main*Math.sin(Math.Radian(degree));
      }
      graph_client_demo_temp.circle
        .attr("cx"       , c_x_temp)
        .attr("cy"       , c_y_temp)
        .attr("r"        , demo_radius_biggest)
        .attr("transform", "translate(" + demo_translate.x + "," + demo_translate.y + ")");
    }
  }
}