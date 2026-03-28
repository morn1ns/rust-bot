import logging
from telebot import TeleBot, types
import os
from pathlib import Path
import time

logging.basicConfig(level=logging.INFO)

# Получаем токен
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    print("❌ ОШИБКА: BOT_TOKEN не найден!")
    exit(1)

print(f"✅ Токен получен: {BOT_TOKEN[:10]}...") # v2

bot = TeleBot(BOT_TOKEN)

# Путь к картинкам (в корне репозитория)
BASE_DIR = Path(__file__).parent

# Словарь с именами картинок (8 структур!)
STRUCTURE_IMAGES = {
    'wood_wall': 'wood_wall.png',
    'stone_wall': 'stone_wall.png',
    'metal_wall': 'metal_wall.png',
    'armored_wall': 'armored_wall.png',
    'wood_door': 'wood_door.png',
    'metal_door': 'metal_door.png',
    'garage_door': 'garage_door.png',
    'armored_door': 'armored_door.png'  # НОВАЯ!
}

RAID_DATA = {
    'wood_wall': {
        'name': '🪵 Деревянная стена',
        'health': 200,
        'methods': {
            'bobovki': {'count': 13, 'sulfur': 2600, 'powder': 1300},
            'satchels': {'count': 3, 'sulfur': 1440, 'powder': 720},
            'explosive_ammo': {'count': 48, 'sulfur': 1200, 'powder': 480},
            'rockets': {'count': 2, 'sulfur': 2800, 'powder': 960},
            'c4': {'count': 1, 'sulfur': 2200, 'powder': 480}
        }
    },
    'stone_wall': {
        'name': '🪨 Каменная стена',
        'health': 500,
        'methods': {
            'bobovki': {'count': 46, 'sulfur': 9200, 'powder': 4600},
            'satchels': {'count': 10, 'sulfur': 4800, 'powder': 2400},
            'explosive_ammo': {'count': 182, 'sulfur': 4550, 'powder': 1820},
            'rockets': {'count': 4, 'sulfur': 5600, 'powder': 1920},
            'c4': {'count': 2, 'sulfur': 4400, 'powder': 960}
        }
    },
    'metal_wall': {
        'name': '🔩 Железная стена',
        'health': 1000,
        'methods': {
            'bobovki': {'count': 112, 'sulfur': 22400, 'powder': 11200},
            'satchels': {'count': 23, 'sulfur': 11040, 'powder': 5520},
            'explosive_ammo': {'count': 399, 'sulfur': 9975, 'powder': 3990},
            'rockets': {'count': 8, 'sulfur': 11200, 'powder': 3840},
            'c4': {'count': 4, 'sulfur': 8800, 'powder': 1920}
        }
    },
    'armored_wall': {
        'name': '🏛️ МВК стена',
        'health': 2000,
        'methods': {
            'bobovki': {'count': 223, 'sulfur': 44600, 'powder': 22300},
            'satchels': {'count': 46, 'sulfur': 22080, 'powder': 11040},
            'explosive_ammo': {'count': 798, 'sulfur': 19950, 'powder': 7980},
            'rockets': {'count': 16, 'sulfur': 22400, 'powder': 7680},
            'c4': {'count': 8, 'sulfur': 17600, 'powder': 3840}
        }
    },
    'wood_door': {
        'name': '🚪 Деревянная дверь',
        'health': 200,
        'methods': {
            'bobovki': {'count': 6, 'sulfur': 1200, 'powder': 600},
            'satchels': {'count': 2, 'sulfur': 960, 'powder': 480},
            'explosive_ammo': {'count': 18, 'sulfur': 450, 'powder': 180},
            'rockets': {'count': 1, 'sulfur': 1400, 'powder': 480},
            'c4': {'count': 1, 'sulfur': 2200, 'powder': 480}
        }
    },
    'metal_door': {
        'name': '🚪 Железная дверь',
        'health': 800,
        'methods': {
            'bobovki': {'count': 18, 'sulfur': 3600, 'powder': 1800},
            'satchels': {'count': 4, 'sulfur': 1920, 'powder': 960},
            'explosive_ammo': {'count': 63, 'sulfur': 1575, 'powder': 630},
            'rockets': {'count': 2, 'sulfur': 2800, 'powder': 960},
            'c4': {'count': 1, 'sulfur': 2200, 'powder': 480}
        }
    },
    'garage_door': {
        'name': '🏭 Гаражная дверь',
        'health': 1500,
        'methods': {
            'bobovki': {'count': 42, 'sulfur': 8400, 'powder': 4200},
            'satchels': {'count': 9, 'sulfur': 4320, 'powder': 2160},
            'explosive_ammo': {'count': 150, 'sulfur': 3750, 'powder': 1500},
            'rockets': {'count': 3, 'sulfur': 4200, 'powder': 1440},
            'c4': {'count': 2, 'sulfur': 4400, 'powder': 960}
        }
    },
    'armored_door': {  # НОВАЯ МВК ДВЕРЬ!
        'name': '🏛️ МВК дверь',
        'health': 2000,
        'methods': {
            'bobovki': {'count': 223, 'sulfur': 44600, 'powder': 22300},
            'satchels': {'count': 46, 'sulfur': 22080, 'powder': 11040},
            'explosive_ammo': {'count': 798, 'sulfur': 19950, 'powder': 7980},
            'rockets': {'count': 16, 'sulfur': 22400, 'powder': 7680},
            'c4': {'count': 8, 'sulfur': 17600, 'powder': 3840}
        }
    }
}

