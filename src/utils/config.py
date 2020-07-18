import yaml


class Config:
    def __init__(self, configFile):
        with open(configFile, "r") as stream:
            self.configData = yaml.safe_load(stream)

    def getSetting(self, configName):
        currData = self.configData
        for subheading in configName.split("."):
            if subheading:
                if type(currData) == dict:
                    currData = currData.get(subheading)
                elif type(currData) == list:
                    currData = currData[subheading]
            else:
                raise Exception()

        return currData
