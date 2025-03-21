import logging
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackContext
from infrastructure.embedding import get_embedding

# Глобальная переменная для векторного индекса (будет установлена из main.py)
global_index = None

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Привет! Я бот-рекомендатор манги. Отправь мне любой текстовый запрос, и я найду для тебя подходящие манги."
    )

async def handle_text(update: Update, context: CallbackContext) -> None:
    query = update.message.text.strip()
    if not query:
        return
    query_embedding = get_embedding(query)
    results = global_index.search(query_embedding, k=5)
    if results:
        response_text = f'✨ Результаты для запроса *"{query}"*:\n\n'
        for manga, score in results:
            # Получаем базовые данные
            manga_id = manga.get("id", "N/A")
            title = manga.get("title", {}).get("english") or manga.get("title", {}).get("romaji", "Без названия")
            genres = ", ".join(manga.get("genres", []))

            # Форматируем теги (выбираем название тега для каждого)
            tags_list = manga.get("tags", [])
            tags = ", ".join(tag.get("name", "N/A") for tag in tags_list)

            # Описание и отзывы
            description = manga.get("description", "Нет описания")
            reviews_count = manga.get("reviews", {}).get("pageInfo", {}).get("total", 0)

            # Собираем строку с информацией
            response_text += f"📖 *{title}* (ID: {manga_id}) (Релевантность: {score:.2f})\n"
            response_text += f"Жанры: {genres}\n"
            response_text += f"Теги: {tags}\n"
            response_text += f"Описание: {description}\n"
            response_text += f"Отзывы: {reviews_count}\n\n"

        await update.message.reply_text(response_text, parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text("Ничего не найдено.")


def run_bot(index):
    """
    Устанавливает глобальный индекс и запускает Telegram-бота, который обрабатывает все входящие текстовые сообщения.
    """
    global global_index
    global_index = index

    from config import TELEGRAM_BOT_TOKEN
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Запуск Telegram-бота для поиска манги.")

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, handle_text))
    app.run_polling()