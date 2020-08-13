class Relation:
    def __init__(self):
        self.cols = []
    def columns(self):
        return self.cols

class Named_Relation(Relation):
    def __init__(self, name):
        Relation.__init__(self)
        self.name = name
    def ident(self):
        return self.name

class Table(Named_Relation):
    def __init__(self, name, schema, is_insertable, is_base_table):
        Named_Relation.__init__(self, name)
        self.schema = schema
        self.is_insertable = is_insertable
        self.is_base_table = is_base_table
        self.constraints = []
    def ident(self):
        return ".".join([self.schema, self.name])

class Sqltype(object):
    def __init__(self, name):
        self.name = name
        self.typemap = {}
    
    def get(self, n):
        if n in self.typemap:
            return self.typemap.get(n)
        else:
            print("no")
            self.typemap[n] = Sqltype(n)
            return self.typemap[n]
    
    def consistent(self, rvalue):
        return self == rvalue

class Op(object):
    def __init__(self, name, left, right, result):
        self.name = name
        self.left = Sqltype(left) 
        self.right = Sqltype(right)
        self.result = Sqltype(result) 

class Column:
    def __init__(self, name, type=None):
        self.name = name
        self.name = None

class Routine:
    def __init__(self, schema, specific_name, data_type, name):
        self.specific_name = specific_name 
        self.schema = schema
        self.restype = data_type
        self.name = name
        self.argtypes = []
    
    def ident(self):
        if len(self.schema) != 0:
            return self.schema + "." + self.name
        else:
            return self.name
    
    def __str__(self):
        return " | ".join([str(self.specific_name), str(self.schema), str(self.restype),
                            str(self.name), str(self.argtypes)])
    



# def main():
    

# if __name__ == "__main__":
#     main()