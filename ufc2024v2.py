from ursina import *
import random

app = Ursina()

# --- СОХРАНЕНИЯ ---
p_save = {"money": 0, "wins": 0, "hp_lvl": 0, "dmg_lvl": 0, "auto_mode": False}

# --- РОСТЕР ---
opponents = {
    "STREET (0+ wins)": [("Drunk Joe", 120, 5), ("Slim Shady", 150, 8)],
    "REGIONAL (5+ wins)": [("Gym Owner", 450, 22), ("Pro Prospect", 500, 25)],
    "UFC TOP (15+ wins)": [("Makhachev", 750, 35), ("Jon Jones", 950, 50)]
}

game_active = False

def start_fight(name, hp, dmg):
    global game_active
    menu_parent.enabled = False
    my_hp = 150 + (p_save["hp_lvl"] * 100)
    my_dmg = (5 + p_save["dmg_lvl"] * 5, 10 + p_save["dmg_lvl"] * 7)
    
    f1.setup("SIGMA", my_hp, my_dmg, color.cyan)
    f2.setup(name, hp, (dmg-2, dmg+4), color.red)
    f1.enabled = f2.enabled = game_active = True

class Fighter(Entity):
    def __init__(self, x):
        super().__init__(model='cube', scale=(1.2, 2, 1.2), position=(x, 1, 0), enabled=False)
        self.hp_bar = Entity(parent=self, model='quad', color=color.red, scale=(1.5, 0.2), y=1.7)
        self.stamina = 100
        self.attack_cooldown = 0 

    def setup(self, name, hp, dmg, col):
        self.fname = name; self.max_hp = self.hp = hp; self.dmg_range = dmg
        self.stamina = 100; self.color = col; self.rotation = (0,0,0)
        self.scale = (1.2, 2, 1.2)
        self.attack_cooldown = 0
        self.hp_bar.scale_x = 1.5

    def blink(self, blink_color=color.white, duration=0.1):
        original_color = self.color
        self.color = blink_color
        invoke(setattr, self, 'color', original_color, delay=duration)

    def update(self):
        if not game_active: return
        target = f2 if self == f1 else f1
        
        if distance(self, target) > 1.8:
            self.look_at(target)
            self.position += self.forward * time.dt * 6
        else:
            self.attack_cooldown -= time.dt
            if self.attack_cooldown <= 0:
                if self == f2 or (self == f1 and p_save["auto_mode"]):
                    self.attack(target)
                    self.attack_cooldown = random.uniform(0.4, 0.8)

        self.stamina = min(100, self.stamina + time.dt * 25)

    def attack(self, target):
        if not game_active or self.stamina < 25 or target.hp <= 0: return
        
        self.stamina -= 25
        self.animate_position(self.position + self.forward * 0.4, duration=0.05)
        self.animate_position(self.position, duration=0.05, delay=0.05)
        
        # Эффект крови
        blood = Entity(model='cube', color=color.red, scale=0.15, position=target.position + (0, 1, 0))
        blood.animate_position(blood.position + (random.uniform(-1,1), random.uniform(-0.5, 0.5), random.uniform(-1,1)), duration=0.3)
        destroy(blood, delay=0.3)

        dmg = random.randint(self.dmg_range[0], self.dmg_range[1])
        target.hp -= dmg
        target.hp_bar.scale_x = max(0.0, (target.hp / target.max_hp) * 1.5)
        target.blink(color.white, duration=0.1)
        
        if target.hp <= 0:
            target.animate_rotation_x(90, duration=0.15) # Эпичное падение в нокаут
            self.victory()

    def victory(self):
        global game_active
        game_active = False
        self.animate_scale(Entity().scale * 1.4, duration=0.2)
        self.animate_scale(Entity().scale * 1.2, duration=0.2, delay=0.2)
        if self == f1:
            p_save["money"] += 200
            p_save["wins"] += 1
        invoke(self.reset, delay=1.5)

    def reset(self):
        f1.enabled = f2.enabled = False
        menu_parent.enabled = True
        update_menu()

# --- ИНТЕРФЕЙС ---
menu_parent = Entity(parent=camera.ui)
list_parent = Entity(parent=menu_parent)
stat_txt = Text(parent=menu_parent, y=0.45, origin=(0,0), scale=1.5, color=color.gold)

def update_menu():
    for c in list_parent.children: destroy(c)
    stat_txt.text = f"CAREER: Wins {p_save['wins']} | Cash ${p_save['money']}"
    
    y_off = 0.2
    for tier, f_list in opponents.items():
        req = int(tier.split('+')[0].split('(')[1])
        lock = p_save["wins"] < req
        Text(text=tier, parent=list_parent, y=y_off, x=-0.4, color=color.gray if lock else color.white)
        if not lock:
            for n, h, d in f_list:
                y_off -= 0.06
                b = Button(text=f"{n} (HP:{h})", parent=list_parent, x=-0.25, y=y_off, scale=(0.3, 0.04))
                b.on_click = Func(start_fight, n, h, d)
        y_off -= 0.1

def toggle_auto(btn):
    p_save["auto_mode"] = not p_save["auto_mode"]
    btn.text = f"AUTO: {'ON' if p_save['auto_mode'] else 'OFF'}"
    btn.color = color.green if p_save["auto_mode"] else color.black66

auto_btn = Button(text="AUTO: OFF", parent=menu_parent, x=0.3, y=0.2, scale=(0.2, 0.08), color=color.black66)
auto_btn.on_click = Func(toggle_auto, auto_btn)

Button(text="TRAIN HP ($300)", parent=menu_parent, x=0.3, y=0.05, scale=(0.2, 0.08), on_click=lambda: buy_stat("hp_lvl"))
Button(text="TRAIN DMG ($300)", parent=menu_parent, x=0.3, y=-0.05, scale=(0.2, 0.08), on_click=lambda: buy_stat("dmg_lvl"))

def buy_stat(stat):
    if p_save["money"] >= 300:
        p_save["money"] -= 300
        p_save[stat] += 1
        update_menu()

def input(key):
    if game_active and not p_save["auto_mode"] and key == 'left mouse down':
        if distance(f1, f2) < 2: f1.attack(f2)

Sky(); f1, f2 = Fighter(-4), Fighter(4)
camera.position, camera.rotation_x = (0, 15, -24), 30
update_menu()
app.run()
