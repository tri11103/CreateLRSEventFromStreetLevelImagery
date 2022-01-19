import pytest
import arcpy
import sys
sys.path.append("../")
from CreateLRSEventsFromStreetLevelImagery import *


def test_CreateLRSEventsFromStreetLevelImagery_InputRasterFieldNotInPointFeatures_AssertToolFailsWithInputRasterFieldNotFound():
    tool = CreateLRSEventsFromStreetLevelImagery()
    parameters = ["../DeepLearningModel/Deep Learning Model.dlpk", ["StopSign", "SpeedLimit", "OtherSigns"],
                  "./Test Data/Test Data.gdb/LRS/Network", "./Test Data/Test Data.gdb/PointWithImagery", "FIELD", 100]

    with pytest.raises(InputRasterFieldNotFound):
        tool.execute(parameters, messages=None)


@pytest.mark.skip()
def test_CreateLRSEventsFromStreetLevelImagery_InputClassNamesContainsClassNotFoundInMLOutput_AssertToolFailsWithClassNotFoundInInputClassNames():
    tool = CreateLRSEventsFromStreetLevelImagery()
    parameters = ["../DeepLearningModel/Deep Learning Model.dlpk", ["StopSign", "SpeedLimit", "OtherSigns", "CLASS"],
                  "./Test Data/Test Data.gdb/LRS/Network", "./Test Data/Test Data.gdb/PointWithImagery", "Path", 100]

    with pytest.raises(ClassNotFoundInInputClassNames):
        tool.execute(parameters, messages=None)


def test_CreateLRSEventsFromStreetLevelImagery_IncorrectPathToDeepLearningModel_AssertToolFailsWithFileNotFoundError():
    tool = CreateLRSEventsFromStreetLevelImagery()
    parameters = ["../DeepLearningModel/FOLDER/Deep Learning Model.dlpk", ["StopSign", "SpeedLimit", "OtherSigns"],
                  "./Test Data/Test Data.gdb/LRS/Network", "./Test Data/Test Data.gdb/PointWithImagery", "Path", 100]

    with pytest.raises(FileNotFoundError):
        tool.execute(parameters, messages=None)


def test_CreateLRSEventsFromStreetLevelImagery_InputLRSNetworkValueIsNotLRSSchemaNetwork_AssertToolFails():
    tool = CreateLRSEventsFromStreetLevelImagery()
    parameters = ["../DeepLearningModel/Deep Learning Model.dlpk", ["StopSign", "SpeedLimit", "OtherSigns"],
                  "./Test Data/Test Data.gdb/PointWithImagery", "./Test Data/Test Data.gdb/PointWithImagery", "Path", 100]

    with pytest.raises(InputNetworkIsNotLRSNetwork):
        tool.execute(parameters, messages=None)


def test_CreateLRSEventsFromStreetLevelImagery_InputPointFeaturesIsNotAPointFC_AssertToolFails():
    tool = CreateLRSEventsFromStreetLevelImagery()
    parameters = ["../DeepLearningModel/Deep Learning Model.dlpk", ["StopSign", "SpeedLimit", "OtherSigns"],
                  "./Test Data/Test Data.gdb/LRS/Network", "./Test Data/Test Data.gdb/LineWithImagery", "Path", 100]

    with pytest.raises(InputPointFeaturesAreNotPoints):
        tool.execute(parameters, messages=None)
