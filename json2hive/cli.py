import argparse
import os
from json2hive.utils import infer_schema_from_file
from json2hive.generators import generate_json_table_statement

def main():
    parser = argparse.ArgumentParser(description='Generate Hive table from JSON')
    parser.add_argument('json_file', help="Path to a new-line delimited json file with sample records")
    parser.add_argument('-t', '--table', help="Name of Hive table that will be created")
    parser.add_argument('-d', '--database', help="Name of Hive database where table will be created", default='default')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-l', '--location', help="Location of the data backing the Hive table", default='')
    group.add_argument('-m', '--managed', help="Create a managed table (instead of external)", action='store_true')
    args = parser.parse_args()
    file_basename = ".".join(os.path.basename(args.json_file).rsplit(".")[:-1])
    table_name = args.table if args.table else file_basename
    schema = infer_schema_from_file(args.json_file)
    print(generate_json_table_statement(table_name, schema, data_location=args.location, database=args.database, managed=args.managed))