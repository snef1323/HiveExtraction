import arcade
import random

# Constants
SPRITE_SCALING_PLAYER = 0.2
SPRITE_SCALING = 0.5
TILE_SCALING = 0.5
MOVEMENT_SPEED = 5

# Window
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Hive Extraction"


class TitleView(arcade.View):

    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("images/Title_Screen.jpg")

    def on_show(self):
        """Runs once we switch to this view"""
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)
        # Reset viewpoint back to 0,0
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        """Draw this view"""

        arcade.start_render()

        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT)

        arcade.draw_text("Hive Extraction", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
                     arcade.color.WHITE, font_size=50, anchor_x='center')
        arcade.draw_text("Controls:", 300, SCREEN_HEIGHT / 2-75, arcade.color.WHITE,
                     font_size=20, anchor_x='left')
        arcade.draw_text("WASD or Arrow Keys", 300,
                     SCREEN_HEIGHT / 2-105, arcade.color.WHITE, font_size=20, anchor_x='left')
        arcade.draw_text('Click to advance', SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2-250, arcade.color.WHITE, font_size=20,
                     anchor_x='center')

    def on_mouse_press(self, _x, _y, button, _modifiers):
        """If the user presses the mouse button, start the game"""
        game_view = Extraction()
        game_view.setup()
        self.window.show_view(game_view)


class GameOver(arcade.View):

    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("images/gameover.png")

    def on_draw(self):
        self.clear()
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT)


# Main Game View
class Extraction(arcade.View):

    def __init__(self):
        """Initialize all the variables"""
        super().__init__()

        """Sprite lists + health"""
        self.empty_list = None
        self.player_list = None
        self.alien_list = None
        self.player_sprite = None
        self.alien_sprite = None
        self.health = 100

        """Background+physics"""
        self.physics_engine = None
        self.background = None
        arcade.set_background_color(arcade.csscolor.GHOST_WHITE)

    def setup(self):
        """Load the background"""
        self.background = arcade.load_texture("images/Hive Extraction Background.jpg")

        """Create Sprite Lists"""
        self.player_list = arcade.SpriteList()
        self.empty_list = arcade.SpriteList(use_spatial_hash=True)
        self.alien_list = arcade.SpriteList()

        """Place and create player"""
        self.player_sprite = arcade.Sprite("images/topdown_pc.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 1120
        self.player_sprite.center_y = 255
        self.player_list.append(self.player_sprite)

        """Place and create aliens"""
        for i in range(20):
            self.alien_sprite = arcade.Sprite("images/topdown_alien.png", SPRITE_SCALING)
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

        # Health on screen
        arcade.draw_text("Health", 930, 700, arcade.color.YELLOW, 40, 80, 'left')
        arcade.draw_text(self.health, 1100, 700, arcade.color.YELLOW, 40, 80, 'left')

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

        # Health on screen
        arcade.draw_text("Health", 30, 30, arcade.color.YELLOW, 40, 80, 'left')

        # Collision detection
        colliding = arcade.check_for_collision_with_list(self.player_sprite, self.alien_list)

        if colliding:
            self.health -= 1

        # Gameover check
        if self.health <= 0:
            view = GameOver()
            self.window.show_view(view)


def main():

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = TitleView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()


