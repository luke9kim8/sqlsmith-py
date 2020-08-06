import sqlalchemy
from sqlalchemy import create_engine
from relmodel import Sqltype
from schema import Schema
class pg_type(Sqltype):
    def __init__(self, name, oid, typdelim, typrelid, typelem, typarray, typtype):
        self.oid = oid
        self.typdelim = typdelim
        self.typrelid = typrelid
        self.typelem = typelem
        self.typarray = typarray
        self.typtype = typtype

class Schema_pqxx(Schema):
    oid2type = {}
    name2type = {}

    def quote_name(self, word):
        return "'"+word+"'"

    def schema_pqxx(self, connInfo, no_catalog):
        postgresString = "postgresql://myuser:mypass@localhost:5432/dvdrental"
        # connString = "postgresql://%s:%s@%s:%s/%s".format(connInfo)
        engine = create_engine(postgresString)
        
        with engine.connect() as conn:
            result_set = conn.execute("SHOW server_version_num")
            version_num = int(result_set.fetchone()[0])
            procedure_is_aggregate = "proisagg" if version_num < 110000 else "prokind = 'a'"
            procedure_is_window = "proiswindow" if version_num < 110000 else "prokind = 'w'"

            print("loading types...")
            rows = engine.execute("select quote_ident(typname), oid,"+ 
                                    "typdelim, typrelid, typelem, typarray, " + 
                                    "typtype from pg_type")
            for row in rows:
                t = pg_type(row[0], row[1], row[2][0], row[3], row[4], row[5], row[6][0])
                self.oid2type[row[1]] = t
                self.name2type[row[0]] = t
                # TODO: Implement types.push_back(t)
                # TODO: Verify types of t, some of them should be ints
            self.boolType = self.name2type['bool']
            self.intType = self.name2type['int4']
            self.internalType = self.name2type['internal']
            self.arrayType = self.name2type['anyarray']
            print("done.")

            print("Loading tables...")
            query = "".join(["select table_name, ",
		        "table_schema, ",
	            "is_insertable_into, ",
	            "table_type ",
	            "from information_schema.tables"])
            rows = engine.execute(query)
            for row in rows:
                if no_catalog and (row[1] == "pg_catalog" or row[1] == "information_schema"):
                    continue
                self.tables.append()



def __main__():
    pqxx = Schema_pqxx()
    pqxx.schema_pqxx("")

if __name__ == "__main__":
    __main__()
