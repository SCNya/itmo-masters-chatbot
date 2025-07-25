import json

import requests
from bs4 import BeautifulSoup


def parse_program_info(url: str) -> dict:
    """
    Парсит информацию о программе с веб-сайта и возвращает словарь.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
    json_data = json.loads(script_tag.string)

    api_program_data = json_data["props"]["pageProps"]["apiProgram"]
    json_program_data = json_data["props"]["pageProps"]["jsonProgram"]

    return {
        "title": api_program_data["title"],
        "description": json_program_data["about"]["desc"],
        "career": json_program_data["career"]["lead"],
        "admission": api_program_data["directions"][0]["disciplines"],
    }
