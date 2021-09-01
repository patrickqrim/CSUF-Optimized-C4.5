class Node(object):
    '''
    Class that represents a node on the decision tree
    '''
    def __init__(self, isLeaf, label, testCondition, classification, children):
        '''
        Initializing method for the Node class
    
        Parameters
        -------
        isLeaf : boolean
            whether or not the node is a leaf
        label: string
            the label of a leaf. empty string if not a leaf.
        testCondition: string
            the attribute that will be used to further partition the tree. empty string if a leaf.
        classification: string
            the classification of the current node. 'ROOT' if the root of the tree.
        children: list
            the list of the current node's children
        '''
        self.isLeaf = isLeaf
        self.label = label
        self.testCondition = testCondition
        self.classification = classification
        self.children = children

# awfloo Python global variables took me 2 hours to fix :(
