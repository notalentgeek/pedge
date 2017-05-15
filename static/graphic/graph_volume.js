var axis_graph_volume           = null;
var bottom_padding_graph_volume = null;
var div_container_graph_volume  = "";
var duration_graph_volume       = null;
var has_inited_graph_volume     = false;
var height_graph_volume         = null;
var limit_graph_volume          = null;
var line_graph_volume           = null;
var now_graph_volume            = null;
var path_data_graph_volume      = null;
var path_graph_volume           = null;
var svg_graph_volume            = null;
var width_graph_volume          = null;
var x_graph_volume              = null;
var y_graph_volume              = null;
function init_graph_volume () {
  bottom_padding_graph_volume   = $(div_container_graph_volume).height()/6;
  duration_graph_volume         = 750;
  height_graph_volume           = $(div_container_graph_volume).height() - bottom_padding_graph_volume;
  limit_graph_volume            = 60;
  width_graph_volume            = $(div_container_graph_volume).width();
  now_graph_volume              = new Date(Date.now() - duration_graph_volume);

  path_data_graph_volume = {
    volume:{
      color:"goldenrod",
      data:d3.range(limit_graph_volume).map(function () {
        return 0;
      }),
      value:0
    }
  };

  x_graph_volume = d3.scaleTime()
    .domain([now_graph_volume - (limit_graph_volume - 2), now_graph_volume - duration_graph_volume])
    .range([0, width_graph_volume]);
  y_graph_volume = d3.scaleLinear()
    .domain([0, 0.1])
    .range([height_graph_volume, 0]);

  line_graph_volume = d3.line()
    .curve(d3.curveBasis)
    .x(function (d, i) {
      return x_graph_volume(now_graph_volume - (limit_graph_volume - 1 - i)*duration_graph_volume);
    })
    .y(function (d) {
      return y_graph_volume(d);
    });

  svg_graph_volume = d3.select(div_container_graph_volume).append("svg")
    .attr("class", "chart")
    .attr("width", width_graph_volume)
    .attr("height", height_graph_volume + bottom_padding_graph_volume);

  axis_graph_volume = svg_graph_volume.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height_graph_volume + ")")
    .call(x_graph_volume.axis = d3.axisBottom().scale(x_graph_volume));

  path_graph_volume = svg_graph_volume.append("g")

  path_data_graph_volume["volume"].path = path_graph_volume.append("path")
    .data([path_data_graph_volume["volume"].data])
    .attr("class", "volume path")
    .style("stroke", path_data_graph_volume["volume"].color);

  loop_graph_volume();
}
function loop_graph_volume () {
  now_graph_volume = new Date();

  path_data_graph_volume["volume"].data.push(value_volume);
  path_data_graph_volume["volume"].path.attr("d", line_graph_volume);

  x_graph_volume.domain([
    now_graph_volume - (limit_graph_volume - 2)*duration_graph_volume,
    now_graph_volume - duration_graph_volume
  ]);

  axis_graph_volume
    .transition()
    .duration(duration_graph_volume)
    .ease(d3.easeLinear)
    .call(x_graph_volume.axis);

  path_graph_volume.attr("transform", null)
    .transition()
    .attr("transform", "translate(" + x_graph_volume(now_graph_volume - (limit_graph_volume - 1)*duration_graph_volume) + ")")
    .duration(duration_graph_volume)
    .ease(d3.easeLinear)
    .on("end", loop_graph_volume);

  //Remove oldest data point from each groups.
  path_data_graph_volume["volume"].data.shift();
}
// Function to re - adjust the position and size of this graph.
function resize_graph_volume () {
  bottom_padding_graph_volume = $(div_container_graph_volume).height()/6;
  height_graph_volume = $(div_container_graph_volume).height() - bottom_padding_graph_volume;
  width_graph_volume = $(div_container_graph_volume).width();
  x_graph_volume.range([0, width_graph_volume]);
  y_graph_volume.range([height_graph_volume, 0]);
  svg_graph_volume
    .attr("width", width_graph_volume)
    .attr("height", height_graph_volume + bottom_padding_graph_volume);
  axis_graph_volume
    .attr("transform", "translate(0," + height_graph_volume + ")");
  path_graph_volume.attr("transform", "translate(" + x_graph_volume(now_graph_volume - (limit_graph_volume - 1)*duration_graph_volume) + ")");
}