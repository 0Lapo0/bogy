from quopri import ESCAPE
from time import time_ns

import pygame as py
import math
import random
import numpy as np
from pygame import Rect, K_ESCAPE
from pygame.sprite import Sprite

game = True
time = 0
py.init()
screen_col = (0, 0, 0)
screen = py.display.set_mode((0, 0), py.FULLSCREEN)
tick = 0
clock = py.time.Clock()
path_st = r"C:\Users\hukel\OneDrive\Desktop\python\Bogi\st.png"
path_ja = r"C:\Users\hukel\OneDrive\Desktop\python\Bogi\ja.png"
path_bull = r"C:\Users\hukel\OneDrive\Desktop\python\Bogi\footagecrate-looping-blaster-bolt-triple-prev-full.png"
path_box = r"C:\Users\hukel\OneDrive\Desktop\python\Bogi\box.png"
l = True
f = []
ma = []
t = 50
s = 10
co = False
stop = False
time_n = 1000
side_rep = []
side_des =[]
fields = []

def sprite_rot(self,img, angle):
    #self.img = py.image.load_extended(img)
    #self.img = py.transform.scale(self.img, (300, 300))
    self.st_rect = self.img.get_rect(center=(self.x, self.y))
   # print(angle)
   # print(self.img)

    self.st_im_rot = py.transform.rotate(self.img, angle)
    self.st_rect_rot = self.st_im_rot.get_rect(center=self.st_rect.center)
    screen.blit(self.st_im_rot, self.st_rect_rot)


        


def angle(v_start, v_ziel):
    a = [0, 1]
   # print(v_start, v_ziel)
    v_direct = v_ziel - v_start
   # print(v_direct)

    if v_start[0] > v_ziel[0]:
        # angle = angle + 180
        a = [0, -1]
        b = 180

    else:
        b=0
    angle = math.acos(np.dot(a, v_direct) / (np.linalg.norm(a) * np.linalg.norm(v_direct)))
   # print("an0: ", angle)
    angle = math.degrees(angle)
   # print("an1: ", angle)
    angle = (angle + 360) % 360 + b
    #print("an: ", angle)
    return angle


def random_point(a, b):

    pu = [random.randint(a[0], a[1]), random.randint(b[0], b[1])]
    return pu


def mouse_pos():
    mouse = py.mouse.get_pos()
    mouse_x = mouse[0]
    mouse_y = mouse[1]
    text = f"mouse: {mouse_x}, {mouse_y}"
    text_m = py.font.SysFont(None, 30)
    tex = text_m.render(text, True, (255,0,0))
    screen.blit(tex, (100, 100))





class java:
    def __init__(self, colour, x, y, speed, life):
        self.colour = colour
        self.x = x
        self.y = y
        self.im = py.image.load(path_ja)
        self.img = py.transform.scale(self.im, (300, 300))
        self.angle = 0
        self.rect = self.img.get_rect(center= (self.x, self.y))
        self.speed = speed
        self.life = life
    def loose(self, l):
        for bull in l:
            if py.Rect.colliderect(self.rect, bull[5]):
                self.life -= 1
                if l.__contains__(bull):
                    l.remove(bull)
                if self.life <= 0:
                    return True


    def draw(self):
        key = py.key.get_pressed()
        if key[py.K_d] and not (key[py.K_s] or key[py.K_w]):
            self.angle = 90
        elif key[py.K_w] and not (key[py.K_d] or key[py.K_a]):
            self.angle = 180
        elif key[py.K_a] and not (key[py.K_s] or key[py.K_w]):
            self.angle = 270
        elif key[py.K_s] and not (key[py.K_d] or key[py.K_a]):
            self.angle = 0
        elif key[py.K_d] and key[py.K_w]:
            self.angle = 135
        elif key[py.K_d] and key[py.K_s]:
            self.angle = 45
        elif key[py.K_a] and key[py.K_w]:
            self.angle = 225
        elif key[py.K_a] and key[py.K_s]:
            self.angle = 315



        #py.draw.rect(screen, self.colour, self.rect)
        sprite_rot(self, path_ja, self.angle)

    def move(self, speed):
        key = py.key.get_pressed()
        if key[py.K_d]:
            self.x += self.speed
        if key[py.K_a]:
            self.x -= self.speed
        if key[py.K_s]:
            self.y += self.speed
        if key[py.K_w]:
            self.y -= self.speed

        self.rect = self.img.get_rect(center= (self.x, self.y))
