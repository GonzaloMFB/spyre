import pygame
import random

NODE_TYPES = ("fight", "shop", "event", "chest")

NODE_SIZE = (10, 10)
NODE_SPACE = 32
FIRST_NODE = "event"


class Node:
    def __init__(self, node_type: str):
        self.connections: list[Node] = []
        self.node_type = node_type
        # Calculated during render and used for click events.
        self.node_pos = None


class Map:
    def __init__(self):
        # Slay the Spire organizes map nodes in Floors.
        # That's how wing boots let you travel to any Node in the floor.
        self.layers: list[list[Node]] = []
        self.paths = []
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

    def generate_map(self, test=False):
        # Reset previous map.
        self.layers = []
        # Boss node has no forward connections.
        boss_node = Node("boss")
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
                    node_type = (
                        FIRST_NODE if layer_idx == 0 else random.choice(NODE_TYPES)
                    )
                    self.layers[layer_idx][selected_node] = Node(node_type)
        # Connect nodes based on paths
        for path in paths:
            for idx in range(len(path) - 1):
                current_node = self.layers[idx][path[idx]]
                next_node = self.layers[idx + 1][path[idx + 1]]
                if next_node not in current_node.connections:
                    current_node.connections.append(next_node)
        self.paths = paths

        # Connect boss node
        for node in self.layers[-1]:
            if node:
                node.connections.append(boss_node)
        self.layers.append([boss_node])

    def can_navigate_to(self, dst_node: Node, curr_node: Node):
        if not curr_node and dst_node in self.layers[0]:
            # Player can navigate to any node in the first layer to start.
            return True
        if curr_node and dst_node in curr_node.connections:
            # Player can navigate to nodes connected to the current node.
            return True
        return False

    def _render_paths(self, screen):
        # To render paths, consider:
        # * Iterate over paths array
        # * In each path, the idx is the layer, the value is the node_idx
        # * Keep track of previous
        for path in self.paths:
            # print(f"Path {idx}: {path}")
            prev_x = None
            prev_y = None
            for layer_idx, node_idx in enumerate(path):
                node_x = (1 + node_idx) * NODE_SPACE
                node_y = (len(self.layers) - 1 - layer_idx) * NODE_SPACE
                if prev_x is None and prev_y is None:
                    node_x = (1 + node_idx) * NODE_SPACE
                    node_y = (len(self.layers) - 1 - layer_idx) * NODE_SPACE
                    prev_x = node_x + NODE_SIZE[0] / 2
                    prev_y = node_y + NODE_SIZE[1] / 2
                    continue
                x2 = node_x + NODE_SIZE[0] / 2
                y2 = node_y + NODE_SIZE[1] / 2
                pygame.draw.line(screen, "black", (prev_x, prev_y), (x2, y2))
                prev_x = x2
                prev_y = y2

    def _render_nodes(self, screen, current_node: Node):
        # To render the map, use layer and node idx
        node_colors = {
            "fight": "orange",
            "chest": "purple",
            "event": "blue",
            "shop": "green",
            "boss": "black",
        }
        for layer_idx, layer in enumerate(self.layers):
            for node_idx, node in enumerate(layer):
                if not node:
                    continue
                vfx = pygame.surface.Surface(NODE_SIZE)
                vfx.fill(node_colors.get(node.node_type) or "red")
                node_x = (1 + node_idx) * NODE_SPACE
                node_y = (len(self.layers) - 1 - layer_idx) * NODE_SPACE
                node.node_pos = (node_x, node_y)
                if current_node and node in current_node.connections:
                    # Draws marker on nodes connected to the current one.
                    c_x = node_x + NODE_SIZE[0] / 2
                    c_y = node_y + NODE_SIZE[1] / 2
                    pygame.draw.circle(
                        screen, "black", (c_x, c_y), NODE_SIZE[0] / 2 + 5
                    )
                elif not current_node and layer_idx == 0:
                    c_x = node_x + NODE_SIZE[0] / 2
                    c_y = node_y + NODE_SIZE[1] / 2
                    pygame.draw.circle(
                        screen, "black", (c_x, c_y), NODE_SIZE[0] / 2 + 5
                    )
                screen.blit(vfx, (node_x, node_y))

    def render_map(self, screen: pygame.surface.Surface, current_node=None):
        """
        Renders map on top of provided surface.
        """
        self._render_paths(screen)
        self._render_nodes(screen, current_node)


if __name__ == "__main__":
    test_map = Map()
    test_map.generate_map(test=False)
    # for idx, layer in enumerate(test_map.layers):
    #     print(f"Layer {idx}:")
    #     for node in layer:
    #         if node:
    #             print(f" Node {node}, connects to {len(node.connections)}")

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        screen.fill("gray45")
        test_map.render_map(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
