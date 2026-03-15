import requests
import json
from pathlib import Path

URL = "https://www.cbr-xml-daily.ru/daily_json.js"
SAVE_FILE = Path(__file__).parent / "resource" / "save.json"

class CurrencyMonitor:
    def __init__(self):
        self.currencies = {}
        self.groups = {}
        self.load_groups()  

    def fetch_currencies(self):
        """Загружает актуальные курсы с сайта ЦБ."""
        try:
            response = requests.get(URL, timeout=10)
            self.currencies = response.json()["Valute"]
            print("Курсы валют успешно загружены")
        except Exception as e:
            print(f"Ошибка загрузки: {e}")

    def load_groups(self):
        if SAVE_FILE.exists():
            try:
                with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                    self.groups = json.load(f)
            except:
                self.groups = {}
        else:
            SAVE_FILE.parent.mkdir(exist_ok=True)
            self.groups = {}

    def save_groups(self):
        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.groups, f, ensure_ascii=False, indent=2)

    def _print_table_header(self):
        line = "=" * 95
        print(line)
        print("| {:3} | {:35} | {:7} | {:15} | {:13} |".format(
            "Код", "Валюта", "Номинал", "Курс за номинал", "Курс за 1 ед."))
        print(line)

    def _print_currency_row(self, code, data):
        print("| {:3} | {:35} | {:7} | {:15.2f} | {:13.2f} |".format(
            data["CharCode"],
            data["Name"][:35],
            data["Nominal"],
            data["Value"],
            data["Value"] / data["Nominal"]
        ))

    def show_all(self):
        if not self.currencies:
            print("Сначала загрузите данные (пункт 8)")
            return
        self._print_table_header()
        for code in sorted(self.currencies.keys()):
            self._print_currency_row(code, self.currencies[code])
        print("=" * 95)

    def show_by_code(self, code):
        code = code.upper()
        if code not in self.currencies:
            print(f"Валюта {code} не найдена")
            return
        data = self.currencies[code]
        print(f"\n{code} — {data['Name']}")
        print(f"  ID: {data['ID']}")
        print(f"  Номинал: {data['Nominal']}")
        print(f"  Курс: {data['Value']:.2f} ₽ за {data['Nominal']} ед.")
        print(f"  Курс за 1 ед.: {data['Value'] / data['Nominal']:.2f} ₽")

    def create_group(self, name):
        if not name:
            print(" Название не может быть пустым")
            return
        if name in self.groups:
            print(f"Группа '{name}' уже существует")
            return
        self.groups[name] = []
        self.save_groups()
        print(f"Группа '{name}' создана")

    def show_groups(self):
        """Показывает все группы."""
        if not self.groups:
            print(" У вас пока нет групп")
            return
        print("\n Ваши группы:")
        for name, currencies in self.groups.items():
            print(f"  {name} — валют: {len(currencies)}")

    def show_group_currencies(self, name):
        if name not in self.groups:
            print(f"Группа '{name}' не найдена")
            return
        if not self.groups[name]:
            print(f" В группе '{name}' пока нет валют")
            return
        print(f"\nГруппа: {name}")
        self._print_table_header()
        for code in self.groups[name]:
            if code in self.currencies:
                self._print_currency_row(code, self.currencies[code])
        print("=" * 95)

    def add_to_group(self, group_name, currency_code):
        currency_code = currency_code.upper()
        if group_name not in self.groups:
            print(f" Группа '{group_name}' не найдена")
            return
        if currency_code not in self.currencies:
            print(f" Валюта '{currency_code}' не найдена")
            return
        if currency_code in self.groups[group_name]:
            print(f" Валюта '{currency_code}' уже есть в группе")
            return
        self.groups[group_name].append(currency_code)
        self.save_groups()
        print(f" Валюта '{currency_code}' добавлена в группу '{group_name}'")

    def remove_from_group(self, group_name, currency_code):
        currency_code = currency_code.upper()
        if group_name not in self.groups:
            print(f" Группа '{group_name}' не найдена")
            return
        if currency_code not in self.groups[group_name]:
            print(f" Валюты '{currency_code}' нет в группе")
            return
        self.groups[group_name].remove(currency_code)
        self.save_groups()
        print(f" Валюта '{currency_code}' удалена из группы '{group_name}'")


def main():
    monitor = CurrencyMonitor()
    
    while True:
        print("\n" + "="*50)
        print(" МОНИТОРИНГ ВАЛЮТ")
        print("="*50)
        print("1.  Показать все валюты")
        print("2.  Найти валюту по коду")
        print("3.  Создать группу")
        print("4.  Показать все группы")
        print("5.  Показать валюты группы")
        print("6.  Добавить валюту в группу")
        print("7.  Удалить валюту из группы")
        print("8.  Загрузить курсы с ЦБ")
        print("0.  Выход")
        print("-"*50)
        
        choice = input("Выберите действие: ").strip()
        
        if choice == "1":
            monitor.show_all()
        elif choice == "2":
            code = input("Введите код валюты: ").upper()
            monitor.show_by_code(code)
        elif choice == "3":
            name = input("Введите название группы: ").strip()
            monitor.create_group(name)
        elif choice == "4":
            monitor.show_groups()
        elif choice == "5":
            name = input("Введите название группы: ").strip()
            monitor.show_group_currencies(name)
        elif choice == "6":
            group = input("Название группы: ").strip()
            code = input("Код валюты: ").upper()
            monitor.add_to_group(group, code)
        elif choice == "7":
            group = input("Название группы: ").strip()
            code = input("Код валюты: ").upper()
            monitor.remove_from_group(group, code)
        elif choice == "8":
            monitor.fetch_currencies()
        elif choice == "0":
            print("Бб")
            break
        else:
            print(" Неверный выбор")

        input("\nНажмите Enter, чтобы продолжить...")

if __name__ == "__main__":
    main()