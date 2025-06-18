import asyncio
import logging
from bs4 import BeautifulSoup
import requests
from src.checker.router import active_users
from src.create_bot import bot

logger = logging.getLogger(__name__)


async def sender():
    last = {}
    while True:
        res = parcer()
        if last != res and last:
            for user_id in active_users:
                await bot.send_message(
                    user_id,
                    "Результаты обновлены\n\nhttps://www.ege.spb.ru/result/index.php?mode=ege2025&wave=1",
                )
        else:
            logger.info("No updates")
        last = res
        await asyncio.sleep(60)


def parcer() -> bool:
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif\
            ,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://www.ege.spb.ru",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer": "https://www.ege.spb.ru/result/index.php?mode=ege2025&wave=1",
        "sec-ch-ua": '"Google Chrome";v="137", \
            "Chromium";v="137", "Not/A)Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    }

    params = {
        "mode": "ege2025",
        "wave": "1",
    }

    data = "pLastName=%CF%E0%ED%F2%E5%EB%E5%E5%E2&Series=4021&Number=964119&Login=%CF\
        %EE%EA%E0%E7%E0%F2%FC+%F0%E5%E7%F3%EB%FC%F2%E0%F2%FB"

    response = requests.post(
        "https://www.ege.spb.ru/result/index.php",
        params=params,
        headers=headers,
        data=data,
    )
    soup = BeautifulSoup(response.text, "lxml")
    data = soup.find_all(class_="exam-title row")
    result = {}
    for exam_data in data:
        exam_name = (
            exam_data.find(class_="exam-subject-info").text.strip().split("\xa0")[0]
        )
        exam_result = exam_data.find(class_="exam-result").text.strip()
        result[exam_name] = exam_result
    return result
