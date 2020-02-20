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

vendorPath = 'vendors' + os.sep
allVendorYamls = os.listdir(vendorPath)

schemaPath = vendorPath + "vendor_schema.yaml"
schema = yaml.load(open(schemaPath), Loader=yaml.FullLoader)
validator = rx.make_schema(schema)

for file in allVendorYamls:
    if file != "vendor_schema.yaml" and file != "vendor_template.yaml":
        with open(vendorPath + file) as f:
            print(file)
            data = yaml.load(f, Loader=yaml.FullLoader)
            validator.validate(data)
            print(data)

