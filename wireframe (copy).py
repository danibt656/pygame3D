#
# Wireframe class
#
import math

class Node:
    
    def __init__(self, coordinates):
        """
        Init coordinates: X, Y, Z
        """
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.z = coordinates[2]


class Edge:

    def __init__(self, start, stop):
        self.start = start
        self.stop = stop


class Wireframe:

    def __init__(self):
        self.nodes = np.zeros((0, 4))
        self.edges = []
    
    def addNodes(self, node_list):
        for node in node_list:
            self.nodes.append(Node(node))

    def addEdges(self, edge_list):
        for (start, stop) in edge_list:
            self.edges.append(Edge(self.nodes[start], self.nodes[stop]))
    
    # For debugging
    def outputNodes(self):
        print("\n --- Nodes ---")
        for i, node in enumerate(self.nodes):
            print(f" {i}: ({node.x}, {node.y}, {node.z})")

    def outputEdges(self):
        print("\n --- Edges ---")
        for i, edge in enumerate(self.edges):
            print(f" {i}: ({edge.start.x}, {edge.start.y}, {edge.start.z})")
            print(f"  to: ({edge.start.x}, {edge.start.y}, {edge.start.z})")

    def translate(self, axis, d):
        """
        Translate each node of a wireframe by d along given axis
        """
        if axis in ['x', 'y', 'z']:
            for node in self.nodes:
                setattr(node, axis, getattr(node, axis) + d)

    def scale(self, centre_x, centre_y, scale):
        """
        Scale the wireframe from the centre of the screen
        """
        for node in self.nodes:
            node.x = centre_x + scale * (node.x - centre_x)
            node.y = centre_y + scale * (node.y - centre_y)
            node.z *= scale

    def rotateX(self, cx, cy, cz, radians):
        for node in self.nodes:
            y = node.y - cy
            z = node.z - cz
            d = math.hypot(y, z)
            theta = math.atan2(y, z) + radians
            node.z = cz + d * math.cos(theta)
            node.y = cy + d * math.sin(theta)

    def rotateY(self, cx, cy, cz, radians):
        for node in self.nodes:
            x = node.x - cx
            z = node.z - cz
            d = math.hypot(x, z)
            theta = math.atan2(x, z) + radians
            node.z = cz + d * math.cos(theta)
            node.x = cx + d * math.sin(theta)

    def rotateZ(self, cx, cy, cz, radians):
        for node in self.nodes:
            x = node.x - cx
            y = node.y - cy
            d = math.hypot(y, x)
            theta = math.atan2(y, x) + radians
            node.x = cx + d * math.cos(theta)
            node.y = cy + d * math.sin(theta)

    def findCenter(self):
        """
        Find center of the wireframe
        """
        num_nodes = len(self.nodes)
        meanX = sum([node.x for node in self.nodes]) / num_nodes
        meanY = sum([node.y for node in self.nodes]) / num_nodes
        meanZ = sum([node.z for node in self.nodes]) / num_nodes

        return (meanX, meanY, meanZ)
