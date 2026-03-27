from PIL import Image, ImageDraw, ImageFont
import os

# Пути
references_dir = 'D:/video/references'
output_dir = 'D:/video'

# Данные для рейдов
raid_data = {
    'wood_wall': {
        'name': 'Wooden Wall',
        'hp': 200,
        'timed_charges': 13,
        'satchels': 3,
        'explosive_ammo': 48,
        'rockets': 2,
        'c4': 1
    },
    'stone_wall': {
        'name': 'Stone Wall',
        'hp': 500,
        'timed_charges': 46,
        'satchels': 10,
        'explosive_ammo': 182,
        'rockets': 4,
        'c4': 2
    },
    'metal_wall': {
        'name': 'Metal Wall',
        'hp': 1000,
        'timed_charges': 112,
        'satchels': 23,
        'explosive_ammo': 399,
        'rockets': 8,
        'c4': 4
    },
    'armored_wall': {
        'name': 'Armored Wall (HQM)',
        'hp': 2000,
        'timed_charges': 223,
        'satchels': 46,
        'explosive_ammo': 798,
        'rockets': 16,
        'c4': 8
    },
    'wood_door': {
        'name': 'Wooden Door',
        'hp': 200,
        'timed_charges': 6,
        'satchels': 2,
        'explosive_ammo': 18,
        'rockets': 1,
        'c4': 1
    },
    'metal_door': {
        'name': 'Metal Door',
        'hp': 800,
        'timed_charges': 18,
        'satchels': 4,
        'explosive_ammo': 63,
        'rockets': 2,
        'c4': 1
    },
    'garage_door': {
        'name': 'Garage Door',
        'hp': 1500,
        'timed_charges': 42,
        'satchels': 9,
        'explosive_ammo': 150,
        'rockets': 3,
        'c4': 2
    }
}

# Иконки ресурсов
RESOURCE_ICONS = {
    'timed_charges': 'timed_charge_ref.png',
    'satchels': 'satchel_ref.png',
    'explosive_ammo': 'explosive_ammo_ref.png',
    'rockets': 'rocket_ref.png',
    'c4': 'c4_ref.png'
}

def load_icon(icon_name):
    """Загружает иконку и изменяет её размер"""
    icon_path = os.path.join(references_dir, icon_name)
    if os.path.exists(icon_path):
        icon = Image.open(icon_path).convert('RGBA')
        # Изменяем размер до 32x32
        icon = icon.resize((32, 32), Image.Resampling.LANCZOS)
        return icon
    return None

def create_raid_image(key, data):
    # Путь к референсу структуры
    ref_path = os.path.join(references_dir, f'{key}_ref.png')
    
    # Открываем референс структуры
    if os.path.exists(ref_path):
        bg_img = Image.open(ref_path).convert('RGBA')
        # Изменяем размер до 640x360 если нужно
        if bg_img.size != (640, 360):
            bg_img = bg_img.resize((640, 360), Image.Resampling.LANCZOS)
    else:
        print(f"⚠️  Референс не найден: {ref_path}")
        bg_img = Image.new('RGBA', (640, 360), (40, 40, 40, 255))
    
    # Создаём прозрачный слой для текста и иконок
    overlay = Image.new('RGBA', bg_img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Заголовок (сверху по центру)
    title = f"{data['name']} - {data['hp']} HP"
    try:
        title_font = ImageFont.truetype("arial.ttf", 28)
    except:
        title_font = ImageFont.load_default()
    
    draw.text((320, 25), title, fill='white', anchor='mm', font=title_font)
    
    # Полоска HP
    hp_width = 400
    hp_height = 20
    hp_x = (640 - hp_width) // 2
    hp_y = 50
    draw.rectangle([hp_x, hp_y, hp_x + hp_width, hp_y + hp_height], fill=(255, 0, 0, 200))
    
    # Загружаем иконки
    icons = {}
    for res_name, icon_file in RESOURCE_ICONS.items():
        icons[res_name] = load_icon(icon_file)
    
    # Ресурсы (слева) с иконками
    resources_y = 90
    resource_items = [
        ('timed_charges', f"{data['timed_charges']} Timed Charges"),
        ('satchels', f"{data['satchels']} Satchels"),
        ('explosive_ammo', f"{data['explosive_ammo']} Explosive Ammo"),
        ('rockets', f"{data['rockets']} Rockets"),
        ('c4', f"{data['c4']} C4")
    ]
    
    try:
        text_font = ImageFont.truetype("arial.ttf", 20)
    except:
        text_font = ImageFont.load_default()
    
    for icon_key, text in resource_items:
        # Вставляем иконку
        icon = icons.get(icon_key)
        if icon:
            overlay.paste(icon, (20, resources_y), icon)
        # Рисуем текст
        draw.text((60, resources_y + 6), text, fill='white', font=text_font)
        resources_y += 50
    
    # Объединяем фон и оверлей
    result = Image.alpha_composite(bg_img, overlay)
    
    # Сохраняем
    output_path = os.path.join(output_dir, f'{key}.png')
    result.convert('RGB').save(output_path, 'PNG')
    print(f"✅ Создано: {output_path}")

# Создаем все 7 изображений
print("🎨 Создание изображений для рейдов с иконками...\n")
for key, data in raid_data.items():
    create_raid_image(key, data)

print(f"\n🎉 Все 7 изображений созданы в папке {output_dir}/")
print("\nТеперь загрузите их на GitHub в папку images/")