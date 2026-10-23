from collections import deque

mapa_carreteras = {
    "Tijuana": ["Tecate", "Rosarito"],
    "Tecate": ["Tijuana", "Mexicali", "Ensenada"],
    "Rosarito": ["Tijuana", "Ensenada"],
    "Mexicali": ["Tecate", "San Luis Rio Colorado", "San Felipe"],
    "Ensenada": ["Tecate", "Rosarito", "San Quintin", "San Felipe"],
    "San Luis Rio Colorado": ["Mexicali", "Sonoyta"],
    "San Felipe": ["Mexicali", "Ensenada"],
    "San Quintin": ["Ensenada", "Guerrero Negro"]

}

def breadth_first_search_mapa(grafo, inicio, destino):

    # problem.IS-GOAL anticipado para el estado inicial
    if inicio == destino:
        return [inicio]
    
    # Estructuras de datos 
    frontier = deque([inicio]) # frontier: cola FIFO
    reached = {inicio}         # reached: conjunto (set) de descubiertos
    parent = {inicio: None}    # parent: diccionario para reconstrucción de la ruta
    
    # while not IS-EMPTY(frontier)
    while frontier:
        # node =  extrae el primero en entrar
        node = frontier.popleft()
        
        # for each child in EXPAND(problem, node)
        for child in grafo.get(node, []):
            
            # if s is not in reached
            if child not in reached:
                # add s to reached & add child to frontier
                reached.add(child)
                parent[child] = node
                frontier.append(child)
                
                # if problem.IS-GOAL(s) then return child 
                if child == destino:
                    return reconstruir_ruta(parent, destino)
                    
    # Si la frontera se vacía sin alcanzar el destino
    return "failure"

def reconstruir_ruta(parent, destino):

    ruta = []
    actual = destino
    while actual is not None:
        ruta.append(actual)
        actual = parent[actual]
    ruta.reverse() # Invertir para que vaya de inicio a fin
    return ruta


estado_inicial = "Tijuana"
estado_objetivo = "San Quintin"

resultado = breadth_first_search_mapa(mapa_carreteras, estado_inicial, estado_objetivo)
print(f"Ruta optima desde {estado_inicial} hasta {estado_objetivo}:")
print(" -> ".join(resultado))