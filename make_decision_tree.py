import attribute_selection_methods as asm
import sys
from node import Node
import statistics
from statistics import mode
'''
Created on Jun 29, 2020

@author: Patrick Rim
@author: Erin Liu
'''
# renaming things from asm
data = asm.data
class_attribute = asm.class_attribute
# list of attributes
attributes = list(data[0].keys())
# remove class attribute from attributes list
attributes.remove(class_attribute)

def findBestSplit(D, F):
    '''
    Method that calculates the best attribute to use to split the data
    
    Parameters
    -------
    D : list
        a particular set of data
    F: list
        a list of the unused attributes
    '''
    maxVal = -sys.maxsize - 1
    bestSplit = ''
    for k in F:
        if asm.gainRatio(D, k) > maxVal:
            maxVal = asm.gainRatio(D, k)
            bestSplit = k
    return bestSplit

def stoppingCondition(D, F):
    '''
    Method that checks whether or not the tree should stop partitioning
    
    Parameters
    -------
    D : list
        a particular set of data
    F: list
        a list of the unused attributes
    '''
    # check if there are any attributes left
    if len(F) == 0:
        return True

    # check if there are any samples left
    if len(D) == 0:
        return True
    
    # check if all samples belong to same class
    samples = []
    for x in D:
        samples.append(x[class_attribute])
    if len(set(samples)) == 1:
        return True

    # otherwise, return false
    return False

def classify(D):
    '''
    Method that classifies a finalized group of data
    
    Parameters
    -------
    D : list
        a particular set of data
    '''
    samples = []
    for x in D:
        samples.append(x[class_attribute])
    return mode(samples)

def buildTree(D, F, classification):
    '''
    Method that creates the decision tree
    
    Parameters
    -------
    D : list
        a particular set of data
    F: list
        a list of the unused attributes
    classification: string
        the classification of the node to be created
    '''
    if stoppingCondition(D, F):
        leaf = Node(True, classify(D), '', classification, [])
        return leaf
    else:
        root = Node(False, '', findBestSplit(D, F), classification, [])
        
        samples = [] # all possible values of testCondition
        for x in D:
            samples.append(x[root.testCondition])
            
        copyF = list(F) # make a copy of F
        copyF.remove(root.testCondition)
        
        for i in set(samples):
            copyD = list(D)
            for j in D:
                if(j[root.testCondition] != i):
                    copyD.remove(j)
            # check for empty nodes
            if len(copyD) != 0:
                # recursive call
                # print(i) # test
                root.children.append(buildTree(copyD, copyF, i))

        # return the root
        return root

# build the decision tree
decisionTree = buildTree(data, attributes, 'ROOT')

# IT WORKSSS :):):)
            



        
        
