from master_program_chatbot.data.parser import parse_program_info


def test_parse_program_info():
    url = "https://abit.itmo.ru/program/master/ai_product"
    data = parse_program_info(url)

    assert isinstance(data, dict)
    assert data is not None

    assert "title" in data
    assert "description" in data
    assert "career" in data
    assert "admission" in data
