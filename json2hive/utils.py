import json
import genson


def infer_schema(json_objects):
    s = genson.Schema()
    s.add_schema({"type": "object", "properties": {}})
    for o in json_objects:
        s.add_object(o)
    return s.to_dict()


def infer_schema_from_file(json_file_path):
    with open(json_file_path, 'r') as f:
        objects = [json.loads(line) for line in f.readlines()]
    return infer_schema(objects)
