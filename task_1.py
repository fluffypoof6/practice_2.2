import requests

urls = [
    "https://github.com/",
    "https://www.binance.com/en",
    "https://tomtit.tomsk.ru/",
    "https://jsonplaceholder.typicode.com/",
    "https://moodle.tomtit-tomsk.ru/"
]

def check_website(url):
    try:
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            status = "доступен"
        elif response.status_code == 403:
            status = "вход запрещен"
        elif response.status_code == 404:
            status = "не найден"
        elif response.status_code >= 500:
            status = "ошибка сервера"
        else:
            status = "не доступен"
        
        return status, response.status_code
    except requests.exceptions.ConnectionError:
        return "не доступен (нет соединения)", None
    except requests.exceptions.Timeout:
        return "не доступен (таймаут)", None
    except Exception as e:
        return f"ошибка", None

print("Проверка доступности сайтов")
print("=" * 60)

for url in urls:
    status, code = check_website(url)
    
    if code:
        print(f"{url} – {status} – {code}")
    else:
        print(f"{url} – {status}")
print("=" * 60)