from collections import deque
import matplotlib.pyplot as plt
import networkx as nx


"""""""""
https://python-graph-gallery.com/320-basic-network-from-pandas-data-frame/
"""""""""


# 1. Definición del Grafo Ponderado (Grafo no dirigido con las 39 ciudades)
mapa_carreteras = {

    # Baja California
    "Tijuana": {"Tecate": 52, "Rosarito": 20},
    "Rosarito": {"Tijuana": 20, "Ensenada": 85},
    "Tecate": {"Tijuana": 52, "Mexicali": 135, "Ensenada": 100},
    "Ensenada": {
        "Tecate": 100,
        "Rosarito": 85,
        "San Felipe": 246,
        "San Quintin": 185,
    },

    "Mexicali": {"Tecate": 135, "San Luis Rio Colorado": 80, "San Felipe": 197},
    "San Felipe": {"Mexicali": 197, "Ensenada": 246, "Guerrero negro": 394},
    "San Quintin": {"Ensenada": 185, "Guerrero negro": 425},
    # Baja California Sur
    "Guerrero negro": {
        "San Quintin": 425,
        "San Felipe": 394,
        "Santa Rosalia": 220,
    },
    "Santa Rosalia": {"Guerrero negro": 220, "Mulegé": 63},
    "Mulegé": {"Santa Rosalia": 63, "Ciudad Constitución": 283},
    "Ciudad Constitución": {"Mulegé": 283, "San Carlos": 61, "La Paz": 210},
    "San Carlos": {"Ciudad Constitución": 61},
    "La Paz": {
        "Ciudad Constitución": 210,
        "Cabo San Lucas": 157,
        "San José del Cabo": 201,
    },
    "San José del Cabo": {"La Paz": 201, "Cabo San Lucas": 38},
    "Cabo San Lucas": {"La Paz": 157, "San José del Cabo": 38},
    # Sonora
    "San Luis Rio Colorado": {"Mexicali": 80, "Sonoyta": 203},
    "Sonoyta": {
        "San Luis Rio Colorado": 203,
        "Puerto Peñasco": 98,
        "Caborca": 149,
    },
    "Puerto Peñasco": {"Sonoyta": 98, "Caborca": 176},
    "Caborca": {"Sonoyta": 149, "Puerto Peñasco": 176, "Santa Ana": 107},
    "Nogales": {"Santa Ana": 107, "Cananea": 99},
    "Santa Ana": {
        "Caborca": 107,
        "Nogales": 107,
        "Cananea": 125,
        "Hermosillo": 171,
    },
    "Cananea": {"Nogales": 99, "Santa Ana": 125, "Agua Prieta": 86},
    "Agua Prieta": {"Cananea": 86, "Moctezuma": 199, "Janos": 160},
    "Hermosillo": {
        "Santa Ana": 171,
        "Moctezuma": 178,
        "Yécora": 278,
        "Guaymas": 135,
    },
    "Moctezuma": {"Agua Prieta": 199, "Hermosillo": 178, "Yécora": 257},
    "Guaymas": {"Hermosillo": 135, "Ciudad Obregón": 130},
    "Ciudad Obregón": {"Guaymas": 130},
    "Yécora": {
        "Hermosillo": 278,
        "Moctezuma": 257,
        "Ciudad Cuauhtemoc": 309,
    },
    # Chihuahua
    "Janos": {"Agua Prieta": 160, "Ciudad Juárez": 212, "Flores Magón": 173},
    "Ciudad Juárez": {"Janos": 212, "Villa Ahumada": 125},
    "Villa Ahumada": {"Ciudad Juárez": 125, "Flores Magón": 93, "Sueco": 85},
    "Flores Magón": {
        "Janos": 173,
        "Villa Ahumada": 93,
        "Sueco": 60,
        "Ciudad Cuauhtemoc": 211,
    },
    "Sueco": {"Villa Ahumada": 85, "Flores Magón": 60, "Chihuahua": 158},
    "Ciudad Cuauhtemoc": {
        "Yécora": 309,
        "Flores Magón": 211,
        "Chihuahua": 105,
    },
    "Chihuahua": {
        "Sueco": 158,
        "Ciudad Cuauhtemoc": 105,
        "Ojinaga": 379,
        "Delicias": 87,
        "Parral": 225,
    },
    "Ojinaga": {"Chihuahua": 379},
    "Delicias": {"Chihuahua": 87, "Ciudad Jiménez": 139},
    "Ciudad Jiménez": {"Delicias": 139, "Parral": 215},
    "Parral": {"Chihuahua": 225, "Ciudad Jiménez": 215},

}


# 2. Creación del objeto Grafo en NetworkX
G = nx.Graph()
for origen, vecinos in mapa_carreteras.items():
    for destino, km in vecinos.items():
        G.add_edge(origen, destino, weight=km)


# Configuración del diseño gráfico (distribución de nodos fija)
pos = nx.spring_layout(G, seed=58, k=0.8)  # Distribuye los nodos ordenadamente

