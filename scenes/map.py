import random

NODE_TYPES = ("fight", "shop", "event", "chest")


class Node:
    def __init__(self, node_type: str):
        self.connections: list[Node] = []
        self.node_type = node_type


class Map:
    def __init__(self):
        # Slay the Spire organizes map nodes in Floors.
        # That's how wing boots let you travel to any Node in the floor.
        self.layers: list[list[Node]] = []
        self.current_node: Node = None
        self.max_width = 4
        self.n_floors = 16

    def _init_empty_map(self):
        # Inits empty map for path-based generation.
        layers = []
        for _ in range(self.n_floors):
            layer = []
            for _ in range(self.max_width):
                layer.append(None)
            layers.append(layer)
        self.layers = layers

    def generate_map(self, test=True):
        # Reset previous map.
        self.layers = []
        self.current_node = None
        # Boss node has no forward connections.
        boss_node = Node("boss")
        if test:
            # Generate smaller map with only 1 connection for testing.
            self.layers.append([Node("fight")])
            for i in range(1, 4):
                new_node = Node(NODE_TYPES[i])
                self.layers[i - 1][0].connections.append(new_node)
                self.layers.append([new_node])
            self.layers[-1][0].connections.append(boss_node)
            self.layers.append([boss_node])
            self.current_node = self.layers[0][0]
            return
        # Random generation. The map of each Act has 16 floors + 1 Boss battle.
        # Generate paths.
        n_paths = random.randint(3, 5)
        paths = []
        self._init_empty_map()
        # Generate nodes
        for _ in range(n_paths):
            path = []
            for _ in range(self.n_floors):
                path.append(random.randint(0, self.max_width - 1))
            paths.append(path)
        print("Number of paths:", n_paths)
        # Create nodes based on the paths.
        for path in paths:
            for layer_idx, selected_node in enumerate(path):
                if not self.layers[layer_idx][selected_node]:
                    # Create node.
                    node_type = "fight" if layer_idx == 0 else random.choice(NODE_TYPES)
                    self.layers[layer_idx][selected_node] = Node(node_type)
        # Connect nodes based on paths
        for path in paths:
            for idx in range(len(path) - 1):
                current_node = self.layers[idx][path[idx]]
                next_node = self.layers[idx + 1][path[idx + 1]]
                if next_node not in current_node.connections:
                    current_node.connections.append(next_node)

        # Connect boss node
        for node in self.layers[-1]:
            if node:
                node.connections.append(boss_node)
        self.layers.append([boss_node])

    def can_navigate_to(self, node: Node):
        if node in self.current_node.connections:
            return True
        return False


if __name__ == "__main__":
    test_map = Map()
    test_map.generate_map(test=False)
    for idx, layer in enumerate(test_map.layers):
        print(f"Layer {idx}:")
        for node in layer:
            if node:
                print(
                    f" Node {node}, connects to {len(node.connections)}: {node.connections}"
                )
