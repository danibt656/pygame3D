import wireframe as wf
import pygame as pg
import numpy as np


KEY_TO_FUNCTION = {
    # Movement
    pg.K_a: (lambda x: x.translateAll([-10, 0, 0])),
    pg.K_d: (lambda x: x.translateAll([10, 0, 0])),
    pg.K_LSHIFT: (lambda x: x.translateAll([0, 10, 0])),
    pg.K_SPACE: (lambda x: x.translateAll([0, -10, 0])),
    pg.K_w: (lambda x: x.scaleAll(1.25)),
    pg.K_s: (lambda x: x.scaleAll(0.8)),

    # Rotation
    pg.K_q: (lambda x: x.rotateAll('X',  0.1)),
    pg.K_e: (lambda x: x.rotateAll('X', -0.1)),
    pg.K_f: (lambda x: x.rotateAll('Y',  0.1)),
    pg.K_g: (lambda x: x.rotateAll('Y', -0.1)),
    pg.K_z: (lambda x: x.rotateAll('Z',  0.1)),
    pg.K_x: (lambda x: x.rotateAll('Z', -0.1))
}

class ProjectionViewer:
    """
    Displays 3D objects on a Pygame screen
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption('Wireframe Display')
        self.background = (10, 10, 50)

        self.wireframes = {}
        self.displayNodes = True
        self.displayEdges = True
        self.nodeColor = (255, 255, 255)
        self.edgeColor = (200, 200, 200)
        self.nodeRadius = 4

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
        centre_x = self.width / 2
        centre_y = self.height / 2

        matrix = wf.scaleMatrix(*scale)
        for wireframe in self.wireframes.values():
            wireframe.scale(centre_x, centre_y, scale)

    def rotateAll(self, axis, theta):
        """
        Rotate all wireframes about their centre, along given axis by given angle
        """
        rotateFunction = 'rotate' + axis.upper()

        for wireframe in self.wireframes.values():
            center = wireframe.findCenter()
            getattr(wireframe, rotateFunction)(*center, theta)



if __name__ == '__main__':
    cube = wf.Wireframe()
    cube_nodes = [(x, y, z) for x in (50,250) for y in (50,250) for z in (50,250)]
    cube.addNodes(np.array(cube_nodes))
    cube.addEdges([(n,n+4) for n in range(0,4)] + \
                  [(n,n+1) for n in range(0,8,2)] + \
                  [(n,n+2) for n in (0,1,4,5)])
    
    pv = ProjectionViewer(400, 300)
    pv.addWireframe('cube', cube)
    pv.run()