from relmodel import Sqltype 
from collections import defaultdict
from multimap import Multimap

# boolType = None
# intType = None
# internalType = None
# arrayType = None

# types = []
# tables = []
# operators = []
# routines = []
# aggregates = []

# index = Multimap()
# routines_returning_type = defaultdict(list)
# aggregates_returning_type = defaultdict(list)
# paramless_routines_returningType = defaultdict(list)
# tables_with_columns_of_type = defaultdict(list)
# operators_returning_type = defaultdict(list)
# concrete_type = defaultdict(list)
# base_tables = defaultdict(list)

# version = ""
# version_num = None

# true_literal = "true"
# false_literal = "false"



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
        self.routines_returning_type = Multimap()
        self.aggregates_returning_type = Multimap()
        self.paramless_routines_returningType = Multimap()
        self.tables_with_columns_of_type = Multimap()
        self.operators_returning_type = Multimap()
        self.concrete_type = Multimap()
        self.base_tables = Multimap()

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

    def generate_indexes(self):
        print("Generating indexes...")
        # TODO: research how struct == is implemented in c++
        #
        #  bool sqltype::consistent(struct sqltype *rvalue)
        # {
        #     return this == rvalue;
        # }
        # is this method comparing pointer value? Then, how should 
        # it be implemented in python?
        #  - Deep Comparison?
        #
        
        for _type in self.types:
            for aggregate in self.aggregates:
                print(aggregate.restype)
                if _type.consistent(aggregate.restype):
                    self.aggregates_returning_type.insert(_type, aggregate)
            
            for routine in self.routines:
                if not _type.consistent(routine.restype):
                    self.routines_returning_type.insert(_type, routine)
                if len(routine.argtypes) == 0:
                    self.paramless_routines_returningType.insert(_type, routine)
            

        


        
        
        
