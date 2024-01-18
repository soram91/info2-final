import pyxel

class Player:
    def __init__(self, field_width, field_height):  #初期位置
        self.field_width = field_width
        self.px = field_width / 2
        self.py = field_height - 12
        self.p_height = 12
        self.p_width = 30
        self.move_speed = 5

    def pmove(self):
        self.px = pyxel.mouse_x
        if self.px < 0:
            self.px = 0
        if self.px > self.field_width:
            self.px = self.field_width

class Bullet:
    def __init__(self, player_x, field_height):
        self.b_size = 8
        self.b_speed = 7
        self.bx = player_x - self.b_size/2
        self.by = field_height - 10

    def bmove(self):
        self.by -= self.b_speed

class Enemy:
    def __init__(self, field_width):
        self.field_width = field_width
        self.enemy_position_reset()
        
    def enemy_position_reset(self):
        self.ey = pyxel.rndi(0, 10)
        self.e_size = 10
        self.e_speed = 2
        self.ex = pyxel.rndi(-10, self.field_width- self.e_size)

    def restart(self, field_width):
        self.ey = 0
        self.ex = pyxel.rndi(0, field_width)

    def emove(self):
        self.ey += self.e_speed
        
class Cloud:
    def __init__(self, field_width, x, y):
        self.c_speed = 1
        self.cx = x
        self.cy = y
        self.field_width = field_width
        self.field_height = self.field_width * 2

    def cloud_reset(self):
        self.cy = 0

    def cmove(self):
        self.cy += self.c_speed
        if self.cy > self.field_height:
            self.cloud_reset()

class Bird:
    def __init__(self, field_width):
        self.field_width = field_width
        self.field_height = self.field_width * 2
        self.bireset()
        
    def bireset(self):
        self.bispeed = 3
        self.bix = self.field_width + 30
        self.biy = pyxel.rndi(0, int(2*self.field_height/3))

    def bimove(self):
        self.bix -= self.bispeed
        self.biy += self.bispeed/2
        if self.bix <= -10:
            self.bireset()
    
    def bidraw(self):
        pyxel.rect(self.bix, self.biy, 1, 1, 0)
        pyxel.rect(self.bix+1, self.biy-1, 1, 1, 0)
        pyxel.rect(self.bix+2, self.biy-2, 1, 1, 0)
        pyxel.rect(self.bix+3, self.biy-2, 1, 1, 0)
        pyxel.rect(self.bix+4, self.biy-2, 1, 1, 0)
        pyxel.rect(self.bix+5, self.biy-1, 1, 1, 0)
        pyxel.rect(self.bix+6, self.biy, 1, 1, 0)
        pyxel.rect(self.bix+7, self.biy+1, 1, 1, 0)
        pyxel.rect(self.bix+8, self.biy, 1, 1, 0)
        pyxel.rect(self.bix+9, self.biy-1, 1, 1, 0)
        pyxel.rect(self.bix+10, self.biy-2, 1, 1, 0)
        pyxel.rect(self.bix+11, self.biy-2, 1, 1, 0)
        pyxel.rect(self.bix+12, self.biy-2, 1, 1, 0)
        pyxel.rect(self.bix+13, self.biy-1, 1, 1, 0)
        pyxel.rect(self.bix+14, self.biy, 1, 1, 0)


#画面切り替え
SCENE_TITLE = 0 #title
SCENE_PLAY = 1  #
SCENE_GAMEOVER = 2  #gameover

