import csv
import math
import continuous_attribute_split as cas
from pprint import pprint
'''
Module that imports data and contains attribute selection methods.

Variables
-------
class_attribute : string
    attribute used for ultimate classification of the data
data : list of dictionaries
    data imported from file (created in cas module )

Methods
-------
info(D), info_A(D, attribute), gain(D, attribute), splitInfo(D, attribute), gain_ratio(D, attribute)
'''
class_attribute = cas.class_attribute
data = [] # a list of dictionaries
#imports data from file (created in cas module)
with open('training_data_split.csv') as f:
    reader = csv.DictReader(f, delimiter=',')
    for line in reader:
        data.append(line)

def info(D):
    '''
    Method that calculates expected information (entropy) needed to classify a tuple in a set of data.
    
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

def infoA(D, attribute):
    '''
    Method that calculates information needed after using a certain attribute to split the data.
    
    Parameters
    -------
    D : list
        a particular set of data
    attribute : string
        attribute used to split the data
    '''
    samples = []
    info_needed = 0
    for x in D:
        samples.append(x[attribute])
    for i in set(samples):
        p = samples.count(i) / len(samples)
        subset = []
        for x in D:
            if x[attribute] == i:
                subset.append(x)
        info_needed+=p*info(subset)
    return info_needed

def gain(D, attribute):
    '''
    Method that calculates information gain by splitting the data with attribute A.
    
    Parameters
    -------
    D : list
        a particular set of data
    attribute : string
        attribute used to split the data
    '''
    return info(D) - infoA(D, attribute)

def splitInfo(D, attribute):
    '''
    Method that calculates the split information of an attribute for a set of data.
    
    Parameters
    -------
    D : list
        a particular set of data
    attribute : string
        attribute used to split the data
    '''
    samples = []
    split_info = 0
    for x in D:
        samples.append(x[attribute])
    for i in set(samples):
        p = samples.count(i) / len(samples)
        split_info += p*math.log2(p)
    return split_info * -1

def gainRatio(D, attribute):
    '''
    Method that calculates the gain ratio of an attribute for a set of data.
    
    Parameters
    -------
    D : list
        a particular set of data
    attribute : string
        attribute used to split the data
    '''
    # **IMPORTANT**: splitInfo becomes 0 when there is 1 in each category
    # This is because log2(1) = 0
    # I'm not sure how to correct this but for now I replaced it with 0.0000001 and it seems to work
    if splitInfo(D, attribute) == 0:
        return gain(D, attribute) / 0.0000001
    return gain(D, attribute) / splitInfo(D, attribute)

# printing stuff to see if they work:
#print(gainRatio(data, 'income'))
#pprint(data)
