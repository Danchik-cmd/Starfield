import pygame
import sys
from random import randint
from math import sin, cos, acos, sqrt
from time import time

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

w = 720
h = 720


class Vector(object):
    def __init__(self, length, angle):
        self.length = length
        self.angle = angle
        self.x = cos(self.angle) * self.length
        self.y = sin(self.angle) * self.length


class Star(object):
    # vector length = point speed
    def __init__(self, x, y, a, size=1, color=WHITE, speed=0):
        self.size = size
        self.color = color
        self.speed = speed
        self.a = a
        self.x = x
        self.y = y

        length = sqrt((w / 2 - x)**2 + (h / 2 - y)**2)
        vecAngl = acos((self.x - w / 2) / length)
        if self.y > h / 2:
            vecAngl = -vecAngl

        self.vec = Vector(self.speed, -vecAngl)

    def move(self):
        self.x += self.vec.x
        self.y += self.vec.y
        self.vec = Vector(self.vec.length + self.a, self.vec.angle)

    def draw(self, scr, oldX, oldY):
        pygame.draw.line(scr, self.color, (int(self.x), int(self.y)), (int(oldX), int(oldY)), self.size)


class Display(object):
    def __init__(self, width, height, count):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((width, height))
        self.caption = "Starfield"
        pygame.display.set_caption(self.caption)
        self.font = pygame.font.Font(None, 36)
        self.status = True
        self.count = count
        self.frame_rate = 120
        self.stars = []
        self.maxA = 0.019
        self.maxL = sqrt((w / 2)**2 + (h / 2)**2)

    def create_stars(self):
        count = self.count - len(self.stars)
        for i in range(count):
            x = randint(0, w)
            y = randint(0, h)
            length = sqrt((w / 2 - x)**2 + (h / 2 - y)**2)
            while length < 30:
                x = randint(0, w)
                y = randint(0, h)
                length = sqrt((w / 2 - x) ** 2 + (h / 2 - y) ** 2)

            L = sqrt((w / 2 - x)**2 + (h / 2 - y)**2)
            a = self.maxA * (self.maxL / L)

            self.stars.append(Star(x, y, a))

    def update(self):
        pygame.display.update()
        self.clock.tick(self.frame_rate)

    def handle_events(self):
        key = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

        if key[pygame.K_UP]:
            self.maxA += 0.003
        if key[pygame.K_DOWN]:
            self.maxA -= 0.003
        if key[pygame.K_RIGHT]:
            self.count += 1
        if key[pygame.K_LEFT]:
            self.count -= 1
        if key[pygame.K_F1]:
            pygame.image.save(self.screen, "Screenshots/starfield_" + str(time()) + '.jpeg')

    def draw(self):
        self.screen.fill(BLACK)
        for star in self.stars:
            oldX = star.x
            oldY = star.y

            star.move()

            if (star.x > w or star.x < 0) or (star.y > h or star.y < 0):
                indx = self.stars.index(star)
                del self.stars[indx]
                self.create_stars()
            else:
                star.draw(self.screen, oldX, oldY)

    def show_info(self):
        if self.maxA < 0:
            speed = str(self.maxA)[0:6]
        else:
            speed = str(self.maxA)[0:5]

        sp = self.font.render('speed: ' + speed, 1, WHITE)
        cnt = self.font.render('count: ' + str(self.count), 1, WHITE)
        self.screen.blit(sp, (10, 10))
        self.screen.blit(cnt, (200, 10))

    def main(self):
        self.create_stars()
        while self.status:
            self.handle_events()
            self.draw()
            self.show_info()
            self.update()


starfield = Display(w, h, 250)


if __name__ == '__main__':
    starfield.main()






