import yaml
import os
import Rx

cobotPath = 'cobots' + os.sep
allCobotYamls = os.listdir(cobotPath)
print(allCobotYamls)

rx = Rx.Factory({ "register_core_types": True })

schemaPath = cobotPath + "cobot_schema.yaml"
schema = yaml.load(open(schemaPath), Loader=yaml.FullLoader)
validator = rx.make_schema(schema)

for file in allCobotYamls:
    if file != "cobot_schema.yaml" and file != "cobot_template.yaml":
        with open(cobotPath + file) as f:
            print(file)
            data = yaml.load(f, Loader=yaml.FullLoader)
            validator.validate(data)
            print(data)

manufacturerPath = 'manufacturers' + os.sep
allManufacturerYamls = os.listdir(manufacturerPath)

schemaPath = manufacturerPath + "manufacturer_schema.yaml"
schema = yaml.load(open(schemaPath), Loader=yaml.FullLoader)
validator = rx.make_schema(schema)

for file in allManufacturerYamls:
    if file != "manufacturer_schema.yaml" and file != "manufacturer_template.yaml":
        with open(manufacturerPath + file) as f:
            print(file)
            data = yaml.load(f, Loader=yaml.FullLoader)
            validator.validate(data)
            print(data)

