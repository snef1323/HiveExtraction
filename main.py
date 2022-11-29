import arcade
import random

SPRITE_SCALING_PLAYER = 0.2
SPRITE_SCALING = 0.5
TILE_SCALING = 0.5

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Hive Extraction"

MOVEMENT_SPEED = 5

Alien_Count = 20


class Extraction(arcade.Window):

    def __init__(self):

        """Initialize all the variables"""

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        """Variables that will hold the sprite lists"""

        self.player_list = None
        self.empty_list = None
        self.alien_list = None

        self.player_sprite = None
        self.alien_sprite = None

        self.background = None

        self.physics_engine = None

        arcade.set_background_color(arcade.csscolor.GHOST_WHITE)

    def setup(self):
        """Load the background"""
        self.background = arcade.load_texture("../HiveExtraction/images/Hive Extraction Background.jpg")

        """Create Sprite Lists"""
        self.player_list = arcade.SpriteList()
        self.empty_list = arcade.SpriteList(use_spatial_hash=True)
        self.alien_list = arcade.SpriteList()

        """Place and create player"""
        self.player_sprite = arcade.Sprite("../HiveExtraction/images/topdown_pc.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 1120
        self.player_sprite.center_y = 255
        self.player_list.append(self.player_sprite)

        """Place and create alien(IT WORKSSSSS)"""
        for i in range(20):
            self.alien_sprite = arcade.Sprite("../HiveExtraction/images/topdown_alien.png", SPRITE_SCALING)
            self.alien_sprite.center_x = random.randrange(110, 1000)
            self.alien_sprite.center_y = random.randrange(120, 710)
            self.alien_list.append(self.alien_sprite)

        # Create the physics engine
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.empty_list)

    def on_draw(self):

        arcade.start_render()

        # Create the screen
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        self.player_list.draw()
        self.alien_list.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()

        # For the boundaries
        if self.player_sprite.left < 100:
            self.player_sprite.change_x = +0.1

        if self.player_sprite.right > 1150:
            self.player_sprite.change_x = -0.1

        if self.player_sprite.bottom < 110:
            self.player_sprite.change_y = +0.1

        if self.player_sprite.top > 735:
            self.player_sprite.change_y = -0.1


def main():

    window = Extraction()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()


