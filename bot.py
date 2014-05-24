from pb.game_reader import GameReader, ItemNotFound
from pb.position import get_position
import time
from pymouse import PyMouse

reader = GameReader()
mouse = PyMouse()

print "Calibration"
logo_position = None
while logo_position is None:
    try:
        logo_position = reader.get_location_from_entire_screen('8ball logo')
    except ItemNotFound:
        time.sleep(1)

print "found logo at ", logo_position
print "clicking play btn"
mouse.click(*get_position('logo', logo_position, 'menu play'))

city = 'london'
print "searching for %s game" % (city,)
game_top_left = get_position('logo', logo_position, 'game top left')
left_arrow = get_position('logo', logo_position, 'left arrow')
city_position = None
max_iter = 20
iterations = 0
while city_position is None:
    try:
        city_position = reader.get_location_from_game(city+' logo', game_top_left)
    except ItemNotFound:
        mouse.click(*left_arrow)
        iterations += 1
        if iterations > max_iter:
            raise ItemNotFound('Cannot find city: ' + city)
        time.sleep(1)

