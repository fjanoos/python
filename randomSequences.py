#!/usr/bin/env python

''' 
Generate different types of random numbers
'''

import random

def generateSequence1(count):
    '''
    - How do I generate a list of 4000 random variables that together average to 6000. 
    The min value the random variable can take on is 500 and the max is 7500. 
    Each of the random variables can only take on values (between the min and max) in increments of 100.
    i. generate a list x_1 ... x_4000, where all x_i = 6000.
    ii. repeat the following until you are happy
     a. select any 2 numbers from the list x and y. you can select at random or deterministically.
     b. generate a random positive number z such that
           x + z < 7500
           x - z > 500
          z is a multiple of 100
    '''
    


