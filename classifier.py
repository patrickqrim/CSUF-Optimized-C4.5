import make_decision_tree as mdt
import continuous_attribute_split as cas
import math
import csv
from operator import itemgetter

class_attribute = 'buys_computer'
data_filename = 'unclassified_data.csv'
data = []
decisionTree = mdt.decisionTree
continuous_attributes_list = cas.continuous_attributes_list
splitpoints = cas.splitpoints
#imports data from file
with open(data_filename) as f:
    reader = csv.DictReader(f, delimiter=',')
    for line in reader:
        data.append(line)

# categorize continuous attributes
def rewrite_continuous(D):
    '''
    Method that splits the continuous attributes using splitpoints calculated by 'cas'

    Parameters
    -------
    D: a list
        the data set to be classified
    '''
    for i in range(len(splitpoints)):
        for x in D:
            if int(x[continuous_attributes_list[i]]) <= splitpoints[i]:
                x[continuous_attributes_list[i]] = '<=' + str(splitpoints[i])
            else:
                x[continuous_attributes_list[i]] = '>' + str(splitpoints[i])

#MAIN: classify the data
#to ponder: what to do for data with no precedents? for now i put "uncategorized"
        
def classify(x, node):
    if(node.isLeaf):
        #print(node.label)
        return node.label
    else:
        test = node.testCondition
        for n in node.children:
            if(n.classification == x[test]):
                return classify(x, n)
        return "uncategorized"

def rewrite_data(D):
    for x in D:
        x[class_attribute] = classify(x, decisionTree)

rewrite_continuous(data)
rewrite_data(data)

with open('FINAL_classified_data.csv', 'w', newline='') as csvfile:
    fieldnames = list(data[0].keys())
    writer = csv.DictWriter(csvfile, fieldnames)
    writer.writeheader()
    writer.writerows(data)
