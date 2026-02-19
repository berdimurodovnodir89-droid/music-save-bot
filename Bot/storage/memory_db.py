# Kategoriyalar
CATEGORIES = ["Ishda", "Ko'chada", "Dam olishda"]

# Menyudagi knopka nomi
BTN_CATEGORIES = "Categoriyalar"


def ensure_db(bot_data: dict) -> None:
    """
    bot_data ichida umumiy DB bo'lmasa yaratadi:
    bot_data["music_db"] = { user_id: {category: [ {file_id, title}, ... ] } }
    """
    if "music_db" not in bot_data:
        bot_data["music_db"] = {}


def ensure_user(bot_data: dict, user_id: int) -> None:
    """
    Foydalanuvchi uchun DB bo'lmasa yaratadi:
    { "Ishda": [], "Ko'chada": [], "Dam olishda": [] }
    """
    ensure_db(bot_data)

    if user_id not in bot_data["music_db"]:
        bot_data["music_db"][user_id] = {}
        for c in CATEGORIES:
            bot_data["music_db"][user_id][c] = []


def add_music(
    bot_data: dict, user_id: int, category: str, file_id: str, title: str
) -> None:
    """
    Audio file_id ni berilgan kategoriya ichiga qo'shadi.
    """
    ensure_user(bot_data, user_id)

    # agar kategoriya noto'g'ri bo'lsa, qo'shmaymiz
    if category not in CATEGORIES:
        return

    bot_data["music_db"][user_id][category].append({"file_id": file_id, "title": title})


def get_categories(bot_data: dict, user_id: int) -> dict:
    """
    User kategoriyalari va ichidagi listni qaytaradi.
    """
    ensure_user(bot_data, user_id)
    return bot_data["music_db"][user_id]


def get_category_items(bot_data: dict, user_id: int, category: str) -> list:
    """
    Bitta kategoriya ichidagi musiqalar ro'yxatini qaytaradi.
    """
    ensure_user(bot_data, user_id)

    if category not in CATEGORIES:
        return []

    return bot_data["music_db"][user_id][category]


def count_category(bot_data: dict, user_id: int, category: str) -> int:
    """
    Kategoriyadagi musiqalar soni.
    """
    items = get_category_items(bot_data, user_id, category)
    return len(items)


def clear_category(bot_data: dict, user_id: int, category: str) -> None:
    """
    Kategoriyani bo'shatib tashlaydi (hamma musiqani o'chiradi).
    """
    ensure_user(bot_data, user_id)

    if category in CATEGORIES:
        bot_data["music_db"][user_id][category] = []


def remove_music_by_index(
    bot_data: dict, user_id: int, category: str, index: int
) -> bool:
    """
    Kategoriya ichidan index bo'yicha 1 ta musiqani o'chiradi.
    True qaytsa o'chdi, False qaytsa o'chmadi.
    """
    items = get_category_items(bot_data, user_id, category)

    if index < 0 or index >= len(items):
        return False

    items.pop(index)
    return True
