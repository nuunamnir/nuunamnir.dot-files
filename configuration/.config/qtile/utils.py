import os
import io
import json
import uuid


def load_system_variables(
    input_file_path=os.path.expanduser(
        os.path.join("~", ".config", "qtile", "config.json")
    )
):
    """load system/hardware specific configuration options"""
    system_variables = {}
    with io.open(
        input_file_path,
        "r",
        encoding="utf-8",
    ) as input_handle:
        system_configurations = json.load(input_handle)

    for option in system_configurations["default"]["options"]:
        system_variables[option] = system_configurations["default"]["options"][option]

    system_id = uuid.getnode()
    try:
        for option in system_configurations[system_id]["options"]:
            system_variables[option] = system_configurations[system_id]["options"][
                option
            ]
    except KeyError:
        pass

    return system_variables
