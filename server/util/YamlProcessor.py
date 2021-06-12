import yaml
import os


def __getPathOfYamlFile():
    return os.getenv("CONFIG_YAML_PATH")


def getVariables() -> dict:
    with open(__getPathOfYamlFile()) as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        return yaml.safe_load(file)


def getVariable(key: str):
    with open(__getPathOfYamlFile()) as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        return yaml.safe_load(file).get(key)


def addUpdateVariable(key: str, value):
    allVars = getVariables()
    with open(__getPathOfYamlFile(), 'w') as file:
        allVars[key] = value
        yaml.dump(allVars, file)
