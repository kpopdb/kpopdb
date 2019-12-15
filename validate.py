##
# validate.py
#
# Validate group and idol json files against the schema
#

import argparse
import glob
import logging
import json
import os
import jsonschema

from jsonschema.validators import validator_for

class KpopValidator(object):
    def __init__(self, base_folder):
        self.base_path = os.path.abspath(base_folder)

        with open(os.path.join(self.base_path, "group.schema.json")) as f:
            group_schema = json.load(f)
        _validator_class = validator_for(group_schema)
        _validator_class.check_schema(group_schema)
        self.v_group = _validator_class(group_schema)

        with open(os.path.join(self.base_path, "idol.schema.json")) as f:
            idol_schema = json.load(f)
        _validator_class = validator_for(idol_schema)
        _validator_class.check_schema(idol_schema)
        self.v_idol = _validator_class(idol_schema, format_checker=jsonschema.FormatChecker())

        with open(os.path.join(self.base_path, "alias.schema.json")) as f:
            idol_schema = json.load(f)
        _validator_class = validator_for(idol_schema)
        _validator_class.check_schema(idol_schema)
        self.v_alias = _validator_class(idol_schema, format_checker=jsonschema.FormatChecker())

    def _validate_group(self, folder):
        """Validate a group's kpop data

        Criteria:
         - There should be one .group.json file.
         - folder name should match .group.json file name.
         - Group data fits group schema
         - All .idol.json files underneath should match the group.
         - All idol data fits idol schema
        """
        logging.info("Validating {}".format(folder))
        group_list = glob.glob(os.path.join(folder, '*.group.json'))

        # Only one .group.json file
        if len(group_list) != 1:
            raise RuntimeError(f"Too many .group files in {folder}: {group_list}")
        group = group_list[0]
        with open(group, 'r') as f:
            group_data = json.load(f)
        # Validate against schema
        self.v_group.validate(group_data)
        # Save off group data for idol data consistency
        group_hangul = group_data['nameHangul']
        group_roman = group_data['nameRoman']
        group_status = group_data['status']

        # Validate idols
        idol_list = glob.iglob(os.path.join(folder, '*.idol.json'))
        for idol in idol_list:
            logging.debug("Validating {}".format(idol))
            with open(idol, 'r') as f:
                idol_data = json.load(f)
            # Validate against schema
            self.v_idol.validate(idol_data)
            # Idol data should have consistent group data
            if ((idol_data['groupHangul'] != group_hangul) or
                (idol_data['groupRoman'] != group_roman)):
                raise RuntimeError(f"Idol group data for {idol_data['stageNameRoman']} does not match group name: {group_hangul} {group_roman}")
            # Check idol status for disbanded groups
            # Must be "disbanded" to show the final lineup
            if group_status == "disbanded":
                if not (idol_data['status'] == "disbanded" or
                        idol_data['status'] == "former"):
                    raise RuntimeError(f"Idol status does not match group disbanded status")

        # Validate alias in group
        alias_list = glob.iglob(os.path.join(folder, '*.alias.json'))
        for alias in alias_list:
            logging.debug("Validating {}".format(alias))
            with open(alias, 'r') as f:
                alias_data = json.load(f)
            # Validate against schema
            self.v_alias.validate(alias_data)
            # Idol data should have consistent group data
            if ((alias_data['groupHangul'] != group_hangul) or
                (alias_data['groupRoman'] != group_roman)):
                raise RuntimeError(f"Idol alias group data for {alias_data['stageNameRoman']} does not match group name: {group_hangul} {group_roman}")
            if group_status == "disbanded":
                if not (alias_data['status'] == "disbanded" or
                        alias_data['status'] == "former"):
                    raise RuntimeError(f"Idol alias status does not match group disbanded status")

        return

    def _validate_solo(self):
        """Validate solo idols"""
        for path in glob.iglob(os.path.join(self.base_path, 'solo/*.idol.json')):
            logging.info("Validating {}".format(path))
            with open(path, 'r') as f:
                idol_data = json.load(f)
            self.v_idol.validate(idol_data)
            # Check for alias existence

    def _validate_aliases(self):
        """Validate aliases of idols"""
        for path in glob.iglob(os.path.join(self.base_path, '**/*.alias.json'), recursive=True):
            logging.info("Validating {}".format(path))
            with open(path, 'r') as f:
                alias_data = json.load(f)
            self.v_alias.validate(alias_data)
            # Check for alias existence
            if not os.path.exists(os.path.join(self.base_path, alias_data['alias'])):
                raise RuntimeError(f"Idol file not found for {path}: {alias_data['alias']}")

    def validate(self):
        """Validate all data in base_path
        """
        for path in glob.iglob(os.path.join(self.base_path, '**/*.group.json'), recursive=True):
            folder = os.path.split(path)[0]
            self._validate_group(folder)

        self._validate_solo()
        self._validate_aliases()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    v = KpopValidator(os.path.split(os.path.abspath(__file__))[0])
    v.validate()
