json2hive
=========

json2hive is a command line utility that can automatically generate CREATE TABLE statements for
Hive tables backed by JSON data.

Features
--------

- Automatically infer schema of JSON data by analysing JSON records
- Supports external and managed Hive tables
- Can be used as command line utility or programmatically

Installation
------------

You can install ``json2hive`` using pip:

.. code-block:: bash

    $ pip install json2hive

It is **strongly recommended** that you install ``json2hive`` inside a `virtual environment`_!

.. _virtual environment: http://docs.python-guide.org/en/latest/dev/virtualenvs/

Usage
-----

**On the Command Line**

Run the following and follow the instructions:

.. code-block:: bash

    $ json2hive --help

**As a library**

.. code-block:: python

    from json2hive.utils import infer_schema
    from json2hive.generators import generate_json_table_statement

    # infer schema from objects, these objects could be the result of json.loads(...)
    object1 = {'name': 'John', age: 25}
    object2 = {'name': 'Mary', age: 23}
    schema = infer_schema([object1, object2])

    # Generate CREATE TABLE statement
    statement = generate_json_table_statement('example', schema, managed=True)
    print(statement)
