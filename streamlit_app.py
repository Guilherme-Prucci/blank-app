import streamlit as st
from pyvis import network as net
import streamlit.components.v1 as components
import networkx as nx

nodes = [
    "Filosofia",
    "Matemática",
    "Estatística",
    "Lógica",
    "Física",
    "Física Quântica",
    "Biologia",
    "Química",
    "Engenharia",
    "Ciência da Computação",
    "Inteligência Artificial",
    "Neurociência",
    "Psicologia",
    "Linguística",
    "Sociologia"
]

edges = [
    ("Filosofia", "Lógica"),
    ("Filosofia", "Matemática"),
    ("Filosofia", "Física"),
    ("Filosofia", "Psicologia"),
    ("Filosofia", "Linguística"),
    ("Matemática", "Estatística"),
    ("Matemática", "Física"),
    ("Matemática", "Ciência da Computação"),
    ("Matemática", "Engenharia"),
    ("Estatística", "Inteligência Artificial"),
    ("Estatística", "Ciência da Computação"),
    ("Lógica", "Matemática"),
    ("Lógica", "Ciência da Computação"),
    ("Física", "Física Quântica"),
    ("Física", "Engenharia"),
    ("Física", "Química"),
    ("Física Quântica", "Filosofia"),
    ("Física Quântica", "Matemática"),
    ("Química", "Biologia"),
    ("Biologia", "Neurociência"),
    ("Neurociência", "Psicologia"),
    ("Psicologia", "Sociologia"),
    ("Linguística", "Psicologia"),
    ("Linguística", "Ciência da Computação"),
    ("Ciência da Computação", "Inteligência Artificial"),
    ("Inteligência Artificial", "Neurociência"),
    ("Engenharia", "Ciência da Computação"),
]

# Criar rede
g = net.Network(height="800px", width="100%", directed=False)

g_nx = nx.DiGraph()
g_nx.add_nodes_from(nodes)
g_nx.add_edges_from(edges)

# Adicionar nós
for node in nodes:
    g.add_node(node, label=node)

# Adicionar arestas
for source, target in edges:
    g.add_edge(source, target)

#lista de sliders para opções de física
gravitationalConstant = st.slider('Gravitational Constant', -3000, 0, -500, 5)
centralGravity = st.slider('Central Gravity', 0.0, 10.0, 0.1, 0.01)
springLength = st.slider('Spring Length', 0.0, 1000.0, 100.0, 10.0)
springConstant = st.slider('Spring Constant', 0.0, 1.2, 0.1, 0.01)
damping = st.slider('Damping', 0.0, 1.0, 0.1, 0.01)
avoidOverlap = st.slider('Avoid Overlap', 0.0, 1.0, 0.1, 0.01)
maxVelocity = st.slider('Max Velocity', 0.0, 1000.0, 100.0, 10.0)
minVelocity = st.slider('Min Velocity', 0.0, 1.0, 0.1, 0.01)
solver = st.selectbox('Solver', ['barnesHut', 'repulsion', 'hierarchicalRepulsion', 'forceAtlas2Based', 'forceAtlas2BasedWithGravity', 'forceAtlas2BasedWithGravityAndRepulsion'])
timestep = st.slider('Timestep', 0.0, 1.0, 0.1, 0.01)



physics_options = f"""
var options = {{
  "physics": {{
    "solver": "{solver}",
    "barnesHut": {{
      "gravitationalConstant": {gravitationalConstant},
      "centralGravity": {centralGravity},
      "springLength": {springLength},
      "springConstant": {springConstant},
      "damping": {damping},
      "avoidOverlap": {avoidOverlap}
    }},
    "maxVelocity": {maxVelocity},
    "minVelocity": {minVelocity},
    "timestep": {timestep}
  }}
}}
"""
g.set_options(physics_options)

densidade = nx.density(g_nx)
assortatividade = nx.degree_assortativity_coefficient(g_nx)
clustering_global = nx.average_clustering(g_nx.to_undirected())
componentes_fortes = list(nx.strongly_connected_components(g_nx))
componentes_fracos = list(nx.weakly_connected_components(g_nx))

st.markdown("### Métricas de Análise de Rede")
st.write(f"**Densidade da rede**: {densidade:.4f}")
st.write("Ela compara o número de conexões existentes com o número máximo possível de conexões.\n")
st.write(f"**Assortatividade**: {assortatividade:.4f}")
st.write("Mede se nós com grau alto tendem a se conectar com outros nós com grau alto (e vice-versa).\n")
st.write(f"**Coeficiente de clustering global**: {clustering_global:.4f}")
st.write("Mede o grau em que os vizinhos de um nó estão interconectados entre si.Ou seja, qual a probabilidade de se formarem triângulos.\n")
st.write(f"**Componentes fortemente conectados**: {len(componentes_fortes)}")
st.write("Subconjuntos de nós em que existe um caminho direcionado de qualquer nó para qualquer outro.\n")
st.write(f"**Componentes fracamente conectados**: {len(componentes_fracos)}")
st.write("Subconjuntos de nós em que existe um caminho entre eles se ignorarmos a direção das arestas\n")
g.save_graph('example.html')
with open('example.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

components.html(html_content, height=400)
st.write("fim")
