import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from master_program_chatbot.bot import (
    get_program_info,
    handle_message,
    help_command,
    qa_command,
    recommend_command,
    start,
)


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
        "'Управление AI-продуктами'.\n\n"
        "Используйте /qa, чтобы задать вопрос о программах.\n"
        "Используйте /recommend, чтобы получить рекомендации по курсам."
    )


@pytest.mark.asyncio
async def test_get_program_info_ai():
    update = MagicMock()
    update.message.text = "/ai"
    update.message.reply_text = AsyncMock()
    context = MagicMock()
    context.user_data = {}
    with patch(
        "master_program_chatbot.bot.parse_program_info"
    ) as mock_parse_program_info:
        mock_parse_program_info.return_value = {
            "title": "Test Program",
            "description": "Test Description",
            "career": "Test Career",
            "admission": "Test Admission",
        }
        await get_program_info(update, context)
    update.message.reply_text.assert_called_once()


@pytest.mark.asyncio
async def test_get_program_info_aiproduct():
    update = MagicMock()
    update.message.text = "/aiproduct"
    update.message.reply_text = AsyncMock()
    context = MagicMock()
    context.user_data = {}
    with patch(
        "master_program_chatbot.bot.parse_program_info"
    ) as mock_parse_program_info:
        mock_parse_program_info.return_value = {
            "title": "Test Program",
            "description": "Test Description",
            "career": "Test Career",
            "admission": "Test Admission",
        }
        await get_program_info(update, context)
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
async def test_qa_command():
    update = MagicMock()
    update.message.reply_text = AsyncMock()
    context = MagicMock()
    context.user_data = {}
    await qa_command(update, context)
    update.message.reply_text.assert_called_once_with("Пожалуйста, задайте свой вопрос.")
    assert context.user_data["state"] == "awaiting_question"


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
async def test_handle_message_qa():
    update = MagicMock()
    update.message.text = "What is the admission process?"
    update.message.reply_text = AsyncMock()
    context = MagicMock()
    context.user_data = {
        "state": "awaiting_question",
        "program_data": {
            "title": "Test Program",
            "description": "Test Description",
            "career": "Test Career",
            "admission": "Test Admission",
        },
    }
    with patch("master_program_chatbot.bot.create_qa_chain") as mock_create_qa_chain:
        mock_qa_chain = MagicMock()
        mock_create_qa_chain.return_value = mock_qa_chain
        with patch("master_program_chatbot.bot.get_answer") as mock_get_answer:
            mock_get_answer.return_value = "The admission process is..."
            await handle_message(update, context)
            mock_get_answer.assert_called_once_with(
                mock_qa_chain, "What is the admission process?"
            )
    update.message.reply_text.assert_called_once_with("The admission process is...")
    assert context.user_data["state"] is None


@pytest.mark.asyncio
async def test_handle_message_qa_no_program_data():
    update = MagicMock()
    update.message.text = "What is the admission process?"
    update.message.reply_text = AsyncMock()
    context = MagicMock()
    context.user_data = {"state": "awaiting_question", "program_data": None}
    with patch(
        "master_program_chatbot.bot.parse_program_info"
    ) as mock_parse_program_info:
        mock_parse_program_info.side_effect = [
            {
                "title": "AI Program",
                "description": "AI Description",
                "career": "AI Career",
                "admission": "AI Admission",
            },
            {
                "title": "AI Product Program",
                "description": "AI Product Description",
                "career": "AI Product Career",
                "admission": "AI Product Admission",
            },
        ]
        with patch(
            "master_program_chatbot.bot.create_qa_chain"
        ) as mock_create_qa_chain:
            mock_qa_chain = MagicMock()
            mock_create_qa_chain.return_value = mock_qa_chain
            with patch("master_program_chatbot.bot.get_answer") as mock_get_answer:
                mock_get_answer.return_value = "The admission process is..."
                await handle_message(update, context)
                mock_create_qa_chain.assert_called_once()
                mock_get_answer.assert_called_once_with(
                    mock_qa_chain, "What is the admission process?"
                )
    update.message.reply_text.assert_called_once_with("The admission process is...")
    assert context.user_data["state"] is None


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


@pytest.mark.asyncio
async def test_get_program_info_long_message():
    update = MagicMock()
    update.message.text = "/ai"
    update.message.reply_text = AsyncMock()
    update.message.reply_text.side_effect = [
        Exception("Message is too long"),
        None,
        None,
    ]
    context = MagicMock()
    context.user_data = {}

    # Mock the parse_program_info function to return a long description
    long_description = "a" * 4097
    with patch(
        "master_program_chatbot.bot.parse_program_info"
    ) as mock_parse_program_info:
        mock_parse_program_info.return_value = {
            "title": "Test Program",
            "description": long_description,
            "career": "Test Career",
            "admission": "Test Admission",
        }
        await get_program_info(update, context)

    # Check if the message was split into multiple messages
    assert update.message.reply_text.call_count > 1


@pytest.mark.asyncio
async def test_get_program_info_invalid_markdown():
    update = MagicMock()
    update.message.text = "/ai"
    update.message.reply_text = AsyncMock()
    update.message.reply_text.side_effect = [Exception("Can't parse entities"), None]
    context = MagicMock()
    context.user_data = {}

    # Mock the parse_program_info function to return invalid Markdown
    with patch(
        "master_program_chatbot.bot.parse_program_info"
    ) as mock_parse_program_info:
        mock_parse_program_info.return_value = {
            "title": "Test Program",
            "description": "Invalid *Markdown",
            "career": "Test Career",
            "admission": "Test Admission",
        }
        await get_program_info(update, context)

    # Check if the message was sent with parse_mode=None
    update.message.reply_text.assert_any_call(unittest.mock.ANY, parse_mode=None)
