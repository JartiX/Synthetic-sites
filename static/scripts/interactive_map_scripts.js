// Функция для добавления сетки
function addGrid() {
    var gridSize = 50;

    var xScale = d3.scaleLinear()
        .domain([0, svgWidth])
        .range([0, svgWidth]);

    var yScale = d3.scaleLinear()
        .domain([0, svgHeight])
        .range([svgHeight, 0]);

    var xAxis = d3.axisBottom(xScale)
        .ticks(svgWidth / gridSize)
        .tickSize(-svgHeight)
        .tickFormat('');

    var yAxis = d3.axisLeft(yScale)
        .ticks(svgHeight / gridSize)
        .tickSize(-svgWidth)
        .tickFormat('');

    g.append('g')
        .attr('class', 'grid')
        .call(xAxis)
        .attr('transform', `translate(0, ${svgHeight})`);

    g.append('g')
        .attr('class', 'grid')
        .call(yAxis);
}

function zoomIn() {
    svg.transition().duration(500).call(zoom.scaleBy, 1.2);
}

function zoomOut() {
    svg.transition().duration(500).call(zoom.scaleBy, 0.8);
}


var svg = d3.select('#map');
var svgWidth = +svg.attr('width');
var svgHeight = +svg.attr('height');

// Преобразование координат Y для начала координат в левом нижнем углу
objects.forEach(d => {
    d.coords[1] = svgHeight - d.coords[1];
});

var g = svg.append('g'); // Создание группы для масштабирования

// Добавление сетки на карту
addGrid();

// Добавление меток на карту
g.selectAll('.marker')
    .data(objects)
    .enter()
    .append('g')
    .attr('class', 'marker')
    .attr('transform', d => `translate(${d.coords[0]}, ${d.coords[1]})`)
    .style('cursor', 'pointer')
    .on('mouseover', function (event, d) {
        d3.select(this).select('circle').attr('fill', 'blue');
        d3.select(this).select('polygon').attr('fill', 'blue');

        // Создание группы для подсказки
        var tooltip = g.append('g')
            .attr('class', 'tooltip')
            .attr('transform', `translate(${d.coords[0] + 15}, ${d.coords[1] - 25})`)
            .attr('pointer-events', 'none');

        // Отступы
        var padding = 15;

        // Добавление текста имени
        var nameText = tooltip.append('text')
            .attr('x', padding)
            .attr('y', 0)
            .attr('class', 'name')
            .text(d.name);

        // Добавление текста типа
        var typeText = tooltip.append('text')
            .attr('x', padding)
            .attr('y', padding)
            .attr('class', 'type')
            .text(d.category);

        // Задержка для рендеринга текста перед измерением размеров
        requestAnimationFrame(() => {
            var nameBBox = nameText.node().getBBox();
            var typeBBox = typeText.node().getBBox();

            var width = Math.max(nameBBox.width, typeBBox.width) + padding * 2; // Ширина с отступами
            var height = nameBBox.height + typeBBox.height + padding; // Высота с отступами

            // Добавление фона для подсказки после получения размеров текста
            tooltip.insert('rect', ':first-child')
                .attr('class', 'tooltip-bg')
                .attr('width', width)
                .attr('height', height)
                .attr('x', 0)
                .attr('y', -padding);
        });
    })
    .on('mouseout', function () {
        d3.select(this).select('circle').attr('fill', 'red');
        d3.select(this).select('polygon').attr('fill', 'red');
        g.select('.tooltip').remove(); // Удалить всплывающую подсказку
    })
    .on('click', function (event, d) {
        parent.postMessage({
            type: 'selectLocation',
            id: d.id
        }, '*');
    })
    .append('circle')
    .attr('r', 10) // Радиус круга
    .attr('cx', 0)
    .attr('cy', 0)
    .attr('stroke', '#fff')
    .attr('stroke-width', 2)
    .attr('fill', 'red');

// Добавление треугольника как нижней части метки
g.selectAll('.marker')
    .append('polygon')
    .attr('points', '-5,5 5,5 0,15') // Координаты треугольника
    .attr('fill', 'red');

// Создание функции масштабирования
var zoom = d3.zoom()
    .on('zoom', function (event) {
        g.attr('transform', event.transform);
    });

// Применение масштабирования к SVG элементу
svg.call(zoom);