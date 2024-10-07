import json

def map_to_dict(map_objects):
    map_representation = []
    for obj in map_objects:
        map_representation.append({
            "name": obj.name,
            "position": obj.position.tolist(),
            "boundingBox": obj.boundingBox,
            "object_type": obj.object_type,
            "condition": obj.condition,
            "properties": obj.properties
        })
    return map_representation

def map_to_string(map_objects):
    """
    Converts a list of mapObject instances into a string where each object is on a new line.

    Parameters:
    - map_objects: List of mapObject instances.

    Returns:
    - A string representation of all mapObjects, each on a new line.
    """
    # Use a list comprehension to create a list of string representations of each mapObject
    map_objects_lines = [obj.__repr__() for obj in map_objects]
    
    # Join the list into a single string with new lines
    map_objects_string = "\n".join(map_objects_lines)
    
    return map_objects_string

def calculate_area(bounding_box):
    """Calculate the area of a bounding box given by two points ((x1, y1), (x2, y2))."""
    (x1, y1), (x2, y2) = bounding_box
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    return width * height

def filter_objects_by_size(objects, min_size):
    """
    Filter out mapObjects from a list that are below the specified size threshold.
    
    Parameters:
    - objects: List of mapObject instances.
    - min_size: Minimum area threshold to filter objects by.

    Returns:
    - A list of mapObject instances that are equal to or larger than the minimum size.
    """
    return [obj for obj in objects if calculate_area(obj.boundingBox) >= min_size]