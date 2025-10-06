#Описание скрипта
Скрипт сохраняет n случайных цитат Канье Уэста в CSV-файл
[**Kanye API**](https://api.kanye.rest/)
##Инструкция
1. Установить Python (например, 3.13)
2. Установить библиотеки:
    'pip install pandas'
    'pip install requests'
3. Запустить 'api_reader.py'
## Алгоритм скрипта
1. Обращение к https://api.kanye.rest/ с помощью GET-запроса
2. Получение ответа в виде json-файла
3. Добавление цитаты из json-файла в список цитат
4. Повторение 1.-3. n раз, заданное в коде
5. Преобразование конечного списка цитат к pandas.DataFrame
6. Вывод датафрейма в терминал
7. Экспорт pandas.DataFrame в CSV
8. 'Канье счастлив.'
## Пример работы скрипта:
<img width="980" height="247" alt="изображение" src="https://github.com/user-attachments/assets/4cb2e2fa-6f03-4191-91ee-f062fdd910a4" />
