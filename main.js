const data = [10, 100, 500, 900];

const size = 600;

var mainView = d3.select('body').append('svg')
    .attr('width', size)
    .attr('height', size);

var lines = d3.select('svg').selectAll('line').data(data);

// value scaling
var vertCoordScaler = d3.scaleLinear().domain([0, 1000]).range([0, size]);

// enter
var lines_enter = lines.enter().append('line')
    .attr('x1', 0)
    .attr('y1', v => vertCoordScaler(v))
    .attr('x2', 1000)
    .attr('y2', v => vertCoordScaler(v))
    .attr('stroke', 'green');