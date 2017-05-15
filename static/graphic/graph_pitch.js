var axis_graph_pitch           = null;
var bottom_padding_graph_pitch = null;
var div_container_graph_pitch  = "";
var duration_graph_pitch       = null;
var has_inited_graph_pitch     = false;
var height_graph_pitch         = null;
var limit_graph_pitch          = null;
var line_graph_pitch           = null;
var now_graph_pitch            = null;
var path_data_graph_pitch      = null;
var path_graph_pitch           = null;
var svg_graph_pitch            = null;
var width_graph_pitch          = null;
var x_graph_pitch              = null;
var y_graph_pitch              = null;
function init_graph_pitch () {
  bottom_padding_graph_pitch   = $(div_container_graph_pitch).height()/6;
  duration_graph_pitch         = 750;
  height_graph_pitch           = $(div_container_graph_pitch).height() - bottom_padding_graph_pitch;
  limit_graph_pitch            = 60;
  width_graph_pitch            = $(div_container_graph_pitch).width();
  now_graph_pitch              = new Date(Date.now() - duration_graph_pitch);

  path_data_graph_pitch = {
    pitch:{
      color:"gold",
      data:d3.range(limit_graph_pitch).map(function () {
        return 0;
      }),
      value:0
    }
  };

  x_graph_pitch = d3.scaleTime()
    .domain([now_graph_pitch - (limit_graph_pitch - 2), now_graph_pitch - duration_graph_pitch])
    .range([0, width_graph_pitch]);
  y_graph_pitch = d3.scaleLinear()
    .domain([0, 5000])
    .range([height_graph_pitch, 0]);

  line_graph_pitch = d3.line()
    .curve(d3.curveBasis)
    .x(function (d, i) {
      return x_graph_pitch(now_graph_pitch - (limit_graph_pitch - 1 - i)*duration_graph_pitch);
    })
    .y(function (d) {
      return y_graph_pitch(d);
    });

  svg_graph_pitch = d3.select(div_container_graph_pitch).append("svg")
    .attr("class", "chart")
    .attr("width", width_graph_pitch)
    .attr("height", height_graph_pitch + bottom_padding_graph_pitch);

  axis_graph_pitch = svg_graph_pitch.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height_graph_pitch + ")")
    .call(x_graph_pitch.axis = d3.axisBottom().scale(x_graph_pitch));

  path_graph_pitch = svg_graph_pitch.append("g")

  path_data_graph_pitch["pitch"].path = path_graph_pitch.append("path")
    .data([path_data_graph_pitch["pitch"].data])
    .attr("class", "pitch path")
    .style("stroke", path_data_graph_pitch["pitch"].color);

  loop_graph_pitch();
}
function loop_graph_pitch () {
  now_graph_pitch = new Date();

  path_data_graph_pitch["pitch"].data.push(value_pitch);
  path_data_graph_pitch["pitch"].path.attr("d", line_graph_pitch);

  x_graph_pitch.domain([
    now_graph_pitch - (limit_graph_pitch - 2)*duration_graph_pitch,
    now_graph_pitch - duration_graph_pitch
  ]);

  axis_graph_pitch
    .transition()
    .duration(duration_graph_pitch)
    .ease(d3.easeLinear)
    .call(x_graph_pitch.axis);

  path_graph_pitch.attr("transform", null)
    .transition()
    .attr("transform", "translate(" + x_graph_pitch(now_graph_pitch - (limit_graph_pitch - 1)*duration_graph_pitch) + ")")
    .duration(duration_graph_pitch)
    .ease(d3.easeLinear)
    .on("end", loop_graph_pitch);

  //Remove oldest data point from each groups.
  path_data_graph_pitch["pitch"].data.shift();
}
// Function to re - adjust the position and size of this graph.
function resize_graph_pitch () {
  bottom_padding_graph_pitch = $(div_container_graph_pitch).height()/6;
  height_graph_pitch = $(div_container_graph_pitch).height() - bottom_padding_graph_pitch;
  width_graph_pitch = $(div_container_graph_pitch).width();
  x_graph_pitch.range([0, width_graph_pitch]);
  y_graph_pitch.range([height_graph_pitch, 0]);
  svg_graph_pitch
    .attr("width", width_graph_pitch)
    .attr("height", height_graph_pitch + bottom_padding_graph_pitch);
  axis_graph_pitch
    .attr("transform", "translate(0," + height_graph_pitch + ")");
  path_graph_pitch.attr("transform", "translate(" + x_graph_pitch(now_graph_pitch - (limit_graph_pitch - 1)*duration_graph_pitch) + ")");
}