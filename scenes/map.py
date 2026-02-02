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

    def generate_map(self, random=True):
        # Reset previous map.
        self.layers = []
        self.current_node = None
        # Boss node has no forward connections.
        boss_node = Node("boss")
        if not random:
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
        for i in range(16):
            # TODO
            pass

    def can_navigate_to(self, node: Node):
        if node in self.current_node.connections:
            return True
        return False


test_map = Map()
test_map.generate_map(random=False)
for idx, layer in enumerate(test_map.layers):
    print(f"Layer{idx}:")
    for node in layer:
        print(f" Node {node}, connects to: {node.connections}")
