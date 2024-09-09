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
    if pa.static and pb.static:
        return
    elif pa.static:
        circleCircleCollision(pb,pa)
        return
    elif pa.static:
        return

    dx = pa.x - pb.x
    dy = pa.y - pb.y
    distance = math.sqrt(dx**2 + dy**2)

    if distance <= pa.size + pb.size:
        nx = dx / distance if distance != 0 else 0
        ny = dy / distance if distance != 0 else 0

        dvx = pa.vx - pb.vx
        dvy = pa.vy - pb.vy
        vn = dvx * nx + dvy * ny  

        if vn > 0:
            return

        m1 = pa.mass
        m2 = pb.mass
        impulse = 2 * vn / (m1 + m2) *GLOBAL.FRICTION

        pa.vx -= impulse * m2 * nx
        pa.vy -= impulse * m2 * ny
        pb.vx += impulse * m1 * nx
        pb.vy += impulse * m1 * ny


def circleRectangleCollision(pa,pb):

    if pa.static and pb.static:
        return
    elif pa.static:
        circleRectangleCollision(pb,pa)
        return
    elif pa.static:
        return


    closestX = clamp(pa.x, pb.x - pb.size*2 / 2, pb.x + pb.size*2 / 2)
    closestY = clamp(pa.y, pb.y - pb.size*2 / 2, pb.y + pb.size*2 / 2)

    distanceX = pa.x - closestX
    distanceY = pa.y - closestY

    distanceSquared = distanceX * distanceX + distanceY * distanceY

    if distanceSquared <= pa.size * pa.size:

        nx = distanceX
        ny = distanceY
        distance = math.sqrt(nx**2 + ny**2)
        if distance != 0 :
            nx /= distance 
            ny /= distance 
        else:
            nx = 0
            ny = 0

        dvx = pa.vx - pb.vx
        dvy = pa.vy - pb.vy
        vn = dvx * nx + dvy * ny

        if vn > 0: 
            return

        m1 = pa.mass
        m2 = pb.mass
        impulse = 2 * vn / (m1 + m2) *GLOBAL.FRICTION

        pa.vx -= impulse * m2 * nx
        pa.vy -= impulse * m2 * ny
        pb.vx += impulse * m1 * nx
        pb.vy += impulse * m1 * ny

def clamp(value, min_, max_):
    if value < min_:
        return min_
    if value > max_:
        return max_
    return value

def rectangleRectangleCollision(pa,pb):

    if pa.static and pb.static:
        return
    elif pa.static:
        rectangleRectangleCollision(pb,pa)
        return
    elif pa.static:
        return

    dx = pa.x - pb.x
    dy = pa.y - pb.y

    overlapX = (pa.size*2 + pb.size*2) / 2 - abs(dx)
    overlapY = (pa.size*2 + pb.size*2) / 2 - abs(dy)

    if overlapX > 0 and overlapY > 0:
        if overlapX < overlapY:
            if dx > 0:
                pa.x += overlapX / 2
                pb.x -= overlapX / 2
            else:
                pa.x -= overlapX / 2
                pb.x += overlapX / 2
        else:
            if dy > 0:
                pa.y += overlapY / 2
                pb.y -= overlapY / 2
            else:
                pa.y -= overlapY / 2
                pb.y += overlapY / 2

        nx = dx
        ny = dy
        distance = math.sqrt(nx**2 + ny**2)
        if distance != 0 :
            nx /= distance 
            ny /= distance 
        else:
            nx = 0
            ny = 0

        dvx = pa.vx - pb.vx
        dvy = pa.vy - pb.vy
        vn = dvx * nx + dvy * ny

        if vn > 0: 
            return

        m1 = pa.mass
        m2 = pb.mass
        impulse = 2 * vn / (m1 + m2) *GLOBAL.FRICTION

        if not pa.static:
            pa.vx -= impulse * m2 * nx
            pa.vy -= impulse * m2 * ny
        if not pb.static:
            pb.vx += impulse * m1 * nx
            pb.vy += impulse * m1 * ny

