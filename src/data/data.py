import json
import pint


class DataPoint:
    def __init__(self, **kwargs):
        self.coolantTemp = kwargs.get("coolantTemp")
        self.oilPressure = kwargs.get("oilPressure")
        self.batteryVoltage = kwargs.get("batteryVoltage")
        self.lambdaValue = kwargs.get("lambdaValue")
        self.engineRpm = kwargs.get("engineRpm")
        self.throttlePosition = kwargs.get("throttlePosition")
        # TODO: think about other data (e.g. wheel speed)

    def toJson(self):
        quantities = vars(self)

        jsonDict = {}
        for quantityName in quantities:
            quantity = quantities[quantityName]
            jsonDict[quantityName] = {"value": quantity._magnitude, "unit": str(quantity._units)}

        return json.dumps(jsonDict)

