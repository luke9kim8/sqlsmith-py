import sqlalchemy
from sqlalchemy import create_engine
def schema_pqxx(connInfo):
    # postgresString = "postgresql://myuser:mypass@localhost:5432/dvdrental"
    # connString = "postgresql://%s:%s@%s:%s/%s".format(connInfo)
    conn = create_engine(connInfo, echo=True)
    result_set = conn.execute("SHOW server_version_num")
    print("luke")
    for r in result_set:  
        print(r)
    
    