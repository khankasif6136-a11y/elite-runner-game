
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.core.window import Window
from random import randint


Window.clearcolor = (0.03, 0.04, 0.07, 1)


class RunnerGame(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.player_x = 80
        self.player_y = 100
        self.player_size = 55

        self.velocity_y = 0
        self.gravity = -0.9
        self.jump_power = 17

        self.ground_y = 100

        self.obstacle_x = 900
        self.obstacle_w = 45
        self.obstacle_h = 70

        self.coin_x = 1200
        self.coin_y = 230
        self.coin_size = 30

        self.speed = 7

        self.score = 0
        self.coins = 0

        self.game_over = False

        self.score_label = Label(
            text="SCORE: 0",
            font_size="22sp",
            bold=True,
            size_hint=(None, None),
            size=(180, 50),
            pos=(20, 520)
        )

        self.coin_label = Label(
            text="🪙 0",
            font_size="20sp",
            bold=True,
            size_hint=(None, None),
            size=(100, 50),
            pos=(20, 475)
        )

        self.game_over_label = Label(
            text="",
            font_size="32sp",
            bold=True,
            halign="center",
            valign="middle",
            size_hint=(None, None),
            size=(400, 180),
            pos=(150, 250)
        )

        self.add_widget(self.score_label)
        self.add_widget(self.coin_label)
        self.add_widget(self.game_over_label)

        Clock.schedule_interval(self.update, 1 / 60)

    def draw_game(self):

        self.canvas.before.clear()

        with self.canvas.before:

            # Sky/background
            Color(0.03, 0.04, 0.07, 1)
            Rectangle(
                pos=(0, 0),
                size=self.size
            )

            # Moon
            Color(0.8, 0.85, 1, 1)
            Ellipse(
                pos=(self.width - 100, self.height - 120),
                size=(55, 55)
            )

            # Ground
            Color(0.12, 0.14, 0.18, 1)
            Rectangle(
                pos=(0, 0),
                size=(self.width, self.ground_y)
            )

            # Ground line
            Color(0.2, 0.8, 0.9, 1)
            Rectangle(
                pos=(0, self.ground_y),
                size=(self.width, 5)
            )

            # Player shadow
            Color(0, 0, 0, 0.4)
            Ellipse(
                pos=(self.player_x - 5, self.player_y - 8),
                size=(65, 15)
            )

            # Player
            Color(0.1, 0.8, 1, 1)
            Rectangle(
                pos=(self.player_x, self.player_y),
                size=(self.player_size, self.player_size)
            )

            # Player face
            Color(1, 1, 1, 1)
            Ellipse(
                pos=(self.player_x + 12, self.player_y + 30),
                size=(8, 8)
            )

            Ellipse(
                pos=(self.player_x + 35, self.player_y + 30),
                size=(8, 8)
            )

            # Obstacle
            Color(1, 0.25, 0.25, 1)
            Rectangle(
                pos=(self.obstacle_x, self.ground_y),
                size=(self.obstacle_w, self.obstacle_h)
            )

            # Coin
            Color(1, 0.8, 0.05, 1)
            Ellipse(
                pos=(self.coin_x, self.coin_y),
                size=(self.coin_size, self.coin_size)
            )

            # Coin center
            Color(1, 0.95, 0.5, 1)
            Ellipse(
                pos=(self.coin_x + 8, self.coin_y + 8),
                size=(14, 14)
            )

    def reset_game(self):

        self.player_y = self.ground_y
        self.velocity_y = 0

        self.obstacle_x = self.width + 100
        self.coin_x = self.width + 400

        self.score = 0
        self.coins = 0

        self.speed = 7

        self.game_over = False

        self.game_over_label.text = ""

    def jump(self):

        if self.game_over:
            self.reset_game()
            return

        if self.player_y <= self.ground_y + 2:
            self.velocity_y = self.jump_power

    def collision(self):

        player_left = self.player_x
        player_right = self.player_x + self.player_size
        player_bottom = self.player_y
        player_top = self.player_y + self.player_size

        obstacle_left = self.obstacle_x
        obstacle_right = self.obstacle_x + self.obstacle_w
        obstacle_bottom = self.ground_y
        obstacle_top = self.ground_y + self.obstacle_h

        return (
            player_right > obstacle_left
            and player_left < obstacle_right
            and player_top > obstacle_bottom
            and player_bottom < obstacle_top
        )

    def coin_collision(self):

        player_left = self.player_x
        player_right = self.player_x + self.player_size
        player_bottom = self.player_y
        player_top = self.player_y + self.player_size

        coin_left = self.coin_x
        coin_right = self.coin_x + self.coin_size
        coin_bottom = self.coin_y
        coin_top = self.coin_y + self.coin_size

        return (
            player_right > coin_left
            and player_left < coin_right
            and player_top > coin_bottom
            and player_bottom < coin_top
        )

    def update(self, dt):

        if self.width <= 0:
            return

        if not self.game_over:

            # Player physics
            self.velocity_y += self.gravity
            self.player_y += self.velocity_y

            if self.player_y <= self.ground_y:
                self.player_y = self.ground_y
                self.velocity_y = 0

            # Move obstacle
            self.obstacle_x -= self.speed

            if self.obstacle_x < -self.obstacle_w:
                self.obstacle_x = self.width + randint(100, 350)

                self.score += 1

                # Slowly increase difficulty
                if self.speed < 14:
                    self.speed += 0.2

            # Move coin
            self.coin_x -= self.speed

            if self.coin_x < -self.coin_size:
                self.coin_x = self.width + randint(250, 600)
                self.coin_y = randint(160, 300)

            # Coin collected
            if self.coin_collision():
                self.coins += 1
                self.score += 2

                self.coin_x = self.width + randint(300, 650)
                self.coin_y = randint(160, 300)

            # Obstacle collision
            if self.collision():
                self.game_over = True

                self.game_over_label.text = (
                    "GAME OVER\n\n"
                    f"Score: {self.score}\n"
                    f"Coins: {self.coins}\n\n"
                    "Tap to Restart"
                )

            self.score_label.text = f"SCORE: {self.score}"
            self.coin_label.text = f"COINS: {self.coins}"

        self.draw_game()

    def on_touch_down(self, touch):

        self.jump()
        return True


class EliteRunnerApp(App):

    def build(self):

        game = RunnerGame()

        return game


if __name__ == "__main__":
    EliteRunnerApp().run()
  