def get_image_path(structure_key):
    """Возвращает путь к изображению структуры"""
    image_name = STRUCTURE_IMAGES.get(structure_key)
    if image_name:
        return BASE_DIR / image_name
    return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("🪵 Деревянная стена", callback_data="wood_wall"),
        types.InlineKeyboardButton("🪨 Каменная стена", callback_data="stone_wall"),
        types.InlineKeyboardButton("🔩 Железная стена", callback_data="metal_wall"),
        types.InlineKeyboardButton("🏛️ МВК стена", callback_data="armored_wall"),
        types.InlineKeyboardButton("🚪 Деревянная дверь", callback_data="wood_door"),
        types.InlineKeyboardButton("🚪 Железная дверь", callback_data="metal_door"),
        types.InlineKeyboardButton("🏭 Гаражная дверь", callback_data="garage_door"),
        types.InlineKeyboardButton("🏛️ МВК дверь", callback_data="armored_door"),  # НОВАЯ!
    ]
    markup.add(*buttons)
    
    bot.send_message(message.chat.id, 
        "🎮 **Rust Raid Helper** 🎮\n\n"
        "📊 Актуальные данные по рейдам\n\n"
        "Выберите структуру:", 
        reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data in RAID_DATA)
def show_raid_info(call):
    structure_key = call.data
    structure = RAID_DATA[structure_key]
    methods = structure['methods']
    
    try:
        image_path = get_image_path(structure_key)
        if image_path and image_path.exists():
            with open(image_path, 'rb') as img_file:
                caption = (
                    f"💥 **СПОСОБЫ БАБАХА:**\n\n"
                    f"🟡 **Бобовки:** `{methods['bobovki']['count']}` шт.\n"
                    f"   💰 Сера: `{methods['bobovki']['sulfur']:,}` | ⚫ Порох: `{methods['bobovki']['powder']:,}`\n\n"
                    f"🎒 **Сачель:** `{methods['satchels']['count']}` шт.\n"
                    f"   💰 Сера: `{methods['satchels']['sulfur']:,}` | ⚫ Порох: `{methods['satchels']['powder']:,}`\n\n"
                    f"🔫 **Разрывные патроны:** `{methods['explosive_ammo']['count']}` шт.\n"
                    f"   💰 Сера: `{methods['explosive_ammo']['sulfur']:,}` | ⚫ Порох: `{methods['explosive_ammo']['powder']:,}`\n\n"
                    f"🚀 **Ракеты:** `{methods['rockets']['count']}` шт.\n"
                    f"   💰 Сера: `{methods['rockets']['sulfur']:,}` | ⚫ Порох: `{methods['rockets']['powder']:,}`\n\n"
                    f"💥 **C4:** `{methods['c4']['count']}` шт.\n"
                    f"   💰 Сера: `{methods['c4']['sulfur']:,}` | ⚫ Порох: `{methods['c4']['powder']:,}`"
                )
                
                bot.send_photo(
                    call.message.chat.id,
                    img_file,
                    caption=caption,
                    parse_mode='Markdown',
                    reply_markup=types.InlineKeyboardMarkup().add(
                        types.InlineKeyboardButton("🔙 Назад", callback_data="back")
                    )
                )
        else:
            raise FileNotFoundError("Image not found")
    except Exception as e:
        print(f"⚠️ Ошибка отправки картинки: {e}")
        caption = (
            f"{structure['name']}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💚 **HP:** {structure['health']}\n\n"
            f"💥 **СПОСОБЫ БАБАХА:**\n\n"
            f"🟡 **Бобовки:** `{methods['bobovki']['count']}` шт.\n"
            f"   💰 Сера: `{methods['bobovki']['sulfur']:,}` | ⚫ Порох: `{methods['bobovki']['powder']:,}`\n\n"
            f"🎒 **Сачель:** `{methods['satchels']['count']}` шт.\n"
            f"   💰 Сера: `{methods['satchels']['sulfur']:,}` | ⚫ Порох: `{methods['satchels']['powder']:,}`\n\n"
            f"🔫 **Разрывные патроны:** `{methods['explosive_ammo']['count']}` шт.\n"
            f"   💰 Сера: `{methods['explosive_ammo']['sulfur']:,}` | ⚫ Порох: `{methods['explosive_ammo']['powder']:,}`\n\n"
            f"🚀 **Ракеты:** `{methods['rockets']['count']}` шт.\n"
            f"   💰 Сера: `{methods['rockets']['sulfur']:,}` | ⚫ Порох: `{methods['rockets']['powder']:,}`\n\n"
            f"💥 **C4:** `{methods['c4']['count']}` шт.\n"
            f"   💰 Сера: `{methods['c4']['sulfur']:,}` | ⚫ Порох: `{methods['c4']['powder']:,}`\n"
            f"━━━━━━━━━━━━━━━━━━━━"
        )
        
        bot.send_message(
            call.message.chat.id,
            caption,
            parse_mode='Markdown',
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("🔙 Назад", callback_data="back")
            )
        )
    
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "back")
def go_back(call):
    bot.answer_callback_query(call.id)
    send_welcome(call.message)

if __name__ == '__main__':
    print("🤖 Rust Raid Bot запущен на Railway!")
    try:
        bot.infinity_polling(
            none_stop=True,
            interval=3,
            timeout=60,
            long_polling_timeout=60
        )
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        time.sleep(5)
