import os
import time


def clear_cache_folder():
    cache_folder = "cache"  # Путь к папке cache

    # Проверяем существование папки cache
    if not os.path.exists(cache_folder):
        print("Папка cache не существует")
        return

    try:
        # Получаем список файлов в папке cache
        files = os.listdir(cache_folder)

        # Проходимся по всем файлам в папке и удаляем их
        for file_name in files:
            file_path = os.path.join(cache_folder, file_name)
            os.remove(file_path)

        print("Файлы в папке cache успешно удалены")

    except Exception as e:
        print(f"Произошла ошибка при удалении файлов из папки cache: {e}")


# Запускаем функцию каждый час
while True:
    clear_cache_folder()
    time.sleep(3600*4)  # Подождать 1 час (3600 секунд)
