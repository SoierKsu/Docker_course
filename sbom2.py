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
/XMLSchema\schema-instance">componentA</ns0:bom-ref>
<ns0:name>Component A</ns0:name>
<ns0:dependencies>
    <ns0:dependency ref="componentB"/>
</ns0:dependencies>
</ns0:component>
<ns0:component xmlns:ns0="http://cyclonedx.org/schema/bom/1.4">
<ns0:bom-ref>bom-ref-2</ns0:bom-ref>
<ns0:name>Component B</ns0:name>
<ns0:dependencies/>
</ns0:component>
</ns0:components>
</ns0:bom>
