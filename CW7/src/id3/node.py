import numpy as np

class Node:
    def __init__(self, attribute=None, result=None):
        self.attribute = attribute
        self.children = {}
        self.result = result

