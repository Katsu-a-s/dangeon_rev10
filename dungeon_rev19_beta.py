import pygame
import sys 
import random
from pygame.locals import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
BLINK = [(224, 255, 255), (192, 240, 255), (128, 224, 255), (64, 192, 255), (128, 224, 255), (192, 240, 255)]

imgTitle = pygame.image.load("image/title2.jpg")
imgWall = pygame.image.load("image/wall.png")
imgWall2 = pygame.image.load("image/wall2.png")
imgDark = pygame.image.load("image/dark.png")
imgPara = pygame.image.load("image/parameter.png")
imgPara2 = pygame.image.load("image/parameter2.png")
imgBtlBG = pygame.image.load("image/btlbg.png")
imgEnemy = pygame.image.load("image/enemy0.png")
imgItem = [pygame.image.load("image/potion.png"),
           pygame.image.load("image/blaze_gem.png"),
           pygame.image.load("image/spoiled.png"),
           pygame.image.load("image/apple.png"),
           pygame.image.load("image/meat.png"),
           pygame.image.load("image/sord.png"),
           pygame.image.load("image/shield.png")]
imgDamage = pygame.image.load("image/Damage.png")
imgFloor = [pygame.image.load("image/floor.png"),
            pygame.image.load("image/tbox.png"),
            pygame.image.load("image/cocoon.png"),
            pygame.image.load("image/stairs.png"),
            pygame.image.load("image/floor_trap.png")]
imgPlayer = [pygame.image.load("image/mychr0.png"),
             pygame.image.load("image/mychr1.png"),
             pygame.image.load("image/mychr2.png"),
             pygame.image.load("image/mychr3.png"),
             pygame.image.load("image/mychr4.png"),
             pygame.image.load("image/mychr5.png"),
             pygame.image.load("image/mychr6.png"),
             pygame.image.load("image/mychr7.png"),
             pygame.image.load("image/mychr8.png")]

imgEffect = [pygame.image.load("image/effect_a.png"),
             pygame.image.load("image/effect_b.png")]

speed = 1
idx = 0
tmr = 0
floor = 0
fl_max = 1
welcome = 0

#追加
moving = False
move_dx = 0
move_dy = 0
move_progress = 0.0
base_move_speed = 0.25
MOVE_SPEED = base_move_speed

hold_dir = None
hold_timer = 0.0
hold_delay = 12
hold_interval = 4

pl_x = 0
pl_y = 0
pl_d = 0
pl_a = 0
pl_lifemax = 0
pl_life = 0
pl_str = 0
pl_lv = 1
food = 0
potion = 0
blazegem = 0
treasure = 0
pl_def_base = 0
pl_def_buff = 0
def_pill = 0
flg_action = False

emy_name=""
emy_lifemax = 0
emy_life = 0
emy_str = 0
emy_x = 0
emy_y = 0
emy_step = 0
emy_blink = 0
typ = 0

dmg_eff = 0
btl_cmd = 0

COMMAND = ["[A]ttack", "[P]otion","[B]laze gem","[R]un", "[D]efense"]
TRE_NAME = ["Potion", "Blaze gem", "Food spoiled.", "Food + 20", "Food + 100", "Sord", "Defense Pill"]
EMY_NAME = ["Green slime", "Red slime", "Axe beast", "Ogre", "Sword man", 
            "Death hornet", "Signal slime", "Devil plant", "Twin killer", "Hell", 
            "Dragon gear", "Devil", "King Slime"]

MAZE_W = 11
MAZE_H = 9
maze = []
for y in range(MAZE_H):
    maze.append([0]*MAZE_W)
    
DUNGEON_W = MAZE_W*3
DUNGEON_H = MAZE_H*3
dungeon = []
for y in range(DUNGEON_H):
    dungeon.append([0]*DUNGEON_W)
    
