import yaml


# Loads the testing config.
# To use:
# Create and instance of this class, and pass the env that you wish to use (The default is qas).
# Ex: data = Config.Config('qas')

class Config:
    def __init__(self, env='qas'):
        # The base YAML config object.
        f = open("Api_Testing_py/features/support/config.yaml", 'r')
        # YAML file will be turned into a dict and saves it in the config_data variable.
        self.config_data = yaml.load(f)
        # The name of the profile to load.
        # @return [String] The name of the profile to load.
        self.env = env

    # As the name Implies, it return a dict so ti can be stored in a variable,
    # i have found this to be useful with behave so you can store all data in the variable
    # context.data and that way it wll be available everywhere, even the environment file
    # were we keep the Hooks for the automation
    def save_to_var(self):
        return self.config_data[self.env]

    def get(self, key):
        # Gets a key from the config object.
        # @param key [String] The key of the object to get from the config object.
        # @param env [String] The env sets the profile to be used in the automation.
        # @return [Object] The value stored at `key` in the config object.
        return self.config_data[self.env][key]

    def add(self, key, value):
        # Sets or overrides the value of a key on the config.yaml.
        # @param key [String] The key of the object on the config object to replace or create.
        # @param value [Object] The value to save in the key.
        self.config_data[self.env].update({key: value})
