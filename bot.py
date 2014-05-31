from pb.game_reader import GameReader, ItemNotFound, PS_YOUR_TURN
from pb.position import get_position
import pb.solver
import pb.ball
import time
import pb.player
from pymouse import PyMouse

class Bot:
    def __init__(self):
        self.reader = GameReader(debug=True)
        self.player = pb.player.Player()

    def calibrate(self):
        print "calibrating"
        self.logo_position = None
        while self.logo_position is None:
            try:
                self.logo_position = self.reader.get_location_from_entire_screen('8ball logo')
            except ItemNotFound:
                time.sleep(1)

    def at_menu(self):
        try:
            self.reader.get_location_from_game('8ball logo')
            return True
        except ItemNotFound:
            return False

    def start_game(self, city):
        print "found logo at ", logo_position
        print "clicking play btn"
        self.player.click(get_position('logo', self.logo_position, 'menu play'))

        print "searching for %s game" % (city,)
        game_top_left = get_position('logo', self.logo_position, 'game top left')
        left_arrow = get_position('logo', self.logo_position, 'left arrow')
        city_position = None
        max_iter = 20
        iterations = 0
        while city_position is None:
            try:
                city_position = self.reader.get_location_from_game(city+' logo', game_top_left)
            except ItemNotFound:
                self.player.click(left_arrow)
                iterations += 1
                if iterations > max_iter:
                    raise ItemNotFound('Cannot find city: ' + city)
                time.sleep(1)

        print "city found. going in"
        self.player.click(get_position('logo', self.logo_position, '1v1 play'))

    def take_turn(self):
        if self.reader.get_player_status() == PS_YOUR_TURN:
            print "checking target ball"
            target = self.reader.get_target()
            print "got type:", target

            print "it's your turn, getting table"
            table = self.reader.get_table()

            try:
                solver = pb.solver.Solver(table)
                target_ball_type = self.reader.get_target()
                target = None

                if target_ball_type is None:
                    target, power = solver.find_target_pos_and_power(pb.ball.TYPE_STRIPE)
                    if target is None:
                        target, power = solver.find_target_pos_and_power(pb.ball.TYPE_SOLID)
                else:
                    target, power = solver.find_target_pos_and_power(target_ball_type)

                if target is None:
                    print "Found no target, going to use the closest target"
                    if target_ball_type is None:
                        target, d1 = solver.get_closest_open_shot(pb.ball.TYPE_STRIPE)
                        t2, d2 = solver.get_closest_open_shot(pb.ball.TYPE_SOLID)
                        if d2 < d1:
                            target = t2
                    else:
                        target, d1 = solver.get_closest_open_shot(target_ball_type)
                        
                print "Shooting"
                self.player.shoot(
                        target, 
                        power, 
                        reader.get_table_offset(), 
                        table.get_target_balls(pb.ball.TYPE_CUE)[0])

            except Exception as e:
                print "Error: %s" % (e,)

if __name__ == '__main__':
    bot = Bot()
    bot.calibrate()
    while True:
        bot.start_game('london')
        turns = 0
        while True:
            bot.take_turn()
            turns += 1
            if turns % 20 == 0 && bot.at_menu():
                break

