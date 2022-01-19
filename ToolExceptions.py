class InputPointFeaturesAreNotPoints(Exception):
    def __init__(self, *args, point_features):
        self.message = "{} is not a point feature class.".format(point_features)

    def __str__(self):
        return self.message


class InputNetworkIsNotLRSNetwork(Exception):
    def __init__(self, *args, lrs_network):
        self.message = "{} is not a valid LRS network.".format(lrs_network)

    def __str__(self):
        return self.message


class InputRasterFieldNotFound(Exception):
    def __init__(self, *args, raster_field, feature_class):
        self.message = "Input Raster Field '{}' is not in '{}'".format(raster_field, feature_class)

    def __str__(self):
        return self.message


class ClassNotFoundInInputClassNames(Exception):
    def __init__(self, *args, class_name):
        self.message = "'{}' not found in in_class_names".format(class_name)

    def __str__(self):
        return self.message

