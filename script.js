// Загрузите ваш SVG файл (замените на путь к вашему SVG)
d3.xml('path/to/your/graph.svg').then(function(xml) {
    // Добавляем содержимое SVG в DOM
    const svgNode = document.importNode(xml.documentElement, true);
    d3.select('#graph').node().appendChild(svgNode);

    // Получаем все узлы графа (предположим, что они имеют класс 'node')
    const nodes = d3.selectAll('.node');

    // Добавляем кнопку для каждого узла
    nodes.each(function(d, i) {
        const node = d3.select(this);
        const bbox = node.node().getBBox();

        // Создаем кнопку '+'
        const button = node.append('text')
            .attr('class', 'button')
            .attr('x', bbox.x + bbox.width + 5)
            .attr('y', bbox.y + bbox.height / 2 + 4)
            .text('+')
            .on('click', function(event) {
                toggleChildren(node);
            });
    });

    // Функция для скрытия/показа дочерних элементов узла
    function toggleChildren(node) {
        const children = node.selectAll('.child'); // Предположим, что дочерние элементы имеют класс 'child'
        if (children.empty()) return;

        const isVisible = children.style('display') !== 'none';
        children.style('display', isVisible ? 'none' : 'inline');
        
        // Меняем текст кнопки в зависимости от состояния
        const button = node.select('.button');
        button.text(isVisible ? '+' : '-');
    }

    // Автоматическое масштабирование SVG для вписывания в окно
    autoFitSvg();
});

function autoFitSvg() {
    const svg = d3.select('#graph');
    const viewBox = svg.attr('viewBox').split(' ').map(Number);
    const width = viewBox[2];
    const height = viewBox[3];

    const containerWidth = window.innerWidth;
    const containerHeight = window.innerHeight;

    const scaleX = containerWidth / width;
    const scaleY = containerHeight / height;
    const scale = Math.min(scaleX, scaleY);

    svg.attr('width', width * scale)
       .attr('height', height * scale);
}

// Пересчитываем размер при изменении размера окна
window.addEventListener('resize', autoFitSvg);
