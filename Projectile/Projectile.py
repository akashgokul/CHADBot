import numpy as np 
from math import cos
from math import sin
from math import fabs
from math import radians
import sys


def projectile():
	a=0 
	init_pos = sys.argv[0].split(',')
	target = sys.argv[1].split(',')
	print(init_pos[1])
	print(target[0])
	#distance = float(target[0]) - float(init_pos[0])
	v=?
	g=9.81 
	
	best_angle=None
	nearest_answer=None

	while a<45: 
	    r = (2*v**2)/g*cos(radians(a))*sin(radians(a))
	    if not nearest_answer or fabs(r-distance)< fabs(nearest_answer-distance):
	        nearest_answer = r
	        best_angle = a
	    a+=.1 
	    #print(best_angle)
projectile()
	


