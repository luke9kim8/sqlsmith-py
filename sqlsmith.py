import argparse
import postgres
def main():
    parser = argparse.ArgumentParser(description='Form connection to DB')
    parser.add_argument('--target', type=str)
    args = parser.parse_args()
    postgres.schema_pqxx(args.target)
if __name__ == "__main__":
    main()