class bot:
    def __init__(self, colour, x, y, i, death):
        self.colour = colour
        self.x = x
        self.y = y
        self.v = 0
        self.angle = 0
        self.st_im = py.image.load(path_st)
        self.u = 1
        self.l = 1
        self.i = i
        self.t = 0
        self.pu = random_point([0, screen.get_width()], [0, screen.get_height()])
        self.img = py.transform.scale(self.st_im, (300, 300))
        self.rect = self.img.get_rect(center= (self.x, self.y))
        f.append(self)
        self.shots = []
        self.deg = 0
        self.mass = 80
        self.ex = True
        self.death_max = death
        self.death = self.death_max
        self.life = 100
    def draw(self):
        self.v = 5
        self.angle = self.v * math.pi / 180
        #py.draw.rect(screen, self.colour, self.rect)

        #py.draw.circle(screen, self.colour, (self.x + 500, self.y + 500), 10)
    def coll(self, l):
        if self.ex:
            for bull in l:
                print(bull[8])

                if bull[8]:
                    if py.Rect.colliderect(self.rect, bull[5]):
                        l.remove(bull)
                        self.life -= 1
                        if self.life <= 0:
                            self.ex = False
                            print(self)
                            if f.__contains__(self):
                                f.remove(self)
        elif not self.ex:
            self.death -= 1
            if self.death <= 0:
                self.life = 100
                self.ex = True
                self.death = self.death_max
                self.x -= 100
                self.y -= 100
                f.append(self)

    def move(self, player, speed):
        radius = speed
        if self.ex:

            if self.i == 1:
                print(self.l)
                #print(self.v)


                x = self.l * math.cos(self.angle)
                y = self.u * math.sin(self.angle)





                n = math.sqrt(math.pow(x, 2)+math.pow(y, 2))

                x = x/ n * radius
                y = y/ n * radius
                print(self.angle)
                print(x)
                print(y)
                self.x1 = self.x
                self.y1 = self.y
                self.x += x
                self.y += y
                if self.x < 0 or self.x > screen.get_width():
                    self.l *= -1
                    self.x -= x
                    self.y -= y
                    if self.x < 0:
                        self.x = 0.1
                    elif self.x > screen.get_width():
                        self.x = screen.get_width() - 0.1

                if self.y < 0 or self.y > screen.get_height():
                    self.u *= -1
                    self.x -= x
                    self.y -= y
                    if self.y < 0:
                        self.y = 0.1
                    elif self.y > screen.get_height():
                        self.y = screen.get_height() - 0.1

                self.deg = math.asin(x / radius) * 180 / math.pi
                print("d", self.deg)
                sprite_rot(self, path_st, self.deg)
            elif self.i == 2:

                tx = player.x
                ty = player.y
                py.draw.circle(screen, (255,0,255), (tx, ty), 10)

                xl = tx - self.x
                yl = ty - self.y


                vect2 = [xl, yl]


                n = math.sqrt(math.pow(xl, 2)+math.pow(yl, 2))

                x = xl/ n * radius
                y = yl/ n * radius
                self.x += x
                self.y += y
                #self.angle = math.acos(yl / n)
                #print("a: ", self.angle)
                #self.deg = self.angle * 180 / math.pi

                self.deg = angle(np.array([self.x, self.y]), np.array([player.x, player.y]))

                print("d", self.deg)

                sprite_rot(self, path_st, self.deg)
            elif self.i == 3:

                punkte = [[1000, 1500], [500,100], [500, 1500], [1000, 100]]

                v = [punkte[self.t][0] - self.x, punkte[self.t][1] - self.y]

                n = math.sqrt(math.pow(v[0], 2) + math.pow(v[1], 2))

                x = v[0] / n * radius
                y = v[1] / n * radius
                self.x += x
                self.y += y
                if n <= radius:
                    self.t += 1
                    if self.t >= len(punkte):
                        self.t = 0

                self.deg = angle(np.array([self.x, self.y]), np.array(punkte[self.t]))
                print("d", self.deg)
                sprite_rot(self, path_st, self.deg)
            elif self.i == 4:
                v = [self.pu[0] - self.x, self.pu[1] - self.y]

                n = math.sqrt(math.pow(v[0], 2) + math.pow(v[1], 2))

                x = v[0] / n * radius
                y = v[1] / n * radius

                self.pos = [self.x, self.y]

                self.x += x
                self.y += y

                if n <= radius:
                    self.pu = random_point([0, screen.get_width()], [0, screen.get_height()])

                self.deg = angle(np.array(self.pos), np.array([self.x, self.y]))
                print("d", self.deg)
                sprite_rot(self, path_st, self.deg)
            else:
                print('Error self.i is wrong')
            print(f'Self.deg: {self.deg}')
            self.rect = self.img.get_rect(center= (self.x, self.y))





