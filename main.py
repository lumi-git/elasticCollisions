import pygame as pg
import random
from collisions import *
from GLOBAL import GLOBAL
from spatialHashmap import spatialHashMap


class particle:
    def __init__(self, x, y, vx, vy, size = 10,mass=1,shape = "circle",static = False):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = size
        self.id = GLOBAL.getID()
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.mass = mass
        self.shape = shape
        self.static = static

    def switchColor(self):
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

    def move(self):
        self.x += self.vx
        self.y += self.vy


def initWithRandom(collisionSystem,n,size,speed):
    for _ in range(n):
        p = particle(random.randint(0,GLOBAL.SCREENSIZE[0]), random.randint(0,GLOBAL.SCREENSIZE[1]),(random.random()-0.5)*speed, (random.random()-0.5)*speed,size)
        collisionSystem.Instantiate(p)

screen = pg.display.set_mode((GLOBAL.SCREENSIZE[0], GLOBAL.SCREENSIZE[1]), pg.RESIZABLE,pg.DOUBLEBUF)

clock = pg.time.Clock()

def main():
    particleSize = 30
    collisionSystem = spatialHashMap(particleSize)
    initWithRandom(collisionSystem,2,particleSize,10)

    pg.init()

    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            # if screen is resized update the GLOBAl.SCREENSIZE
            if event.type == pg.VIDEORESIZE:
                GLOBAL.SCREENSIZE = event.size
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_d:
                    GLOBAL.DEBUG = not GLOBAL.DEBUG
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    collisionSystem.Instantiate(particle(event.pos[0], event.pos[1],(random.random()-0.5)*10, (random.random()-0.5)*10,particleSize))
                if event.button == 3:
                    collisionSystem.Instantiate(particle(event.pos[0], event.pos[1],0, 0,particleSize,static = True,mass=10000000,shape="rectangle"))
                if event.button == 2:
                    collisionSystem.Instantiate(particle(event.pos[0], event.pos[1],0, 0,particleSize,shape="rectangle"))


        screen.fill((0, 0, 0))
        update(collisionSystem.particles.values(),collisionSystem)
        for p in collisionSystem.particles.values():
            if p.shape == "circle":
                pg.draw.circle(screen, p.color, (int(p.x), int(p.y)), p.size)
            elif p.shape == "rectangle":
                pg.draw.rect(screen, p.color, (p.x-p.size, p.y-p.size, p.size*2, p.size*2))
        pg.display.flip()
        clock.tick(60)


def update(particles,collisionSystem):
    totalEnergy = 0
    for p in particles:
        totalEnergy += 0.5 * p.mass * (p.vx**2 + p.vy**2)
        collisionSystem.append(p)
        p.move()
        if p.x >= GLOBAL.SCREENSIZE[0]-p.size or p.x <= p.size:
            p.vx = -p.vx
            p.x = max(p.size,min(GLOBAL.SCREENSIZE[0]-p.size,p.x))
        if p.y >= GLOBAL.SCREENSIZE[1]-p.size or p.y <= p.size:
            p.vy = -p.vy
            p.y = max(p.size,min(GLOBAL.SCREENSIZE[1]-p.size,p.y))

        

    pg.display.set_caption(f"fps: {round(clock.get_fps())} | Particles: {len(particles)} | Total Energy: {totalEnergy}")

    collisionSystem.bordPhase()
    collisionSystem.clear()

if __name__ == '__main__':
    main()
