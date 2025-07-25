from unittest.mock import AsyncMock, MagicMock

import pytest

from master_program_chatbot.bot import (get_program_info, handle_message,
                                        help_command, recommend_command, start)


@pytest.mark.asyncio
async def test_start():
    update = MagicMock()
    update.message.reply_text = AsyncMock()
    await start(update, None)
    update.message.reply_text.assert_called_once_with(
        "Привет! Я бот, который поможет тебе с выбором магистерской программы."
    )


@pytest.mark.asyncio
async def test_help_command():
    update = MagicMock()
    update.message.reply_text = AsyncMock()
    await help_command(update, None)
    update.message.reply_text.assert_called_once_with(
        "Я могу предоставить информацию о магистерских программах "
        "'Искусственный интеллект' и 'Управление AI-продуктами' в "
        "Университете ИТМО. Используйте /ai для программы "
        "'Искусственный интеллект' и /aiproduct для программы "
        "'Управление AI-продуктами'."
    )


@pytest.mark.asyncio
async def test_get_program_info_ai():
    update = MagicMock()
    update.message.text = "/ai"
    update.message.reply_text = AsyncMock()
    await get_program_info(update, None)
    update.message.reply_text.assert_called_once()


@pytest.mark.asyncio
async def test_get_program_info_aiproduct():
    update = MagicMock()
    update.message.text = "/aiproduct"
    update.message.reply_text = AsyncMock()
    await get_program_info(update, None)
    update.message.reply_text.assert_called_once()


@pytest.mark.asyncio
async def test_get_program_info_invalid():
    update = MagicMock()
    update.message.text = "/invalid"
    update.message.reply_text = AsyncMock()
    await get_program_info(update, None)
    update.message.reply_text.assert_called_once_with(
        "Неверная команда. Используйте /ai или /aiproduct."
    )


@pytest.mark.asyncio
async def test_recommend_command():
    update = MagicMock()
    update.message.reply_text = AsyncMock()
    context = MagicMock()
    context.user_data = {}
    await recommend_command(update, context)
    update.message.reply_text.assert_called_once_with(
        "Пожалуйста, опишите свой бэкграунд и интересы."
    )
    assert context.user_data["state"] == "awaiting_background"


@pytest.mark.asyncio
async def test_handle_message_recommend():
    update = MagicMock()
    update.message.text = "I have a background in machine learning and deep learning."
    update.message.reply_text = AsyncMock()
    context = MagicMock()
    context.user_data = {"state": "awaiting_background"}
    await handle_message(update, context)
    update.message.reply_text.assert_called_once()
    assert context.user_data["state"] is None


@pytest.mark.asyncio
async def test_handle_message_unknown():
    update = MagicMock()
    update.message.text = "hello"
    update.message.reply_text = AsyncMock()
    context = MagicMock()
    context.user_data = {}
    await handle_message(update, context)
    update.message.reply_text.assert_called_once_with(
        "Я не уверен, что вы имеете в виду. Используйте /help, чтобы "
        "узнать, что я могу делать."
    )
