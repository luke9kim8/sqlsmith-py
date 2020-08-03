import sqlalchemy
from sqlalchemy import create_engine
from relmodel import Sqltype

class pg_type(Sqltype):
    def __init__(self, name, oid, typdelim, typrelid, typelem, typarray, typtype):
        self.oid = oid
        self.typdelim = typdelim
        self.typrelid = typrelid
        self.typelem = typelem
        self.typarray = typarray
        self.typtype = typtype


def schema_pqxx(connInfo):
    # postgresString = "postgresql://myuser:mypass@localhost:5432/dvdrental"
    # connString = "postgresql://%s:%s@%s:%s/%s".format(connInfo)
    engine = create_engine(connInfo)
    with engine.connect() as conn:
        result_set = conn.execute("SHOW server_version_num")
        version_num = int(result_set.fetchone()[0])
        procedure_is_aggregate = "proisagg" if version_num < 110000 else "prokind = 'a'"
        procedure_is_window = "proiswindow" if version_num < 110000 else "prokind = 'w'"

        print("Loading types...")
        rows = engine.execute("select quote_ident(typname), oid,"+ 
                                "typdelim, typrelid, typelem, typarray, " + 
                                "typtype from pg_type")
        for row in rows:
            t = pg_type(row[0], row[1], row[2][0], row[3], row[4], row[5], row[6][0])
            

        


   
    
    
    