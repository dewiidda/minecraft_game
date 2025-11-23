from direct.showbase.ShowBase import ShowBase
from mapmanager import Mapmanager
from hero import Hero # Added Hero import

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # Set up field of view
        base.camLens.setFov(90)

        # Initialize the map manager
        self.land = Mapmanager()
        self.land.loadLand("land.txt")

        # Initialize the hero (player) and bind all controls
        # Assuming a starting position of (0, 0, 2)
        self.hero = Hero(pos=(0, 0, 2), land=self.land)


game = Game()
game.run()