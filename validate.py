##
# validate.py
#
# Validate group and idol json files against the schema
#

import argparse
import json
import os

from jsonschema.validators import validator_for

# FIXME: Glob for all .group.json
# FIXME: Glob for all .idol.json
with open("group.schema.json") as f:
    GROUP_SCHEMA = json.load(f)
_validator_class = validator_for(GROUP_SCHEMA)
_validator_class.check_schema(GROUP_SCHEMA)
group = _validator_class(GROUP_SCHEMA)

with open("idol.schema.json") as f:
    IDOL_SCHEMA = json.load(f)
_validator_class = validator_for(IDOL_SCHEMA)
_validator_class.check_schema(IDOL_SCHEMA)
idol = _validator_class(IDOL_SCHEMA)

file_path = os.path.join("gg", "fromis_9", "fromis_9.group.json")
with open(file_path, 'r') as f:
    data = json.load(f)

print("Validating {}".format(file_path))
group.validate(data)

file_path = os.path.join("gg", "fromis_9", "lee_saerom.idol.json")
with open(file_path, 'r') as f:
    data = json.load(f)
print("Validating {}".format(file_path))
idol.validate(data)
