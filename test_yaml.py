# This file is part of the Open Robot Database by Jörn Malzahn available at https://github.com/joernmalzahn/OpenRobotDatabase. 
# This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
#
# The information in this file is provided "as is" without warranty of any kind. The maintainer of this file exercises reasonable efforts to 
# include accurate and up-to-date information; he, however, does not make any warranties or representations as to its accuracy or completeness. 
# Information in this file may periodically be added, changed, or updated without notice. 
# 
# If you make decisions based on the data provided in the Open Robot Database including any of its files, you do so at your own risk and it is strongly
# recommended to verify the information contained in this file through other channels.
#
# The information in this file is made available in the hope that it will be helpful to others. Contributions in the form of feedback, corrections, data, code, etc. is highly welcome and will 
# be credited. Please visit https://github.com/joernmalzahn/OpenRobotDatabase/blob/master/README.md on how to get in touch and provide feedback.

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

