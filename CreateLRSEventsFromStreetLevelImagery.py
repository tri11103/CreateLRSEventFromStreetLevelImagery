import arcpy


class CreateLRSEventsFromStreetLevelImagery(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Create LRS Events From Street Level Imagery"
        self.description = "Python Geoprocessing Tool that converts street level imagery attached to point features " \
                           "into LRS schema event features."
        self.canRunInBackground = True

    def getParameterInfo(self):
        input_deep_learning_model_param = arcpy.Parameter(
            displayName="Input Deep Learning Model",
            name="in_deep_learning_model",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )

        input_lrs_network_param = arcpy.Parameter(
            displayName="Input LRS Network",
            name="in_lrs_network",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input"
        )

        input_point_features_param = arcpy.Parameter(
            displayName="Input Point Features",
            name="in_point_features",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input"
        )

        params = [input_deep_learning_model_param, input_lrs_network_param, input_point_features_param]
        return params

    def isLicensed(self):
        lr_license = arcpy.CheckExtension("LocationReferencing")
        ia_license = arcpy.CheckExtension("ImageAnalyst")

        if lr_license is not '' and ia_license is not '':
            return True

        return False

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        return
