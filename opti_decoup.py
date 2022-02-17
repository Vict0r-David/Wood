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
from bib_cut import *


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