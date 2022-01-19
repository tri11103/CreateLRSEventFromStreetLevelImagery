import arcpy
import os
import datetime
from ToolExceptions import *


class CreateLRSEventsFromStreetLevelImagery(object):
    def __init__(self):
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

        tolerance_param = arcpy.Parameter(
            displayName="Tolerance",
            name="tolerance",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input"
        )

        input_class_names_param.columns = [["Field"]]

        params = [input_deep_learning_model_param, input_class_names_param, input_lrs_network_param,
                  input_point_features_param, input_raster_field_param, tolerance_param]

        return params


    def get_feature_dataset(self, fc):
        fc_path = arcpy.Describe(fc).catalogPath
        fc_home = os.path.dirname(fc_path)

        if arcpy.Describe(fc_home).dataType == "FeatureDataset":
            return fc_home
        else:
            return None


    def try_create_new_point_events_based_on_in_class_names(self, lrs_network, in_class_names):
        for class_name in in_class_names:
            try:
                arcpy.AddMessage("Creating LRS Event: {}".format(class_name))
                arcpy.locref.CreateLRSEvent(lrs_network, class_name, "POINT", "EventId", "RouteId", "FromDate",
                                            "ToDate", "LocError", "Measure", "", "NO_SPANS_ROUTES", "", "NO_STORE_ROUTE_NAME",
                                            "", "")
            except:
                arcpy.AddMessage("Event {} already exists in the LRS".format(class_name))


    def create_new_weighted_dictionary(self, in_class_names):
        dict = {}
        for class_name in in_class_names:
            dict[class_name] = 0
        return dict


    def get_most_frequent_class(self, in_class_names, weighted_dictionary):
        most_frequent_class = ""
        frequency = 0
        for class_name in in_class_names:
            if weighted_dictionary[class_name] > frequency:
                most_frequent_class = class_name
                frequency = weighted_dictionary[class_name]
        return most_frequent_class


    def get_closest_route_info_from_point(self, point, lrs_network, tolerance):
        route_id = ""
        from_date = ""
        to_date = ""
        measure = 0
        out_fc = "tmp_SpatialJoinOutput"
        tmp_point_fc_name = "tmpPoints"
        tmp_point_fc = arcpy.management.CreateFeatureclass(out_path=arcpy.env.workspace, out_name=tmp_point_fc_name, geometry_type="POINT",
                                                           has_z="ENABLED", spatial_reference=arcpy.Describe(lrs_network).spatialReference)

        with arcpy.da.InsertCursor(tmp_point_fc_name, ["SHAPE@XY"]) as cursor:
            cursor.insertRow([point])

        arcpy.analysis.SpatialJoin(tmp_point_fc, lrs_network, out_fc, "JOIN_ONE_TO_ONE", "KEEP_ALL",
                                   'FromDate "FromDate" true true false 8 Date 0 0,First,#,{},FromDate,-1,-1;ToDate "ToDate" true true false 8 Date 0 0,First,#,{},ToDate,-1,-1;RouteId "RouteId" true true false 255 Text 0 0,First,#,{},RouteId,0,255'.format(lrs_network, lrs_network, lrs_network),
                                   "INTERSECT", "{} Meters".format(tolerance), '')

        with arcpy.da.SearchCursor(out_fc, ["RouteId", "FromDate", "ToDate"]) as cursor:
            # Only take the first row...
            for row in cursor:
                route_id = row[0]
                from_date = row[1]
                to_date = row[2]
                break

        out_table = "tmpLocateFeaturesAlongRoutesTable"
        arcpy.lr.LocateFeaturesAlongRoutes(tmp_point_fc_name, lrs_network, "RouteId", tolerance, out_table,
                                           "RouteId POINT DerivedMeasure")

        # TODO: Rather than take the first row here, choose the route measure that aligns with the event's time slice
        with arcpy.da.SearchCursor(out_table, ["DerivedMeasure"]) as cursor:
            # Only take the first row...
            for row in cursor:
                measure = row[0]
                break

        arcpy.management.Delete(out_fc)
        arcpy.management.Delete(tmp_point_fc)
        arcpy.management.Delete(out_table)

        return route_id, from_date, to_date, measure

    def validate_parameters(self, parameters):
        deep_learning_model = parameters[0] if type(parameters[0]) is str else parameters[0].valueAsText
        class_names = parameters[1] if type(parameters[1]) is list else parameters[1].valueAsText.split(";")
        lrs_network = parameters[2] if type(parameters[2]) is str else parameters[2].valueAsText
        point_features = parameters[3] if type(parameters[3]) is str else parameters[3].valueAsText
        raster_field = parameters[4] if type(parameters[4]) is str else parameters[4].valueAsText
        tolerance = parameters[5] if (type(parameters[5]) is float or type(parameters[5]) is int) else parameters[5].value

        if not os.path.exists(deep_learning_model):
            raise FileNotFoundError()

        field_names_in_point_features = [x.name for x in arcpy.ListFields(point_features)]
        if raster_field not in field_names_in_point_features:
            raise InputRasterFieldNotFound(raster_field=raster_field, feature_class=point_features)

        lrs_dataset = self.get_feature_dataset(lrs_network)
        if not lrs_dataset:
            raise InputNetworkIsNotLRSNetwork(lrs_network=lrs_network)

        if arcpy.Describe(point_features).shapeType != "POINT":
            raise InputPointFeaturesAreNotPoints(point_features=point_features)

        return deep_learning_model, class_names, lrs_network, point_features, raster_field, tolerance


    def execute(self, parameters, messages):
        deep_learning_model, class_names, lrs_network, point_features, raster_field, tolerance = self.validate_parameters(parameters)

        self.try_create_new_point_events_based_on_in_class_names(lrs_network, class_names)

        with arcpy.da.SearchCursor(point_features, [raster_field, "SHAPE@XY"]) as point_features_cursor:
            i = 0

            for point_features_row in point_features_cursor:
                i += 1
                out_fc = "DetectObjects{}".format(i)
                arcpy.AddMessage("Processing image record: {}".format(i))
                arcpy.AddMessage(point_features_row[0])
                arcpy.ia.DetectObjectsUsingDeepLearning(point_features_row[0], out_fc, deep_learning_model,
                                                        class_value_field="Class")

                weighted_dictionary = self.create_new_weighted_dictionary(class_names)
                with arcpy.da.SearchCursor(out_fc, ["Class"]) as detected_objects_cursor:
                    for detected_objects_row in detected_objects_cursor:
                        if detected_objects_row[0] not in class_names:
                            raise ClassNotFoundInInputClassNames(detected_objects_row[0])

                        weighted_dictionary[detected_objects_row[0]] += 1

                most_frequent_class = self.get_most_frequent_class(class_names, weighted_dictionary)
                arcpy.AddMessage("Found {}".format(most_frequent_class))

                with arcpy.da.InsertCursor(r"{}\{}".format(lrs_dataset, most_frequent_class), ["SHAPE@XY", "EventId", "RouteId",
                                                                                               "FromDate", "ToDate",
                                                                                               "Measure"]) as event_update_cursor:
                    x, y = point_features_row[1]
                    point = arcpy.Point(x, y)
                    route_id, from_date, to_date, measure = self.get_closest_route_info_from_point(point, lrs_network, tolerance)
                    event_id = "{}".format(datetime.datetime.now())
                    event_update_cursor.insertRow([point, event_id, route_id, from_date, to_date, measure])

                arcpy.management.Delete(out_fc)

