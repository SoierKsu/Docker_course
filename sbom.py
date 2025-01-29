import json
import networkx as nx
import matplotlib.pyplot as plt

def parse_cyclonedx(sbom_file):
    with open(sbom_file, 'r') as f:
        sbom_data = json.load(f)
    return sbom_data

def build_graph(sbom_data):
    G = nx.DiGraph()

    components = sbom_data.get('components', [])
    for component in components:
        component_name = component.get('name')
        if component_name:
            G.add_node(component_name)

        dependencies = component.get('dependencies', [])
        for dep in dependencies:
            ref = dep.get('ref')
            if ref:
                G.add_edge(component_name, ref)

    return G

def visualize_graph(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold')
    plt.show()

if __name__ == "__main__":
    sbom_file = "path_to_your_sbom.json"  # Замените на путь к вашему SBOM файлу
    sbom_data = parse_cyclonedx(sbom_file)
    G = build_graph(sbom_data)
    visualize_graph(G)
