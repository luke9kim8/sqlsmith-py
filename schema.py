from relmodel import Sqltype 
from collections import defaultdict
from multimap import Multimap
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

        self.index = Multimap()
        self.routines_returning_type = defaultdict(list)
        self.aggregates_returning_type = defaultdict(list)
        self.paramless_routines_returningType = defaultdict(list)
        self.tables_with_columns_of_type = defaultdict(list)
        self.operators_returning_type = defaultdict(list)
        self.concrete_type = defaultdict(list)
        self.base_tables = defaultdict(list)

        self.version = ""
        self.version_num = None

        self.true_literal = "true"
        self.false_literal = "false"

    def summary(self):
        print("Found ${size} user table(s) in information schema.".format(size=len(self.tables)))

    def fill_scope(self, s):
        for table in self.tables:
            s.tables.append(table)
        s.schema = self
    
    def register_operator(self, o):
        self.operators.append(o)
        t = (o.left, o.right, o.result)
        self.index.insert(t, o)
    
    def register_routine(self, r):
        self.routines.append(r)
    
    def register_aggregate(self, r):
        self.aggregates.append(r)
    
    # def find_operator(self, left, right, res):
    #     t = (left, right, res)
    #     cons = self.index.equal_range(t)
    #     if cons.first == cons.second
    #         return index.

    def generate_indexes(self):
        for t in self.types:
            for r in self.aggregates:
                

        


        
        
        
