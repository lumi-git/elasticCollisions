import pygame as pg
import random
from collisions import *
from GLOBAL import GLOBAL
from spatialHashmap import spatialHashMap
from threading import Thread

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
        # switch color based on speed, green = slow, red = fast
        combinedSpeed = abs(self.vx) + abs(self.vy)
        color = max(min(255,int(combinedSpeed*255/1)),0)
        self.color = (255-color,color,0)

def initWithRandom(collisionSystem,n,size,speed):
    for _ in range(n):
        p = particle(random.randint(0,GLOBAL.SCREENSIZE[0]), random.randint(0,GLOBAL.SCREENSIZE[1]),(random.random()-0.5)*speed, (random.random()-0.5)*speed,size)
        collisionSystem.Instantiate(p)

screen = pg.display.set_mode((GLOBAL.SCREENSIZE[0], GLOBAL.SCREENSIZE[1]), pg.RESIZABLE,pg.DOUBLEBUF)

clock = pg.time.Clock()

def main():
    particleSize = 5
    collisionSystem = spatialHashMap()
    initWithRandom(collisionSystem,4000,particleSize,1)

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


        screen.fill((10, 10, 10))
        update(collisionSystem.particles.values(),collisionSystem)
        for p in collisionSystem.particles.values():
            if p.shape == "circle":
                pg.draw.circle(screen, p.color, (int(p.x), int(p.y)), p.size)
            elif p.shape == "rectangle":
                pg.draw.rect(screen, p.color, (p.x-p.size, p.y-p.size, p.size*2, p.size*2))
        pg.display.flip()
        clock.tick(GLOBAL.FPS)


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


def shell():
    while True:
        cmd = input("$> ")
        command = cmd.split(" ")[0]
        args = cmd.split(" ")[1:] 
        if cmd == "exit":
            exit()
        elif command == "GLOBAL" and len(args) >= 1:
            if args[0] == "GRAVITY":
                GLOBAL.GRAVITY = float(args[1])
            elif args[0] == "FRICTION":
                GLOBAL.FRICTION = float(args[1])
            elif args[0] == "DEBUG":
                GLOBAL.DEBUG = not GLOBAL.DEBUG
            elif args[0] == "CELLSIZE":
                GLOBAL.CELLSIZE = int(args[1])
            elif args[0] == "FPS":
                GLOBAL.FPS = int(args[1])
        else:
            print("Unknown Command")

if __name__ == '__main__':

    shellThread = Thread(target=shell)
    shellThread.start()
    main()

