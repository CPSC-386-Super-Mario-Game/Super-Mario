class Settings:
    def __init__(self):
        #   Screen Settings
        self.screenWidth = 1600             # Screen width set to 1600 pixels
        self.screenHeight = 896
        self.bgColor = (0, 0, 0)            # Background color is black
        self.topOfGame = 0                  # Stores pixel of top left corner for actual game

        #   Game Settings
        self.gameTitle = "Super Mario Bros"
        self.FPS = 144

        #   Block Settings
        self.tileSize = 56
