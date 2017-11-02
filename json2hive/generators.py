def generate_field_definitions(schema, level=0):
    keywords = ['timestamp', 'date', 'datetime']
    tab = "  "
    type_separator = " " if level == 0 else ": "
    field_separator = "\n" if level == 0 else ",\n"
    field_definitions = []
    new_level = level + 1
    indentation = new_level * tab
    for name, attributes in schema.items():
        cleaned_name = "`{}`".format(name) if name.lower() in keywords else name
        if attributes['type'] == 'object':
            field_definitions.append("{indentation}{name}{separator}STRUCT<\n{definitions}\n{indentation}>".format(
                indentation=indentation,
                name=cleaned_name,
                separator=type_separator,
                definitions=generate_field_definitions(attributes['properties'], new_level)
            ))
        elif attributes['type'] == 'array':
            extra_indentation = (new_level + 1) * tab
            if attributes['items']['type'] == 'object':
                closing_bracket = "\n" + indentation + ">"
                array_type = "STRUCT<\n{definitions}\n{indentation}>".format(
                    indentation=extra_indentation,
                    definitions=generate_field_definitions(attributes['items']['properties'], new_level + 1)
                )
            else:
                closing_bracket = ">"
                array_type = attributes['items']['type'].upper()
            field_definitions.append("{indentation}{name}{separator}ARRAY<{definitions}{closing_bracket}".format(
                indentation=indentation,
                name=cleaned_name,
                separator=type_separator,
                definitions=array_type,
                closing_bracket=closing_bracket
            ))
        else:
            field_definitions.append("{indentation}{name}{separator}{type}".format(
                indentation=indentation,
                name=cleaned_name,
                separator=type_separator,
                type=attributes['type'].upper()
            ))
    return field_separator.join(field_definitions)

def generate_json_table_statement(table, schema, data_location='', database='default', managed=False):
    field_definitions = generate_field_definitions(schema['properties'])
    external_marker = "EXTERNAL " if not managed else ""
    location = "\nLOCATION '{}'".format(data_location) if not managed else ''
    statement = """CREATE {external_marker}TABLE {database}.{table} (
{field_definitions}
)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'{location};""".format(
        external_marker=external_marker,
        database=database,
        table=table,
        field_definitions=field_definitions,
        location=location
    )
    return statement