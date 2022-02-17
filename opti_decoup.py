#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sys
import random
from pylab import *
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as patches

from decimal import Decimal


# d'une liste de piece a découper et d'un rayon de tron, renvoie la liste contenant pour chaque piece:
# - le nombre maximal de piece que l'on peut decouper dans dans l'air du disque (théoriquement sans considérer que c'est un disque)
# - nbx est le nombre de piece que l'on peut mettre sur la diametre selon la largeur de la piece (en x)
# - nby est le nombre de piece que l'on peut mettre sur la diametre selon la hauteur de la piece (en y) --> consideration d'un carré de coté = diamètre
def air_pieces_max(liste_piece, rayon):
	air_disque = rayon * rayon * 3.14159
	output = []
	for p in liste_piece:
		nb_piece_max =int(air_disque/(p[0]*p[1]))
		#surface_max = nb_piece_max * p[0] * p[1]
		nbx = int((2*rayon)/p[0])
		nby = int((2*rayon)/p[1])
		output.append([nb_piece_max, nbx, nby])

	return output


# ENTREE : Liste de piece et rayon du tron
# Sortie : nbx , nby de la piece qui possede la plus grande aire du nb de piece, dimension x et y de la piece, les 4 coordonnées du carré et l'air
def best_option_init(liste_piece,rayon):
	liste_option = air_pieces_max(liste_piece, rayon)

	output = []

	meilleur = 0

	for k in range(len(liste_option)):

		startx = int(-(liste_option[k][1]*liste_piece[k][0])/2)
		endx = int((liste_option[k][1]*liste_piece[k][0])/2)

		starty = int(-(liste_option[k][2]*liste_piece[k][1])/2)
		endy = int((liste_option[k][2]*liste_piece[k][1])/2)

		# test des décalages de start x et y
		for delta in range(-50,50,1):

			i = startx + delta

			som = 0
			while i < endx + delta:
				j = starty + delta
				while j < endy+delta:
					if goodcoord(i,j,rayon,liste_piece[k][0],liste_piece[k][1]):
						som +=1
					j += liste_piece[k][1]
				i += liste_piece[k][0]

			if meilleur < som * liste_piece[k][0] * liste_piece[k][1]:
				meilleur = som * liste_piece[k][0] * liste_piece[k][1]
				output = [liste_option[k][1],liste_option[k][2],liste_piece[k][0],liste_piece[k][1], startx + delta, endx+delta, starty + delta, endy + delta, meilleur]

	return output


# test si d'une coordonné i,j les dimensions de la piece x,y rentre dans le disque de rayon r
def goodcoord(i,j,r,x,y):
	return (np.sqrt(i*i+j*j) < r and np.sqrt((i+x)*(i+x)+(j+y)*(j+y)) < r and np.sqrt((i+x)*(i+x)+(j)*(j)) < r and np.sqrt((i)*(i)+(j+y)*(j+y)) < r)


# Entree : liste de piece
# Sortie : liste de piece avec rotation
def pivot_piece(liste_piece):
	output = []
	for p in liste_piece:
		output.append(p)
		if p[0] != p[1]:
			output.append([p[1],p[0]])

			output.append([-p[1],p[0]])
			output.append([p[1],-p[0]])
			output.append([-p[1],-p[0]])
			output.append([-p[0],p[1]])
			output.append([p[0],-p[1]])
			output.append([-p[0],-p[1]])
		else:
			output.append([-p[0],p[1]])
			output.append([p[0],-p[1]])
			output.append([-p[0],-p[1]])


	return output

