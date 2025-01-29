<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Interactive SBOM Graph</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        .node {
            cursor: pointer;
        }
        .node circle {
            fill: #fff;
            stroke: steelblue;
            stroke-width: 3px;
        }
        .node text {
            font: 12px sans-serif;
        }
        .link {
            fill: none;
            stroke: #ccc;
            stroke-width: 2px;
        }
    </style>
</head>
<body>
    <svg width="960" height="600"></svg>
    <script>
        const svg = d3.select("svg"),
              width = +svg.attr("width"),
              height = +svg.attr("height");

        const zoom = d3.zoom()
            .scaleExtent([1 / 2, 8])
            .on("zoom", zoomed);

        svg.call(zoom);

        const g = svg.append("g");

        // Загрузите ваш JSON файл здесь
        d3.json("bom.cdx.json").then(function(graph) {
            const simulation = d3.forceSimulation(graph.nodes)
                .force("link", d3.forceLink(graph.links).id(d => d.id))
                .force("charge", d3.forceManyBody())
                .force("center", d3.forceCenter(width / 2, height / 2));

            const link = g.append("g")
                .attr("class", "link")
                .selectAll("line")
                .data(graph.links)
                .enter().append("line");

            const node = g.append("g")
                .attr("class", "node")
                .selectAll("g")
                .data(graph.nodes)
                .enter().append("g");

            node.append("circle")
                .attr("r", 10)
                .call(drag(simulation));

            node.append("text")
                .attr("dy", 3)
                .text(d => d.name);

            node.on("click", function(event, d) {
                // Логика для скрытия/открытия веток
                console.log(d);
            });

            simulation.on("tick", () => {
                link
                    .attr("x1", d => d.source.x)
                    .attr("y1", d => d.source.y)
                    .attr("x2", d => d.target.x)
                    .attr("y2", d => d.target.y);

                node
                    .attr("transform", d => `translate(${d.x},${d.y})`);
            });
        });

        function drag(simulation) {   
            function dragstarted(event, d) {
                if (!event.active) simulation.alphaTarget(0.3).restart();
                d.fx = d.x;
                d.fy = d.y;
            }
            
            function dragged(event, d) {
                d.fx = event.x;
                d.fy = event.y;
            }
            
            function dragended(event, d) {
                if (!event.active) simulation.alphaTarget(0);
                d.fx = null;
                d.fy = null;
            }
            
            return d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended);
        }

        function zoomed(event) {
            g.attr("transform", event.transform);
        }
    </script>
</body>
</html>
