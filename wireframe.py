#
# Wireframe class
#
import numpy as np
from numpy.linalg import multi_dot
import math


def translationMatrix(dx=0, dy=0, dz=0):
    """
    Return matrix for translation along vector (dx, dy, dz)
    """
    return np.array([[1,0,0,0],
                     [0,1,0,0],
                     [0,0,1,0],
                     [dx,dy,dz,1]])

def scaleMatrix(sx=0, sy=0, sz=0):
    """
    Return matrix for scaling along all axes centered on (sx, sy, sz)
    """
    return np.array([[sx, 0, 0, 0],
                     [0, sy, 0, 0],
                     [0, 0, sz, 0],
                     [0, 0, 0, 1]])

def rotateXMatrix(radians):
    """
    Return matrix for rotating about the x-axis by given radians
    """
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[1, 0, 0, 0],
                     [0, c,-s, 0],
                     [0, s, c, 0],
                     [0, 0, 0, 1]])

def rotateYMatrix(radians):
    """
    Return matrix for rotating about the y-axis by given radians
    """
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[c, 0, s, 0],
                     [0, 1, 0, 0],
                     [-s,0, c, 0],
                     [0, 0, 0, 1]])

def rotateZMatrix(radians):
    """
    Return matrix for rotating about the z-axis by given radians
    """
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[c,-s, 0, 0],
                     [s, c, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])

class Wireframe:

    def __init__(self):
        self.nodes = np.zeros((0, 4))
        self.edges = []
        self.faces = []
        self.colors = []
    
    def addNodes(self, node_list):
        ones_column = np.ones((len(node_list), 1))
        ones_added = np.hstack((node_list, ones_column))
        self.nodes = np.vstack((self.nodes, ones_added))

    def addEdges(self, edge_list):
        self.edges += edge_list

    def addFaces(self, face_list):
        self.faces += face_list

    def addColors(self, color_list):
        self.colors += color_list
    
    ## For debugging ##
    def outputNodes(self):
        print("\n --- Nodes ---")
        for i, (x, y, z, _) in enumerate(self.nodes):
            print(f" {i}: ({x}, {y}, {z})")

    def outputEdges(self):
        print("\n --- Edges ---")
        for i, (node1, node2) in enumerate(self.edges):
            print(f" {i}: {node1} -> {node2}")
    ####################

    def transform(self, matrix):
        """
        Apply transformation defined by given matrix
        """
        self.nodes = np.dot(self.nodes, matrix)

    def scale(self, scaleMatrix):
        center = np.array(self.findCenter())
        centerInv = center * -1

        tf_center = translationMatrix(*center)
        tf_centerInv = translationMatrix(*centerInv)

        tf_scale = multi_dot([tf_centerInv, scaleMatrix, tf_center])
        self.nodes = np.dot(self.nodes, tf_scale)

    def rotateX(self, rotateXMatrix):
        center = np.array(self.findCenter())
        centerInv = center * -1

        tf_center = translationMatrix(*center)
        tf_centerInv = translationMatrix(*centerInv)

        tf_rotate = multi_dot([tf_centerInv, rotateXMatrix, tf_center])
        self.nodes = np.dot(self.nodes, tf_rotate)

    def rotateY(self, rotateYMatrix):
        center = np.array(self.findCenter())
        centerInv = center * -1

        tf_center = translationMatrix(*center)
        tf_centerInv = translationMatrix(*centerInv)

        tf_rotate = multi_dot([tf_centerInv, rotateYMatrix, tf_center])
        self.nodes = np.dot(self.nodes, tf_rotate)
    
    def rotateZ(self, rotateZMatrix):
        center = np.array(self.findCenter())
        centerInv = center * -1

        tf_center = translationMatrix(*center)
        tf_centerInv = translationMatrix(*centerInv)

        tf_rotate = multi_dot([tf_centerInv, rotateZMatrix, tf_center])
        self.nodes = np.dot(self.nodes, tf_rotate)

    def findCenter(self):
        """
        Find center of the wireframe
        """
        num_nodes = len(self.nodes)
        meanX = sum([node[0] for node in self.nodes]) / num_nodes
        meanY = sum([node[1] for node in self.nodes]) / num_nodes
        meanZ = sum([node[2] for node in self.nodes]) / num_nodes

        return (meanX, meanY, meanZ)

    def getFacesAvgZ(self):
        avgZ = []
        i = 0
        for f in self.faces:
            z = (self.nodes[f[0]][2] + self.nodes[f[1]][2] + \
                 self.nodes[f[2]][2] + self.nodes[f[3]][2]) / 4.0
            avgZ.append([i, z])
            i = i + 1
        return avgZ



if __name__ == "__main__":
    """
    Quick debug function
    """
    cube = Wireframe()

    cube_nodes = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]

    cube.addNodes(np.array(cube_nodes))
    cube.addEdges([(n, n + 4) for n in range(0, 4)])
    cube.addEdges([(n, n + 1) for n in range(0, 8, 2)])
    cube.addEdges([(n, n + 2) for n in (0, 1, 4, 5)])

    cube.outputNodes()
    cube.outputEdges()