def test_segment(segment, list_seg):
	for seg in list_seg:
		# si intersection avec seg horizontal et segment verticale
		if (seg[0][1] == seg[1][1] and segment[0][0] == segment[1][0] and min(segment[0][1],segment[1][1]) < seg[0][1] and max(segment[0][1],segment[1][1]) > seg[0][1] and \
		min(seg[0][0],seg[1][0]) < segment[0][0] and max(seg[0][0],seg[1][0]) > seg[0][0] ):
			return False

		# si intersection avec seg vertical et segment horizontal
		if (seg[0][0] == seg[1][0] and segment[0][1] == segment[1][1] and min(segment[0][0],segment[1][0]) < seg[0][0] and max(segment[0][0],segment[1][0]) > seg[0][0] and \
		min(seg[0][1],seg[1][1]) < segment[0][1] and max(seg[0][1],seg[1][1]) > seg[0][1] ):
			return False

		# si le segment est horizontal
		if segment[0][1]==segment[1][1]:

			# seg horizontal born au dessus le segment + soit seg est inclus dans le segment (en x) soit le segment est inclus dans le seg
			if (seg[0][1]==seg[1][1] and seg[0][1] > segment[0][1] and ((min(seg[0][0],seg[1][0]) >= min(segment[0][0],segment[1][0]) and max(seg[0][0],seg[1][0]) <= max(segment[0][0],segment[1][0])) or \
			(min(seg[0][0],seg[1][0]) > min(segment[0][0],segment[1][0]) and min(seg[0][0],seg[1][0]) < max(segment[0][0],segment[1][0])) or  (min(seg[0][0],seg[1][0]) < min(segment[0][0],segment[1][0]) and max(seg[0][0],seg[1][0]) > min(segment[0][0],segment[1][0])) or \
			(min(seg[0][0],seg[1][0]) <= min(segment[0][0],segment[1][0]) and max(seg[0][0],seg[1][0]) >= max(segment[0][0],segment[1][0])) ) ):
				# seg2 born horizontal en dessous le segment
				for seg2 in list_seg:
					if (seg2[0][1]==seg2[1][1] and seg2[0][1] < segment[0][1] and ((min(seg2[0][0],seg2[1][0]) >= min(segment[0][0],segment[1][0]) and max(seg2[0][0],seg2[1][0]) <= max(segment[0][0],segment[1][0])) or \
					(min(seg2[0][0],seg2[1][0]) > min(segment[0][0],segment[1][0]) and min(seg2[0][0],seg2[1][0]) < max(segment[0][0],segment[1][0])) or  (min(seg2[0][0],seg2[1][0]) < min(segment[0][0],segment[1][0]) and max(seg2[0][0],seg2[1][0]) > min(segment[0][0],segment[1][0])) or \
					(min(seg2[0][0],seg2[1][0]) <= min(segment[0][0],segment[1][0]) and max(seg2[0][0],seg2[1][0]) >= max(segment[0][0],segment[1][0])) ) ):
						return False
		
		# si le segment est vertical
		if segment[0][0]==segment[1][0]:

			# seg vertical born a droite du segment + soit seg est inclus dans le seg (en y) soit le segment est inclus dans le seg
			if (seg[0][0]==seg[1][0] and seg[0][0] > segment[0][0] and ((min(seg[0][1],seg[1][1]) >= min(segment[0][1],segment[1][1]) and max(seg[0][1],seg[1][1]) <= max(segment[0][1],segment[1][1])) or \
			(min(seg[0][1],seg[1][1]) > min(segment[0][1],segment[1][1]) and min(seg[0][1],seg[1][1]) < max(segment[0][1],segment[1][1])) or  (min(seg[0][1],seg[1][1]) < min(segment[0][1],segment[1][1]) and max(seg[0][1],seg[1][1]) > min(segment[0][1],segment[1][1])) or \
			(min(seg[0][1],seg[1][1]) <= min(segment[0][1],segment[1][1]) and max(seg[0][1],seg[1][1]) >= max(segment[0][1],segment[1][1])) ) ):
				# seg2 born verticale a gauhce le segment
				for seg2 in list_seg:
					if (seg2[0][0]==seg2[1][0] and seg2[0][0] < segment[0][0] and ((min(seg2[0][1],seg2[1][1]) >= min(segment[0][1],segment[1][1]) and max(seg2[0][1],seg2[1][1]) <= max(segment[0][1],segment[1][1])) or \
					(min(seg2[0][1],seg2[1][1]) > min(segment[0][1],segment[1][1]) and min(seg2[0][1],seg2[1][1]) < max(segment[0][1],segment[1][1])) or  (min(seg2[0][1],seg2[1][1]) < min(segment[0][1],segment[1][1]) and max(seg2[0][1],seg2[1][1]) > min(segment[0][1],segment[1][1])) or \
					(min(seg2[0][1],seg2[1][1]) <= min(segment[0][1],segment[1][1]) and max(seg2[0][1],seg2[1][1]) >= max(segment[0][1],segment[1][1])) ) ):
						return False

	return True


