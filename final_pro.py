import pyxel

class Player:
    def __init__(self, field_width, field_height):  #Playerの初期化   
        self.field_width = field_width
        self.px = field_width / 2    #px, py: 初期位置
        self.py = field_height - 12
        self.p_height = 12
        self.p_width = 30
        self.move_speed = 5

    def pmove(self):    #移動を行うメソッド
        self.px = pyxel.mouse_x
        if self.px < 0:
            self.px = 0
        if self.px > self.field_width:
            self.px = self.field_width
        #playerが画面外に出ないようにする    #x座標を0~field_widthまでに限定

class Bullet:
    def __init__(self, player_x, field_height):
        self.b_size = 8
        self.b_speed = 7
        self.bx = player_x - self.b_size/2    #bx, by=弾の初期位置
        self.by = field_height - 10

    def bmove(self):    #弾の移動
        self.by -= self.b_speed

class Enemy:
    def __init__(self, field_width):
        self.field_width = field_width
        self.enemy_position_reset()
        #enemy_position_resetメソッドを呼び出して敵の初期位置をリセット
        
    def enemy_position_reset(self):    #敵の位置をリセット    #初期化時に呼び出される
        self.ey = pyxel.rndi(0, 10)
        self.e_size = 10
        self.e_speed = 2
        self.ex = pyxel.rndi(-10, self.field_width- self.e_size)

    def restart(self, field_width):    #敵の位置を再設定    #画面外に移動した場合などに呼び出される
        self.ey = 0    #ey座標を0にリセット
        self.ex = pyxel.rndi(0, field_width)    #exをランダム座標に

    def emove(self):
        self.ey += self.e_speed    #ey座標をe_speed分増加    #敵を画面下方向に移動
        
class Cloud:
    def __init__(self, field_width, x, y):    #新しい雲の初期化
        self.c_speed = 1
        self.cx = x
        self.cy = y
        self.field_width = field_width
        self.field_height = self.field_width * 2
        #cloudオブジェクトの初期化

    def cloud_reset(self):    #雲の位置をリセット
        self.cy = 0    #cy=0にリセット

    def cmove(self):    #雲の移動をい行う
        self.cy += self.c_speed       #cyをc_speed分増加    #画面下方向に移動
        if self.cy > self.field_height:
            self.cloud_reset()
        #雲が画面の下を超えたらcloud_resetメソッドを呼び出して雲の位置をリセット（上から出てくるようにする）

class Bird:
    def __init__(self, field_width):
        self.field_width = field_width
        self.field_height = self.field_width * 2
        self.bireset()
        #field_width, field_heightを初期化、biresetを呼び出して初期位置をリセット
        
    def bireset(self):    #鳥の位置をリセット
        self.bispeed = 3
        self.bix = self.field_width + 30
        self.biy = pyxel.rndi(0, int(2*self.field_height/3))
        #bispeed, bix, biyを初期化    #鳥の初期位置x:右端から30離れたところ, y:ランダム

    def bimove(self):    #鳥の移動を行う
        self.bix -= self.bispeed
        self.biy += self.bispeed/2
        #鳥を左にbispeed分、下にbispeed/2分移動
        if self.bix <= -10:
            self.bireset()
        #鳥が左端を超えたらbiresetを呼び出して鳥の位置を再設定
    
    def bidraw(self):    #鳥を描画
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
SCENE_PLAY = 1  #playscene
SCENE_GAMEOVER = 2  #gameover

