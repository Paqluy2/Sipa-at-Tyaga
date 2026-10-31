import pygame
import sys
import os
import random

pygame.init()
pygame.mixer.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
hs_file = os.path.join(BASE_DIR, "highscore.txt")
audio_dir = os.path.join(BASE_DIR, "audio")
font_file = os.path.join(BASE_DIR, "font", "ZeroCool.ttf")

dis_width, dis_height = 1000, 600
screen = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("SIPA at tyaga")
clock = pygame.time.Clock()
FPS = 60

THRESHOLD_1 = 300   
THRESHOLD_2 = 800   

white, black, sky_blue = (255, 255, 255), (0, 0, 0), (135, 206, 235)
red, green, yellow, purple, orange = (255, 50, 50), (50, 255, 50), (255, 215, 0), (128, 0, 128), (255, 165, 0)


try:
    font_title    = pygame.font.Font(font_file, 50) 
    font_hud      = pygame.font.Font(font_file, 28)  
    font_button   = pygame.font.Font(font_file, 24) 
    font_card     = pygame.font.Font(font_file, 16)  
    font_feedback = pygame.font.Font(font_file, 32)  
    font_sub      = pygame.font.Font(font_file, 14)  
    font_pause     = pygame.font.Font(font_file, 80) 
    font_quit      = pygame.font.Font(font_file, 20)  
except FileNotFoundError:
    font_title    = pygame.font.Font(None, 48)
    font_hud      = pygame.font.Font(None, 32)
    font_button   = pygame.font.Font(None, 28)
    font_card     = pygame.font.Font(None, 18)
    font_feedback = pygame.font.Font(None, 36)
    font_sub      = pygame.font.Font(None, 16)
    font_pause     = pygame.font.Font(None, 40)  
    font_quit      = pygame.font.Font(None, 20)  

# --- BACKGROUND TOWER ---
try:
    img_dir = os.path.join(BASE_DIR, "img")
    bg_tower = [
        pygame.transform.scale(pygame.image.load(os.path.join(img_dir, "barangay.png")).convert_alpha(), (dis_width, dis_height)),
        pygame.transform.scale(pygame.image.load(os.path.join(img_dir, "sky_low.png")).convert_alpha(), (dis_width, dis_height)),
        pygame.transform.scale(pygame.image.load(os.path.join(img_dir, "trans_low_to_high.png")).convert_alpha(), (dis_width, dis_height)),
        pygame.transform.scale(pygame.image.load(os.path.join(img_dir, "sky_high.png")).convert_alpha(), (dis_width, dis_height)),
        pygame.transform.scale(pygame.image.load(os.path.join(img_dir, "trans_high_to_space.png")).convert_alpha(), (dis_width, dis_height)),
        pygame.transform.scale(pygame.image.load(os.path.join(img_dir, "space_deep.png")).convert_alpha(), (dis_width, dis_height))
    ]
    bgs_loaded = True
except FileNotFoundError:
    bg_tower = []
    bgs_loaded = False

# --- CHARACTER ASSETS ---
try:
    idle_img = pygame.transform.scale(pygame.image.load(os.path.join(img_dir, "idle.png")).convert_alpha(), (400, 300))
    kick_high_img = pygame.transform.scale(pygame.image.load(os.path.join(img_dir, "kick.png")).convert_alpha(), (400, 300))
    kick_perfect_img = pygame.transform.scale(pygame.image.load(os.path.join(img_dir, "kicking.png")).convert_alpha(), (400, 300))
    kick_low_img = pygame.transform.scale(pygame.image.load(os.path.join(img_dir, "kickings.png")).convert_alpha(), (400, 300))
    sipa_img = pygame.transform.scale(pygame.image.load(os.path.join(img_dir, "sipa.png")).convert_alpha(), (50, 50))
    sipa_radius = sipa_img.get_width() // 2        
    assets_loaded = True

except FileNotFoundError:
    assets_loaded = False
    sipa_radius = 20

try:
    bird_img = pygame.transform.scale(
        pygame.image.load(os.path.join(img_dir, "bird.png")).convert_alpha(),
        (48, 36)  
    )
    bird_loaded = True
except (FileNotFoundError, pygame.error):
    bird_loaded = False


try:

    logo_raw = pygame.image.load(os.path.join(img_dir, "logo.png")).convert_alpha()
    logo_width = 420
    logo_height = int(logo_raw.get_height() * (logo_width / logo_raw.get_width()))
    logo_img = pygame.transform.scale(logo_raw, (logo_width, logo_height))
    logo_loaded = True
except (FileNotFoundError, pygame.error):
    logo_loaded = False

