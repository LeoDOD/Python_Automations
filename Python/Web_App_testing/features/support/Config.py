import yaml


# Loads the testing config.
# To use:
# Create and instance of this class, and pass the env that you wish to use (The default is qas).
# Ex: data = Config.Config('qas')

class Config:
    def __init__(self, env='qas'):
        # The base YAML config object.
        file = open("Web_App_testing/features/support/config.yaml", 'r')
        # YAML file will be turned into a dict and saves it in the config_data variable.
        self.config_data = yaml.load(file)
        # The name of the profile to load.
        # @return [String] The name of the profile to load.
        self.env = env

    # As the name Implies, it return a dict so it can be stored in a variable,
    # i have found this to be useful with behave so you can store all data in the variable
    # context.data and that way it wll be available everywhere, even the environment file
    # where we keep the Hooks for the automation
    def save_to_var(self):
        return self.config_data[self.env]