def test_add_piece(coord,piece,list_seg):
	# pour tester une piece on test ses 4 segments sur la liste des segments deja trace
	if (test_segment([[coord[0],coord[1]],[coord[0]+piece[0],coord[1]]],list_seg) == False) or \
		(test_segment([[coord[0],coord[1]],[coord[0],coord[1]+ piece[1]]],list_seg) == False) or \
		(test_segment([[coord[0],coord[1]+ piece[1]],[coord[0]+piece[0],coord[1]+ piece[1]]],list_seg) == False) or \
		(test_segment([[coord[0]+piece[0],coord[1]],[coord[0]+piece[0],coord[1]+ piece[1]]],list_seg) == False) :
		return False
	else:
		return True



def add_segment(segment, list_seg):
	seul = True
	for seg in list_seg:
		# test si le seg englobe le segment de la piece en x avec un y identique (segments horizontaux)
		if (max(seg[0][0],seg[1][0]) >= max(segment[0][0],segment[1][0]) and min(seg[0][0],seg[1][0]) <= min(segment[0][0],segment[1][0])) and \
			(seg[0][1] == seg[1][1] == segment[0][1] == segment[1][1]) :
			seul = False
			# si c'est exactement le meme segment on le supprime
			if (max(seg[0][0],seg[1][0]) == max(segment[0][0],segment[1][0]) and min(seg[0][0],seg[1][0]) == min(segment[0][0],segment[1][0])):
				list_seg.remove(seg)
			# sinon on garde la partie du seg moins le segment de la piece
			else:
				list_seg.remove(seg)
				# s'il y a un bou du seg avant le min du segment on le garde
				if (min(seg[0][0],seg[1][0]) < min(segment[0][0],segment[1][0])):
					list_seg.append([ [min(seg[0][0],seg[1][0]),seg[0][1]] , [min(segment[0][0],segment[1][0]),seg[0][1]] ])

				# s'il y a un bou du seg après le max du segment on le garde
				if (max(seg[0][0],seg[1][0]) > max(segment[0][0],segment[1][0])):
					list_seg.append([ [max(segment[0][0],segment[1][0]),seg[0][1]] , [max(seg[0][0],seg[1][0]),seg[0][1]] ])

			#return list_seg

		# test si le seg EST englobé par un segment de la piece en x avec un y identique (segments horizontaux)
		elif (max(seg[0][0],seg[1][0]) <= max(segment[0][0],segment[1][0]) and min(seg[0][0],seg[1][0]) >= min(segment[0][0],segment[1][0])) and \
			(seg[0][1] == seg[1][1] == segment[0][1] == segment[1][1]) :
			seul = False
			# si c'est exactement le meme segment on le supprime
			if (max(seg[0][0],seg[1][0]) == max(segment[0][0],segment[1][0]) and min(seg[0][0],seg[1][0]) == min(segment[0][0],segment[1][0])):
				list_seg.remove(seg)
			# sinon on garde la partie du seg moins le segment de la piece
			else:
				list_seg.remove(seg)
				# s'il y a un bou du segment avant le min du seg on le garde
				if (min(seg[0][0],seg[1][0]) > min(segment[0][0],segment[1][0])):
					list_seg.append([ [min(segment[0][0],segment[1][0]),seg[0][1]] , [min(seg[0][0],seg[1][0]),seg[0][1]] ])

				# s'il y a un bou du segment après le max du seg on le garde
				if (max(seg[0][0],seg[1][0]) < max(segment[0][0],segment[1][0])):
					list_seg.append([ [max(seg[0][0],seg[1][0]),seg[0][1]] , [max(segment[0][0],segment[1][0]),seg[0][1]] ])
			#return list_seg

		# test si le seg englobe un segment de la piece en y avec un x identique (segments verticaux)
		elif (max(seg[0][1],seg[1][1]) >= max(segment[0][1],segment[1][1]) and min(seg[0][1],seg[1][1]) <= min(segment[0][1],segment[1][1])) and \
			(seg[0][0] == seg[1][0] == segment[0][0] == segment[1][0]) :
			seul = False
			# si c'est exactement le meme segment on le supprime
			if (max(seg[0][1],seg[1][1]) == max(segment[0][1],segment[1][1]) and min(seg[0][1],seg[1][1]) == min(segment[0][1],segment[1][1])):
				list_seg.remove(seg)
			# sinon on garde la partie du seg moins le segment de la piece
			else:
				list_seg.remove(seg)
				# s'il y a un bou du seg avant le min du segment on le garde
				if (min(seg[0][1],seg[1][1]) < min(segment[0][1],segment[1][1])):
					list_seg.append([ [seg[0][0],min(seg[0][1],seg[1][1])] , [seg[0][0],min(segment[0][1],segment[1][1])] ])

				# s'il y a un bou du seg après le max du segment on le garde
				if (max(seg[0][1],seg[1][1]) > max(segment[0][1],segment[1][1])):
					list_seg.append([ [seg[0][0],max(segment[0][1],segment[1][1])] , [seg[0][0],max(seg[0][1],seg[1][1])] ])
			#return list_seg

		# test si le seg EST englobé par un segment de la piece en y avec un x identique (segments verticaux)
		elif (max(seg[0][1],seg[1][1]) <= max(segment[0][1],segment[1][1]) and min(seg[0][1],seg[1][1]) >= min(segment[0][1],segment[1][1])) and \
			(seg[0][0] == seg[1][0] == segment[0][0] == segment[1][0]) :
			seul = False
			# si c'est exactement le meme segment on le supprime
			if (max(seg[0][1],seg[1][1]) == max(segment[0][1],segment[1][1]) and min(seg[0][1],seg[1][1]) == min(segment[0][1],segment[1][1])):
				list_seg.remove(seg)
			# sinon on garde la partie du seg moins le segment de la piece
			else:
				list_seg.remove(seg)
				# s'il y a un bou du segment avant le min du seg on le garde
				if (min(seg[0][1],seg[1][1]) > min(segment[0][1],segment[1][1])):
					list_seg.append([ [seg[0][0],min(segment[0][1],segment[1][1])] , [seg[0][0],min(seg[0][1],seg[1][1])] ])

				# s'il y a un bou du segment après le max du seg on le garde
				if (max(seg[0][1],seg[1][1]) < max(segment[0][1],segment[1][1])):
					list_seg.append([ [seg[0][0],max(seg[0][1],seg[1][1])] , [seg[0][0],max(segment[0][1],segment[1][1])] ])
			#return list_seg
	if seul:
		list_seg.append(segment)
	return list_seg

