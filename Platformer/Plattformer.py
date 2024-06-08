import arcade.gui, random

class Spiel(arcade.Window):
    def __init__(self):
        super().__init__(2200, 1200, "Platformer")
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.bildschirm = "Menü"
        self.spieler = arcade.Sprite("marioStill.png", 0.5)
        self.spielertexturen = ["marioStill.png", "marioLaufen1.png", "marioLaufen2.png", "marioSpringen1.png", "marioSpringen2.png"]
        self.animation_delta = 0
        self.level = 0
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()
        self.v_box = arcade.gui.UIBoxLayout(space_between=20)
        self.coin_sound = arcade.load_sound("Coin.wav")
        self.win_sound = arcade.load_sound("Win.wav")
        self.lose_sound = arcade.load_sound("Oops.wav")
        self.lose2_sound = arcade.load_sound("troll.wav")
        self.new_item_sound = arcade.load_sound("Unlock_Element.wav")
        #self.all_coins = arcade.load_sound("Bonus.wav")
        self.highscore_beaten = arcade.load_sound("Final_Level.wav")
        self.hurt_sound = arcade.load_sound("Hurt.wav")
        self.troll_face = arcade.Sprite("loser-face.png", 3)
        style1 = {"font_name":"Kenney Blocks","font_size":50,"font_color":arcade.color.BLACK,"border_width":10,"border_color":arcade.color.BLACK,"bg_color":arcade.color.RED,"bg_color_pressed":arcade.color.WHITE,"border_color_pressed":arcade.color.RED,"font_color_pressed":arcade.color.RED}
        style2 = {"font_name":"Kenney Blocks","font_size":50,"font_color":arcade.color.BLACK,"border_width":10,"border_color":arcade.color.BLACK,"bg_color":arcade.color.ORANGE,"bg_color_pressed":arcade.color.WHITE,"border_color_pressed":arcade.color.ORANGE,"font_color_pressed":arcade.color.ORANGE}
        style3 = {"font_name":"Kenney Blocks","font_size":50,"font_color":arcade.color.BLACK,"border_width":10,"border_color":arcade.color.BLACK,"bg_color":arcade.color.YELLOW,"bg_color_pressed":arcade.color.WHITE,"border_color_pressed":arcade.color.YELLOW,"font_color_pressed":arcade.color.YELLOW}
        style4 = {"font_name":"Kenney Blocks","font_size":50,"font_color":arcade.color.BLACK,"border_width":10,"border_color":arcade.color.BLACK,"bg_color":arcade.color.GREEN,"bg_color_pressed":arcade.color.WHITE,"border_color_pressed":arcade.color.GREEN,"font_color_pressed":arcade.color.GREEN}
        style5 = {"font_name":"Kenney Blocks","font_size":50,"font_color":arcade.color.BLACK,"border_width":10,"border_color":arcade.color.BLACK,"bg_color":arcade.color.BLUE,"bg_color_pressed":arcade.color.WHITE,"border_color_pressed":arcade.color.BLUE,"font_color_pressed":arcade.color.BLUE}
        self.level1button = arcade.gui.UIFlatButton(text="Level 1", style=style1, width=400, height=150)
        self.level2button = arcade.gui.UIFlatButton(text="Level 2", style=style2, width=400, height=150)
        self.level3button = arcade.gui.UIFlatButton(text="Level 3", style=style3, width=400, height=150)
        self.level4button = arcade.gui.UIFlatButton(text="Level 4", style=style4, width=400, height=150)
        self.level5button = arcade.gui.UIFlatButton(text="Level 5", style=style5, width=400, height=150)
        self.level1button.on_click = self.level1
        self.level2button.on_click = self.level2
        self.level3button.on_click = self.level3
        self.level4button.on_click = self.level4
        self.level5button.on_click = self.level5
        open_levels = int(open("Level_open.txt", "r").read())
        if open_levels >= 1:
            self.v_box.add(self.level1button)
        if open_levels >= 2:
            self.v_box.add(self.level2button)
        if open_levels >= 3:
            self.v_box.add(self.level3button)
        if open_levels >= 4:
            self.v_box.add(self.level4button)
        if open_levels >= 5:
            self.v_box.add(self.level5button)
        self.ui_manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.v_box))
        self.animation_frame = 0
        self.kamera = arcade.Camera(2200, 1200)
    
    def level1(self, event):
        self.level = 1
        self.setup()
    
    def level2(self, event):
        self.level = 2
        self.setup()

    def level3(self, event):
        self.level = 3
        self.setup()
    
    def level4(self, event):
        self.level = 4
        self.setup()

    def level5(self, event):
        self.level = 5
        self.setup()

    def setup(self):
        self.ui_manager.disable()
        self.tilemap = arcade.load_tilemap(f"Level{self.level}.tmj", 3)
        self.szene = arcade.Scene.from_tilemap(self.tilemap)
        self.szene["Blöcke"].enable_spatial_hashing()
        if self.level <= 2:
            self.physik = arcade.PhysicsEnginePlatformer(self.spieler, self.szene["Bewegte Platformen"], 0.4, self.szene["Wasser"], self.szene["Blöcke"])
        else:
            self.physik = arcade.PhysicsEnginePlatformer(self.spieler, None, 0.4, self.szene["Wasser"], self.szene["Blöcke"])
        self.bewegung = 0
        self.richtung = 0
        if self.level == 2 or self.level == 4:
            self.portale = self.szene["Portale"]
        elif self.level >= 3:
            self.lava = self.szene["Lava"]
        self.teleported = False
        self.physik.enable_multi_jump(2)
        self.zeit = 240
        self.score = 0
        self.health = 3
        self.highscore = open(f"Highscore{self.level}.txt", "r").read()
        self.spieler.center_x = 250
        self.spieler.center_y = 1100
        self.spieler.change_x = 0
        self.spieler.change_y = 0
        self.bildschirm = "Spiel"

    def on_key_press(self, symbol, modifiers):
        if self.bildschirm == "Spiel":
            if symbol == arcade.key.R:
                self.setup()
            elif symbol == arcade.key.UP or symbol == arcade.key.W or symbol == arcade.key.SPACE:
                if self.physik.can_jump():
                    self.spieler.change_y = 10
                    self.bewegung = 3
                    self.physik.increment_jump_counter()
                elif self.physik.is_on_ladder():
                    self.spieler.change_y = 4
            elif symbol == arcade.key.DOWN or symbol == arcade.key.S:
                self.spieler.change_y = -8
            elif symbol == arcade.key.RIGHT or symbol == arcade.key.D:
                self.spieler.change_x = 8
                self.bewegung = 1
                self.richtung = 1
            elif symbol == arcade.key.LEFT or symbol == arcade.key.A:
                self.spieler.change_x = -8
                self.bewegung = 1
                self.richtung = -1
            elif symbol == arcade.key.L:
                self.bildschirm = "Levelauswahl"
        if self.bildschirm == "Menü":
            if symbol == arcade.key.P:
                self.bildschirm = "Levelauswahl"
            elif symbol == arcade.key.H:
                self.bildschirm = "Highscore"
        if self.bildschirm == "Highscore":
            if symbol == arcade.key.Z:
                self.bildschirm = "Menü"
            elif symbol == arcade.key.W:
                open("Highscore1.txt", "w").write("0")
                open("Highscore2.txt", "w").write("0")
                open("Highscore3.txt", "w").write("0")
        if self.bildschirm == "Levelauswahl":
            if symbol == arcade.key.NUM_1:
                self.level = 1
                self.bildschirm = "Spiel"
                self.setup()
            if symbol == arcade.key.NUM_2:
                self.level = 2
                self.bildschirm = "Spiel"
                self.setup()
            if symbol == arcade.key.NUM_3:
                self.level = 3
                self.bildschirm = "Spiel"
                self.setup()
            if symbol == arcade.key.NUM_4:
                self.level = 4
                self.bildschirm = "Spiel"
                self.setup()
            if symbol == arcade.key.NUM_5:
                self.level = 5
                self.bildschirm = "Spiel"
                self.setup()
        if self.bildschirm == "Ziel" or self.bildschirm == "Verloren":
            if symbol == arcade.key.J:
                self.bildschirm = "Levelauswahl"
                self.ui_manager.enable()
            elif symbol == arcade.key.N:
                arcade.exit()
        if symbol == arcade.key.Q:
            arcade.exit()
    
    def on_key_release(self, symbol, modifiers):
        if self.bildschirm == "Spiel":
            if symbol == arcade.key.LEFT or symbol == arcade.key. A or symbol == arcade.key.RIGHT or symbol == arcade.key.D:
                self.spieler.change_x = 0
            self.bewegung = 0
        
    def kamera_zu_spieler(self):
        pos_x = self.spieler.center_x - self.width / 2
        pos_y = self.spieler.center_y - self.height / 2
        if pos_x < 0:
            pos_x = 0
        if pos_y < 0:
            pos_y = 0
        if pos_x > self.tilemap.width*self.tilemap.tile_width*self.tilemap.scaling-self.width:
            pos_x = self.tilemap.width*self.tilemap.tile_width*self.tilemap.scaling-self.width
        if pos_y > self.tilemap.height*self.tilemap.tile_height*self.tilemap.scaling-self.height:
            pos_y = self.tilemap.height*self.tilemap.tile_height*self.tilemap.scaling-self.height
        self.kamera.move_to((pos_x, pos_y))
    
    def on_update(self, delta_time):
        if self.bildschirm == "Spiel":
            self.zeit -= delta_time
            if self.bewegung == 0:
                if self.richtung == 1:
                    self.spieler.texture = arcade.load_texture(self.spielertexturen[0], flipped_horizontally=False)
                elif self.richtung == -1:
                    self.spieler.texture = arcade.load_texture(self.spielertexturen[0], flipped_horizontally=True)
            else:
                self.animation_delta += delta_time
                if self.animation_delta > 0.2:
                    if self.richtung == 1:
                        self.spieler.texture = arcade.load_texture(self.spielertexturen[self.bewegung+self.animation_frame], flipped_horizontally=False)
                    elif self.richtung == -1:
                        self.spieler.texture = arcade.load_texture(self.spielertexturen[self.bewegung+self.animation_frame], flipped_horizontally=True)
                    self.animation_frame = 1 - self.animation_frame
                    self.animation_delta = 0
            self.spieler.update()
            self.physik.update()
            self.kamera.use()
            self.kamera_zu_spieler()
            if self.level <= 2:
                if arcade.check_for_collision_with_list(self.spieler, self.szene["Bewegte Platformen"]) and self.spieler.change_y == 0:
                    self.spieler.center_y += 8
            if self.level == 2 or self.level == 4:
                if arcade.check_for_collision_with_list(self.spieler, self.portale) and not self.teleported:
                    self.spieler.position = self.portale[random.randint(0, len(self.portale)-1)].position
                    self.teleported = True
                if not arcade.check_for_collision_with_list(self.spieler, self.portale):
                    self.teleported = False
            self.szene.update()
            coins = arcade.check_for_collision_with_list(self.spieler, self.szene["Coins"])
            if len(coins) > 0:
                self.score += 1
                arcade.play_sound(self.coin_sound)
                coins[0].kill()
            if arcade.check_for_collision_with_list(self.spieler, self.szene["Ziel"]):
                self.bildschirm = "Ziel"
                self.kamera.move_to((0, 0))
                if self.zeit > float(self.highscore):
                    self.highscore = self.zeit
                    open(f"Highscore{self.level}.txt", "w").write(str(self.highscore))
                    arcade.play_sound(self.highscore_beaten)
                    self.bildschirm = "Ziel"
                    open_levels = int(open("Level_open.txt", "r").read())
                    if open_levels == self.level:
                        open_levels = self.level+1
                        open("Level_open.txt", "w").write(str(open_levels))
                    return
                open_levels = int(open("Level_open.txt", "r").read())
                if open_levels == self.level:
                    open_levels = self.level+1
                    open("Level_open.txt", "w").write(str(open_levels))
                arcade.play_sound(self.win_sound)
                open_levels = int(open("Level_open.txt", "r").read())
                self.ui_manager.remove(self.v_box)
                self.v_box.clear()
                if open_levels >= 1:
                    self.v_box.add(self.level1button)
                if open_levels >= 2:
                    self.v_box.add(self.level2button)
                if open_levels >= 3:
                    self.v_box.add(self.level3button)
                if open_levels >= 4:
                    self.v_box.add(self.level4button)
                if open_levels >= 5:
                    self.v_box.add(self.level5button)
                self.ui_manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.v_box))
            if self.zeit <= 0:
                self.bildschirm = "Verloren"
                arcade.play_sound(self.lose2_sound)
                self.death = "Die Zeit ist abgelaufen."
            if self.level >= 3:
                if arcade.check_for_collision_with_list(self.spieler, self.szene["Lava"]):
                    self.health -= 1
                    arcade.play_sound(self.hurt_sound)
                    self.spieler.change_y = random.randint(6, 12)
                    self.spieler.change_x = random.randint(-10, 10)
                    if self.health == 0:
                        self.bildschirm = "Verloren"
                        arcade.play_sound(self.lose2_sound)
                        self.death = "Du bist verbrannt."
                elif self.spieler.center_y < 0:
                    self.bildschirm = "Verloren"
                    arcade.play_sound(self.lose2_sound)
                    self.death = "Du bist aus der Welt gefallen."
    
    def on_draw(self):
        self.clear()
        if self.bildschirm == "Menü":
            arcade.draw_text("Platformer", 0, 1100, arcade.color.WHITE, 60, self.width, "center", "Kenney Blocks")
            arcade.draw_text("Anleitung:", 0, 1020, arcade.color.BLUE, 40, self.width, "center", "Kenney Blocks")
            arcade.draw_text("Spiele diese Platformer während einer begrenzten Zeit durch.\nSammle dabei so viele Münzen, wie möglich ein.\nMit denen kannst du dann neue Themen freischalten oder neue Skins kaufen.\nDer Diamantblock ist das Ziel! Wenn du ihn erreichst, schaltet sich das nächste Level frei.", 0, 950, arcade.color.BLUE, 30, self.width, "center", "Kenney Blocks")
            arcade.draw_text("Steuerung:", 0, 610, arcade.color.RED, 40, self.width, "center", "Kenney Blocks")
            arcade.draw_text("Bewegung - Pfeiltasten/WASD\nNeustart - R\nBeenden - Q\nSpielen - P\nHighscore - H\nLevelauswahl - L\nAnmelden - A", 0, 540, arcade.color.RED, 30, self.width, "center", "Kenney Blocks")
            arcade.draw_text("Viel Spaß!", 0, 50, arcade.color.BLACK, 60, self.width, "center", "Kenney Blocks")
        elif self.bildschirm == "Highscore":
            self.highscore1_draw = round(240-float(open("Highscore1.txt", "r").read()), 2)
            self.highscore2_draw = round(240-float(open("Highscore2.txt", "r").read()), 2)
            self.highscore3_draw = round(240-float(open("Highscore3.txt", "r").read()), 2)
            arcade.draw_text("W zum Zurücksetzen", 0, 1000, arcade.color.BLACK, 60, self.width, "center", "Kenney Blocks")
            arcade.draw_text(f"Level 1: {self.highscore1_draw} sekunden", 0, 900, arcade.color.BLACK, 60, self.width, "center", "Kenney Blocks")
            arcade.draw_text(f"Level 2: {self.highscore2_draw} sekunden", 0, 800, arcade.color.BLACK, 60, self.width, "center", "Kenney Blocks")
            arcade.draw_text(f"Level 3: {self.highscore3_draw} sekunden", 0, 700, arcade.color.BLACK, 60, self.width, "center", "Kenney Blocks")
        elif self.bildschirm == "Levelauswahl":
            arcade.draw_text("Wähle hier dein Level aus.", 0, 1080, arcade.color.BLACK, 60, self.width, "center", "Kenney Blocks")
            self.ui_manager.draw()
        elif self.bildschirm == "Spiel":
            self.szene.draw()
            self.spieler.draw()
            arcade.draw_text(f"Score: {self.score}", self.kamera.position[0]+10, self.kamera.position[1]+10, arcade.color.BLACK, 20, font_name="Kenney Blocks")
            arcade.draw_text(f"Leben: {self.health}", self.kamera.position[0]+180, self.kamera.position[1]+10, arcade.color.BLACK, 20, font_name="Kenney Blocks")
            arcade.draw_text(f"Zeit: {round(self.zeit, 2)}", self.kamera.position[0]+360, self.kamera.position[1]+10, arcade.color.BLACK, 20, font_name="Kenney Blocks")
        elif self.bildschirm == "Ziel":
            arcade.draw_text("Win", self.kamera.position[0], self.kamera.position[1]+1080, arcade.color.GREEN, 60, self.width, "center", "Kenney Blocks")
            arcade.draw_text(f"Du hast es in {round(240 - self.zeit, 2)} Sekunden geschafft. Nochmal spielen? J = ja, N = nein", self.kamera.position[0], self.kamera.position[1]+500, arcade.color.BLACK, 40, self.width, "center", "Kenney Blocks")
        elif self.bildschirm == "Verloren":
            arcade.draw_text("Lose", self.kamera.position[0], self.kamera.position[1]+1080, arcade.color.RED, 60, self.width, "center", "Kenney Blocks")
            arcade.draw_text(f"{self.death} Nochmal spielen? J = ja, N = nein", self.kamera.position[0], self.kamera.position[1]+500, arcade.color.BLACK, 40, self.width, "center", "Kenney Blocks")
            self.troll_face.set_position(self.kamera.position[0]+self.width/2+random.randint(-2, 2), self.kamera.position[1]+self.height/2+random.randint(-2, 2))
            self.troll_face.draw()

Spiel()
arcade.run()

# TODO:
# Shop
#   Skins
#   Items
#   Textures