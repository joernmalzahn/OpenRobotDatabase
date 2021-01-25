# Open Robot Database (ORD)

The Open Robot Database - short "ORD" - essentially is a collection of yaml files listing properties of robots that you typially find in robot datasheets. There are plenty of [great resources](https://planet-robotics.net/articles/link-dump-compare-the-cobots-on-the-market/) listing different robots along with their payload capacity, maximum reachability, Cartesian velocity or repeatability. However, I wanted to add also other information and wanted to query, filter and [visualize](https://planet-robotics.net/articles/payload-vs-maximum-reach-for-57-cobots/) such information. So I sat down and created these yaml files, which I wish to share  with the community through this repository for journalistic purpose in the hope this data will be helpful to someone. 

## Repository Organization
The yaml files are organized in two directories. The script `test_yaml.py` checks whether the data in all files is formatted correctly. It uses  [Rx](http://rx.codesimply.com/) and points to possible schema violations, so that they can be corrected easily.

### The `manufacturers` Directory
The `manufacturers` directory lists all the yaml files containing data about robot manufacturers. It has two special files. The yaml files follow a data schema defined in `./manufacturers/manufacturer_schema.yaml`. A template for manufacturer yaml files is given in `./manufacturers/manufacturer_template.yaml`.

### The `cobots` Directory
The `cobots` directory lists all the yaml files containing data about collaborative robots (so-called cobots). It is where everything originally started, as I was looking into Cobots. Hopefully, there will be other types of robots in the future as well. The directory has two special yaml files. The yaml files follow a data schema defined in `./cobots/cobot_schema.yaml`. A template for robot yaml files is given in `./cobots/cobot_template.yaml`.

### The `figures` Directory
This directory is for figures that have been created using the data in the repository.

### OcdCore Class
OcdCore is the Python class, which allows to collect the information in the yaml files and to convert it into a SQLite3 database. The `cobot_config.yaml` and `manufacturer_config.yaml` define which fields of the yaml files in the corresponding directories shall be ported into the database file. 

### OrdSqlInterface
OrdSqlInterface is a Python class providing convenience functions for SQLite3 to OcdCore.

## Disclaimer
If you make decisions based on the data provided in the Open Robot Database including any of its files, you do so at your own risk and it is strongly recommended to verify the information contained in this file through other channels such as the robot manufacturer's original site.

## A Quick Example
In the example below, we instantiate an OrdCore class and visualize the payload capacity versus the maximum reach for all robots in the database using [Matplotlib](https://matplotlib.org/).

```
from ord_core import OrdCore
import matplotlib.pyplot as plt

# The name of our database will be:
database = "ord_database.db"
    
# Initialize the ORD core:
core = OrdCore(db_filename=database)

# Convert .yamls into a SQLite database
core.create_db()        

# Next we are going to plot the payload mass capacity for each robot 
# versus the robot's maximum reach.

# Extract and organize desired columns from the database
data = core.get_data('cobots', ['payload mass', 'max reach'])
payloads, reaches = zip(*data)

# Plotting
plt.plot(reaches, payloads,'o')
ax = plt.gca()
ax.set_xlim([0,1800])
ax.set_ylim([0,26])
ax.set_xlabel("Max. Reach [mm]")
ax.set_ylabel("Payload Mass [kg]")
plt.title("Number of Cobots: %d" % len(reaches))
plt.show()

data = core.get_data('manufacturers')
print(data)

```
The result should look somehow like this:
![a_quick_example.svg](https://github.com/joernmalzahn/OpenRobotDatabase/blob/master/figures/a_quick_example.svg)

## Call for Contributions

Keeping the database up-to-date is hard and time consuming work. Any support, contribution and help is grately appreciated and of course credited.

Even if you don't feel to have enough knowldege about GitHub, pushes, commits, pull requests, YAML and databases, programming or open source in general, **you can still contribute** and be part of creating something great! While this holds for any open source project, **the Open Robot Database in particular will benefit from**:

- sharing the knowledge about the existence of the Open Robot Database mouth-to-mouth or on social networks
- notifications about new robots to add
- new robot data
- corrections of erroneous data
- providers of missing data
- feedback on how to improve the database
- some visualisations of the data
- participate in the discussion and provide some hints for listed [issues](https://github.com/joernmalzahn/OpenRobotDatabase/issues)

If you are comfortable with GitHub and can carve out some time to support this project, please feel free to create a pull request with additions, corrections, suggested modifications. If you are a **first time user**, you can drop a message using GitHub issues. Quickly learn about issues with a quick read of the [corresponding section](https://docs.github.com/en/free-pro-team@latest/github/managing-your-work-on-github/creating-an-issue) in the GitHub documentation or [watch this short video](https://youtu.be/WMykv2ZMyEQ).

Looking forward and thanks a lot in advance!

## License Information

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/Dataset" property="dct:title" rel="dct:type">Open Robot Database</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="https://github.com/joernmalzahn/OpenRobotDatabase" property="cc:attributionName" rel="cc:attributionURL">Jörn Malzahn</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.<br />Based on the work at <a xmlns:dct="http://purl.org/dc/terms/" href="https://github.com/joernmalzahn/OpenRobotDatabase" rel="dct:source">https://github.com/joernmalzahn/OpenRobotDatabase</a>.