class field:
    def __init__(self, colour, x, y, force, size1, size2, angle, box):
        self.x = x
        self.y = y
        self.force = force
        self.colour = colour
        self.size1 = size1
        self.size2 = size2
        self.angle = angle
        self.rect = Rect(self.x, self.y, self.size1, self.size2)
        self.img = py.image.load(box)
        self.img = py.transform.scale(self.img, (200, 200))
        self.mask = py.mask.from_surface(self.img)
        self.rect = self.img.get_rect(center= (self.x, self.y))
        self.side_rep = []
        self.v = [[max(math.cos(self.angle) * self.size1, 0.000000000000000000000001), max(math.sin(self.angle) * self.size1, 0.00000000000000000001)], [math.cos(self.angle - 90) * self.size2, math.sin(self.angle - 90) * self.size2]]
        self.en = 0
        fields.append(self)


    def draw(self):
       # py.draw.rect(screen, self.colour, self.rect)
        screen.blit(self.img, self.rect)


    def coll(self, player):
        if py.Rect.colliderect(self.rect, player.rect):
            return True


    def move(self, player):

        key = py.key.get_pressed()

        if key[py.K_d]:
            self.x += player.speed
        if key[py.K_a]:
            self.x -= player.speed
        if key[py.K_s]:
            self.y += player.speed
        if key[py.K_w]:
            self.y -= player.speed

        self.rect = self.img.get_rect(center= (self.x, self.y))


    def push(self, t, force, m, stop, k, en):
        radius = 40
        self.stop = stop
        self.en = en
        if self.en > 0:
            self.en -= 1
            for s in t:

                self.force = force
                v = [s.x - ((self.x) + self.size1 / 2), s.y - (self.y + self.size2 / 2)]

                n = math.sqrt(math.pow(v[0], 2) + math.pow(v[1], 2))
                n = max(n, 300)
                h = self.force / (2 * math.pi * n / 4)

                E = 1/2 * h * math.pow(self.force, 2)

                g = math.sqrt(E * 2/s.mass)

                x = v[0] / n * g
                y = v[1] / n * g

                s_pos = [s.x, s.y]

                s.x += x * m
                s.y += y * m

            for bull in k:
                if len(bull[4]) == 0:
                    print(bull[4])
                    return
                self.force = force
                v = [bull[0] - (self.x), bull[1] - (self.y)]

                n = math.sqrt(math.pow(v[0], 2) + math.pow(v[1], 2))
                n = max(n, 300)
                h = self.force / (2 * math.pi * n / 4)

                E = 1/2 * h * math.pow(self.force, 2)

                g = math.sqrt(E * 2/bull[3])

                x = v[0] / n * g * m
                y = v[1] / n * g * m

                #x = bull[4][0] + x
                #y = bull[4][1] + y

                s_pos = [bull[0], bull[1]]

                #bull[4] = [x, y]

                bull[0] += x
                bull[1] += y


                bull[2] = angle(np.array(s_pos), np.array([bull[0], bull[1]]))
                bull[8] = True
                print(bull[8])

               # bull[2] = angle(np.array(bull[4]), np.array([x, y]))

    def rep(self, l):
        for s in l:
            if len(s[4]) == 2:
                if py.Rect.colliderect(s[5], self.rect):
                    coll_point = py.sprite.collide_mask(self, k)
                    s[0] -= s[4][0]
                    s[1] -= s[4][1]
                    s[5] = Rect(s[0], s[1], 20, 20)
                    s[8] = True
                    print("coll: ", coll_point)

                    if s[5].left > self.rect.right - 1 or s[5].right < self.rect.left + 1:
                        a = 180 - s[2] * 2
                        s[2] += 180 + a
                    else:
                        a = s[2] * 2
                        s[2] += 180 - a
            else:
                return



       #for s in k:

       #    t1 = s[4][0] - (s[4][1] * self.v[0][0]) / self.v[0][1]
       #    t2 = self.x - s[0] - self.y * self.v[0][0] / self.v[0][1] + s[1] * self.v[0][0] / self.v[0][1]
       #    n = t1 / t2
       #    if 0 < n < 1:
       #        pass

    def des(self, l, en):
        self.en = en
        for bull in l:
            if py.Rect.colliderect(self.rect, bull[5]):
                self.en += 1
                if l.__contains__(bull):
                    l.remove(bull)















