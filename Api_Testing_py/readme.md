# Api Testing using Python

This Automation will send Requests of all methods to an Api, validate the response, and can read into the json response to assert a certain Response. 
This automation is also ale to automatically write the results of a test case into a Test plan in JIRA. Also For Ease of management There is a Config.py file that, before the automation is ran, set all the variables needed to test that application by reading from the config.yaml file.
The Python code is in the Steps File and the Environment file.
## Prerequisites

For this repo to be ran locally you will need to have [Python 3.5](https://www.python.org/downloads/) at least. Run the command below a terminal / shell to find the version of Python you have installed

```
python
```

## Built With

* [Behave](https://pypi.org/project/behave/) - Gherkin Testing Framework
* [Requests](https://pypi.org/project/requests/) - Easy HTTP Framework
* [PyYaml](https://pypi.org/project/PyYAML/) - Yaml Parser for config files
