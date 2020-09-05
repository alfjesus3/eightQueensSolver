#!/usr/bin/env python3

import numpy as np
import random as rd
import math

from termcolor import colored

RANGE = 8


def evolve(num_gens, popu_size):

	popu = np.ndarray(shape=(popu_size, 8), dtype=tuple)

	# The first generation of elements cannot have individuals with 
	# several queens in the same place
	for i in range(popu.shape[0]):
		tmp = [(rd.randint(1,RANGE),rd.randint(1,RANGE)) for _ in range(8)]
		while len(set(tmp)) != 8:
			#print("equal", len(set(tmp)))
			tmp =[(rd.randint(1,RANGE),rd.randint(1,RANGE)) for _ in range(8)]
		popu[i] = tmp
		#print(popu[i])

	# Evaluation of Initial Generation
	fit_popu = evaluate(popu)

	# Crossover of Parents
	new_popu = recombination(popu)
	# Mutations
	# new_popu = mutation(new_popu)


	#Evaluation of the new Population
	fit_popu = evaluate(new_popu)
	# Selection process
	selected = selection(new_popu, fit_popu, popu_size)

	#Update population
	popu = new_popu[selected]
	fit_popu = fit_popu[selected]




	return popu


def stats():
	pass


def visualize_indiv(individual):
	indiv = individual.tolist()
	print(indiv)
	for i in range(RANGE, 0, -1):
		print(colored(i, 'yellow'), end =" ") # row index
		for j in range(1, RANGE+1):
			if tuple((i,j)) in  indiv:
				print(colored("q", 'red'), end =" ")
			else:
				print("o", end =" ")
		print("")

	# column index
	print(" ", end =" ")
	for i in range(1, RANGE+1):
		print(colored(i, "yellow"), end= " ")
	print("")


def evaluate(popu): # It assess the fitness level of the population indiv.
	return np.array(list(map(lambda e: fitness(e), popu)))


def fitness(indiv): # It describes the fitness function
	tmp = 0
	fitV = 0
	for q in indiv:
		tmp = fitV
		for other in indiv:
			#i)
			if (other[0] == q[0]) and (other != q):
				fitV -=1
			#ii)
			if (other[1] == q[1]) and (other != q):
				fitV -=1
			#iii)
			if (abs(other[0] - q[0]) == abs(other[1] - q[1])) and (other != q):
				fitV -=1 

		if tmp == fitV:
			fitV +=1 # this queen has no checks
			
	return fitV


def recombination(popu):
	new_popu = np.copy(popu)

	for i in range(0,len(popu),2):
		ind1 = popu[i]
		ind2 = popu[i+1]

		idx1 = np.random.choice([i for i in range(0,RANGE)], size=4, replace=False)
		#print(idx1)

		idx2 = np.random.choice([i for i in range(0,RANGE)], size=4, replace=False)
		#print(idx2)

		genes1 = ind1[idx1]
		genes2 = ind2[idx2]
		new_indiv = np.append(genes1, [genes2])
		while(len(set(new_indiv)) !=8):
			print("Repeating the recombination")
			print(np.append(genes1, [genes2]))

			idx2 = np.random.choice([i for i in range(0,RANGE)], size=4, replace=False)
			genes2 = ind2[idx2]
			new_indiv = np.append(genes1, [genes2])

		#print(ind1)
		#print(ind2)
		#print(new_indiv)
		
		#int(new_popu.shape)
		new_popu = np.append(new_popu, [new_indiv], axis=0)
		#rint(new_popu.shape)

	return new_popu


def mutation(popu):
	new_popu = np.copy(popu)
	#TODO to implement
	return new_popu


def selection(popu, fit_popu, popu_size):
	assert popu.shape[0] == len(fit_popu) # To guaranteed that the fitness evaluation is updated

	# normalizing the fitness values for converting to Probabilities
	
	min_fit = fit_popu.min()
	max_fit = fit_popu.max()
	rangeFit = max_fit - min_fit
	print("\nmin {}, max {}, range {}".format(min_fit, max_fit, rangeFit))

	probs = np.zeros(popu.shape[0])
	#print(probs.shape)
	for i in range(probs.shape[0]):
		if rangeFit > 0:
			probs[i] = (fit_popu[i] - min_fit)/(max_fit - min_fit)
		else:
			probs[i] = 1e-05
	#print(probs)
	probs = probs/np.sum(probs) # the sum of the probabilities requires to be 1
	#print(probs)

	#print("----")

	#print(popu.shape[0], [i for i in range(popu.shape[0])], probs.shape, popu_size)
	idxs = rd.choices([i for i in range(popu.shape[0])], probs, k =popu_size)
	print(idxs)
	# This means that good configuration are likely to have several inviduals 
	#assert set(idxs) == len(idxs)

	return idxs


if __name__ == "__main__":
	# At the moment the parameters are selected arbitrarily
	num_gens = 30
	prob_mut = 0.2
	popu_size = 2 * 10

	popu = evolve(num_gens, popu_size)

	"""
	for i in range(len(popu)):
		print("The fitness of the configuration is {}".format(fit_popu[i]))
		visualize_indiv(popu[i])
	"""
	stats()
