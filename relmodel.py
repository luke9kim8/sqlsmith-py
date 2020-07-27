# struct sqltype {
#   string name;
#   static map<string, struct sqltype*> typemap;
#   static struct sqltype *get(string s);
#   sqltype(string n) : name(n) { }

#   /** This function is used to model postgres-style pseudotypes.
#       A generic type is consistent with a more concrete type.
#       E.G., anyarray->consistent(intarray) is true
#             while int4array->consistent(anyarray) is false

#       There must not be cycles in the consistency graph, since the
#       grammar will use fixpoint iteration to resolve type conformance
#       situations in the direction of more concrete types  */
#   virtual bool consistent(struct sqltype *rvalue);
# };
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

class Op(object):
    def __init__(self, name, left, right, result):
        self.name = name
        self.left = Sqltype(left) 
        self.right = Sqltype(right)
        self.result = Sqltype(result) 



def main():
    sqltype = Sqltype("sqltype1")
    print(sqltype.get("sqltype1").name)
    op = Op("luke", "kim", "is", "aight")

if __name__ == "__main__":
    main()