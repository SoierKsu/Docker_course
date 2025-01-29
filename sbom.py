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

def visualize_graph(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold')
    plt.show()

if __name__ == "__main__":
    sbom_file = "path_to_your_sbom.json"  # Замените на путь к вашему SBOM файлу
    try:
        sbom_data = parse_cyclonedx(sbom_file)
        G = build_graph(sbom_data)
        if G.number_of_nodes() > 0:
            visualize_graph(G)
        else:
            print("No components found in the SBOM file.")
    except Exception as e:
        print(f"Error processing the SBOM file: {e}")
