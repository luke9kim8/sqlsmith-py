import argparse
import postgres
def main():
    parser = argparse.ArgumentParser(description='Form connection to DB')
    parser.add_argument("-d", "--DBURI", required=True, 
        help="DB URI to execute select queries")
    args = vars(parser.parse_args())
    postgres.schema_pqxx(args['DBURI'])
if __name__ == "__main__":
    main()