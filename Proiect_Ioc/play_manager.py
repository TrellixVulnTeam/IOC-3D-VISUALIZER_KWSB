import math

import numpy as np
import matplotlib.pyplot as plt
from pynput.mouse import Button, Controller
import matplotlib.animation as ani


class PlayManager:
    def __init__(self):
        self.x_axis_values = [i for i in range(50)]
        self.buffer_x_axis_values = [i for i in range(100)]
        self.y_axis_values = []
        self.mouse = Controller()
        self.screen_width = 1920
        self.screen_height = 1080
        self.animator = None

        self.arg = [i / 25 for i in range(50)]
        self.y2_axis_values = [5 * math.sin(2 * math.pi * (self.arg[i] + 0.1)) for i in range(50)]

        self.buffer = [100 for i in range(100)]
        self.stop = False

    def play(self):
        self.buffer = [100 for i in range(100)]
        self.stop = False
        fig = plt.figure()
        self.y_axis_values = [0 for i in range(50)]
        self.animator = ani.FuncAnimation(fig, self.refresh, interval=150, repeat=True)
        plt.show()

    def refresh(self, x):
        self.y_axis_values = self.y_axis_values[1:] + self.y_axis_values[:1]
        self.y_axis_values[-1] = ((self.screen_height - self.mouse.position[1]) / self.screen_height - 0.5) * 20
        self.y2_axis_values = self.y2_axis_values[1:] + self.y2_axis_values[:1]

        self.buffer = self.buffer[1:] + self.buffer[:1]
        self.buffer[-1] = (self.y2_axis_values[-1] - self.y_axis_values[-1]) ** 2

        avg_err = sum(self.buffer) / len(self.buffer)

        if avg_err < 4:
            self.stop = True
            self.animator = None
            plt.close()

        if not self.stop:
            plt.subplot(211)
            plt.cla()
            plt.plot(self.x_axis_values, self.y_axis_values)
            plt.plot(self.x_axis_values, self.y2_axis_values)
            plt.title('Err ' + str(avg_err))

            plt.subplot(212)
            plt.cla()
            plt.plot(self.buffer_x_axis_values, self.buffer)