class orb:
    def __init__(self, t, s):
        self.t = t
        self.s = s
        for i in range(5):
            self.pos = [random.randint(0, screen.get_width()), random.randint(0, screen.get_height())]
            ma.append(self.pos)
    def spawn(self, player):
        for i in range(len(ma)):
            py.draw.circle(screen, (255, 255, 255), (ma[i][0], ma[i][1]), 10)
            self.rect = Rect(ma[i][0], ma[i][1], 20, 20)
            if py.Rect.colliderect(self.rect, player.rect):
                ma.pop(i)
                self.pos = [random.randint(0, screen.get_width()), random.randint(0, screen.get_height())]
                ma.append(self.pos)
                self.t += 5
                self.s += 2


class shot:
    def __init__(self, x, y, f, time, time_n, path):
        self.x = x
        self.y = y
        self.bots = f
        self.b = []
        self.time = time
        self.time_n = time_n
        self.shots = []
        self.img = py.image.load(path)
        self.img = py.transform.scale(self.img, (50, 50))
        self.mask = py.mask.from_surface(self.img)
        self.rect = self.img.get_rect()
        for s in self.bots:
            bot = [s.x, s.y, s.deg]
            self.b.append(bot)
    def shoot(self, time, time_n):
        self.bots = f
        self.time = time
        self.time_n = time_n
        self.b.clear()
        radius = 40
        for s in self.bots:
            radius = 40
            bot = [s.x, s.y, s.deg]
            self.b.append(bot)

        if self.time >= self.time_n:
            for s in self.b:
                if self.time >= self.time_n:
                    x = math.cos((-s[2] + 90) * math.pi / 180)
                    y = math.sin((-s[2] + 90) * math.pi / 180)
                    n = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
                    x = x / n * (radius + 100)
                    y = y / n * (radius + 100)
                    s[0] += x
                    s[1] += y

                    rect = Rect(s[0], s[1], 20, 20)
                    shot = [s[0], s[1], s[2], 0.112, [], rect, 1, 1, False, None, None, None]
                    self.shots.append(shot)
        for s in self.shots:
            if -500 < s[0] < screen.get_width() + 500 and -500 < s[1] < screen.get_height() + 500:
                if not math.isnan(s[2]):
                    if s[9] == s[2]:

                        s[0] += s[4][0]
                        s[1] += s[4][1]        

                        s[5] = Rect(s[0], s[1], 20, 20)           

                        self.x = s[0]
                        self.y = s[1]

                        sprite_rot(self, path_bull, s[10] + 270)
                        print(s[8])
                    else:
                        s[9] = s[2]
                        print(f"s2: {s[2]}")
                        x = math.cos((-s[2] + 90) * math.pi / 180)
                        y = math.sin((-s[2] + 90) * math.pi / 180)
                        print(x, y)
                        n = math.sqrt(math.pow(x, 2) + math.pow(y, 2))

                        x = x / n * radius
                        y = y / n * radius

                        s[4] = [x, y]

                        s[10] = angle(np.array([s[0], s[1]]), np.array([s[0] + x, s[1] + y]))
                        print(s[4])
                        s[0] += x
                        s[1] += y
                        s[5] = Rect(s[0], s[1], 20, 20)
                        self.x = s[0]
                        self.y = s[1]

                        sprite_rot(self, path_bull, s[10] + 270)
                        
                        print(s[8])
                elif math.isnan(s[2]):
                    pass
            else:
                self.shots.remove(s)
        text = f"shots: {len(self.shots)}"
        text_m = py.font.SysFont(None, 30)
        tex = text_m.render(text, True, (255, 0, 0))
        screen.blit(tex, (100, 150))
