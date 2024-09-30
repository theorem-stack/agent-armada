import numpy as np

class mapObject:
    def __init__(self, name, position, boundingBox, object_type, condition=None, properties=None):
        self.name = name  # string
        self.position = np.array(position, dtype=float)  # np.array([x, y], dtype=float)
        self.boundingBox = boundingBox  # ((x1, y1), (x2, y2)) - bounding box defining the size/area of the object
        self.object_type = object_type  # string, type of object (e.g., "building", "tree", "animal", "flood", etc.)
        self.condition = condition  # string, e.g., "damaged", "intact", "flooded", "destroyed"
        self.properties = properties or {}  # dict, optional additional properties such as water level, material, etc.

    def __repr__(self):
        return f"mapObject(name={self.name}, position={self.position}, boundingBox={self.boundingBox}, type={self.object_type}, condition={self.condition}, properties={self.properties})"
