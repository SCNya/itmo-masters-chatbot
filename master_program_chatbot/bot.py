import logging

import pandas as pd
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from telegram.helpers import escape_markdown

from master_program_chatbot.data.parser import parse_program_info
from master_program_chatbot.qa import create_qa_chain, get_answer
from master_program_chatbot.recommender import recommend_courses

# Включаем логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

AI_URL = "https://abit.itmo.ru/program/master/ai"
AI_PRODUCT_URL = "https://abit.itmo.ru/program/master/ai_product"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет сообщение, когда пользователь вводит команду /start."""
    await update.message.reply_text(
        "Привет! Я бот, который поможет тебе с выбором магистерской программы."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет сообщение, когда пользователь вводит команду /help."""
    await update.message.reply_text(
        "Я могу предоставить информацию о магистерских программах "
        "'Искусственный интеллект' и 'Управление AI-продуктами' в "
        "Университете ИТМО. Используйте /ai для программы "
        "'Искусственный интеллект' и /aiproduct для программы "
        "'Управление AI-продуктами'.\n\n"
        "Используйте /qa, чтобы задать вопрос о программах.\n"
        "Используйте /recommend, чтобы получить рекомендации по курсам."
    )


async def get_program_info(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Получает информацию о программе."""
    program = update.message.text.split("/")[1]
    if program == "ai":
        url = AI_URL
    elif program == "aiproduct":
        url = AI_PRODUCT_URL
    else:
        await update.message.reply_text(
            "Неверная команда. Используйте /ai или /aiproduct."
        )
        return

    data = parse_program_info(url)
    context.user_data["program_data"] = data

    message = f"""
*Название:* {data['title']}
*Описание:* {data['description']}
*Карьера:* {data['career']}
*Поступление:* {data['admission']}
    """
    safe_message = escape_markdown(message, version=2)

    try:
        await update.message.reply_text(safe_message, parse_mode="MarkdownV2")
    except Exception as e:
        if "Message is too long" in str(e):
            for i in range(0, len(message), 4096):
                await update.message.reply_text(message[i : i + 4096])
        else:
            await update.message.reply_text(message, parse_mode=None)


async def qa_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Запрашивает у пользователя вопрос."""
    context.user_data["state"] = "awaiting_question"
    await update.message.reply_text("Пожалуйста, задайте свой вопрос.")


async def recommend_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Запрашивает у пользователя информацию о его бэкграунде."""
    context.user_data["state"] = "awaiting_background"
    await update.message.reply_text(
        "Пожалуйста, опишите свой бэкграунд и интересы."
    )


async def handle_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Обрабатывает обычное сообщение."""
    if context.user_data.get("state") == "awaiting_question":
        question = update.message.text
        program_data = context.user_data.get("program_data")

        if not program_data:
            await update.message.reply_text(
                "Сначала выберите программу с помощью /ai или /aiproduct."
            )
            return

        text = (
            f"Название: {program_data['title']}\n"
            f"Описание: {program_data['description']}\n"
            f"Карьера: {program_data['career']}\n"
            f"Поступление: {program_data['admission']}"
        )

        qa_chain = create_qa_chain(text)
        answer = get_answer(qa_chain, question)

        await update.message.reply_text(answer)

        context.user_data["state"] = None
    elif context.user_data.get("state") == "awaiting_background":
        user_background = update.message.text

        courses = pd.DataFrame(
            {
                "course_name": [
                    "Введение в ИИ",
                    "Машинное обучение",
                    "Глубокое обучение",
                    "Управление AI-продуктами",
                    "Принятие решений на основе данных",
                    "UX для ИИ",
                ],
                "course_type": [
                    "обязательный",
                    "обязательный",
                    "элективный",
                    "обязательный",
                    "обязательный",
                    "элективный",
                ],
                "credits": [3, 4, 4, 3, 4, 4],
            }
        )

        recommendations = recommend_courses(user_background, courses)

        message = (
            "Основываясь на вашем бэкграунде, вот несколько "
            "рекомендуемых элективных курсов:\n\n"
        )
        for _, row in (
            recommendations[recommendations["course_type"] == "элективный"]
            .head(3)
            .iterrows()
        ):
            message += f"- {row['course_name']}\n"

        await update.message.reply_text(message)

        context.user_data["state"] = None
    else:
        await update.message.reply_text(
            "Я не уверен, что вы имеете в виду. Используйте /help, чтобы "
            "узнать, что я могу делать."
        )


def main() -> None:
    """Запускает бота."""
    application = (
        Application.builder()
        .token("7602127348:AAG5lmyFCbndDepZFTaVCiSorG8-_itnDB4")
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ai", get_program_info))
    application.add_handler(CommandHandler("aiproduct", get_program_info))
    application.add_handler(CommandHandler("qa", qa_command))
    application.add_handler(CommandHandler("recommend", recommend_command))

    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    application.run_polling()


if __name__ == "__main__":
    main()
