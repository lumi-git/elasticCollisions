# Collision system

## board phase

Using a spatial hashmap algorithme

## narrow phase 

using inertia and impuls methods

## Shell

Being able to modify parameters during exeuction is a great way to learn more and improve the system.

in the console you ran the script, type the commands to modify parameters present in the GLOBAL config.

>`GLOBAL CELLSIZE <int>` -> modify the hashmap celle size, influence the density/cell..

> `GLOBAL GRAVITY <int>` -> modify the gravity

>`GLOBAL DEBUG` -> Show/hide the cells of the hashmap & other debug details

>`GLOBAL FRICTION <float>` -> modify the collision friction energy loss: 0.99 means 99% of the energy remains after a hit.