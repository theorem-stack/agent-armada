import numpy as np

class mapObject:
    def __init__(self, name, position, boundingBox, object_type, condition=None, properties=None):
        self.name = name  # string
        self.position = position # [x, y] - position of the object
        self.boundingBox = boundingBox  # ((x1, y1), (x2, y2)) - bounding box defining the size/area of the object
        self.object_type = object_type  # string, type of object (e.g., "building", "tree", "animal", "flood", etc.)
        self.condition = condition  # string, e.g., "damaged", "intact", "flooded", "destroyed"
        self.properties = properties or {}  # dict, optional additional properties such as water level, material, etc.
        self.detected = False # has object been detected flag

    def __repr__(self):
        return f"mapObject(name={self.name}, position={self.position}, boundingBox={self.boundingBox}, type={self.object_type}, condition={self.condition}, properties={self.properties})"

    def convert_to_dict(self):
        return {
            "name": self.name,
            "position": self.position,
            "boundingBox": self.boundingBox,
            "object_type": self.object_type,
            "condition": self.condition,
            "properties": self.properties,
            "detected": self.detected
        }