try:
    sfx_card_draw = pygame.mixer.Sound(os.path.join(audio_dir, "card_draw_1.wav"))
    sfx_card_fan  = pygame.mixer.Sound(os.path.join(audio_dir, "card_fan_2.wav"))
    sfx_fah       = pygame.mixer.Sound(os.path.join(audio_dir, "fah.mp3"))
    sfx_ice       = pygame.mixer.Sound(os.path.join(audio_dir, "ice_in_water.wav"))
    sfx_kick      = pygame.mixer.Sound(os.path.join(audio_dir, "kick.wav"))
    sfx_select    = pygame.mixer.Sound(os.path.join(audio_dir, "select_4.wav"))


    menu_music_path = os.path.join(audio_dir, "Honobono Teahouse.mp3")
    pygame.mixer.music.load(menu_music_path)
    pygame.mixer.music.play(-1)  # Loop continuously
    music_playing = True
except (pygame.error, FileNotFoundError) as e:
    print(f"Audio Load Warning: {e}")

    class DummySound:
        def play(self): pass
    sfx_card_draw = sfx_card_fan = sfx_fah = sfx_ice = sfx_kick = sfx_select = DummySound()
    music_playing = False

# --- LOAD SFX ---
try:
    sfx_pwede = pygame.mixer.Sound(os.path.join(BASE_DIR, "audio", "pwede_mag_tanong.wav"))
    sfx_pwede.set_volume(0.9)
    pwede_loaded = True
except Exception as e:
    print(f"Failed to load pwede_mag_tanong.wav: {e}")
    pwede_loaded = False

try:
    car_img = pygame.image.load(os.path.join(BASE_DIR, "img", "car.png")).convert_alpha()
    car_img = pygame.transform.scale(car_img, (350, 200))  # Adjust size as needed
except Exception:
    car_img = None

try:
    sfx_revive = pygame.mixer.Sound(os.path.join(audio_dir, "revive.wav"))
    sfx_revive.set_volume(0.8)
except Exception:
    try:
        sfx_revive = pygame.mixer.Sound(os.path.join(audio_dir, "fah.mp3"))
    except Exception:
        sfx_revive = None

# --- GAME VARIABLES ---
gravity = 0.2
PIXELS_PER_METER = 80
sipa_x = dis_width // 2
sipa_y = 100
sipa_vel_y = 0
sipa_angle = 0

char_width, char_height = 400, 300                 
char_x, char_y = dis_width // 2 - 200, dis_height - 300             
is_kicking = False
kick_timer, KICK_DURATION = 0, 15 
current_kick_img = None
kick_cooldown, COOLDOWN_DURATION = 0, 25

hit_zone_y = char_y + 160        
hit_zone_height = 100            
hit_zone_width = 160             
perfect_zone_y = hit_zone_y + 20 
perfect_zone_height = 20
menu_timer = 0.0

score = 0
is_rising = False
points_earned_this_kick = 0
feedback_text, feedback_timer = "", 0
camera_y = 0
total_upgrades_bought = 0
game_state = "MAIN_MENU"

bird_x = -60
bird_base_y = 120
bird_speed = 2.5
bird_timer = 0

# --- SECRET QUIZ ---
SECRET_UPGRADE_CHANCE = 0.1
quiz_active = False
quiz_answered = False
quiz_result_msg = ""
quiz_result_timer = 0

# --- CAR CUTSCENE ANIMATION VARIABLES ---
car_x = -350
car_target_x = 220    
car_speed = 10        
car_arrived = False


sari_store_trigger_rect = pygame.Rect(270, 240, 150, 100)

quiz_question = "Pwede magtanong?"
quiz_options = [
    {"text": "A. Hindi nag Grow", "correct": False},
    {"text": "B. Never Grow Old", "correct": True},  
    {"text": "C. Never Enough.", "correct": False}
]