"""

def no_double_list(list_seg):
	for i in range(len(list_seg)):
		for j in range(i+1,len(list_seg)):
			if list_seg[i]==list_seg[j]:
				remove(list_seg[j])
	return list_seg
"""

def fusion_liste_seg(list_seg):
	#list_seg = no_double_list(list_seg)
	fini = False
	while fini == False:
		for seg in list_seg:
			# le segment est vertical
			if seg[0][0] == seg[1][0]:	
				fusion = False			
				for seg2 in list_seg:
					if seg != seg2:
						# on peut le fusionner uniquement avec un autre segment vertical et sur le meme axe vertical
						if seg2[0][0] == seg2[1][0] and seg[0][0] == seg2[0][0]:
							#seg avant seg2
							if (max(seg[0][1],seg[1][1]) == min(seg2[0][1],seg2[1][1])):
								#print("je suis dans le cas fusion vertical 1 avec :", seg, seg2, [[seg[0][0],min(seg[0][1],seg[1][1])], [seg[0][0],max(seg2[0][1],seg2[1][1])]])
								# ajout du segment fusionné
								list_seg.append([[seg[0][0],min(seg[0][1],seg[1][1])], [seg[0][0],max(seg2[0][1],seg2[1][1])]])
								list_seg.remove(seg)
								list_seg.remove(seg2)
								fusion = True
								break

							#seg après seg2
							if (min(seg[0][1],seg[1][1]) == max(seg2[0][1],seg2[1][1])):
								#print("je suis dans le cas fusion vertical 2 avec :", seg, seg2, [[seg[0][0],min(seg[0][1],seg[1][1])], [seg[0][0],max(seg2[0][1],seg2[1][1])]])
								# ajout du segment fusionné
								list_seg.append([[seg[0][0],min(seg2[0][1],seg2[1][1])], [seg[0][0],max(seg[0][1],seg[1][1])]])
								list_seg.remove(seg)
								list_seg.remove(seg2)
								fusion = True
								break

			# le segment est horizontal
			else:# seg[0][0] == seg[1][0]:	
				fusion = False			
				for seg2 in list_seg:
					if seg != seg2:
						# on peut le fusionner uniquement avec un autre segment horizontal et sur le meme axe horizontal
						if seg2[0][1] == seg2[1][1] and seg[1][1] == seg2[1][1] :
							#seg avant seg2
							if (max(seg[0][0],seg[1][0]) == min(seg2[0][0],seg2[1][0])):
								#print("je suis dans le cas fusion horizontal 1 avec :", seg, seg2, [[seg[0][1],min(seg[0][0],seg[1][0])], [seg[0][1],max(seg2[0][0],seg2[1][0])]])
								# ajout du segment fusionné
								list_seg.append([[min(seg[0][0],seg[1][0]),seg[0][1]], [max(seg2[0][0],seg2[1][0]),seg[0][1]]])
								list_seg.remove(seg)
								list_seg.remove(seg2)
								fusion = True
								break

							#seg après seg2
							if (min(seg[0][0],seg[1][0]) == max(seg2[0][0],seg2[1][0])):
								#print("je suis dans le cas fusion horizontal 2 avec :", seg, seg2, [[seg[0][1],min(seg2[0][0],seg2[1][0])], [seg[0][1],max(seg[0][0],seg[1][0])]])
								# ajout du segment fusionné
								list_seg.append([[min(seg2[0][0],seg2[1][0]),seg[0][1]], [max(seg[0][0],seg[1][0]),seg[0][1]]])
								list_seg.remove(seg)
								list_seg.remove(seg2)
								fusion = True
								break

			if fusion:
				break
			else:
				fini = True

	return list_seg	