class App:
    def __init__(self):
        self.field_width = 150
        self.field_height = self.field_width * 2
        pyxel.init(self.field_width, self.field_height, title="Balloon Pops")
        self.score = 0
        self.life = 5
        self.alive = True
        self.bullet = []
        self.player = Player(self.field_width, self.field_height)
        self.max_bullets = 3
        self.enemy = [Enemy(self.field_width) for _ in range(4)]
        self.scene = SCENE_TITLE    #画面切り替えの初期化
        self.cloud = []
        self.bird = Bird(self.field_width)

        """for a in range(2):"""
        for b in range (0, 40, 10):
            self.cloud.append(Cloud(self.field_width, b, 0))
        for c in range (0, 50 , 10):
            self.cloud.append(Cloud(self.field_width, c-5, 10))

        for b in range (0, 50, 10):
            self.cloud.append(Cloud(self.field_width, self.field_width-b, self.field_height/2))
        for c in range (0, 40 , 10):
            self.cloud.append(Cloud(self.field_width, self.field_width-c-5, self.field_height/2+10))

        pyxel.run(self.update, self.draw)

    def hit(self):  #BulletとEnemyが当たる時    #当たる: Bullet(x,y) = Enemy  (x,y)
        for a in self.bullet:
            for n in self.enemy:
                if n.ey < a.by and a.by < n.ey + n.e_size and n.ex - n.e_size * 2 < a.bx and a.bx < n.ex + n.e_size:
                    self.score += 1 #bulletとenemyが当たった+1
                    n.restart(self.field_width) #bulletを再び出せるようにする

        for n in self.enemy:
            if n.ey > self.field_height:
                n.restart(self.field_width)
                self.life -= 1

    def bulletnum(self):    #Bulletの増減
        if pyxel.btnp(pyxel.KEY_SPACE) and len(self.bullet) < self.max_bullets:
            self.bullet.append(Bullet(self.player.px, self.field_height))
        for n in self.bullet:
            if n.by < 0:
                self.bullet.remove(n)

    def update(self):    
        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover_scene()

    def draw_game_over(self):
        pyxel.text(self.field_width // 2 - 20, self.field_height // 2 - 4, "Game Over", 8)

    def update_play_scene(self): #game in play
        self.bulletnum()
        self.player.pmove()
        self.bird.bimove()
        for c in self.cloud:
            c.cmove()

        for a in self.bullet:
            a.bmove()

        for n in self.enemy:
            n.emove()

        self.hit()
        if self.life <= 0:
            self.alive = False
            self.scene = SCENE_GAMEOVER

    def update_gameover_scene(self):    #gameover
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.score = 0
            self.scene = SCENE_TITLE
    
    def update_title_scene(self):    #title
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.score = 0
            self.life = 5
            for e in self.enemy:
                e.enemy_position_reset()
            self.scene = SCENE_PLAY


    def draw(self):
        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover_scene()

        pyxel.rect(self.player.px - self.player.p_width / 2, self.player.py, self.player.p_width, self.player.p_height, 14)

    def draw_play_scene(self):
        pyxel.cls(pyxel.COLOR_LIGHT_BLUE)
        self.bird.bidraw()
        for a in self.bullet:
            pyxel.rect(a.bx, a.by, a.b_size, a.b_size, 8)

        for n in self.enemy:
            pyxel.circ(int(n.ex), int(n.ey), n.e_size, 9)

        for d in self.cloud:
            pyxel.circ(d.cx, d.cy, 8, pyxel.COLOR_WHITE)

        pyxel.text(5, 5, f"Score: {self.score}", 7)
        pyxel.text(6, 6, f"Score: {self.score}", 0)
        pyxel.text(5, 15, f"Life: {self.life}", 7)
        pyxel.text(6, 16, f"Life: {self.life}", 0)

    def draw_title_scene(self):
        pyxel.cls(pyxel.COLOR_LIGHT_BLUE)
        for d in self.cloud:
            pyxel.circ(d.cx, d.cy, 8, pyxel.COLOR_WHITE)
        pyxel.text(45, 55, "BALLOON POPS!", 7)
        pyxel.text(46, 56, "BALLOON POPS!", 0)
        pyxel.text(30, 85, "- PRESS SPACE TO PLAY -", 7)
        pyxel.text(31, 86, "- PRESS SPACE TO PLAY -", 0)


    def draw_gameover_scene(self):
        pyxel.cls(pyxel.COLOR_LIGHT_BLUE)
        for d in self.cloud:
            pyxel.circ(d.cx, d.cy, 8, pyxel.COLOR_WHITE)
        pyxel.text(5, 5, f"Score: {self.score}", 7)
        pyxel.text(6, 6, f"Score: {self.score}", 0)
        pyxel.text(55, 40, "GAME OVER", 7)
        pyxel.text(56, 41, "GAME OVER", 0)
        pyxel.text(45, 80, "- PRESS SPACE -", 7)
        pyxel.text(46, 81, "- PRESS SPACE -", 0)

app = App()
