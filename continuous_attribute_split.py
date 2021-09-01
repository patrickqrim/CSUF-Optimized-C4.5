from pprint import pprint
import math
import csv
from operator import itemgetter
'''
Module that rewrites continuous data as discrete.

Variables
-------
continuous_attributes_list : list
    includes all continuous attributes that need to be discretized
class_attribute : string
    attribute used for ultimate classification of the data
data_filename : string
    filename of original data
data : list of dictionaries
    original data imported from data_filename
'''
continuous_attributes_list = ['age']
splitpoints = [] # for use in "classifier"
class_attribute = 'buys_computer'
data_filename = 'training_data.csv'
data = [] # a list of dictionaries
#imports data from file
with open(data_filename) as f:
    reader = csv.DictReader(f, delimiter=',')
    for line in reader:
        data.append(line)

def find_midpoints(D, continuousAttribute):
    '''
    Method that returns a list of midpoints between each pair of adjacent values in continuous attribute.
    
    Parameters
    -------
    D : list
        a particular set of data
    continuousAttribute : string
        continuous attribute that needs to be discretized
    '''
    midpoints = []
    samples = []
    for x in D:
        samples.append(x[continuousAttribute])
    num_one = sorted(set(samples))
    num_two = sorted(set(samples))
    num_two.pop(0)
    for i in range(len(num_two)):
        midpoint = (int(num_one[i]) + int(num_two[i])) / 2
        midpoints.append(midpoint)
    return midpoints

def info_continuous(D):
    '''
    Method that calculates expected information (entropy) needed to classify a tuple in a set of data.
    *same method as info(D) in asm*
    Parameters
    -------
    D : list
        a particular set of data
    '''
    samples = []
    entropy = 0
    for x in D:
        samples.append(x[class_attribute])
    for i in set(samples):
        p = samples.count(i) / len(samples)
        entropy+=p*math.log2(p)
    return entropy*-1

def info_A_continuous(D, splitpoint, continuousAttribute):
    '''
    Method that calculates information needed after using a certain splitpoint to split the data.
    *slightly different method than info_A(D) in asm*
    Parameters
    -------
    D : list
        a particular set of data
    splitpoint : float
        point that will split attribute into two sections
    '''
    samples = []
    info_needed = 0
    for x in D:
        samples.append(x[continuousAttribute])
    p1 = sum(int(i) <= splitpoint for i in samples) / len(samples)
    p2 = sum(int(i) > splitpoint for i in samples) / len(samples)
    subset1 = []
    subset2 = []
    for x in D:
        if (int(x[continuousAttribute]) <= splitpoint):
            subset1.append(x)
        else:
            subset2.append(x)
    info_needed = p1 * info_continuous(subset1) + p2 * info_continuous(subset2) 
    return info_needed

def find_best_splitpoint(D, splitpoints, continuousAttribute):
    '''
    Method that finds the points with the minimum expected information requirement.  
    Parameters
    -------
    D : list
        a particular set of data
    splitpoints : list
        list of possible split points
    '''
    info_A_list = []
    for i in splitpoints:
        info_A_list.append(info_A_continuous(data, i, continuousAttribute))
    index = info_A_list.index(min(info_A_list))
    return splitpoints[index]

def rewrite_data(D, bestSplitpoint, continuousAttribute):
    '''
    Method that rewrites original data with discretized values for its continuous attribute.

    Parameters
    -------
    D : list
        a particular set of data
    bestSplitpoint : int
        split point to be used to split the continuous attribute
    '''
    for x in D:
        if int(x[continuousAttribute]) <= bestSplitpoint:
            x[continuousAttribute] = '<=' + str(bestSplitpoint)
        else:
            x[continuousAttribute] = '>' + str(bestSplitpoint)

#discretizes all continuous attribute values
for i in continuous_attributes_list:
    continuous_attribute = i
    #sorts data by continuous attribute        
    data = sorted(data, key=itemgetter(continuous_attribute))
    #finds list of possible split points
    split_points = find_midpoints(data, continuous_attribute)
    #finds the split point with the minimum expected information requirement 
    best_splitpoint = find_best_splitpoint(data, split_points, continuous_attribute)
    #for use in "classifier"
    splitpoints.append(best_splitpoint)
    #rewrites data with discretized values based on best_splitpoint
    rewrite_data(data, best_splitpoint, continuous_attribute)
    

#creates new csv file with discretized values for its continuous attributes
with open('training_data_split.csv', 'w', newline='') as csvfile:
    fieldnames = list(data[0].keys())
    writer = csv.DictWriter(csvfile, fieldnames)
    writer.writeheader()
    writer.writerows(data)
    
