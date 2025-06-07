import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from telegram import Update 
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from src.services.post import PostService
from src.database import async_session_maker
from src.utils.db_manager import DBManager


async def start(update: Update, context: ContextTypes):
    logger.info(f"User {update.effective_user.id} started the bot")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, напиши команду /posts для просмотра постов")


async def unknown(update: Update, context: ContextTypes):
    logger.info(f"User {update.effective_user.id} sent unknown command: {update.message.text}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Я не знаю такой команды.")
    

def build_posts_keyboard(posts_titles):
    buttons = [
        [InlineKeyboardButton(text=title, callback_data=f"post_{index}")]
        for index, title in enumerate(posts_titles)
    ]
    return InlineKeyboardMarkup(buttons)


async def posts(update: Update, context: ContextTypes):
    logger.info(f"User {update.effective_user.id} requested posts list")
    async with DBManager(session_factory=async_session_maker) as db:
        posts_titles = await PostService(db).get_posts_titles()
        keyboard = build_posts_keyboard(posts_titles)
        if len(posts_titles) > 0:
            text = "Выберите пост:"
        else:
            text = "Нет постов"
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=keyboard
        )


async def button_handler(update: Update, context: ContextTypes):
    query = update.callback_query
    await query.answer()
    data = query.data
    logger.info(f"User {update.effective_user.id} clicked button with data: {data}")
    async with DBManager(session_factory=async_session_maker) as db:
        posts_titles = await PostService(db).get_posts_titles()
    if data.startswith("post_"):
        index = int(data.split("_")[1])
        if 0 <= index < len(posts_titles):
            post_title = posts_titles[index]
            post = await PostService(db).get_post_by_title(title=post_title)
            created_at_str = post.created_at.strftime("%Y-%m-%d %H:%M:%S")
            message_text = f"<b>{post_title}</b>\n{created_at_str}\n\n{post.text}"
            await query.edit_message_text(text=message_text, parse_mode="HTML")
        else:
            await query.edit_message_text(text="Пост не найден.")
