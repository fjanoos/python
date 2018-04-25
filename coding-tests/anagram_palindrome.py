__author__ = 'fj'


# Problem Statement
# A palindrome is a word that reads the same forwards and backwards. For example, "a", "abba", and "zzz" are
# palindromes, while "ab" and "xxxyx" are not.
# The anagram of a string S is any string we can obtain from S by rearranging its letters. For example, the string
# "haha" has exactly six anagrams: "aahh", "ahah", "ahha", "haah", "haha", and "hhaa".
#
# We are given a String word. We will choose one of its anagrams uniformly at random. Return the probability that the
#  chosen anagram will be a palindrome.
#
# Definition
#
# Class:	PalindromePermutations
# Method:	palindromeProbability
# Parameters:	String
# Returns:	double
# Method signature:	double palindromeProbability(String word)
# (be sure your method is public)
#
#
# Notes
# -	The returned value must have an absolute or a relative error of less than 1e-9.
#
# Constraints
# -	word will contain between 1 and 50 characters, inclusive.
# -	Each character of word will be a lowercase English letter ('a'-'z').
#
# Examples
# 0)
#
# "haha"
# Returns: 0.3333333333333333
# Each of the six anagrams of "haha" will be selected with probability 1/6. Two of them are palindromes: "ahha" and
# "haah". Hence, the probability of selecting a palindrome is 2/6.
# 1)
#
# "xxxxy"
# Returns: 0.2
# 2)
#
# "xxxx"
# Returns: 1.0
# This word only has one anagram: "xxxx". That is a palindrome.
# 3)
#
# "abcde"
# Returns: 0.0
# Regardless of how we rearrange the letters of "abcde", we will never get a palindrome.
# 4)
#
# "hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhff"
# Returns: 0.025641025641025637
# http://community.topcoder.com/stat?c=problem_statement&pm=11856


from pylab import *
from collections import  defaultdict


def factorial(n):return reduce(lambda x,y:x*y,[1]+range(1,n+1))

class PalindromePermutations(object):
	def palindromeProbability(self,  S):
		if type(S) != str:
			return -1

		S = S.lower().replace(' ','')

		# count up each occurence
		char_count = defaultdict(int)

		for c in S:
			char_count[c] += 1

		all_ana = double(factorial(len(S)))      # all anagrams
		pal_ana = double(factorial(int(len(S)/2))) # all palindrome anagrams
		no = 0
		for k in char_count.keys():
			all_ana /= factorial(char_count[k])
			no +=  char_count[k] % 2  # count up number of odd guys
			pal_ana /= double(factorial(int(char_count[k]/2)))

		if no > 1:
			pal_ana = 0; # no anagrams possible

		return  (all_ana, pal_ana, pal_ana / all_ana)



