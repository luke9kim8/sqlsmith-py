class Relation:
    def __init__(self):
        self.cols = []
    def columns(self):
        return self.cols

class Named_Relation(Relation):
    def __init__(self, name):
        self.name = name
    def ident(self):
        return self.name

class Table(Named_Relation):
    def __init__(self, name, schema, is_insertable, is_base_table):
        Named_Relation.__init__(self, name)
        self.schema = schema
        self.is_insertable = is_insertable
        self.is_base_table = is_base_table
    def ident(self):
        return ".".join([self.schema, self.name])