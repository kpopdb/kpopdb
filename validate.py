##
# validate.py
#
# Validate group and idol json files against the schema
#

import argparse
import glob
import json
import os
import jsonschema

from jsonschema.validators import validator_for

if __name__ == '__main__':
    with open("group.schema.json") as f:
        GROUP_SCHEMA = json.load(f)
    _validator_class = validator_for(GROUP_SCHEMA)
    _validator_class.check_schema(GROUP_SCHEMA)
    group = _validator_class(GROUP_SCHEMA)

    with open("idol.schema.json") as f:
        IDOL_SCHEMA = json.load(f)
    _validator_class = validator_for(IDOL_SCHEMA)
    _validator_class.check_schema(IDOL_SCHEMA)
    idol = _validator_class(IDOL_SCHEMA, format_checker=jsonschema.FormatChecker())

    for file_path in glob.iglob('./**/*.group.json', recursive=True):
        print("Validating {}".format(file_path))
        with open(file_path, 'r') as f:
            data = json.load(f)
        group.validate(data)

    for file_path in glob.iglob('./**/*.idol.json', recursive=True):
        print("Validating {}".format(file_path))
        with open(file_path, 'r') as f:
            data = json.load(f)
        idol.validate(data)