def make_dungeon():
    XP = [0, 1, 0, -1]
    YP = [-1, 0, 1, 0]
    
    for x in range(MAZE_W):
        maze[0][x] = 1
        maze[MAZE_H-1][x] = 1
    for y in range(1, MAZE_H-1):
        maze[y][0] = 1
        maze[y][MAZE_W-1] = 1
    for y in range(1, MAZE_H-1):
        for x in range(1, MAZE_W-1):
            maze[y][x] = 0
            
    for y in range(2, MAZE_H-2, 2):
        for x in range(2, MAZE_W-2, 2):
            maze[y][x] = 1
            
    for y in range(2, MAZE_H-2, 2):
        for x in range(2, MAZE_W-2, 2):
            d = random.randint(0, 3)
            if x > 2:
                d = random.randint(0, 2)
            maze[y+YP[d]][x+XP[d]] = 1
    
    for y in range(DUNGEON_H):
        for x in range(DUNGEON_W):
            dungeon[y][x] = 9
    
    for y in range(1, MAZE_H-1):
        for x in range(1, MAZE_W-1):
            dx = x*3+1
            dy = y*3+1
            if maze[y][x] == 0:
                if random.randint(0, 99) < 20:
                    for ry in range(-1, 2):
                        for rx in range(-1, 2):
                            dungeon[dy+ry][dx+rx] = 0
                else:
                    dungeon[dy][dx] = 0
                    if maze[y-1][x] == 0: dungeon[dy-1][dx] = 0
                    if maze[y+1][x] == 0: dungeon[dy+1][dx] = 0
                    if maze[y][x-1] == 0: dungeon[dy][dx-1] = 0
                    if maze[y][x+1] == 0: dungeon[dy][dx+1] = 0
                    
def draw_dungeon(bg, fnt):
    bg.fill(BLACK)
    for y in range(-4, 6):
        for x in range(-5, 6):
            base_x = (x+5)*80
            base_y = (y+4)*80
            
            offset_x = 0
            offset_y = 0
            if moving:
                offset_x = -move_dx * int(move_progress * 80)
                offset_y = -move_dy * int(move_progress * 80)
            X = base_x + offset_x
            Y = base_y + offset_y
            dx = pl_x + x
            dy = pl_y + y
            if 0 <= dx < DUNGEON_W and 0 <= dy < DUNGEON_H:
                if dungeon[dy][dx] <= 4:
                    bg.blit(imgFloor[dungeon[dy][dx]],[X, Y])
                if dungeon[dy][dx] == 9:
                    bg.blit(imgWall, [X, Y-40])
                    if dy >= 1 and dungeon[dy-1][dx] == 9:
                        bg.blit(imgWall2, [X, Y-80])
            if x == 0 and y == 0:
                bg.blit(imgPlayer[pl_a], [X, Y-40])
    bg.blit(imgDark, [0, 0])
    draw_para(bg, fnt)
    
def put_event():
    global pl_x, pl_y, pl_d, pl_a
    while True:
        x = random.randint(3, DUNGEON_W-4)
        y = random.randint(3, DUNGEON_H-4)
        if(dungeon[y][x] == 0):
            for ry in range(-1, 2):
                for rx in range(-1, 2):
                    dungeon[y+ry][x+rx] = 0
            dungeon[y][x] = 3
            break
    for i in range(60):
        x = random.randint(3, DUNGEON_W-4)
        y = random.randint(3, DUNGEON_H-4)
        if(dungeon[y][x] == 0):
            dungeon[y][x] = random.choice([1,1,2,2,2,2,2,2,4])
            
    while True:
        pl_x = random.randint(3, DUNGEON_W-4)
        pl_y = random.randint(3, DUNGEON_H-4)
        if(dungeon[pl_y][pl_x] == 0):
            break
    pl_d = 1
    pl_a = 2
    
def move_player(key):
    global idx, tmr, pl_x, pl_y, pl_d, pl_a
    global pl_life, food, potion, blazegem, treasure, floor ,pl_str
    global pl_def_base, pl_def_buff, def_pill, flg_action
    global moving, move_progress, hold_dir, hold_timer
    
    if dungeon[pl_y][pl_x] == 1:
        dungeon[pl_y][pl_x] = 0
        treasure = random.choice([0,0,0,1,1,1,1,1,1,2,6,6])
        if floor >= 10:
            treasure = random.choice([0,0,0,1,1,1,1,1,1,2,5,6,6])
            r = random.randint(0, 99)
            if treasure in (5, 6) and r < 30:
                treasure = 0
        if treasure == 0:
            potion = potion + 1
        if treasure == 1:
            blazegem = blazegem + 1
        if treasure == 2:
            food = int(food/2)
        if treasure == 5:
            pl_str += 30
        if treasure == 6:
            pl_def_base += 5
            def_pill += 1 
        idx = 3
        tmr = 0
        return
    if dungeon[pl_y][pl_x] == 2:
        dungeon[pl_y][pl_x] = 0
        r = random.randint(0, 99)
        if r < 45:
            treasure = random.choice([3,3,3,3,4,4])
            if treasure == 3: food = food + 30
            if treasure == 4: food = food + 60
            idx = 3
            tmr = 0
        else:
            idx = 10
            tmr = 0
            try:
                moving = False
                move_progress = 0.0
                hold_dir = None
                hold_timer = 0
            except NameError:
                pass
        return
    if dungeon[pl_y][pl_x] == 3:
        idx = 2
        tmr = 0
        return
    
    if dungeon[pl_y][pl_x] == 4:
        dungeon[pl_y][pl_x] = 0
        r = random.randint(0, 99)
        if r < 10:
            pl_life = pl_life - 50
        elif r < 30:
            pl_life = pl_life - 30
        else:
            pl_life = pl_life - 10
        idx = 4
        tmr = 0
        
        if pl_life < 0:
            idx = 9
                
def draw_text(bg, txt, x, y, fnt, col):
    sur = fnt.render(txt, True, BLACK)
    bg.blit(sur, [x+1, y+2])
    sur = fnt.render(txt, True, col)
    bg.blit(sur, [x, y])
    
def draw_para(bg, fnt):
    X = 30
    Y = 600
    bg.blit(imgPara, [X, Y])
    col = WHITE
    if pl_life < 10 and tmr%2 == 0: col = RED
    draw_text(bg, f"{pl_life}/{pl_lifemax}", X+128, Y+6, fnt, col)
    draw_text(bg, str(pl_str), X+128, Y+33, fnt, WHITE)
    col = WHITE
    if food == 0 and tmr%2 == 0: col = RED
    draw_text(bg, str(food), X+128, Y+60, fnt, col)
    draw_text(bg, str(potion), X+266, Y+6, fnt, WHITE)
    draw_text(bg, str(blazegem), X+266, Y+33, fnt, WHITE)
    draw_text(bg, f"Lv:{pl_lv}", X+230, Y+60, fnt, WHITE)
    X2, Y2 = 350, 600
    bg.blit(imgPara2, [X2, Y2])
    draw_text(bg, f"DEF   : {pl_def_base}", X2+10, Y2+6, fnt, WHITE)
    draw_text(bg, f"DEF T: {pl_def_buff}", X2+10, Y2+33, fnt, WHITE)
    shield_img = imgItem[6]
    icon_w = shield_img.get_width()
    icon_h = shield_img.get_height()
    max_icons = 5
    spacing = icon_w + 4
    if def_pill <= max_icons:
        for i in range(def_pill):
            bg.blit(shield_img, [X2+1- + i*spacing, Y2+60])
    else:
        for i in range(max_icons):
            bg.blit(shield_img, [X2+10 + i*spacing, Y2+60])
        draw_text(bg, f"x{def_pill}", X2+10 + max_icons*spacing + 6, Y2+60 + icon_h//4, fnt, WHITE)
    
def init_battle():
    global imgEnemy, emy_name, emy_lifemax, emy_life, emy_str, emy_x, emy_y, typ
    typ = random.randint(0, floor)
    lev = random.randint(1, floor)
    if floor >= 11:
        typ = random.randint(0, 10)
        lev = random.randint(floor-5, floor)
    if floor >= 15:
        typ = random.randint(0, 12)
        lev = random.randint(floor-4, floor)
        z = random.randint(0, 99)
        if typ == 11 and z < 50:
            typ = 10
    imgEnemy = pygame.image.load("image/enemy"+str(typ)+".png")
    emy_name = EMY_NAME[typ]+" LV"+str(lev)
    emy_lifemax = 60*(typ+1)+(lev-1)*10
    emy_str = int(emy_lifemax/8)
    if typ == 11:
        emy_lifemax = 60*(34+1)+(lev-1)*10
        emy_str = int(emy_lifemax/8)
    elif typ == 12:
        emy_lifemax = 100*(typ) + floor*10
        emy_str = 30 + floor*5
    emy_life = emy_lifemax
    emy_x = 440-imgEnemy.get_width()/2
    emy_y = 560-imgEnemy.get_height()
    
def draw_bar(bg, x, y, w, h, val, max):
    pygame.draw.rect(bg, WHITE, [x-2, y-2, w+4, h+4])
    pygame.draw.rect(bg, BLACK, [x, y, w, h])
    if val > 0:
        pygame.draw.rect(bg, (0, 128, 255), [x, y, w*val/max, h])
        
def draw_battle(bg, fnt):
    global emy_blink, dmg_eff
    bx = 0
    by = 0
    if dmg_eff > 0:
        dmg_eff = dmg_eff - 1
        bx = random.randint(-20, 20)
        by = random.randint(-10, 10)
    bg.blit(imgBtlBG, [bx, by])
    if emy_life > 0 and emy_blink%2 ==0:
        bg.blit(imgEnemy, [emy_x, emy_y+emy_step])
    draw_bar(bg, 340, 580, 200, 10, emy_life, emy_lifemax)
    if emy_blink > 0:
        emy_blink = emy_blink-1
    for i in range(10):
        draw_text(bg, message[i], 600, 100+i*50, fnt, WHITE)
    draw_para(bg, fnt)
    
    
def battle_command(bg, fnt, key):
    global btl_cmd
    ent = False
    if key[K_d]:
        btl_cmd = 4
        ent = True
    if key[K_a]:
        btl_cmd = 0
        ent = True
    if key[K_p]:
        btl_cmd = 1
        ent = True
    if key[K_b]:
        btl_cmd = 2
        ent = True
    if key[K_r]:
        btl_cmd = 3
        ent = True
    if key[K_UP] and btl_cmd > 0:
        btl_cmd -= 1
    if key[K_DOWN] and btl_cmd < len(COMMAND) - 1:
        btl_cmd += 1
    if key[K_SPACE] or key[K_RETURN]:
        ent = True
    for i in range(len(COMMAND)):
        c = WHITE
        if btl_cmd == i: c=BLINK[tmr%6]
        draw_text(bg, COMMAND[i], 20, 200+i*60, fnt, c)
    return ent

message = [""]*10
def init_message():
    for i in range(10):
        message[i] = ""
        
def set_message(msg):
    for i in range(10):
        if message[i] == "":
            message[i] = msg
            return
    for i in range(9):
        message[i] = message[i+1]
    message[9] = msg
    
def main():
    global speed, idx, tmr, floor, fl_max, welcome
    global pl_x, pl_y, pl_a, pl_lifemax, pl_life, pl_str, food, potion, blazegem, pl_lv
    global pl_def_base, pl_def_buff, def_pill
    global emy_life, emy_step, emy_blink, dmg_eff, typ
    global moving, move_dx, move_dy, move_progress, MOVE_SPEED, base_move_speed
    global hold_dir, hold_timer, hold_delay, hold_interval
    dmg = 0
    lif_p = 0
    str_p = 0
    
    pygame.init()
    pygame.display.set_caption("Dungeon")
    screen = pygame.display.set_mode((880, 720))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40)
    fontS = pygame.font.Font(None, 30)
    
    se = [pygame.mixer.Sound("sound/ohd_se_attack.ogg"),
          pygame.mixer.Sound("sound/ohd_se_blaze.ogg"),
          pygame.mixer.Sound("sound/ohd_se_potion.ogg"),
          pygame.mixer.Sound("sound/ohd_jin_gameover.ogg"),
          pygame.mixer.Sound("sound/ohd_jin_levup.ogg"),
          pygame.mixer.Sound("sound/ohd_jin_win.ogg")]
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_s:
                    speed = (speed%5) + 1
                    
                    old_move_speed = MOVE_SPEED
                    MOVE_SPEED = base_move_speed * (1 + (speed - 1) * 0.15)
                    try:
                        if old_move_speed > 0:
                            move_progress = move_progress * (old_move_speed/ MOVE_SPEED)
                    except NameError:
                        pass
                #プレーヤー移動
                if idx ==1 and not moving:
                    if event.key == K_UP:
                        if dungeon[pl_y-1][pl_x] != 9:
                            move_dx, move_dy = 0, -1
                            moving= True
                            move_progress = 0.0
                            pl_d = 0
                            pl_a = pl_d * 2 
                    # 下
                    elif event.key == K_DOWN:
                        if dungeon[pl_y+1][pl_x] != 9:
                            move_dx, move_dy = 0, 1
                            moving = True
                            move_progress = 0.0
                            pl_d = 1
                            pl_a = pl_d * 2 
                    # 左
                    elif event.key == K_LEFT:
                        if dungeon[pl_y][pl_x-1] != 9:
                            move_dx, move_dy = -1, 0
                            moving = True
                            move_progress = 0.0
                            pl_d = 2
                            pl_a = pl_d * 2
                    # 右
                    elif event.key == K_RIGHT:
                        if dungeon[pl_y][pl_x+1] != 9:
                            move_dx, move_dy = 1, 0
                            moving = True
                            move_progress = 0.0
                            pl_d = 3
                            pl_a = pl_d * 2
                            
                    if event.key == K_UP:
                        hold_dir = "up"
                        hold_timer = hold_delay
                    elif event.key == K_DOWN:
                        hold_dir = "down"
                        hold_timer = hold_delay
                    elif event.key == K_LEFT:
                        hold_dir = "left"
                        hold_timer = hold_delay
                    elif event.key == K_RIGHT:
                        hold_dir = "right"
                        hold_timer = hold_delay
                        
            if event.type == KEYUP:
                if event.key in (K_UP, K_DOWN, K_LEFT, K_RIGHT):
                    hold_dir = None
                    hold_timer = 0.0

        tmr = tmr +1
        if moving:
            move_progress += MOVE_SPEED
            
            pl_a = pl_d * 2 +(tmr % 2)
            if move_progress >=  1.0 :
                moving = False
                move_progress = 0.0
                pl_x += move_dx
                pl_y += move_dy
                if food > 0:
                    food -= 1
                    if pl_life < pl_lifemax:
                        pl_life += 1
                else:
                    pl_life -= 5
                    if pl_life <= 0:
                        pl_life = 0
                        pygame.mixer.music.stop()
                        idx = 9
                        tmr = 0
                
                move_player([0]*10)
        key = pygame.key.get_pressed()
        
        if hold_dir is not None:
            # フレーム単位でデクリメント
            hold_timer -= 1
            if hold_timer <= 0:
                # moving していなければ自動で1マス移動を開始する
                if not moving:
                    if hold_dir == "up":
                        if dungeon[pl_y-1][pl_x] != 9:
                            move_dx, move_dy = 0, -1
                            moving = True
                            move_progress = 0.0
                            pl_d = 0
                            pl_a = pl_d * 2
                    elif hold_dir == "down":
                        if dungeon[pl_y+1][pl_x] != 9:
                            move_dx, move_dy = 0, 1
                            moving = True
                            move_progress = 0.0
                            pl_d = 1
                            pl_a = pl_d * 2
                    elif hold_dir == "left":
                        if dungeon[pl_y][pl_x-1] != 9:
                            move_dx, move_dy = -1, 0
                            moving = True
                            move_progress = 0.0
                            pl_d = 2
                            pl_a = pl_d * 2
                    elif hold_dir == "right":
                        if dungeon[pl_y][pl_x+1] != 9:
                            move_dx, move_dy = 1, 0
                            moving = True
                            move_progress = 0.0
                            pl_d = 3
                            pl_a = pl_d * 2
                # 初回は hold_delay、以降は hold_interval を使う
                hold_timer = hold_interval
        
        if idx == 0:
            if tmr == 1:
                pygame.mixer.music.load("sound/ohd_bgm_title.ogg")
                pygame.mixer.music.play(-1)
            screen.fill(BLACK)
            screen.blit(imgTitle, [-50, 80])
            if fl_max >= 2:
                draw_text(screen, f"You reached floor {fl_max}.", 300, 460, font, CYAN)
            draw_text(screen, "Press space key", 320, 560, font, BLINK[tmr%6])
            if key[K_SPACE] == 1:
                make_dungeon()
                put_event()
                floor = 1
                welcome = 15
                pl_lifemax = 300
                pl_life = pl_lifemax
                pl_str = 100
                food = 300
                potion = 0
                blazegem = 0
                pl_lv = 1
                idx = 1
                pygame.mixer.music.load("sound/ohd_bgm_field.ogg")
                pygame.mixer.music.play(-1)
                
        elif idx == 1:
            move_player(key)
            draw_dungeon(screen, fontS)
            draw_text(screen, f"floor {floor} ({pl_x} {pl_y})", 60, 40, fontS, WHITE)
            if welcome > 0:
                welcome = welcome - 1
                draw_text(screen, f"Welcome to floor {floor}", 300, 180, font, CYAN)
            
        elif idx == 2:
            draw_dungeon(screen, fontS)
            if 1 <= tmr <= 5:
                h = 80*tmr
                pygame.draw.rect(screen, BLACK, [0, 0, 880, h])
                pygame.draw.rect(screen, BLACK, [0, 720-h, 880, h])
            if tmr == 5:
                floor = floor + 1
                if floor > fl_max:
                    fl_max = floor
                welcome = 15
                make_dungeon()
                put_event()
            if 6 <= tmr <=9:
                h = 80*(10-tmr)
                pygame.draw.rect(screen, BLACK, [0, 0, 880, h])
                pygame.draw.rect(screen, BLACK, [0, 720-h, 880, h])
            if tmr == 10:
                idx = 1
        
        elif idx == 3:
            draw_dungeon(screen, fontS)
            screen.blit(imgItem[treasure], [320, 220])
            draw_text(screen, TRE_NAME[treasure], 380, 240, font, WHITE)
            if tmr == 10:
                idx = 1
        
        elif idx == 4:
            draw_dungeon(screen, fontS)
            screen.blit(imgDamage, [320, 220])
            if tmr == 15:
                idx = 1
        
        elif idx == 9:
            if tmr <= 30:
                PL_TURN = [2, 4, 0, 6]
                pl_a = PL_TURN[tmr%4]
                if tmr == 30: pl_a = 8
                draw_dungeon(screen, fontS)
            elif tmr == 31:
                se[3].play()
                draw_text(screen, "You died.", 360, 240, font, RED)
                draw_text(screen, "Game ovre.", 360, 380, font, RED)
            elif tmr == 100:
                idx = 0
                tmr = 0
                
        elif idx == 10:
            if tmr == 1:
                try:
                    moving = False
                    move_progress = 0.0
                    hold_dir = None
                    hold_timer = 0
                except NameError:
                    pass
                init_battle()
                init_message()
                pygame.mixer.music.load("sound/ohd_bgm_battle.ogg")
                if typ == 11:
                    pygame.mixer.music.load("sound/Tolerance_Deviation.mp3")
                pygame.mixer.music.play(-1)
            elif tmr <= 4:
                bx = (4-tmr)*220
                by = 0
                screen.blit(imgBtlBG, [bx, by])
                draw_text(screen, "Encounter!", 350, 200, font, WHITE)
            elif tmr <= 16:
                draw_battle(screen, fontS)
                draw_text(screen, emy_name+" appear!", 300, 200, font, WHITE)
            else:
                idx = 11
                tmr = 0
                flg_action = False
                turn_msg_shown = False
                no_potion_shown = False
                no_blazegem_shown = False
                no_defensepill_shown = False
                
        elif idx == 11:
            draw_battle(screen, fontS)
            if tmr == 1 and not turn_msg_shown: 
                set_message("Your turn.")
                turn_msg_shown = True
            if battle_command(screen, font, key):
                if not flg_action:
                    if btl_cmd == 0:
                        idx = 12
                        tmr = 0
                        flg_action = True
                    elif btl_cmd == 1:
                        if potion > 0:
                            idx = 20
                            tmr = 0
                            flg_action = True
                        else:
                            if not no_potion_shown:
                                set_message("No Potion!")
                                no_potion_shown = True
                    elif btl_cmd == 2: 
                        if blazegem > 0:
                            idx = 21
                            tmr = 0
                            flg_action = True
                        else:
                            if not no_blazegem_shown:
                                set_message("No Blaze gem!")
                                no_blazegem_shown = True
                    elif btl_cmd == 3:
                        idx = 14
                        tmr = 0
                        flg_action = True
                    elif btl_cmd == 4:
                        if def_pill > 0:
                            idx = 23
                            tmr = 0
                            flg_action = True
                        else:
                            if not no_defensepill_shown:
                                set_message("No Defense Pill!")
                                no_defensepill_shown = True
                                        
        elif idx == 12:
            draw_battle(screen, fontS)
            if tmr ==1:
                set_message("You attack!")
                se[0].play()
                dmg = pl_str + random.randint(0, 9)
            if 2 <= tmr <= 4:
                screen.blit(imgEffect[0], [700-tmr*120, -100+tmr*120])
            if tmr == 5:
                emy_blink = 5
                set_message(str(dmg)+"pts of damage!")
            if tmr == 11:
                emy_life = emy_life - dmg
                if emy_life <= 0:
                    emy_life = 0
                    idx = 16
                    tmr = 0
            if tmr == 16:
                idx = 13
                tmr = 0
                
        elif idx == 13:
            draw_battle(screen, fontS)
            if tmr == 1:
                set_message("Enemy turn.")
            if tmr == 5:
                set_message(emy_name+" attack!")
                se[0].play()
                emy_step = 30
            if tmr == 9:
                dmg_reduction = pl_def_base + pl_def_buff
                dmg =max(1, (emy_str + random.randint(0, emy_str))- dmg_reduction)
                set_message(str(dmg)+"pts of damage!")
                dmg_eff = 5
                emy_step = 0
            if tmr == 15:
                pl_life = pl_life - dmg
                if pl_life < 0:
                    pl_life = 0
                    idx = 15
                    tmr = 0
            if tmr == 20:
                pl_def_buff = max(0, pl_def_buff -5)
                
                flg_action = False
                turn_msg_shown = False
                no_potion_shown = False
                no_blazegem_shown = False
                no_defensepill_shown = False
                
                idx = 11
                tmr = 0
                
        elif idx == 14:
            draw_battle(screen, fontS)
            if tmr == 1: set_message("...")
            if tmr == 2: set_message(".....")
            if tmr == 3: set_message(".......")
            if tmr == 4: set_message(".........")
            if tmr == 5: 
                if random.randint(0, 99) < 60:
                    idx = 22
                else:
                    set_message("You failed to flee.")
            if tmr == 10:
                idx = 13
                tmr = 0
                
        elif idx == 15:
            draw_battle(screen, fontS)
            if tmr == 1:
                pygame.mixer.music.stop()
                set_message("You lose.")
            if tmr == 11:
                idx = 9
                tmr = 29
        
        elif idx == 16:
            draw_battle(screen, fontS)
            if tmr == 1:
                set_message("You win!")
                pygame.mixer.music.stop()
                se[5].play()
            if tmr == 28:
                idx = 22
                if typ == 11:
                    idx = 17
                    tmr = 0
                elif random.randint(0, emy_lifemax) > random.randint(0, pl_lifemax):
                    idx = 17
                    tmr = 0
                    
        elif idx == 17:
            draw_battle(screen, fontS)
            if tmr == 1:
                pl_lv += 1
                set_message(f"Level up! Lv{pl_lv}")
                se[4].play()
                lif_p = random.randint(10, 20)
                str_p = random.randint(5, 10)
                def_inc = random.randint(1, 5)
            if tmr == 21:
                set_message(f"Max life +{lif_p}")
                pl_lifemax += lif_p
            if tmr == 26:
                set_message(f"Str +{str_p}")
                pl_str += str_p
            if tmr == 31:
                set_message(f"Def+{def_inc}")
                pl_def_base += def_inc
            if tmr == 50:
                idx = 22
                
        elif idx == 20:
            draw_battle(screen, fontS)
            if tmr == 1:
                set_message("Potion!")
                se[2].play()
            if tmr == 6:
                pl_life = pl_lifemax
                potion -= 1
            if tmr == 11:
                idx = 13
                tmr = 0
        elif idx == 21:
            draw_battle(screen, fontS)
            img_rz = pygame.transform.rotozoom(imgEffect[1], 30*tmr, (12-tmr)/8)
            X = 440-img_rz.get_width()/2
            Y = 360-img_rz.get_height()/2
            screen.blit(img_rz, [X, Y])
            if tmr == 1:
                set_message("Blaze gem!")
                se[1].play()
            if tmr == 6:
                blazegem -= 1
            if tmr == 11:
                dmg = 1000
                idx = 12
                tmr = 4
                
        elif idx == 22:
            pygame.mixer.music.load("sound/ohd_bgm_field.ogg")
            pygame.mixer.music.play(-1)
            idx = 1
            
        elif idx == 23:
            draw_battle(screen, fontS)
            if tmr == 1:
                set_message("Defense Pill!")
            if tmr == 6:
                buff_amount = random.randint(5, 15)
                pl_def_buff += buff_amount
                def_pill -= 1
                set_message("Buff Def +{buff_amount}")
            if tmr == 20:
                idx = 13
                tmr = 0
                
        draw_text(screen, "[S]peed" + str(speed), 740, 40, fontS, WHITE)
        if idx != 1:
            try:
                hold_dir = None
                hold_timer = 0
            except NameError:
                pass
        pygame.display.update()
        fps = max(1, 4 + 2 *int(speed))
        clock.tick(fps)
        
if __name__ == "__main__":
    main()