class App:
    def __init__(self):
        self.field_width = 150
        self.field_height = self.field_width * 2
        pyxel.init(self.field_width, self.field_height, title="Balloon Pops")    #pyxelの初期化
        self.score = 0
        self.life = 5
        self.alive = True
        self.bullet = []    #弾のリストを初期化
        self.player = Player(self.field_width, self.field_height)    #Playerクラスのインスタンスを作ってself.playerに入れる
        self.max_bullets = 3
        self.enemy = [Enemy(self.field_width) for _ in range(4)]    #Enemyクラスのインスタンス4つ    #self.enemyリストに入れる
        self.scene = SCENE_TITLE    #画面切り替えの初期化
        self.cloud = []    #雲のリストを初期化
        self.bird = Bird(self.field_width)    #Birdクラスのインスタンスを初期化

        """for a in range(2):"""
        for b in range (0, 40, 10):
            self.cloud.append(Cloud(self.field_width, b, 0))
        #雲のリストに上配置の雲を追加
        for c in range (0, 50 , 10):
            self.cloud.append(Cloud(self.field_width, c-5, 10))
        #上2番目配置の雲を追加
        for b in range (0, 50, 10):
            self.cloud.append(Cloud(self.field_width, self.field_width-b, self.field_height/2))
        #下は一の雲を追加
        for c in range (0, 40 , 10):
            self.cloud.append(Cloud(self.field_width, self.field_width-c-5, self.field_height/2+10))
        #下2番目配置の雲を追加
        pyxel.run(self.update, self.draw)

    def hit(self):  #BulletとEnemyが当たる時    #当たる: Bullet(x,y) = Enemy  (x,y)
        for a in self.bullet:
            for n in self.enemy:
                if n.ey < a.by and a.by < n.ey + n.e_size and n.ex - n.e_size * 2 < a.bx and a.bx < n.ex + n.e_size:
                    self.score += 1 #bulletとenemyが当たった+1
                    n.restart(self.field_width) #bulletを再び出せるようにする
        #a,nを比較    #当たり判定が成立する時は得点を増やして敵の位置をリセット

        for n in self.enemy:
            if n.ey > self.field_height:
                n.restart(self.field_width)
                self.life -= 1
        #敵が画面下に達した時、敵を再配置してライフを減らす

    def bulletnum(self):    #Bulletの増減
        if pyxel.btnp(pyxel.KEY_SPACE) and len(self.bullet) < self.max_bullets:
            self.bullet.append(Bullet(self.player.px, self.field_height))
        #スペースキーが押された時の条件を満たすBulletを生成してself.bulletのリストに追加
        for n in self.bullet:
            if n.by < 0:
                self.bullet.remove(n)
        #弾が画面上部を超えたらその球をself.bulletリストから消す

    def update(self):    
        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover_scene()
        #self.sceneに合わせて対応するシーンの更新処理を呼び出す

    def draw_game_over(self):    #画面中央にゲームオーバーを表示    #gameover画面
        pyxel.text(self.field_width // 2 - 20, self.field_height // 2 - 4, "Game Over", 8)

    def update_play_scene(self): #game in play
        self.bulletnum()    #弾の発射・存在条件の管理
        self.player.pmove()    #プレイヤーの移動
        self.bird.bimove()    #鳥の移動
        for c in self.cloud:
            c.cmove()    #雲の移動
        #各オブジェクトの移動や増減を行うメソッドを呼び出す

        for a in self.bullet:
            a.bmove()
        for n in self.enemy:
            n.emove()
        #self.bullet, self.enemyの移動をそれぞれのクラスのメソッドを呼び出して行う

        self.hit()    #hitメソッドを呼び出す    #弾と敵の当たり判定・点の更新
        if self.life <= 0:
            self.alive = False
            self.scene = SCENE_GAMEOVER
        #ライフが０になったらself.alive=Falseにしてgameover画面に変更

    def update_gameover_scene(self):    #gameover
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.score = 0
            self.scene = SCENE_TITLE
        #スペースキーが押されると得点をリセットしてscene titleにする
    
    def update_title_scene(self):    #title画面の更新
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.score = 0
            self.life = 5
            for e in self.enemy:
                e.enemy_position_reset()
            self.scene = SCENE_PLAY
        #スペースキーが押されると得点をリセットしライフを5に戻し、敵の位置をリセットしてからscene playに画面を変える


    def draw(self):    #画面の描画処理
        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover_scene()
        #ゲームのシーンself.sceneに応じて対応する描画メソッドの呼び出しをする

        pyxel.rect(self.player.px - self.player.p_width / 2, self.player.py, self.player.p_width, self.player.p_height, 14)
        #プレイヤーの位置にrectを描画
    
    def draw_play_scene(self):    #プレイ画面の描画処理
        pyxel.cls(pyxel.COLOR_LIGHT_BLUE)    #画面全体の色
        self.bird.bidraw()    #鳥の描画を行うbidrawメソッドの呼び出し
        for a in self.bullet:
            pyxel.rect(a.bx, a.by, a.b_size, a.b_size, 8)
        #self.bulletの位置に対応するrectを描く
        for n in self.enemy:
            pyxel.circ(int(n.ex), int(n.ey), n.e_size, 9)
        #self.enemyの位置に対応するcircを描く
        for d in self.cloud:
            pyxel.circ(d.cx, d.cy, 8, pyxel.COLOR_WHITE)
        #self.cloudの位置に対応するcircを描く

        pyxel.text(5, 5, f"Score: {self.score}", 7)
        pyxel.text(6, 6, f"Score: {self.score}", 0)
        pyxel.text(5, 15, f"Life: {self.life}", 7)
        pyxel.text(6, 16, f"Life: {self.life}", 0)
        #点数とライフの表示

    def draw_title_scene(self):    #タイトル画面の描画処理
        pyxel.cls(pyxel.COLOR_LIGHT_BLUE)    #画面全体の色
        for d in self.cloud:
            pyxel.circ(d.cx, d.cy, 8, pyxel.COLOR_WHITE)
        #self.cloudの位置に対応するcircを描く
        pyxel.text(45, 55, "BALLOON POPS!", 7)
        pyxel.text(46, 56, "BALLOON POPS!", 0)
        #BALLOON POPS!を表示
        pyxel.text(30, 85, "- PRESS SPACE TO PLAY -", 7)
        pyxel.text(31, 86, "- PRESS SPACE TO PLAY -", 0)
        #PRESS SPACE TO PLAYを表示

    def draw_gameover_scene(self):    #gameover画面の描画処理
        pyxel.cls(pyxel.COLOR_LIGHT_BLUE)    #画面全体の色
        for d in self.cloud:
            pyxel.circ(d.cx, d.cy, 8, pyxel.COLOR_WHITE)
        #self.cloudの位置に対応するcircを描く
        pyxel.text(5, 5, f"Score: {self.score}", 7)
        pyxel.text(6, 6, f"Score: {self.score}", 0)
        #点数の表示
        pyxel.text(55, 40, "GAME OVER", 7)
        pyxel.text(56, 41, "GAME OVER", 0)
        #GAME OVERの表示
        pyxel.text(45, 80, "- PRESS SPACE -", 7)
        pyxel.text(46, 81, "- PRESS SPACE -", 0)
        #- PRESS SPACE -の表示

app = App()
