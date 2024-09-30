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

def map_to_json(map_objects):
    return json.dumps(map_to_dict(map_objects), indent=4)

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