def merge_list_seg(list_seg):
	init = len(list_seg)
	do = True
	while do:
		list_seg = fusion_liste_seg(list_seg)
		if init == len(list_seg):
			do = False
		else:
			init = len(list_seg)
	return list_seg


def add_piece(coord,piece,list_seg):
	maj_list_segment1 = add_segment([[coord[0],coord[1]],[coord[0]+piece[0],coord[1]]],list_seg)
	#print("maj1", maj_list_segment1)
	maj_list_segment2 = add_segment([[coord[0],coord[1]],[coord[0],coord[1]+ piece[1]]],maj_list_segment1)
	maj_list_segment3 = add_segment([[coord[0],coord[1]+ piece[1]],[coord[0]+piece[0],coord[1]+ piece[1]]],maj_list_segment2)
	maj_list_segment4 = add_segment([[coord[0]+piece[0],coord[1]],[coord[0]+piece[0],coord[1]+ piece[1]]],maj_list_segment3)

	return maj_list_segment4


"""
def ajouter_type_piece(x,y,re,list_seg,liste_piece_draw,ax,couleur):
	possible = True
	som2 = 0
	#t = 1
	while possible:# and t<5:
		fini = True
		#print("tour:", t)
		print("nb segments: ", len(list_seg))
		for seg in list_seg:
			#segment horizontal
			if seg[0][1] == seg[1][1]:
				for i in range(min(seg[0][0],seg[1][0]),max(seg[0][0],seg[1][0])+1):
					j = seg[0][1]
					if goodcoord(i,j,re,x,y):
						if (([[i,j],[x,y]] in liste_piece_draw) == False):
							if test_add_piece([i,j],[x,y],list_seg):
								rect = patches.Rectangle((i,j),x,y,linewidth=1,edgecolor=couleur,facecolor='none')
								som2 +=1
								# Add the patch to the Axes
								ax.add_patch(rect)
								list_seg = add_piece([i,j],[x,y],list_seg)
								fini = False

								liste_piece_draw.append([[i,j],[x,y]])

								list_seg = merge_list_seg(list_seg)

			#segment vertical
			if seg[0][0] == seg[1][0]:
				for j in range(min(seg[0][1],seg[1][1]),max(seg[0][1],seg[1][1])+1):
					i = seg[0][0]
					if goodcoord(i,j,re,x,y):
						if (([[i,j],[x,y]] in liste_piece_draw) == False):
							if test_add_piece([i,j],[x,y],list_seg):
								rect = patches.Rectangle((i,j),x,y,linewidth=1,edgecolor=couleur,facecolor='none')
								som2 +=1
								# Add the patch to the Axes
								ax.add_patch(rect)
								list_seg = add_piece([i,j],[x,y],list_seg)
								fini = False

								liste_piece_draw.append([[i,j],[x,y]])

								list_seg = merge_list_seg(list_seg)

		#t += 1 
		if fini == True:
			possible = False

	return (list_seg,som2,liste_piece_draw)
	"""




