Шаг 1: Установка необходимых библиотек
Убедитесь, что у вас установлены следующие библиотеки:

sh
Copy
1
pip install pygraphviz json
Также установите Graphviz на вашу систему:

Для Windows: Скачайте и установите с официального сайта Graphviz .
Для macOS: Используйте Homebrew:
sh
Copy
1
brew install graphviz
Для Linux: Используйте пакетный менеджер (например, apt для Ubuntu):
sh
Copy
1
sudo apt-get install graphviz
Шаг 2: Написание скрипта для преобразования и визуализации
Создайте новый Python-скрипт, например, visualize_sbom.py, и добавьте в него следующий код:

python
Copy
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
import json
import pygraphviz as pgv

def parse_cyclonedx(sbom_file):
    with open(sbom_file, 'r') as f:
        sbom_data = json.load(f)
    return sbom_data

def build_graph(sbom_data):
    G = pgv.AGraph(directed=True)

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
    G.layout(prog='dot')
    G.draw('dependency_graph.png')

if __name__ == "__main__":
    sbom_file = "path_to_your_sbom.json"  # Замените на путь к вашему SBOM файлу
    try:
        sbom_data = parse_cyclonedx(sbom_file)
        G = build_graph(sbom_data)
        if G.number_of_nodes() > 0:
            visualize_graph(G)
            print("Dependency graph saved as dependency_graph.png")
        else:
            print("No components found in the SBOM file.")
    except Exception as e:
