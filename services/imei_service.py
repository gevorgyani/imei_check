import cloudscraper
import requests

from core.config import settings

url = "https://api.imeicheck.net/v1/services"

headers = {
    "Authorization": f"Bearer {settings.IMEI_API_TOKEN}",
    "Accept-Language": "en"
}

response = requests.get(url, headers=headers)

print("Статус ответа:", response.status_code)
print("Ответ API:", response.text)
async def check_imei_with_api(imei: str) -> dict:
    try:
        scraper = cloudscraper.create_scraper()  # Автообход защиты Cloudflare
        response = scraper.post(
            f"{settings.IMEI_API_URL}/v1/checks",
            json={
                "deviceId": str(imei),
                "serviceId": 12
            },
            headers={
                "Authorization": f"Bearer {settings.IMEI_API_TOKEN}",
                "Accept-Language": "en",
                "Content-Type": "application/json"
            }
        )

        print(f"Статус ответа: {response.status_code}")
        print(f"Тело ответа: {response.text}")

        response.raise_for_status()  # Генерирует исключение, если код ошибки >= 400
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Ошибка подключения: {e}")
        return {"error": "Ошибка подключения к API"}
    except requests.exceptions.HTTPError as e:
        print(f"Ошибка HTTP: {e.response.status_code} - {e.response.text}")
        return {"error": f"Ошибка API: {e.response.status_code}", "details": e.response.text}

    return {"error": "Не удалось получить данные из сервиса IMEI"}
