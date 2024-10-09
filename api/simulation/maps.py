from .mapObject import mapObject

hurricane_map = [
    mapObject("Home1", [100, 150], ((90, 140), (110, 160)), "building", condition="damaged", properties={"flood_level": 0.5}),
    mapObject("Home2", [250, 300], ((240, 290), (260, 310)), "building", condition="destroyed"),
    mapObject("Flooded Area", [400, 400], ((350, 350), (450, 450)), "flood", condition="flooded", properties={"water_depth": 2.0}),
    mapObject("Fallen Tree", [180, 120], ((170, 110), (190, 130)), "tree", condition="fallen"),
    mapObject("Car", [700, 300], ((490, 590), (510, 610)), "vehicle", condition="damaged", properties={"flood_level": 1.0}),
    mapObject("Person1", [50, 50], ((40, 40), (60, 60)), "person", condition="injured"),
    mapObject("Person2", [200, 250], ((190, 240), (210, 260)), "person", condition="deceased"),
    mapObject("Person3", [400, 500], ((390, 490), (410, 510)), "person", condition="uninjured"),
]

national_park_map = [
    mapObject("Tree1", [50, 100], ((40, 90), (60, 110)), "tree", condition="intact"),
    mapObject("Tree2", [120, 180], ((110, 170), (130, 190)), "tree", condition="intact"),
    mapObject("Deer", [200, 250], ((190, 240), (210, 260)), "animal", properties={"species": "deer", "speed": 10}),
    mapObject("Open Field", [300, 300], ((280, 280), (320, 320)), "open_land", properties={"grass_height": 0.5}),
    mapObject("Lake", [400, 500], ((350, 450), (450, 550)), "water", properties={"depth": 3.0, "type": "freshwater"}),
]

small_town_map = [
    mapObject("House1", [50, 50], ((40, 40), (60, 60)), "building", condition="intact"),
    mapObject("Grocery Store", [100, 150], ((90, 140), (110, 160)), "building", condition="intact"),
    mapObject("Road1", [0, 200], ((0, 190), (100, 210)), "road", properties={"lane_count": 2, "paved": True}),
    mapObject("Strip Center", [300, 300], ((280, 280), (320, 320)), "building", condition="intact"),
    mapObject("Park", [500, 500], ((480, 480), (520, 520)), "open_land", properties={"has_playground": True}),
]

maps = {
    "hurricane_map": hurricane_map,
    "national_park_map": national_park_map,
    "small_town_map": small_town_map,
}