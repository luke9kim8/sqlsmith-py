import argparse
from postgres import Schema_pqxx
def main():
    parser = argparse.ArgumentParser(description='Form connection to DB')
    parser.add_argument('--target', type=str)
    args = parser.parse_args()
    Schema_pqxx().schema_pqxx(args.target, False)
if __name__ == "__main__":
    main()