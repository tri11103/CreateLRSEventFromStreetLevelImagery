import arcpy


class CreateLRSEventsFromStreetLevelImagery(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Create LRS Events From Street Level Imagery"
        self.description = "Python geoprocessing tool that converts street level imagery attached to point features " \
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

        input_class_names_param = arcpy.Parameter(
            displayName="Input Class Names",
            name="in_class_names",
            datatype="GPValueTable",
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

        input_raster_field_param = arcpy.Parameter(
            displayName="Input Raster Field",
            name="in_raster_field",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )

        input_class_names_param.columns = [["Field"]]

        params = [input_deep_learning_model_param, input_class_names_param, input_lrs_network_param,
                  input_point_features_param, input_raster_field_param]

        return params


    def isLicensed(self):
        lr_license = arcpy.CheckExtension("LocationReferencing")
        ia_license = arcpy.CheckExtension("ImageAnalyst")

        if lr_license == 'Available' and ia_license == 'Available':
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
        """
        * Create tmp workspace

        For each point feature...
            * Get the raster field data from the FC,
            * Run the raster through Detect Objects Using Deep Learning
            * Save the output of DOUDL to the tmp workspace
            * Find the frequency of detected objects in the DOUDL output
                * if the output contains a class name that does not appear in in_class_names then fail
            * Take the highest occuring class in the DOUDLE output and...
                * if no event FC exists with the name of the class, create it and append an event record
                * append an event record to the event FC with the same name
                * the location of the event record should be the same location as the original point feature

        * Run Generate Events
        * Delete tmp workspace
        """

        return
