from PyCamellia import *
from abc import ABCMeta

class State:
    __metaclass__ = ABCMeta

    def __init__(self, context):
        pass

    def main(self):
        return "unsupported";

