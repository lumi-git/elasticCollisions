from spatialHashmap import spatialHashMap
import math
from GLOBAL import GLOBAL
import pygame as pg

def collisionChooser(paia,pbid):
    pa = spatialHashMap.INSTANCE.particles[paia]
    pb = spatialHashMap.INSTANCE.particles[pbid]
    if pa.shape == "circle" and pb.shape == "circle":
        return circleCircleCollision(pa,pb)
    elif pa.shape == "circle" and pb.shape == "rectangle":
        return circleRectangleCollision(pa,pb)
    elif pa.shape == "rectangle" and pb.shape == "circle":
        return circleRectangleCollision(pa,pb)
    elif pa.shape == "rectangle" and pb.shape == "rectangle":
        return rectangleRectangleCollision(pa,pb)

def circleCircleCollision(pa,pb):

    distance = math.sqrt((pb.x-pa.x)**2 + (pb.y-pa.y)**2)

    if distance <= pa.size + pb.size:

        pa.x -= impulse * m2 * nx
        pa.y -= impulse * m2 * ny
        pb.x += impulse * m1 * nx
        pb.y += impulse * m1 * ny

