import wireframe as wf
import pygame as pg
import numpy as np
from operator import itemgetter


# Color constants
BG_COLOR = (174, 198, 255)
NODE_COLOR = (204, 0, 0)
EDGE_COLOR = (64, 64, 64)
FACE_COLOR = (0, 255, 0)
TEXT_COLOR = (0, 0, 0)

# Key press functions
KEY_TO_FUNCTION = {
    # Movement
    pg.K_a: (lambda x: x.translateAll([-10, 0, 0])),
    pg.K_d: (lambda x: x.translateAll([10, 0, 0])),
    pg.K_SPACE: (lambda x: x.translateAll([0, 10, 0])),
    pg.K_LSHIFT: (lambda x: x.translateAll([0, -10, 0])),
    pg.K_w: (lambda x: x.scaleAll([1.25]*3)),
    pg.K_s: (lambda x: x.scaleAll([0.5]*3)),

    # Rotation
    pg.K_q: (lambda x: x.rotateAll('X',  0.1)),
    pg.K_e: (lambda x: x.rotateAll('X', -0.1)),
    pg.K_f: (lambda x: x.rotateAll('Y',  0.1)),
    pg.K_g: (lambda x: x.rotateAll('Y', -0.1)),
    pg.K_z: (lambda x: x.rotateAll('Z',  0.1)),
    pg.K_x: (lambda x: x.rotateAll('Z', -0.1)),

    # Debug controls
    pg.K_F1: (lambda x: (x.setDisplayNodes(not x.displayNodes))),
    pg.K_F2: (lambda x: (x.setDisplayEdges(not x.displayEdges))),
    pg.K_F3: (lambda x: (x.setDisplayTextures(not x.displayTextures)))
}

class ProjectionViewer:
    """
    Displays 3D objects on a Pygame screen
    """

    def __init__(self, width, height):
        # Basic window setup
        self.width = width
        self.height = height
        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption('Wireframe Display')
        self.background = BG_COLOR

        # Various display options
        self.wireframes = {}
        self.displayNodes = True
        self.displayEdges = True
        self.displayTextures = True
        self.nodeColor = NODE_COLOR
        self.edgeColor = EDGE_COLOR
        self.nodeRadius = 2
    
        # Set up the text
        self.help_text = f"Nodes [F1]: {self.displayNodes} | Edges [F2]: {self.displayEdges} | Textures[F3]: {self.displayTextures}"
        pg.font.init()
        font = pg.font.SysFont('Arial', 15)
        self.textSurface = font.render(self.help_text, True, TEXT_COLOR)
        self.textRect = self.textSurface.get_rect()

    # For debugging
    def setDisplayNodes(self, d):
        self.displayNodes = d

    def setDisplayEdges(self, d):
        self.displayEdges = d

    def setDisplayTextures(self, d):
        self.displayTextures = d

    def run(self):
        """
        Create pygame screen until it is closed
        """
        running = True
        
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    if event.key in KEY_TO_FUNCTION:
                        KEY_TO_FUNCTION[event.key](self)

            self.display()
            pg.display.flip()

    def addWireframe(self, name, wireframe):
        """
        Add a named wireframe object
        """
        self.wireframes[name] = wireframe

    def display(self):
        """
        Draw the wireframes on the screen
        """
        self.screen.fill(self.background)

        self.screen.blit(self.textSurface, self.textRect)

        for wireframe in self.wireframes.values():
            if self.displayEdges:
                for n1, n2 in wireframe.edges:
                    pg.draw.aaline(self.screen,
                                   self.edgeColor,
                                   wireframe.nodes[n1][:2],
                                   wireframe.nodes[n2][:2],
                                   1)
            if self.displayNodes:
                for node in wireframe.nodes:
                    pg.draw.circle(self.screen,
                                   self.nodeColor,
                                   (int(node[0]), int(node[1])),
                                   self.nodeRadius,
                                   0)
            if self.displayTextures:
                avgZ = wireframe.getFacesAvgZ()
                for zVal in sorted(avgZ,key=itemgetter(1),reverse=True):
                    fIndex = zVal[0]
                    f = wireframe.faces[fIndex]
                    pointList = [(wireframe.nodes[f[0]][0], wireframe.nodes[f[0]][1]), (wireframe.nodes[f[1]][0], wireframe.nodes[f[1]][1]),
                                 (wireframe.nodes[f[1]][0], wireframe.nodes[f[1]][1]), (wireframe.nodes[f[2]][0], wireframe.nodes[f[2]][1]),
                                 (wireframe.nodes[f[2]][0], wireframe.nodes[f[2]][1]), (wireframe.nodes[f[3]][0], wireframe.nodes[f[3]][1]),
                                 (wireframe.nodes[f[3]][0], wireframe.nodes[f[3]][1]), (wireframe.nodes[f[0]][0], wireframe.nodes[f[0]][1])]
                    pg.draw.polygon(self.screen, wireframe.colors[fIndex],pointList)

    def translateAll(self, vector):
        """
        Translate all wireframes by d along a given axis
        """
        matrix = wf.translationMatrix(*vector)
        for wireframe in self.wireframes.values():
            wireframe.transform(matrix)

    def scaleAll(self, scale):
        """
        Scale all wireframes by a given scale, centered on screen's center
        """
        matrix = wf.scaleMatrix(*scale)

        for wireframe in self.wireframes.values():
            wireframe.scale(matrix)

    def rotateAll(self, axis, theta):
        """
        Rotate all wireframes about their centre, along given axis by given angle
        """
        rotateFunction = 'rotate' + axis.upper()
        rotateMatrix = []

        if axis == 'X':
            rotateMatrix = wf.rotateXMatrix(theta)
        elif axis == 'Y':
            rotateMatrix = wf.rotateYMatrix(theta)
        elif axis == 'Z':
            rotateMatrix = wf.rotateZMatrix(theta)

        for wireframe in self.wireframes.values():
            getattr(wireframe, rotateFunction)(rotateMatrix)

# End of ProjectionViewer


def _setup_cube(ix, iy, iz, size):
    """
    Set up a cube of 'size' size on origin (ix, iy, iz)
    """

    cube = wf.Wireframe()
    cube_nodes = [(x, y, z) for x in (ix,ix+size) for y in (iy,iy+size) for z in (iz,iz+size)]
    cube.addNodes(np.array(cube_nodes))
    cube.addEdges([(n,n+4) for n in range(0,4)] + \
                  [(n,n+1) for n in range(0,8,2)] + \
                  [(n,n+2) for n in (0,1,4,5)])
    cube.addFaces([(0,1,2,3),(1,5,6,2),(5,4,7,6),(4,0,3,7),(0,4,5,1),(3,2,6,7)])
    cube.addColors([(255,0,255),(255,0,0),(0,255,0),(0,0,255),(0,255,255),(255,255,0)])
    return cube

if __name__ == '__main__':
    cube1 = _setup_cube(400, 300, 0, 50)
    #cube2 = _setup_cube(80, 50, 50, 30)
    
    pv = ProjectionViewer(800, 600)
    pv.addWireframe('cube1', cube1)
    #pv.addWireframe('cube2', cube2)
    pv.run()
