# game setup
WIDTH    = 1280	
HEIGTH   = 720
FPS      = 60
TILESIZE = 64

BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = '../texture/font/joystix.ttf'
UI_FONT_SIZE = 18

WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
EXPERIENCE_BACKGROUND = '#B6CD4A'
UI_BORDER_COLOR_ACTIVE = 'gold'

weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15, 'graphic': '../texture/weapons/sword/full.png'},
    'lance': {'cooldown': 400, 'damage': 30, 'graphic': '../texture/weapons/lance/full.png'},
    'axe': {'cooldown': 300, 'damage': 20, 'graphic': '../texture/weapons/axe/full.png'},
    'rapier': {'cooldown': 50, 'damage':8, 'graphic': '../texture/weapons/rapier/full.png'},
    'sai': {'cooldown': 80, 'damage': 10, 'graphic': '../texture/weapons/sai/full.png'}
}

magic_data ={
    'flame': {'strength': 5, 'cost': 20, 'graphics': '../texture/particles/flame/fire.png'},
    'heal': {'strength': 20, 'cost': 20, 'graphics': '../texture/particles/heal/heal.png'}
}