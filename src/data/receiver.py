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
    def isNewDataAvailable(self) -> bool:
        return True

    def getData(self) -> DataPoint:
        return DataPoint(
            coolantTemp=unit.Quantity(97.3, unit.degC),
            oilPressure=unit.Quantity(60, unit.psi),
            batteryVoltage=unit.Quantity(12.3, unit.volt),
            lambdaValue=unit.Quantity(14.5),
            engineRpm=unit.Quantity(12500, unit.rpm),
            throttlePosition=unit.Quantity(0.83),
        )


class SerialDataReceiver(DataReceiver):
    def isNewDataAvailable(self) -> bool:
        ...

    def getData(self) -> DataPoint:
        ...
