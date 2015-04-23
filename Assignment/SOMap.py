#!/usr/bin/env python
# encoding: utf=8

import math
import random as r
import scipy
from scipy.spatial import distance as d
import matplotlib.pyplot as plot

def main(iterations):
	C_Chord_M = [1,0,0,0,1,0,0,1,0,0,0,0]
	C_Chord_m = [1,0,0,1,0,0,0,1,0,0,0,0]

	# S_Patterns
	S_Matrix = [[0 for i in range(12)] for i in range(24)]
	S_init(S_Matrix,C_Chord_M,C_Chord_m)

	# R_Patterns
	R_Matrix = [[0 for i in range(12)] for i in range(24)]
	R_init(R_Matrix,S_Matrix)

	# O_Patterns
	O_Matrix = [[0 for i in range(12)] for i in range(24)]
	O_init(O_Matrix,R_Matrix)

	Chord_names = ["C","Cm","C#","C#m","D","Dm","Eb","Ebm","E","Em","F","Fm","F#","F#m","G","Gm","Ab","Abm","A","Am","Bb","Bbm","B","Bm"]

	map = [[[r.random() for i in range(12)] for i in range(20)] for i in range(20)]
	for i in range(iterations):
		for j in range(24):
			index = r.randint(0,23)
			bmui = bmu_index(map,O_Matrix[index])
			update(map,bmui,O_Matrix[index],i)

	distance_map = [[0 for i in range(20)] for i in range(20)]
	CM_Chord = O_Matrix[0]
	for i in range(20):
		for j in range(20):
			distance_map[i][j] = distance(map[i][j],CM_Chord)
	plot.imshow(distance_map,interpolation = 'nearest')
	label_plot(map,O_Matrix,Chord_names)
	plot.show()

def label_plot(map,O_Matrix,Chord_names):
	for i in range(len(Chord_names)):
		bmui = bmu_index(map,O_Matrix[i])
		plot.text(bmui[1],bmui[0],Chord_names[i])

def add_lsts(lst1,lst2):
	for i in range(len(lst1)):
		lst1[i] = lst1[i] + lst2[i]

def sub_lsts(lst1,lst2):
	ans = [0 for i in range(len(lst1))]
	for i in range(len(lst1)):
		ans[i] = lst1[i] - lst2[i]
	return ans

def update(map,bmui,target,iteration):
	for i in range(20):
		for j in range(20):
			td = torus_distance(bmui,[i,j])
			add_lsts(map[i][j],scale(sub_lsts(target,map[i][j]),(.02 * neighborhood(td,iteration))))

def minimum(x1,x2):
	return min(abs(x1 - x2), 20 - abs(x1 - x2))
			
def torus_distance(bmui,iim):
	return math.sqrt((minimum(bmui[0],iim[0])**2) + (minimum(bmui[1],iim[1])**2))

def neighborhood(t_distance, iteration):
	if(iteration >= 0):
		return math.exp(-( (t_distance ** 2) / (2 * (theta(iteration) ** 2))))

def theta(iteration):
	ans = ((1./3) * (19. - (iteration / 20.)))
	return ans

def bmu_index(map,lst):
	si = [0,0]
	smallest_distance = distance(map[si[0]][si[1]],lst)
	for i in range(len(map)):
		for j in range(len(map[i])):
			temp_distance = distance(map[i][j],lst)
			if(temp_distance < smallest_distance):
				si = [i,j]
				smallest_distance = temp_distance
	return si

def distance(lst1,lst2):
	if(len(lst1) == 12 and len(lst2) == 12):
		return d.euclidean(lst1,lst2)
	else:
		print "distance function error lst1 or lst2 length incorrect"

def O_init(O_Matrix,R_Matrix):
	for i in range(len(R_Matrix)):
		max_value = max(R_Matrix[i]) 		# max value in the R_values
		lst = R_Matrix[i]			# temp lst to change permanently
		scale(lst,(1/max_value))		# scaling the temp lst by 1/max
		sum = sum_lst(lst)			# summing all the values of the scaled temp lst
		scalar = (1/math.sqrt(sum))		# right side of multiply in the O patterns formula
		O_Matrix[i] = scale(lst,scalar)		# finishing the O_Paterns formula

def R_init(R_Matrix,S_Matrix):
	temp_matrix = [[0 for i in range(12)]for i in range(12)]
	C_R_Pattern = [1,0,.25,0,0,.5,0,0,.33,.1,.2,0]
	for i in range(12):
		temp_matrix[i] = shift(i,C_R_Pattern)
	for i in range(24):
		for j in range(12):
			if(S_Matrix[i][j] == 1):
				for k in range(12):
					R_Matrix[i][k] += temp_matrix[j][k]

def S_init(S_Matrix,C_Chord_M,C_Chord_m):
	length = len(C_Chord_M) - 1
	count = 0
	for i in range(24):
		if(count % 1 == 0):
			S_Matrix[i] = shift(int(count),C_Chord_M)
			count += .5
		else:
			S_Matrix[i] = shift(int(count-.5),C_Chord_m)
			count += .5

def shift(amount,array):
	return array[-amount:] + array[:-amount]

def scale(lst,scalar):
	for i in range(len(lst)):
		lst[i] = lst[i] * scalar
	return lst

def sum_lst(lst):
	sum = 0
	for i in range(len(lst)):
		sum = sum + lst[i]
	return sum

if __name__ == '__main__':
    import sys
    try:
        iterations = int(sys.argv[1])
    except:
        sys.exit(-1)
    main(iterations)
