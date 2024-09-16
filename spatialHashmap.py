import collisions
from GLOBAL import GLOBAL
from math import sqrt,ceil,floor
import pygame as pg

class spatialHashMap():
    INSTANCE = None
    def __init__(self):
        self.screen = pg.display.get_surface()

        self.particles = {}
        self.map = dict()
        spatialHashMap.INSTANCE = self


    def Instantiate(self,particle):
        self.particles[particle.id] = particle

    def append(self,particle):
        CellsHashs = self.getPositionHashes(particle)
        for CellHash in CellsHashs:
            if self.map.get(CellHash) == None:
                self.map[CellHash] = []
                self.map[CellHash].append(particle.id)
            else:
                self.map[CellHash].append(particle.id)

    def narrowPhase(self,particleA,particleB):
        collisions.collisionChooser(particleA,particleB)

    def bordPhase(self):
        for key in self.map.keys():
            cell = self.map[key]
            i =0
            for particleA in cell:
                i+=1
                for particleB in cell[i:]:
                    if not particleA == particleB:
                        self.narrowPhase(particleA,particleB)

    def getPositionHashes(self,particle):
        positions = []
        pax = particle.x - particle.size
        pay = particle.y - particle.size
        pbx = particle.x + particle.size
        pby = particle.y + particle.size
        if GLOBAL.DEBUG:
            pg.draw.circle(self.screen, (255, 255, 0), (int(pax), int(pay)), 1)#yellow
            pg.draw.circle(self.screen, (255, 0, 0), (int(pbx), int(pay)), 1)#red
            pg.draw.circle(self.screen, (0, 255, 0), (int(pax), int(pby)), 1)#green
            pg.draw.circle(self.screen, (0, 255, 255), (int(pbx), int(pby)), 1) #blue
        
        for i in range(floor(pax/GLOBAL.CELLSIZE),ceil(pbx/GLOBAL.CELLSIZE)):
            for j in range(floor(pay/GLOBAL.CELLSIZE),ceil(pby/GLOBAL.CELLSIZE)):
                positions.append(128633*i + 56127482*j)
                if GLOBAL.DEBUG:
                    pg.draw.rect(self.screen, (255, 255, 255), (i*GLOBAL.CELLSIZE,j*GLOBAL.CELLSIZE,GLOBAL.CELLSIZE,GLOBAL.CELLSIZE))
        return positions

    def clear(self):
        self.map = dict()

    def draw(self,screen):
        pass