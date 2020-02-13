import yaml
import os

cobotPath = 'cobots' + os.sep
allCobotYamls = os.listdir(cobotPath)
print(allCobotYamls)

for file in allCobotYamls:
    with open(cobotPath + file) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        print(data)


print(data['mechanical properties']['mounting'])
print(data['installation time'])

vendorPath = 'vendors' + os.sep
allVendorYamls = os.listdir(vendorPath)
for file in allVendorYamls:
    with open(vendorPath + file) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        print(data)