class storage:
    def __init__(self, x, y, width, colour):
        self.pos = [x, y]
        self.width = width
        self.colour = colour
        self.heigth = 0
    def sto(self, en):
        if self.heigth > en:
            if not self.colour[0] == 0:
                self.colour[0] -= 0.25
            if not self.colour[1] == 255:
                self.colour[1] += 0.25
        if self.heigth < en:
            if not self.colour[0] == 255:
                self.colour[0] += 0.25
            if not self.colour[1] == 0:
                self.colour[1] -= 0.25
        self.heigth = en
        
        self.pos[1] = screen.get_height() - en
        self.rect = Rect(self.pos[0], self.pos[1], self.width, self.heigth)
        print(self.colour)
        py.draw.rect(screen, self.colour, self.rect)














s1 = java((255, 0, 0), 1500, 1500, s, 100000)
b1 = bot((255, 255, 0), screen.get_width() - 1000, screen.get_height() - 1000, 1, 1000)
b2 = bot((0, 255, 0), screen.get_width() - 2000, screen.get_height() - 2000, 2, 1000)
b3 = bot((255, 0, 0), 600, 700, 3, 1000)
b4 = bot((255, 0, 0), 600, 700, 4, 1000)
f1 = field((255, 0, 255), screen.get_width() / 2, screen.get_height() / 2, t, 200, 200, 0, path_box)
o = orb(t, s)
f2 = field((255, 0, 0), 2000, 500, t, 200, 200, 0, path_box)
k = shot(0,0, f, time, time_n, path_bull)
f3 = field((255, 0, 255), screen.get_width() / 2 + 500, screen.get_height() / 2 + 500, t, 200, 200, 0, path_box)
f4 = field((255, 0, 255), screen.get_width() / 2 + 1000, screen.get_height() / 2 + 1000, t, 200, 200, 0, path_box)
f5 = field((255, 0, 255), screen.get_width() / 2, screen.get_height() / 3, t, 200, 200, 0, path_box)
f6 = field((255, 0, 255), screen.get_width() / 3, screen.get_height() / 3, t, 200, 200, 0, path_box)
sto = storage(screen.get_width() - 10, screen.get_height(), 30, [0, 255, 0])
en = 0

while game:
    for event in py.event.get():
        if event.type == py.QUIT:
            game = False

    key = py.key.get_pressed()
    time = py.time.get_ticks()
    screen.fill((0, 0, 0))

    f1.draw()
    f2.draw()
    f3.draw()
    f4.draw()
    f5.draw()
    f6.draw()

    b1.draw()
    b1.move(s1, 20)


    b2.draw()
    b2.move(s1, 5)
    b3.draw()
    b3.move(s1, 20)
    b4.draw()
    b4.move(s1, 20)
    b1.coll(k.shots)
    b2.coll(k.shots)
    b3.coll(k.shots)
    b4.coll(k.shots)

    k.shoot(time, time_n)
    if key[py.K_e] and not key[py.K_f]:
        if f1.coll(s1):
            f1.push(f, t, 1, stop, k.shots, en)
            en = f1.en
        if f2.coll(s1):
            f2.push(f, t, -1, stop, k.shots, en)
            en = f2.en
        if f5.coll(s1):
            f5.push(f, t, -1, stop, k.shots, en)
            en = f5.en
    s1.move(s)
    s1.draw()
    tick += 1
    #print(tick)
    o.spawn(s1)
    t = o.t
    s = o.s
    mouse_pos()
    f3.rep(k.shots)
    f4.rep(k.shots)
    if time >= time_n:
        time_n += 1
    if key[py.K_f]:
        if f1.coll(s1):
            f1.move(s1)
        if f2.coll(s1):
            f2.move(s1)
        if f3.coll(s1):
            f3.move(s1)
        if f4.coll(s1):
            f4.move(s1)
        if f5.coll(s1):
            f5.move(s1)
        if f6.coll(s1):
            f6.move(s1)

    f6.des(k.shots, en)
    en = f6.en
    sto.sto(en)
    if s1.loose(k.shots):
        game = False

#    print("there: ", b1.ex, b2.ex, b3.ex, b4.ex)
    clock.tick(120)
    py.display.update()