# Activar modo interactivo de Matplotlib para la animación
plt.ion()
fig, ax = plt.subplots(figsize=(13, 11))


def renderizar_grafo(aristas_exploradas, aristas_correctas, nodo_actual=None, titulo=""):
    """Redibuja el grafo en tiempo real actualizando colores y grosor de aristas."""
    ax.clear()

    # Asignar colores a las aristas
    edge_colors = []
    edge_widths = []

    for u, v in G.edges():
        pair1, pair2 = (u, v), (v, u)
        if pair1 in aristas_correctas or pair2 in aristas_correctas:
            edge_colors.append("#2ecc71")  # Verde: Ruta óptima final
            edge_widths.append(4.0)
        elif pair1 in aristas_exploradas or pair2 in aristas_exploradas:
            edge_colors.append("#f1c40f")  # Amarillo: Explorada por BFS
            edge_widths.append(2.5)
        else:
            edge_colors.append("#dcdde1")  # Gris: Arista sin explorar
            edge_widths.append(2.0)


    # Colores de los nodos
    node_colors = []
    for node in G.nodes():
        if node == nodo_actual:
            node_colors.append("#e74c3c")  # Rojo: Nodo explorando en este instante
        else:
            node_colors.append("#3498db")  # Azul: Nodo estándar


    # Dibujar componentes del grafo
    nx.draw_networkx_nodes(
        G,
        pos,
        ax=ax,
        node_color=node_colors,
        node_size=800,
        edgecolors="#000000",
    )
    nx.draw_networkx_labels(
        G, pos, ax=ax, font_size=7, font_weight="bold", font_color="black"
    )
    nx.draw_networkx_edges(
        G, pos, ax=ax, edge_color=edge_colors, width=edge_widths
    )

    # Dibujar etiquetas de kilómetros
    km_labels = nx.get_edge_attributes(G, "weight")

    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=km_labels, font_size=6, ax=ax, rotate=False
    )

    plt.title(
        titulo, fontsize=12, fontweight="bold", pad=15, color="000000"
    )
    plt.axis("off")
    plt.tight_layout()
    plt.draw()
    plt.pause(0.3)  # Delay de 300 milisegundos entre cada paso


def breadth_first_search_animado(grafo, inicio, destino):
    if inicio == destino:
        return [inicio], set(), set(), 0

    frontier = deque([inicio])  #Cola FIFO
    reached = {inicio}  #Conjunto de descubiertos
    parent = {inicio: None}  #Diccionario de padres

    aristas_exploradas = set()
    aristas_correctas = set()

    paso = 1

    while frontier:
        node = frontier.popleft()  # Sacar nodo actual[cite: 3]

        vecinos = list(grafo.get(node, {}).keys())

        for child in vecinos:
            if child not in reached:
                reached.add(child)
                parent[child] = node
                frontier.append(child)

                # Registrar la arista recorrida (Amarillo)s
                aristas_exploradas.add((node, child))

                # Actualizar pantalla
                renderizar_grafo(
                    aristas_exploradas,
                    aristas_correctas,
                    nodo_actual=child,
                    titulo=f"PASO {paso}: Explorando tramo {node} -> {child} (Búsqueda BFS)",
                )

                paso += 1
                if child == destino:
                    # Reconstruir la ruta[cite: 4]
                    ruta = []
                    actual = destino
                    while actual is not None:
                        ruta.append(actual)
                        actual = parent[actual]
                    ruta.reverse()

                    # Convertir la ruta en pares de aristas y animar en verde
                    for i in range(len(ruta) - 1):
                        aristas_correctas.add((ruta[i], ruta[i + 1]))
                        renderizar_grafo(
                            aristas_exploradas,
                            aristas_correctas,
                            nodo_actual=ruta[i + 1],
                            titulo=f"¡Ruta Encontrada! Trazando camino final en verde: {ruta[i]} -> {ruta[i+1]}",
                        )
                        plt.pause(1)

                    return ruta, aristas_exploradas, aristas_correctas,paso

        #paso += 1

    return "failure", aristas_exploradas, aristas_correctas, paso


# --- Inicio d programa  ---
origen = "Tijuana"
destino = "Mulegé"

ruta_final, exploradas, correctas, paso = breadth_first_search_animado(mapa_carreteras, origen, destino)

# Mantener la ventana abierta al finalizar

plt.ioff()
if ruta_final != "failure":
    # Calcular kilómetros totales
    km_totales = sum(
        mapa_carreteras[ruta_final[i]][ruta_final[i + 1]]
        for i in range(len(ruta_final) - 1)
    )
    renderizar_grafo(
        exploradas,
        correctas,
        titulo=f"BÚSQUEDA FINALIZADA\nRuta: {' -> '.join(ruta_final)}\n| Distancia Total: {km_totales} km |\n| Pasos:{paso} | ",
    )
else:
    print("No se encontró una ruta.")

plt.show()