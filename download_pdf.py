import requests


def download_pdf(url, filename):
    response = requests.get(url)
    with open(filename, "wb") as f:
        f.write(response.content)


if __name__ == "__main__":
    ai_url = "https://abit.itmo.ru/file_storage/file/exams/master/ai.pdf"
    ai_product_url = (
        "https://abit.itmo.ru/file_storage/file/exams/master/ai_product.pdf"
    )

    download_pdf(ai_url, "ai_curriculum.pdf")
    download_pdf(ai_product_url, "ai_product_curriculum.pdf")
