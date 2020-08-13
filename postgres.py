import sqlalchemy
from sqlalchemy import create_engine
from relmodel import Sqltype, Table, Column, Op, Routine
from schema import Schema
class pg_type(Sqltype):
    def __init__(self, name, oid, typdelim, typrelid, typelem, typarray, typtype):
        self.oid = oid
        self.typdelim = typdelim
        self.typrelid = typrelid
        self.typelem = typelem
        self.typarray = typarray
        self.typtype = typtype
    def __str__(self):
        return " | ".join([str(self.oid), str(self.typdelim), str(self.typrelid),
                            str(self.typelem), str(self.typarray), str(self.typtype)])

class Schema_pqxx(Schema):
    oid2type = {}
    name2type = {}

    def quote_name(self, word):
        return "'"+word+"'"

    def schema_pqxx(self, connInfo, no_catalog):
        postgresString = "postgresql://postgres:krispykreme@localhost:5432/dvdrental"
        # connString = "postgresql://%s:%s@%s:%s/%s".format(connInfo)
        engine = create_engine(postgresString)
        
        with engine.connect() as conn:
            result_set = conn.execute("SHOW server_version_num")
            version_num = int(result_set.fetchone()[0])
            procedure_is_aggregate = "proisagg" if version_num < 110000 else "prokind = 'a'"
            procedure_is_window = "proiswindow" if version_num < 110000 else "prokind = 'w'"

            print("loading types...")
            rows = conn.execute("select quote_ident(typname), oid,"+ 
                                    "typdelim, typrelid, typelem, typarray, " + 
                                    "typtype from pg_type")
            for row in rows:
                t = pg_type(row[0], row[1], row[2][0], row[3], row[4], row[5], row[6][0])
                self.oid2type[row[1]] = t
                self.name2type[row[0]] = t
                self.types.append(t)
            self.boolType = self.name2type['bool']
            self.intType = self.name2type['int4']
            self.internalType = self.name2type['internal']
            self.arrayType = self.name2type['anyarray']
            print("done.")

            # Populate tables information in schema
            print("Loading tables...")
            query = "".join(["select table_name, ",
		        "table_schema, ",
	            "is_insertable_into, ",
	            "table_type ",
	            "from information_schema.tables"])
            rows = conn.execute(query)
            for row in rows:
                _schema = row[1] 
                _insertable = row[2]
                _table_type = row[3]
                if no_catalog and (_schema == "pg_catalog" or _schema == "information_schema"):
                    continue
                self.tables.append(Table(row[0], _schema, True if _insertable == "YES" else False, True if _table_type == "BASE TABLE" else False))
            print("done.")

            print("Loading columns and constraints...")
            for table in self.tables:
                query = "".join(["select attname, "
                            ,"atttypid "
                            ,"from pg_attribute join pg_class c on( c.oid = attrelid ) "
                            ,"join pg_namespace n on n.oid = relnamespace "
                            ,"where not attisdropped "
                            ,"and attname not in "
                            ,"('xmin', 'xmax', 'ctid', 'cmin', 'cmax', 'tableoid', 'oid') "
                            ," and relname = " + self.quote_name(table.name)
                            ," and nspname = " + self.quote_name(table.schema)])
                
                rows = conn.execute(query)
                for row in rows:
                    c = Column(row[0], self.oid2type[row[1]])
                    table.columns().append(c)

                query = "".join(["select conname from pg_class t "
                                ,"join pg_constraint c on (t.oid = c.conrelid) "
                                ,"where contype in ('f', 'u', 'p') "
                                ,"and relnamespace = " " (select oid from pg_namespace where nspname = "
                                ,self.quote_name(table.schema), ")"
                                ," and relname = ", self.quote_name(table.name)])
                
                rows = conn.execute(query) # TODO: Investigate why rows is empty on this query
                for row in rows:
                    table.constraints.append(row[0])
            print("done.")
            
            print("Loading operators...")
            query = "".join(["select oprname, oprleft,"
                            ,"oprright, oprresult "
                            ,"from pg_catalog.pg_operator "
                            ,"where 0 not in (oprresult, oprright, oprleft) "])
            rows = conn.execute(query)
            for row in rows:
                o = Op(row[0], row[1], row[2], row[3])
                self.register_operator(o)
            print("done.")

            print("Loading routines...")
            query = "".join(["select (select nspname from pg_namespace where oid = pronamespace), oid, prorettype, proname "
                            ,"from pg_proc "
                            ,"where prorettype::regtype::text not in ('event_trigger', 'trigger', 'opaque', 'internal') "
                            ,"and proname <> 'pg_event_trigger_table_rewrite_reason' "
                            ,"and proname <> 'pg_event_trigger_table_rewrite_oid' "
                            ,"and proname !~ '^ri_fkey_' "
                            ,"and not (proretset or ", procedure_is_aggregate, " or ", procedure_is_window, ") "])
            rows = conn.execute(query)
            for row in rows:
                proc = Routine(row[0], str(row[1]), row[2], row[3])
                self.register_routine(proc)
            print("done.")

            print("Loading routine parameters...")
            for proc in self.routines:
                query = "select unnest(proargtypes) from pg_proc where oid = " + self.quote_name(proc.specific_name)
                rows = conn.execute(query)
                for row in rows:
                    t = self.oid2type[row[0]]
                    proc.argtypes.append(t)
            print("done.")

            print("Loading aggregates...")
            query = "".join(["select (select nspname from pg_namespace where oid = pronamespace), oid, prorettype, proname "
                            ,"from pg_proc "
                            ,"where prorettype::regtype::text not in ('event_trigger', 'trigger', 'opaque', 'internal') "
                            ,"and proname not in ('pg_event_trigger_table_rewrite_reason') "
                            ,"and proname not in ('percentile_cont', 'dense_rank', 'cume_dist', "
                            ,"'rank', 'test_rank', 'percent_rank', 'percentile_disc', 'mode', 'test_percentile_disc') "
                            ,"and proname !~ '^ri_fkey_' "
                            ,"and not (proretset or ", procedure_is_window ,") "
                            ,"and ", procedure_is_aggregate])
            rows = conn.execute(query)
            for row in rows:
                proc = Routine(str(row[0]), str(row[1]), row[2], str(row[3]))
                self.register_aggregate(proc)
            print("done.")

            print("Loading aggregate parameters...")
            for proc in self.aggregates:
                query = "".join(["select unnest(proargtypes) ", "from pg_proc ", " where oid = ",
                                 self.quote_name(proc.specific_name)])
                rows = conn.execute(query)
                for row in rows:
                    t = self.oid2type[row[0]]
                    proc.argtypes.append(t)
            print("done.")
            # TODO: Implement Generate Index Function

        self.generate_indexes()
                





def __main__():
    pqxx = Schema_pqxx()
    pqxx.schema_pqxx("", False)

if __name__ == "__main__":
    __main__()
