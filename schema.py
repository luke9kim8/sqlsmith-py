from relmodel import Sqltype 
from collections import defaultdict
class Schema(object):
    def __init__(self):
        # sqltype objects
        self.boolType = None
        self.intType = None
        self.internalType = None
        self.arrayType = None

        self.types = []
        self.tables = []
        self.operators = []
        self.routines = []
        self.aggregates = []

        self.index = defaultdict(list)
        self.routinesReturningType = defaultdict(list)
        self.aggregatesReturningType = defaultdict(list)
        self.paramlessRoutinesReturningType = defaultdict(list)
        self.tablesWithColumnsOfType = defaultdict(list)
        self.operatorsReturningType = defaultdict(list)
        self.concreteType = defaultdict(list)
        self.baseTables = defaultdict(list)

        self.version = ""
        self.versionNum = None

        self.trueLiteral = "true"
        self.falseLiteral = "false"



        
        
        
