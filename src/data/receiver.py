import random
from abc import ABC, abstractmethod
from data.data import DataPoint
from utils.config import Config, unit

class DataReceiver(ABC):
    def __init__(self, config: Config):
        self.config = config

    @abstractmethod
    def isNewDataAvailable(self) -> bool:
        pass

    @abstractmethod
    def getData(self) -> DataPoint:
        pass


class StubDataReceiver(DataReceiver):
    def __init__(self, config: Config):
        super().__init__(config)

        self._values = {
            "coolantTemp": 97.3,
            "oilPressure": 60,
            "batteryVoltage": 12.3,
            "lambdaValue": 14.5,
            "engineRpm": 12500,
            "throttlePosition": 0.83,
        }

    def updateValue(self, valueName: str, step: float, minValue: float, maxValue: float) -> float:
        assert minValue <= maxValue
        assert valueName in self._values

        curValue: float = self._values[valueName]
        possChanges = [0]

        if curValue - step >= minValue:
            possChanges.append(-step)
        if curValue + step <= maxValue:
            possChanges.append(step)

        self._values[valueName] = curValue + random.choice(possChanges)
        return self._values[valueName]

    def isNewDataAvailable(self) -> bool:
        return True

    def getData(self) -> DataPoint:
        return DataPoint(
            coolantTemp=unit.Quantity(self.updateValue("coolantTemp", 0.1, 95, 100), unit.degC),
            oilPressure=unit.Quantity(self.updateValue("oilPressure", 1, 55, 65), unit.psi),
            batteryVoltage=unit.Quantity(self.updateValue("batteryVoltage", 0.1, 10, 13), unit.volt),
            lambdaValue=unit.Quantity(self.updateValue("lambdaValue", 0.1, 12, 16)),
            engineRpm=unit.Quantity(self.updateValue("engineRpm", 10, 7000, 13500), unit.rpm),
            throttlePosition=unit.Quantity(self.updateValue("throttlePosition", 0.01, 0, 1)),
        )


class SerialDataReceiver(DataReceiver):
    def isNewDataAvailable(self) -> bool:
        ...

    def getData(self) -> DataPoint:
        ...
