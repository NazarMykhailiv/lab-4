import random
import tkinter as tk
from enum import Enum

from settings import *


class ActionType(Enum):

    STRIKE = 1
    RICOCHET = 2


class Ball:

    radius = BALL_RADIUS

    speed = BALL_SPEED
    x_speed = speed
    y_speed = speed

    color = BALL_COLOR

    def __init__(
            self,
            canvas,
            x,
            y,
            firs_pad,
            second_pad,
            score
    ):
        self.canvas = canvas
        self.x = x
        self.y = y

        self.first_pad = firs_pad
        self.second_pad = second_pad

        self.score = score

        self.ball = self.canvas.create_oval(
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius,
            fill=self.color
        )

    def spawn(self):
        self.canvas.coords(
            self.ball, WIDTH / 2 - self.radius,
            HEIGHT / 2 - self.radius,
            WIDTH / 2 + self.radius,
            HEIGHT / 2 + self.radius
        )

    def bouncing(self, action: ActionType):
        if action == ActionType.STRIKE:
            self.y_speed = random.randrange(-10, 10)
            self.x_speed = -self.x_speed
        else:
            self.y_speed = -self.y_speed


class Pad:

    width = PAD_WIDTH
    height = PAD_HEIGHT

    speed = PAD_SPEED

    color = PAD_COLOR

    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y

        self.pad = self.canvas.create_line(
            self.x + self.width // 2,
            self.y,
            self.x + self.width // 2,
            self.y + self.height,
            width=self.width,
            fill=self.color
        )

    def move_up(self):
        if self.canvas.coords(self.pad)[1] > 0:
            self.canvas.move(self.pad, 0, -self.speed)

    def move_down(self):
        if self.canvas.coords(self.pad)[3] < HEIGHT:
            self.canvas.move(self.pad, 0, self.speed)


class Game(tk.Tk):

    score = [0, 0]

    def __init__(self):
        super().__init__()

        self.geometry('{}x{}'.format(WIDTH, HEIGHT))
        self.title('Ping Pong')

        self.canvas = tk.Canvas(self, width=WIDTH, height=HEIGHT, background=BACKGROUND_COLOR)
        self.canvas.pack()

        self.score_text = self.canvas.create_text(
            WIDTH - WIDTH / 2,
            25,
            text='{}\t{}'.format(*self.score),
            font='Arial 20',
            fill='white')

        self.first_pad = Pad(self.canvas, 0, 0)
        self.second_pad = Pad(self.canvas, WIDTH - Pad.width, 0)

        self.ball = Ball(
            self.canvas,
            WIDTH // 2,
            HEIGHT // 2,
            self.first_pad,
            self.second_pad,
            self.score
        )

        self.bind('<KeyPress>', self.pad_keybord_controller)

        self.start()

    def start(self):
        self.move()

    def pad_keybord_controller(self, event):
        if event.keysym == 'w':
            self.first_pad.move_up()
        if event.keysym == 's':
            self.first_pad.move_down()
        if event.keysym == 'Up':
            self.second_pad.move_up()
        if event.keysym == 'Down':
            self.second_pad.move_down()

    def pad_stop_controller(self, event):
        if event.keysym in ('w', 's'):
            self.first_pad.speed = [0, 0]
        if event.keysym in ('Up', 'Down'):
            self.second_pad.speed = [0, 0]

    def move(self):
        self.ball_update()
        self.after(30, self.move)

    def ball_update(self):
        ball_left, ball_top, ball_right, ball_bot = self.canvas.coords(self.ball.ball)
        ball_center = (ball_top + ball_bot) / 2

        if ball_right + self.ball.x_speed < WIDTH - Pad.width and \
                ball_left + self.ball.x_speed > Pad.width:
            self.canvas.move(self.ball.ball, self.ball.x_speed, self.ball.y_speed)

        elif ball_right == WIDTH - Pad.width or ball_left == Pad.width:
            if ball_right > WIDTH / 2:
                if self.canvas.coords(self.second_pad.pad)[1] < ball_center < self.canvas.coords(self.second_pad.pad)[3]:
                    self.ball.bouncing(ActionType.STRIKE)
                else:
                    self.score[0] += 1
                    self.score_update()
                    self.ball.spawn()
            else:
                if self.canvas.coords(self.first_pad.pad)[1] < ball_center < self.canvas.coords(self.first_pad.pad)[3]:
                    self.ball.bouncing(ActionType.STRIKE)
                else:
                    self.score[1] += 1
                    self.score_update()
                    self.ball.spawn()
        else:
            if ball_right > WIDTH / 2:
                self.canvas.move(self.ball.ball, WIDTH - Pad.width - ball_right, self.ball.y_speed)
            else:
                self.canvas.move(self.ball.ball, -ball_left + Pad.width, self.ball.y_speed)

        if ball_top + self.ball.y_speed < 0 or ball_bot + self.ball.y_speed > HEIGHT:
            self.ball.bouncing(ActionType.RICOCHET)

    def score_update(self):
        self.canvas.itemconfig(self.score_text, text='{}\t{}'.format(*self.score))


app = Game()
app.mainloop()