# 3 choice button rects centered on screen
quiz_choice_rects = [
    pygame.Rect(dis_width // 2 - 250, 280, 500, 48),
    pygame.Rect(dis_width // 2 - 250, 340, 500, 48),
    pygame.Rect(dis_width // 2 - 250, 400, 500, 48)
]

def grant_easter_egg_reward():
    global extra_lives, bounce_power, anting_chance, yelo_inventory, doble_metro_chance, pampaswerte_bonus
    
    # 6 Possible Legendary Buffs
    reward_pool = [
        {"name": "+2 Extra Buhay", "apply": lambda: globals().update(extra_lives=extra_lives + 2)},
        {"name": "Binti V Power (-18 Force)", "apply": lambda: globals().update(bounce_power=-18.0)},
        {"name": "+3 Yelo Packs", "apply": lambda: globals().update(yelo_inventory=yelo_inventory + 3)},
        {"name": "Anting-Anting (85% Dual Upgrades)", "apply": lambda: globals().update(anting_chance=0.85)},
        {"name": "Doble Metro (50% Chance)", "apply": lambda: globals().update(doble_metro_chance=0.50)},
        {"name": "Pampaswerte (+25% Luck)", "apply": lambda: globals().update(pampaswerte_bonus=0.25)}
    ]
    
    # Randomly select exactly 2 distinct rewards
    picked = random.sample(reward_pool, 2)
    for reward in picked:
        reward["apply"]()
        
    return f"{picked[0]['name']} & {picked[1]['name']}"

# --- RNG UPGRADE SYSTEM DEFINITIONS ---
rarity_colors = {
    "Common": white,
    "Uncommon": green,
    "Rare": sky_blue,
    "Epic": purple,
    "Legendary": orange
}

all_upgrades = [
    {"id": "binti_2", "name": "Binti II", "rarity": "Uncommon", "desc": "+2.5 Power"},
    {"id": "binti_1", "name": "Binti I", "rarity": "Common", "desc": "+1.0 Power"},
    {"id": "binti_3", "name": "Binti III", "rarity": "Rare", "desc": "+4.0 Power"},
    {"id": "tsinelas", "name": "Tsinelas", "rarity": "Rare", "desc": "+Perfect Hit Size"},
    {"id": "anting", "name": "Anting-Anting", "rarity": "Rare", "desc": "Chance for 2 Picks"},
    {"id": "buhay", "name": "Extra Buhay", "rarity": "Epic", "desc": "1 Auto-Revive"},
    {"id": "binti_4", "name": "Binti IV", "rarity": "Epic", "desc": "+5.0 Power"},
    {"id": "puntos_1", "name": "Doble Puntos I", "rarity": "Epic", "desc": "2x Score (1 Kick)"},
    {"id": "metro_1", "name": "Doble Metro I", "rarity": "Epic", "desc": "10% x2 Meter Gain"},
    {"id": "pampaswerte", "name": "Pampaswerte", "rarity": "Epic", "desc": "+10% Rare Chances"},
    {"id": "binti_5", "name": "Binti V", "rarity": "Legendary", "desc": "+8.0 Power"},
    {"id": "puntos_2", "name": "Doble Puntos II", "rarity": "Legendary", "desc": "2x Score (2 Kicks)"},
    {"id": "metro_2", "name": "Doble Metro II", "rarity": "Legendary", "desc": "20% x2 Meter Gain"},
    {"id": "yelo", "name": "Yelo (Press Y)", "rarity": "Legendary", "desc": "Stop Sipa Mid-Air"}
]

# --- PLAYER STATS & BUFFS ---
def load_highscore():
    try:
        with open(hs_file, "r") as f: return int(f.read())
    except: return 0

def save_highscore(val):
    with open(hs_file, "w") as f: f.write(str(val))

highscore = load_highscore()
play_btn_rect = pygame.Rect(dis_width//2 - 100, dis_height//2, 200, 50)
pause_btn_rect = pygame.Rect(dis_width - 140, 20, 110, 40)
game_over_menu_btn_rect = pygame.Rect(dis_width//2 - 100, dis_height//2 + 115, 200, 45)

# Card UI Layout
card_width, card_height = 220, 300
card_rects = [
    pygame.Rect(dis_width//2 - card_width - 20, dis_height//2 - card_height//2, card_width, card_height),
    pygame.Rect(dis_width//2 + 20, dis_height//2 - card_height//2, card_width, card_height)
]
current_choices = []
upgrade_picks_remaining = 0

# --- LOAD UPGRADE CARD IMAGES ---
card_images = {}
for upgrade in all_upgrades:
    img_name = upgrade["id"] + ".png"
    try:
        loaded_img = pygame.image.load(os.path.join(img_dir, img_name)).convert_alpha()
        card_images[upgrade["id"]] = pygame.transform.scale(loaded_img, (card_width, card_height))
    except (FileNotFoundError, pygame.error):
        pass

def reset_game():
    global sipa_y, sipa_vel_y, score, game_state, camera_y
    global bounce_power, hit_zone_width, hit_zone_y, perfect_zone_y, perfect_zone_height
    global kicks_landed, kicks_required, points_earned_this_kick, kick_cooldown
    global extra_lives, anting_chance, doble_metro_chance, pampaswerte_bonus
    global yelo_inventory, yelo_timer, double_score_kicks_left, extra_buhay_picked
    global bounce_power, hit_zone_width, hit_zone_y, perfect_zone_y, perfect_zone_height, upgrades_acquired, total_upgrades_bought
    sipa_y, sipa_vel_y, camera_y, score = 100, 0, 0, 0
    kicks_landed, kicks_required, points_earned_this_kick, kick_cooldown = 0, 5, 0, 0
    
    # Base Physical Stats
    bounce_power = -8.0
    hit_zone_y = char_y + 160        
    hit_zone_height = 100            
    hit_zone_width = 160             
    perfect_zone_y = hit_zone_y + 20 
    perfect_zone_height = 20        
    upgrades_acquired = 0 
    
    # Custom Modifiers
    extra_lives = 0
    extra_buhay_picked = False
    anting_chance = 0.0
    doble_metro_chance = 0.0
    pampaswerte_bonus = 0.0
    yelo_inventory = 0
    yelo_timer = 0
    double_score_kicks_left = 0
    total_upgrades_bought = 0
    
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(500)
    
    game_state = "PLAYING"

def generate_upgrades():
    global current_choices
    current_choices = []
    
    # Pampaswerte adjusts the weight of pulling higher tiers
    c_w = max(5, 45 - (pampaswerte_bonus * 100))
    u_w = 25
    r_w = 15 + (pampaswerte_bonus * 30)
    e_w = 10 + (pampaswerte_bonus * 40)
    l_w = 5 + (pampaswerte_bonus * 30)
    
    valid_pool = [u for u in all_upgrades if not (u["id"] == "buhay" and extra_buhay_picked)]
    
    while len(current_choices) < 2:
        roll = random.uniform(0, c_w + u_w + r_w + e_w + l_w)
        if roll <= c_w: target_rarity = "Common"
        elif roll <= c_w + u_w: target_rarity = "Uncommon"
        elif roll <= c_w + u_w + r_w: target_rarity = "Rare"
        elif roll <= c_w + u_w + r_w + e_w: target_rarity = "Epic"
        else: target_rarity = "Legendary"
        
        rarity_items = [item for item in valid_pool if item["rarity"] == target_rarity and item not in current_choices]
        
        # Fallback if a rarity pool is completely empty
        if not rarity_items: 
            rarity_items = [item for item in valid_pool if item not in current_choices]
            
        if rarity_items:
            current_choices.append(random.choice(rarity_items))

def apply_selected_upgrade(upgrade_dict):
    global bounce_power, perfect_zone_height, perfect_zone_y, extra_lives, extra_buhay_picked
    global anting_chance, doble_metro_chance, pampaswerte_bonus, yelo_inventory, double_score_kicks_left
    global upgrade_picks_remaining, kicks_landed, kicks_required, game_state, upgrades_acquired

    upgrades_acquired += 1

    u_id = upgrade_dict["id"]
    if u_id == "binti_1": bounce_power -= 0.5
    elif u_id == "binti_2": bounce_power -= 0.75
    elif u_id == "binti_3": bounce_power -= 1.25
    elif u_id == "binti_4": bounce_power -= 2.0
    elif u_id == "binti_5": bounce_power -= 5.0
    elif u_id == "tsinelas": 
        perfect_zone_height += 10
        perfect_zone_y -= 5
    elif u_id == "buhay":
        extra_lives += 1
        extra_buhay_picked = True
    elif u_id == "anting": anting_chance += 0.15
    elif u_id == "metro_1": doble_metro_chance += 0.10
    elif u_id == "metro_2": doble_metro_chance += 0.20
    elif u_id == "puntos_1": double_score_kicks_left += 1
    elif u_id == "puntos_2": double_score_kicks_left += 2
    elif u_id == "pampaswerte": pampaswerte_bonus += 0.10
    elif u_id == "yelo": yelo_inventory += 1

    upgrade_picks_remaining -= 1
    if upgrade_picks_remaining <= 0:
        kicks_landed = 0 
        kicks_required += 1
        game_state = "PLAYING"
    else:
        generate_upgrades() # Generate fresh cards for the 2nd pick

# --- EVENT LOOP ---
while True:
    action_triggered = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                sfx_select.play()
                pygame.time.delay(150)
                pygame.quit()
                sys.exit()

            if event.key == pygame.K_p:
                sfx_select.play()
                if game_state == "PLAYING":
                    game_state = "PAUSED"
                elif game_state == "PAUSED":
                    game_state = "PLAYING"

            # YELO SFX
            if event.key == pygame.K_y and game_state == "PLAYING" and yelo_inventory > 0 and yelo_timer <= 0:
                sfx_ice.play()
                yelo_inventory -= 1
                yelo_timer = 90

            if event.key in [pygame.K_SPACE, pygame.K_RETURN, pygame.K_UP]:
                if game_state in ["MAIN_MENU", "GAME_OVER"]:
                    sfx_select.play()
                    reset_game()
                elif game_state == "PAUSED":
                    sfx_select.play()
                    game_state = "PLAYING"
                elif game_state != "UPGRADE":
                    action_triggered = True

            if game_state == "UPGRADE":
                if event.key == pygame.K_1:
                    sfx_card_draw.play()
                    apply_selected_upgrade(current_choices[0])
                elif event.key == pygame.K_2:
                    sfx_card_draw.play()
                    apply_selected_upgrade(current_choices[1])

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if game_state == "MAIN_MENU":
                if play_btn_rect.collidepoint(mouse_pos):
                    sfx_select.play()
                    reset_game()
            elif game_state == "PLAYING":
                if pause_btn_rect.collidepoint(mouse_pos):
                    sfx_select.play()
                    game_state = "PAUSED"
                else:
                    action_triggered = True
            elif game_state == "PAUSED":
                if pause_btn_rect.collidepoint(mouse_pos):
                    sfx_select.play()
                    game_state = "PLAYING"
            elif game_state == "GAME_OVER":
                if game_over_menu_btn_rect.collidepoint(mouse_pos):
                    sfx_select.play()
                    game_state = "MAIN_MENU"
                    if not pygame.mixer.music.get_busy():
                        pygame.mixer.music.play(-1)
                else:
                    sfx_select.play()
                    reset_game()
            elif game_state == "UPGRADE":
                for i, rect in enumerate(card_rects):
                    if rect.collidepoint(mouse_pos):
                        sfx_card_draw.play()
                        apply_selected_upgrade(current_choices[i])
                        break
            elif game_state == "SECRET_QUIZ" and car_arrived:
                if not quiz_answered:
                    for idx, rect in enumerate(quiz_choice_rects):
                        if rect.collidepoint(mouse_pos):
                            sfx_select.play()
                            quiz_answered = True
                            chosen = quiz_options[idx]

                            if chosen["correct"]:
                                reward_text = grant_easter_egg_reward()
                                quiz_result_msg = f"TAMA! Natanggap: {reward_text}"
                                
                            else:
                                quiz_result_msg = "MALI! Walang buff para sa 'yo, tyaga muna."

                            quiz_result_timer = 180  # ~3 seconds display

    # --- CORE GAMEPLAY LOGIC ---
    if game_state == "PLAYING":
        if kick_cooldown > 0: kick_cooldown -= 1

        if action_triggered and kick_cooldown <= 0:
            is_kicking = True
            kick_timer = KICK_DURATION 
            kick_cooldown = COOLDOWN_DURATION
            current_kick_img = kick_high_img
            
            hit_success = False
            multiplier = 1.0

            if perfect_zone_y <= sipa_y + sipa_radius <= perfect_zone_y + perfect_zone_height:
                sipa_vel_y = bounce_power * 1.2
                current_kick_img = kick_perfect_img
                hit_success = True
            elif hit_zone_y <= sipa_y + sipa_radius <= hit_zone_y + hit_zone_height:
                sipa_vel_y = bounce_power
                current_kick_img = kick_high_img if (sipa_y + sipa_radius) < perfect_zone_y else kick_low_img
                hit_success = True

            if hit_success:
                sfx_kick.play()
                yelo_timer = 0 # Breaks freeze if kicked
                is_rising = True
                points_earned_this_kick = max(0, int((hit_zone_y - sipa_y) // PIXELS_PER_METER))
                
                # Doble Metro Logic
                meter_gain = 2 if random.random() < doble_metro_chance else 1
                kicks_landed += meter_gain
                
                if kicks_landed >= kicks_required:
                    # Check RNG for the secret encounter
                    if random.random() < SECRET_UPGRADE_CHANCE:
                        sfx_card_fan.play()
                        car_x = -350
                        car_arrived = False
                        quiz_answered = False
                        quiz_result_msg = ""
                        quiz_result_timer = 0
                        game_state = "SECRET_QUIZ"

                    else:
                        sfx_card_fan.play()
                        upgrade_picks_remaining = 2 if random.random() < anting_chance else 1
                        generate_upgrades()
                        game_state = "UPGRADE"

        # Yelo Physics Override
        if yelo_timer > 0:
            yelo_timer -= 1
            sipa_vel_y = 0
        else:
            sipa_vel_y += gravity
            
        distance_to_zone = hit_zone_y - sipa_y
        if distance_to_zone > 150:
            if sipa_vel_y > 50: sipa_vel_y = 50
        else:
            if sipa_vel_y > 7: sipa_vel_y -= 3 
            
        sipa_y += sipa_vel_y

        # Dynamic Sipa Rotation / Tumble
        if sipa_vel_y < 0:
            # Rising: Fast, energetic spin
            sipa_angle = (sipa_angle + 12) % 360
        else:
            # Falling: Smoothly rights itself face-down (0 degrees) with a slight wobble
            target_angle = 0
            # Slerp/ease rotation back toward 0 degrees
            diff = (target_angle - sipa_angle + 180) % 360 - 180
            sipa_angle += diff * 0.1

        target_camera_y = sipa_y - (dis_height // 2)
        camera_y = target_camera_y
        if camera_y > 0: camera_y = 0
            
        if is_rising:
            current_meters = max(0, int((hit_zone_y - sipa_y) // PIXELS_PER_METER))
            if current_meters > points_earned_this_kick:
                gained = current_meters - points_earned_this_kick
                
                # Doble Puntos Logic
                if double_score_kicks_left > 0: gained *= 2
                
                score += gained
                points_earned_this_kick = current_meters

            if sipa_vel_y >= 0: 
                is_rising = False
                if double_score_kicks_left > 0: double_score_kicks_left -= 1
                if points_earned_this_kick < 1:
                    score += (2 if double_score_kicks_left > 0 else 1)
                    points_earned_this_kick = 1
                feedback_text = f"LUPIT! +{points_earned_this_kick}m" if points_earned_this_kick > 3 else f"AYOS! +{points_earned_this_kick}m"
                feedback_timer = 40

        # Ground Collision & Extra Buhay Check
        if sipa_y > dis_height: 
            if extra_lives > 0:
                extra_lives -= 1

                if sfx_revive:
                    sfx_revive.play()

                sipa_y = dis_height - 150
                sipa_vel_y = bounce_power * 1.5 # Auto bounce back
                feedback_text = "EXTRA BUHAY!"
                feedback_timer = 60
            else:
                sfx_fah.play()
                if score > highscore:
                    highscore = score
                    save_highscore(highscore)
                game_state = "GAME_OVER"


    screen.fill(black) 
    

    if game_state == "MAIN_MENU":
        if bgs_loaded:
            screen.blit(bg_tower[0], (0, 0))

        # --- UPDATE & RENDER MENU BIRD ---
        bird_timer += 0.08
        bird_x += bird_speed
        
        # Subtle bobbing up and down to mimic wing flaps
        import math
        bird_y = bird_base_y + int(math.sin(bird_timer * 2) * 8)

        # Reset across the screen once it flies off the right edge
        if bird_x > dis_width + 80:
            bird_x = -60
            bird_base_y = random.randint(80, 220)  # Randomize flight height each pass

        if bird_loaded:
            screen.blit(bird_img, (bird_x, bird_y))
        else:
            # Fallback placeholder if bird.png isn't saved yet
            pygame.draw.ellipse(screen, (139, 69, 19), (bird_x, bird_y, 30, 16))

    elif game_state != "MAIN_MENU":
        if bgs_loaded:
            first_visible = int(abs(camera_y) // dis_height)
            for block_idx in range(first_visible, first_visible + 2):
                t1_blk = int((THRESHOLD_1 * PIXELS_PER_METER) / dis_height) 
                t2_blk = int((THRESHOLD_2 * PIXELS_PER_METER) / dis_height) 
                
                if block_idx == 0: img = bg_tower[0]
                elif block_idx < t1_blk: img = bg_tower[1] 
                elif block_idx == t1_blk: img = bg_tower[2] 
                elif block_idx < t2_blk: img = bg_tower[3] 
                elif block_idx == t2_blk: img = bg_tower[4] 
                else: img = bg_tower[5] 
                    
                screen_y = -(block_idx * dis_height) - camera_y
                screen.blit(img, (0, int(screen_y)))
        else:
            pygame.draw.rect(screen, sky_blue, pygame.Rect(0, -dis_height - camera_y, dis_width, dis_height))


    if game_state in ["PLAYING", "PAUSED", "GAME_OVER", "UPGRADE"]:
        if assets_loaded:
            if is_kicking:
                screen.blit(current_kick_img, (char_x, char_y - camera_y))
                kick_timer -= 1
                if kick_timer <= 0: is_kicking = False
            else: screen.blit(idle_img, (char_x, char_y - camera_y))
        else: pygame.draw.rect(screen, (100, 100, 100), (char_x, char_y - camera_y, char_width, char_height))

        zone_col = green if perfect_zone_y <= sipa_y + sipa_radius <= perfect_zone_y + perfect_zone_height else yellow
        pygame.draw.rect(screen, zone_col, (dis_width//2 - hit_zone_width//2, hit_zone_y - camera_y, hit_zone_width, hit_zone_height), 2)
        pygame.draw.rect(screen, green, (dis_width//2 - hit_zone_width//2, perfect_zone_y - camera_y, hit_zone_width, perfect_zone_height))

        if assets_loaded:
            # Rotate sipa around its center
            rotated_sipa = pygame.transform.rotate(sipa_img, sipa_angle)
            rot_rect = rotated_sipa.get_rect(center=(int(sipa_x), int(sipa_y) - camera_y))
            
            if yelo_timer > 0: 
                pygame.draw.circle(screen, sky_blue, (int(sipa_x), int(sipa_y) - camera_y), sipa_radius + 5, 3)
            
            screen.blit(rotated_sipa, rot_rect.topleft)
        else: 
            pygame.draw.circle(screen, red, (int(sipa_x), int(sipa_y) - camera_y), sipa_radius)

    if game_state == "MAIN_MENU":
        import math
        menu_timer += 0.05
        # Subtle retro floating / bobbing effect (moves 6 pixels up and down)
        float_y = int(math.sin(menu_timer) * 6)
        
        # Center target position
        logo_center_x = dis_width // 2
        logo_center_y = 130 + float_y

        if logo_loaded:
            # Perfectly centers the PNG on screen
            logo_rect = logo_img.get_rect(center=(logo_center_x, logo_center_y))
            screen.blit(logo_img, logo_rect)
        else:
            # Fallback text if logo.png is missing
            title_text = font_title.render("SIPA at tyaga", True, yellow)
            title_shadow = font_title.render("SIPA at tyaga", True, black)
            
            # Shadow
            screen.blit(title_shadow, (logo_center_x - title_text.get_width()//2 + 3, logo_center_y - 20 + 3))
            # Text
            screen.blit(title_text, (logo_center_x - title_text.get_width()//2, logo_center_y - 20))

        # High Score text below logo
        hs_text = font_title.render(f"High Score: {highscore}", True, red)
        screen.blit(hs_text, (dis_width // 2 - hs_text.get_width() // 2, 250))

        # Play Button (Centered)
        play_btn_rect.center = (dis_width // 2, 350)
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = play_btn_rect.collidepoint(mouse_pos)
        
        btn_color = (80, 255, 80) if is_hovered else green
        pygame.draw.rect(screen, btn_color, play_btn_rect, border_radius=6)
        pygame.draw.rect(screen, white, play_btn_rect, 3, border_radius=6)
        
        play_label = "> PLAY <" if is_hovered else "PLAY"
        play_text = font_button.render(play_label, True, black)
        screen.blit(play_text, (play_btn_rect.centerx - play_text.get_width() // 2, 
                                play_btn_rect.centery - play_text.get_height() // 2))

    elif game_state in ["PLAYING", "PAUSED"]:
        hud_color = white if camera_y < -dis_height else black

        screen.blit(font_hud.render(f"Score: {score}", True, hud_color), (20, 20))
        screen.blit(font_card.render(f"Alt: {max(0, int((hit_zone_y - sipa_y) // PIXELS_PER_METER))}m", True, hud_color), (20, 60))
        screen.blit(font_card.render(f"Upgrades: {upgrades_acquired}", True, hud_color), (20, 160))
        if yelo_inventory > 0: screen.blit(font_card.render(f"Yelo: {yelo_inventory} (Press Y)", True, sky_blue), (20, 100))
        if extra_lives > 0: screen.blit(font_card.render("Extra Buhay: Active", True, green), (20, 130))

        # Meter
        fill_ratio = kicks_landed / kicks_required
        fill_y = 100 + (200 - int(fill_ratio * 200))
        pygame.draw.rect(screen, black, (dis_width - 60, 100, 20, 200), 2)
        pygame.draw.rect(screen, red, (dis_width - 60, fill_y, 20, int(fill_ratio * 200)))
        screen.blit(font_card.render("Next Upgrade:", True, hud_color), (840, 75))

        pygame.draw.rect(screen, (50, 50, 50), pause_btn_rect)
        pygame.draw.rect(screen, white, pause_btn_rect, 2)
        screen.blit(font_card.render("PAUSE (P)", True, white), (pause_btn_rect.x + 10, pause_btn_rect.y + 8))

        if feedback_timer > 0 and game_state == "PLAYING":
            col = green if "EXTRA" in feedback_text else (red if "LUPIT" in feedback_text else yellow)
            feed_surface = font_hud.render(feedback_text, True, col)
            screen.blit(feed_surface, (char_x - 10, char_y - 40 - camera_y))
            feedback_timer -= 1

        if game_state == "PAUSED":
            overlay = pygame.Surface((dis_width, dis_height))
            overlay.set_alpha(180)
            overlay.fill(black)
            screen.blit(overlay, (0, 0))
            
            screen.blit(font_pause.render("TAYMPERS", True, yellow), (dis_width//2 - 200, dis_height//2 - 50))
        
    elif game_state == "UPGRADE":
        overlay = pygame.Surface((dis_width, dis_height))
        overlay.set_alpha(200)
        overlay.fill(black)
        screen.blit(overlay, (0, 0))
        
        title = font_title.render("SARI-SARI STORE", True, yellow)
        screen.blit(title, (dis_width//2 - title.get_width()//2, 50))
        if upgrade_picks_remaining > 1:
            sub = font_card.render("Anting-Anting Triggered! Pick 2 Cards!", True, sky_blue)
            screen.blit(sub, (dis_width//2 - sub.get_width()//2, 90))

        # DRAW THE 2 CARDS
        for i, rect in enumerate(card_rects):
            choice = current_choices[i]
            card_col = rarity_colors[choice["rarity"]]
            
            # Draw the Card Background
            if choice["id"] in card_images:
                screen.blit(card_images[choice["id"]], (rect.x, rect.y))
                # Optional: Still draw the border around your PNG to show rarity
                pygame.draw.rect(screen, card_col, rect, 4)
            else:
                # Fallback if PNG is missing
                pygame.draw.rect(screen, (30, 30, 30), rect) 
                pygame.draw.rect(screen, card_col, rect, 4)  
                
                name_txt   = font_card.render(choice["name"], True, white)
                rarity_txt = font_sub.render(choice["rarity"], True, card_col)
                desc_txt   = font_card.render(choice["desc"], True, white)
                key_txt    = font_sub.render(f"Press {i+1}", True, yellow)

    elif game_state == "CAR_CUTSCENE":

        if car_x < car_target_x:
            car_x += car_speed
            if car_x >= car_target_x:
                car_x = car_target_x
        else:
           
            car_wait_timer -= 1
            if car_wait_timer <= 0:
                
                if pwede_loaded:
                    sfx_pwede.play()
                game_state = "SECRET_QUIZ"

        car_draw_y = dis_height - 180
        if car_img:
            screen.blit(car_img, (car_x, car_draw_y))
        else:
            # Fallback box kung wala pang car sprite
            pygame.draw.rect(screen, (40, 40, 180), (car_x, car_draw_y + 30, 220, 70), border_radius=8)
            pygame.draw.rect(screen, (80, 80, 240), (car_x + 35, car_draw_y, 140, 45), border_radius=6)

    elif game_state == "SECRET_QUIZ":
        car_draw_y = dis_height - 180


        if car_x < car_target_x:
            car_x += car_speed
            if car_x >= car_target_x:
                car_x = car_target_x
                car_arrived = True

                if pwede_loaded:
                    sfx_pwede.play()

        # 2. Draw the car
        if car_img:
            screen.blit(car_img, (car_x, car_draw_y))
        else:
            pygame.draw.rect(screen, (40, 40, 180), (car_x, car_draw_y + 30, 220, 70), border_radius=8)

        if car_arrived:
            modal_overlay = pygame.Surface((dis_width, dis_height), pygame.SRCALPHA)
            modal_overlay.fill((0, 0, 0, 200))
            screen.blit(modal_overlay, (0, 0))

            dialog_rect = pygame.Rect(dis_width // 2 - 280, 130, 560, 340)
            pygame.draw.rect(screen, (24, 24, 24), dialog_rect, border_radius=10)
            pygame.draw.rect(screen, yellow, dialog_rect, 3, border_radius=10)

            title_surf = font_sub.render("- SECRET ENCOUNTER: PWEDE MAG TANONG? -", True, sky_blue)
            screen.blit(title_surf, (dialog_rect.centerx - title_surf.get_width() // 2, dialog_rect.y + 20))

            q_surf = font_card.render(quiz_question, True, white)
            screen.blit(q_surf, (dialog_rect.centerx - q_surf.get_width() // 2, dialog_rect.y + 60))

            mouse_pos = pygame.mouse.get_pos()
            for idx, rect in enumerate(quiz_choice_rects):
                is_hovered = rect.collidepoint(mouse_pos) and not quiz_answered
                fill_col = (55, 55, 55) if is_hovered else (35, 35, 35)
                border_col = yellow if is_hovered else (160, 160, 160)

                pygame.draw.rect(screen, fill_col, rect, border_radius=6)
                pygame.draw.rect(screen, border_col, rect, 2, border_radius=6)

                choice_text = font_card.render(quiz_options[idx]["text"], True, white)
                screen.blit(choice_text, (rect.x + 18, rect.centery - choice_text.get_height() // 2))

            if quiz_answered:
                res_col = green if "TAMA" in quiz_result_msg else red
                res_surf = font_sub.render(quiz_result_msg, True, res_col)
                screen.blit(res_surf, (dialog_rect.centerx - res_surf.get_width() // 2, dialog_rect.bottom - 40))

                quiz_result_timer -= 1
                if quiz_result_timer <= 0:
                    if pwede_loaded:
                        sfx_pwede.stop()
                    kicks_landed = 0
                    kicks_required += 2
                    total_upgrades_bought += 1
                    game_state = "PLAYING"

    elif game_state == "GAME_OVER":
        hud_color = white if camera_y < -dis_height else black
        overlay = pygame.Surface((dis_width, dis_height))
        overlay.set_alpha(180)
        overlay.fill(black)
        screen.blit(overlay, (0, 0))

        over_text    = font_title.render("OLAATS! GAME OVER", True, red)
        screen.blit(over_text, (dis_width // 2 - over_text.get_width() // 2, dis_height // 3 - 40))
        final_score  = font_hud.render(f"Final Score: {score}", True, hud_color)
        screen.blit(final_score, (dis_width // 2 - final_score.get_width() // 2, dis_height // 2 - 30))
        best_score   = font_sub.render(f"Best: {highscore}", True, yellow)
        screen.blit(best_score, (dis_width // 2 - best_score.get_width() // 2, dis_height // 2 + 10))
        restart_text = font_button.render("Isa Pa? Click screen or Press SPACE", True, white)
        screen.blit(restart_text, (dis_width // 2 - restart_text.get_width() // 2, dis_height // 2 + 45))
        quit_text = font_quit.render("Uwi na sabi ni MAMA - (Q)Quit", True, white)
        screen.blit(quit_text, (dis_width // 2 - quit_text.get_width() // 2, dis_height // 2 + 85)) 

        # Menu Button
        pygame.draw.rect(screen, (50, 50, 50), game_over_menu_btn_rect)
        pygame.draw.rect(screen, white, game_over_menu_btn_rect, 2)
        menu_btn_text = font_card.render("MAIN MENU", True, white)
        screen.blit(menu_btn_text, (game_over_menu_btn_rect.centerx - menu_btn_text.get_width()//2, 
                                    game_over_menu_btn_rect.centery - menu_btn_text.get_height()//2))

    pygame.display.flip()
    clock.tick(FPS)