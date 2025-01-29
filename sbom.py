import json
import networkx as nx
import plotly.graph_objects as go

def parse_cyclonedx(sbom_file):
    with open(sbom_file, 'r') as f:
        sbom_data = json.load(f)
    return sbom_data

def build_graph(sbom_data):
    G = nx.DiGraph()

    components = sbom_data.get('components', [])
    component_map = {}

    # Добавляем компоненты как узлы в граф
    for component in components:
        component_name = component.get('bom-ref')
        if not component_name:
            component_name = component.get('name')
        if component_name:
            G.add_node(component_name)
            component_map[component_name] = component

    # Добавляем зависимости как ребра в граф
    for component in components:
        component_name = component.get('bom-ref')
        if not component_name:
            component_name = component.get('name')
        
        dependencies = component.get('dependencies', {}).get('dependsOn', [])
        for dep_ref in dependencies:
            if dep_ref in component_map:
                G.add_edge(component_name, dep_ref)

    return G

def visualize_graph(G, output_html='dependency_graph.html', output_image='dependency_graph.png'):
    pos = nx.spring_layout(G)

    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=list(G.nodes()),
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=10,
            color=[],
            line_width=2))

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('# of connections: '+str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Dependency Graph',
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        annotations=[ dict(
                            text="Python code: <a href='https://plotly.com/'> https://plotly.com/</a>",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002 ) ],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    # Сохраняем график в HTML
    fig.write_html(output_html)

    # Сохраняем график в изображение (например, PNG)
    fig.write_image(output_image)

    # Отображаем график
    fig.show()

if __name__ == "__main__":
    sbom_file = "path_to_your_sbom.json"  # Замените на путь к вашему SBOM файлу
    try:
        sbom_data = parse_cyclonedx(sbom_file)
        G = build_graph(sbom_data)
        if G.number_of_nodes() > 0:
            visualize_graph(G, output_html='dependency_graph.html', output_image='dependency_graph.png')
            print("Dependency graph saved as dependency_graph.html and dependency_graph.png")
        else:
            print("No components found in the SBOM file.")
    except Exception as e:
        print(f"Error processing the SBOM file: {e}")