#c1 plus proche du centre que c2
def inf_rayon(c1,c2):
	return np.sqrt(c1[0]*c1[0]+c1[1]*c1[1]) < np.sqrt(c2[0]*c2[0]+c2[1]*c2[1])


# To heapify subtree rooted at index i. 
# n is size of heap 
def heapify(arr, n, i): 
    largest = i  # Initialize largest as root 
    l = 2 * i + 1     # left = 2*i + 1 
    r = 2 * i + 2     # right = 2*i + 2 
  
    # See if left child of root exists and is 
    # greater than root 
    #if l < n and arr[i] < arr[l]: 
    if l < n and inf_rayon(arr[i],arr[l]): 
        largest = l 
  
    # See if right child of root exists and is 
    # greater than root 
    #if r < n and arr[largest] < arr[r]: 
    if r < n and inf_rayon(arr[largest],arr[r]): 
        largest = r 
  
    # Change root, if needed 
    if largest != i: 
        arr[i],arr[largest] = arr[largest],arr[i]  # swap 
  
        # Heapify the root. 
        heapify(arr, n, largest) 
  
# The main function to sort an array of given size 
def heapSort(arr): 
    n = len(arr) 
  
    # Build a maxheap. 
    # Since last parent will be at ((n//2)-1) we can start at that location. 
    for i in range(n // 2 - 1, -1, -1): 
        heapify(arr, n, i) 
  
    # One by one extract elements 
    for i in range(n-1, 0, -1): 
        arr[i], arr[0] = arr[0], arr[i]   # swap 
        heapify(arr, i, 0) 




def list_seg_to_trie_coord(list_seg):
	liste_coord = []
	for seg in list_seg:
		if seg[0][1] == seg[1][1]:
			j = seg[0][1]
			for i in range(min(seg[0][0],seg[1][0]),max(seg[0][0],seg[1][0])+1):
				if not([i,j] in liste_coord):
					liste_coord.append([i,j])



		if seg[0][0] == seg[1][0]:
			i = seg[0][0]
			for j in range(min(seg[0][1],seg[1][1]),max(seg[0][1],seg[1][1])+1):
				if not([i,j] in liste_coord):
					liste_coord.append([i,j])

	#liste_coord = bubbleSort(liste_coord)
	heapSort(liste_coord)

	return liste_coord



def ajouter_type_piece(x,y,re,list_seg,liste_piece_draw,ax,couleur):
	possible = True
	som2 = 0
	t = 1
	print("ajout de la pièce: [",x,',',y,']')
	while possible:# and t<5:
		fini = True
		#print("tour:", t)
		#print("nb segments: ", len(list_seg))
		liste_coord = list_seg_to_trie_coord(list_seg)
		for c in liste_coord:
			i = c[0]
			j = c[1]
			if goodcoord(i,j,re,x,y):
				if (([[i,j],[x,y]] in liste_piece_draw) == False):
					if test_add_piece([i,j],[x,y],list_seg):
						rect = patches.Rectangle((i,j),x,y,linewidth=1,edgecolor=couleur,facecolor='none')
						som2 +=1
						# Add the patch to the Axes
						ax.add_patch(rect)
						list_seg = add_piece([i,j],[x,y],list_seg)
						fini = False

						liste_piece_draw.append([[i,j],[x,y]])

						list_seg = merge_list_seg(list_seg)
		t += 1 
		if fini == True:
			possible = False

	return (list_seg,som2,liste_piece_draw)


	

def main():

	#print(sys.argv)

	print("Bienvenue sur l'optimisation de découpe\n")

	print("Veuillez donner dans un premier temps le rayon du tron : ")

	rayon = int(input())

	print("Quelle est l'épaisseur de l'écorce : ")

	ecorce = int(input())

	print("Quelles sont les dimensions de la première pièce (à donner sous le format [x,y]) :")

	P1 = eval(input())

	print("Quelles sont les dimensions de la secondes pièce (à donner sous le format [x,y]) :")

	P2 = eval(input())	

	#print(237582/9900)
	#print(237582/5400)

	p1 = [45,220]
	p2 = [45,120]
	p3 = [40,40]
	p4 = [22,50]


	#liste_piece = [p1]

	liste_piece = [P1]

	#[p3,p4]
	#liste_piece = pivot_piece(liste_p)

	#créer un vecteur commencant a start finissant a stop avec nb echantillons comme interval (start,stop,echantillons)
	theta = np.linspace(0, 2*np.pi, 100)

	#r = 275
	#re = r+25

	r = int(rayon)
	re = rayon + ecorce

	x1 = r*np.cos(theta)
	x2 = r*np.sin(theta)

	x1e = re*np.cos(theta)
	x2e = re*np.sin(theta)

	fig, ax = plt.subplots(1)

	ax.plot(x1, x2, color='y')
	ax.set_aspect(1)

	ax.plot(x1e,x2e, color='k')

	#plt.xlim(-350,350)
	#plt.ylim(-350,350)
	plt.xlim(-re-40,re+40)
	plt.ylim(-re-40,re+40)

	plt.grid(linestyle='--')

	titre = 'Rayon ' + str(rayon) + ' + ' + str(ecorce) + ' -- P1' + str(P1) + ' -- P2' + str(P2)

	#plt.title('Rayon 275+25 / P1[45,220] / P2[40,40] ', fontsize=10)
	plt.title(titre, fontsize=10)

	plt.savefig("plot_circle_matplotlib_01.png", bbox_inches='tight')



	[nbx, nby, x, y, startx, endx, starty, endy, aire] = best_option_init(liste_piece,re)

	#print('taille et aire: ',x,y,aire)
	

	liste_piece_draw = []

	i = startx

	nb_coord = 0
	liste_coord = []
	list_seg = []

	som = 0
	while i < endx:
		j = starty
		while j < endy:
			#print('je test ', i,j)
			if goodcoord(i,j,re,x,y):
				#print('ca passe ', i,j)
				rect = patches.Rectangle((i,j),x,y,linewidth=1,edgecolor='r',facecolor='none')
				som +=1
				# Add the patch to the Axes
				ax.add_patch(rect)
				liste_piece_draw.append([[i,j],[x,y]])

				list_seg = add_piece([i,j],[x,y],list_seg)

			j += y
		i += x


	#print("nb segments: ", len(list_seg))
	#print("liste des segments: ")


	liste_piece = [P1]

	liste_piece_etendu = pivot_piece(liste_piece)

	#print(liste_piece_etendu)

	#x = p3[0]
	#y = p3[1]
	x = P2[0]
	y = P2[1]

	list_seg = merge_list_seg(list_seg)

	#print("taille : ", len(list_seg))
	#print(list_seg)

	couleur = 'r'

	som2 = 0
	
	for [x,y] in liste_piece_etendu:
		list_seg, som_inter, liste_piece_draw = ajouter_type_piece(x,y,re,list_seg,liste_piece_draw,ax,couleur)
		list_seg = merge_list_seg(list_seg)
		som2 += som_inter

	somP1 = som + som2
	aireP1 = P1[0]*P1[1] * somP1

	liste_piece = [P2]

	liste_piece_etendu = pivot_piece(liste_piece)

	couleur = 'b'

	somP2 = 0
	
	for [x,y] in liste_piece_etendu:
		list_seg, som_inter, liste_piece_draw = ajouter_type_piece(x,y,re,list_seg,liste_piece_draw,ax,couleur)
		list_seg = merge_list_seg(list_seg)
		somP2 += som_inter

	aireP2 = P2[0] * P2[1] * somP2

	aireTron = 	r * r * 3.14159
	aireTrone = re * re * 3.14159

	print("Proportion pieces/ Tronc + écorce = ", ((aireP1+aireP2)/aireTrone)*100, '%' )
	print("Nombre de pièces 1: ", somP1)
	print("Nombre de pièces 2: ", somP2)

	print("Proportion pieces/ Tronc = ", ((aireP1+aireP2)/aireTron)*100, '%' )
	
	#print("taille : ", len(list_seg))
	#print(list_seg)


	#for seg in list_seg:
	#	print(seg)
	#	plot(*zip(*seg),'m')



	plt.show()



if __name__ == "__main__":
    main()