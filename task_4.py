import requests
import json
from pathlib import Path

GITHUB_API = "https://api.github.com"

class GitHubMonitor:
    def __init__(self):
        self.current_user = None
        self.current_user_repos = None
        self.current_username = None

    def _print_header(self, text):
        """Печатает красивый заголовок"""
        print("\n" + "=" * 60)
        print(f" {text}")
        print("=" * 60)

    def _print_repo(self, repo, show_stats=True):
        """Печатает информацию об одном репозитории"""
        print(f"\n {repo['name']}")
        print(f"   Ссылка: {repo['html_url']}")
        
        if show_stats:
            print(f"   Просмотры (watchers): {repo.get('watchers_count', 0)}")
        
        print(f"   Язык: {repo.get('language', 'Не указан')}")

        visibility = "Публичный" if not repo.get('private') else "Приватный"
        print(f"  Видимость: {visibility}")

        default_branch = repo.get('default_branch', 'main')
        print(f"   Ветка по умолчанию: {default_branch}")
        
        if repo.get('description'):
            print(f"  Описание: {repo['description'][:100]}")

    def select_user(self):
        """Выбирает пользователя GitHub для работы"""
        login = input("Введите логин пользователя: ").strip()
        
        if not login:
            print("Логин не может быть пустым")
            return

        user_response = requests.get(f"{GITHUB_API}/users/{login}")
        
        if user_response.status_code == 404:
            print(f"Пользователь '{login}' не найден")
            self.current_user = None
            self.current_username = None
            return
        elif user_response.status_code != 200:
            print(f"Ошибка API: {user_response.status_code}")
            self.current_user = None
            self.current_username = None
            return

        self.current_user = user_response.json()
        self.current_username = login
        repos_response = requests.get(f"{GITHUB_API}/users/{login}/repos")
        if repos_response.status_code == 200:
            self.current_user_repos = repos_response.json()
        
        print(f"Пользователь {login} выбран")

    def show_profile(self):
        if not self.current_user:
            print("Сначала выберите пользователя (пункт 1)")
            return

        self._print_header(f"Профиль: {self.current_username}")

        name = self.current_user.get('name')
        if name is None:
            name = "Не указано"

        discussions = 0
        disc_response = requests.get(
            f"{GITHUB_API}/search/issues?q=author:{self.current_username}+type:discussion"
        )
        if disc_response.status_code == 200:
            discussions = disc_response.json().get('total_count', 0)

        print(f"👤 Имя: {name}")
        print(f"Ссылка: https://github.com/{self.current_username}")
        print(f"Публичных репозиториев: {self.current_user.get('public_repos', 0)}")
        print(f"Обсуждений: {discussions}")
        print(f"Подписок: {self.current_user.get('following', 0)}")
        print(f"Подписчиков: {self.current_user.get('followers', 0)}")

    def show_all_repos(self):
        """Показывает все репозитории текущего пользователя"""
        if not self.current_user:
            print("Сначала выберите пользователя (пункт 1)")
            return

        if not self.current_user_repos:
            print(f"У пользователя {self.current_username} нет публичных репозиториев")
            return

        self._print_header(f"Репозитории: {self.current_username}")

        for i, repo in enumerate(self.current_user_repos, 1):
            print(f"\n{i}. ", end="")
            self._print_repo(repo)

    def search_repo(self):
        """Ищет репозиторий по названию"""
        if not self.current_user:
            print("Сначала выберите пользователя (пункт 1)")
            return

        repo_name = input("Введите название репозитория: ").strip()
        
        if not repo_name:
            print("э Название не может быть пустым")
            return

        # Ищем среди репозиториев текущего пользователя
        found = None
        if self.current_user_repos:
            for repo in self.current_user_repos:
                if repo['name'].lower() == repo_name.lower():
                    found = repo
                    break

        if found:
            self._print_header(f"НАЙДЕН: {repo_name}")
            self._print_repo(found)
        else:
            print(f"Репозиторий '{repo_name}' не найден у пользователя {self.current_username}")

    # ===== ДОПОЛНИТЕЛЬНО: ГЛОБАЛЬНЫЙ ПОИСК =====
    def global_search(self):
        """Ищет репозитории по названию во всем GitHub (из 2-го кода)"""
        query = input("Введите название для поиска: ").strip()
        
        if not query:
            print("Запрос не может быть пустым")
            return

        params = {
            'q': query,
            'sort': 'stars',
            'order': 'desc',
            'per_page': 10
        }

        response = requests.get(f"{GITHUB_API}/search/repositories", params=params)

        if response.status_code != 200:
            print(f"Ошибка при поиске (код {response.status_code})")
            return

        data = response.json()
        total = data['total_count']
        items = data['items']

        self._print_header(f"РЕЗУЛЬТАТЫ ПОИСКА: '{query}'")
        print(f"Всего найдено: {total}\n")

        if not items:
            print("Репозитории не найдены")
            return

        for i, repo in enumerate(items, 1):
            print(f"{i}. {repo['full_name']}")
            self._print_repo(repo, show_stats=False)
            print("-" * 40)

def main():
    monitor = GitHubMonitor()
    
    while True:
        print("\n" + "=" * 50)
        print("GITHUB МОНИТОР")
        print("=" * 50)
        print("1. Выбрать пользователя")
        print("2. Просмотреть профиль")
        print("3. Все репозитории пользователя")
        print("4. Поиск репозитория по названию (у текущего пользователя)")
        print("5. Глобальный поиск по GitHub")
        print("6. Показать конкретный репозиторий")
        print("0. Выход")
        print("-" * 50)

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            monitor.select_user()
        elif choice == "2":
            monitor.show_profile()
        elif choice == "3":
            monitor.show_all_repos()
        elif choice == "4":
            monitor.search_repo()
        elif choice == "5":
            monitor.global_search()
        elif choice == "6":
            monitor.show_specific_repo()
        elif choice == "0":
            print("\n бБ")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите 0-6")

        input("\nНажмите Enter, чтобы продолжить...")


if __name__ == "__main__":
    main()