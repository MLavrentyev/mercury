import json
import pint
import math


class DataPoint:
    def __init__(self, **kwargs):
        self.coolantTemp = kwargs.get("coolantTemp"), 0.1
        self.oilPressure = kwargs.get("oilPressure"), 1
        self.batteryVoltage = kwargs.get("batteryVoltage"), 0.1
        self.lambdaValue = kwargs.get("lambdaValue"), 0.1
        self.engineRpm = kwargs.get("engineRpm"), 10
        self.throttlePosition = kwargs.get("throttlePosition"), 0.01
        # TODO: think about other data (e.g. wheel speed)

    def toJson(self):
        quantities = vars(self)

        jsonDict = {}
        for quantityName in quantities:
            precision: float
            quantity, precision = quantities[quantityName]

            quantityValue = round(quantity._magnitude, -int(round(math.log(precision, 10))))
            quantityValue = int(quantityValue) if type(precision) == int else quantityValue

            jsonDict[quantityName] = {"value": f"{quantityValue:,}", "unit": str(quantity._units)}

        return json.dumps(jsonDict)

