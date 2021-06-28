import pygame
import math
import time

HEIGHT = 1000
WIDTH = int(1.5 * HEIGHT)
LEVY_C_INSERT = [1, 0, -1, -1, 0, 1]


class LevyC:
    def __init__(self, iter=7):
        self.instructions = [0]
        self.instructions = self.fractal_array(iter)
        self.length = HEIGHT / (2 * math.pow(2, iter/2))
        self.starting_point = (WIDTH / 3.0, HEIGHT / 3.0)
        self.next_point = self.starting_point
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.angle = 0.0
        pygame.display.set_caption('Levy C')

    def fractal_array(self, x):
        if x == 0:
            return self.instructions
        output = []
        for i in self.instructions:
            if i == 0:
                output.extend(LEVY_C_INSERT)
            else:
                output.append(i)
        self.instructions.clear()
        self.instructions = output
        return self.fractal_array(x - 1)

    def draw(self, color_values=((0, HEIGHT), (200, 0), (200, 0), (0, 255))):
        reference_point, red_values, green_values, blue_values = color_values
        for i in self.instructions:
            if i != 0:
                self.angle += (float(i) * math.pi) / 4.0
            else:
                sx, sy = self.next_point
                nx = sx + (self.length * math.cos(self.angle))
                ny = sy + (self.length * math.sin(self.angle))
                self.next_point = (nx, ny)

                rpx, rpy = reference_point  # (WIDTH / 2, HEIGHT / 2)
                rrange, rmin = red_values  # (0, 100)
                grange, gmin = green_values  # (100, 0)
                brange, bmin = blue_values  # (100, 100)
                if sx != rpx:
                    cartesian_angle = math.atan(
                        math.fabs((rpy - sy)/(rpx - sx)))
                    relative_x = math.cos(cartesian_angle)
                    relative_y = math.sin(cartesian_angle)
                    i_relative_y = math.sin(
                        math.atan(math.fabs(((HEIGHT - rpy) - sy)/(rpx - sx))))
                    i_relative_x = math.cos(
                        math.atan(math.fabs((rpy - sy) / ((WIDTH - rpx) - sx))))
                    red = ((rrange * relative_x) + rmin)
                    green = (grange * i_relative_x) + gmin
                    blue = (brange * relative_x) + bmin
                # If you use the relative_y value replace the variable with a 1 and replace relative_x with a 0
                else:
                    red = (rmin)
                    green = gmin
                    blue = (bmin)
                pygame.draw.line(
                    self.window, (red, green, blue), (sx, sy), self.next_point, 1)
        self.next_point = self.starting_point

    def run(self):
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            pygame.time.delay(5)
            color_value = ((WIDTH / 2, HEIGHT / 2),
                           (200, 0), (200, 0), (0, 255))
            self.draw(color_value)
            pygame.display.update()


x = int(input("How Many Iterations (Recommended 15 or less):\n"))
levy = LevyC(x)
levy.run()
