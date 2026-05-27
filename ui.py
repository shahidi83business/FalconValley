# ui.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class UI:
    @staticmethod
    def get_market_selection(unlocked_markets: list, base_markets: list):
        """ساخت منوی انتخاب مارکت بر اساس مارکت‌های باز شده کاربر"""
        buttons = []
        # اضافه کردن مارکت‌های پایه
        for m in base_markets:
            buttons.append([InlineKeyboardButton(text=f"🛒 {m.capitalize()} Market", callback_data=f"market_{m}")])
        
        # اضافه کردن مارکت‌های آنلاک شده (AI یا پرو)
        for m_id in unlocked_markets:
            buttons.append([InlineKeyboardButton(text=f"💎 {m_id.replace('_', ' ').title()}", callback_data=f"market_{m_id}")])
            
        # دکمه ساخت مارکت جدید (اگر شرایط را دارد)
        buttons.append([InlineKeyboardButton(text="🧠 Generate New Market (AI)", callback_data="market_gen_start")])
        
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @staticmethod
    def get_strategy_buttons():
        """انتخاب استراتژی اولیه: مذاکره یا جنگ"""
        buttons = [[
            InlineKeyboardButton(text="🤝 Negotiation", callback_data="strat_negotiation"),
            InlineKeyboardButton(text="⚔️ War", callback_data="strat_war")
        ]]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @staticmethod
    def get_negotiation_buttons():
        """دکمه‌های همکاری یا خیانت در فاز تصمیم‌گیری مذاکره"""
        buttons = [[
            InlineKeyboardButton(text="✅ Cooperate", callback_data="choice_cooperate"),
            InlineKeyboardButton(text="❌ Defect", callback_data="choice_defect")
        ]]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @staticmethod
    def get_chicken_buttons():
        """دکمه‌های فاز جنگ (Chicken Game)"""
        buttons = [[
            InlineKeyboardButton(text="🕊 Yield (کوتاه آمدن)", callback_data="war_yield"),
            InlineKeyboardButton(text="🏎 Straight (ادامه دادن)", callback_data="war_straight")
        ]]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @staticmethod
    def get_profile_menu():
        """دکمه‌های ویرایش پروفایل"""
        buttons = [
            [
                InlineKeyboardButton(text="📝 First Name", callback_data="edit_first_name"),
                InlineKeyboardButton(text="📝 Last Name", callback_data="edit_last_name")
            ],
            [InlineKeyboardButton(text="✍️ Edit Bio", callback_data="edit_bio")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @staticmethod
    def get_main_menu():
        """منوی شروع اصلی"""
        buttons = [
            [InlineKeyboardButton(text="🎮 Play Now", callback_data="menu_play")],
            [InlineKeyboardButton(text="👤 My Profile", callback_data="menu_profile")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)
