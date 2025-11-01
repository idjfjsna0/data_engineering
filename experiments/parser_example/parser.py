import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

urls = [
    "https://abit.itmo.ru/rating/master/budget/2305",
    "https://abit.itmo.ru/rating/master/budget/2254",
    "https://abit.itmo.ru/rating/master/budget/2306",
    "https://abit.itmo.ru/rating/master/budget/2310",
    "https://abit.itmo.ru/rating/master/budget/2307",
    "https://abit.itmo.ru/rating/master/budget/2256",
    "https://abit.itmo.ru/rating/master/budget/2312",
]


def abbr(stroka):
    # Разделяем код и название
    parts = stroka.split(" ", 1)
    code = parts[0]
    title = parts[1].strip("«»")

    # Разбиваем название на слова
    words = title.split()

    # Формируем аббревиатуру
    abbr = "".join(word[0].upper() if word.lower() != "и" else "и" for word in words)

    # Собираем итоговую строку
    return f"{code} {abbr}"


def dir_name(url):
    # Загружаем HTML
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Находим JSON внутри <h3 class="RatingPage_rating__title___xoYR">
    script_tag = soup.find("h3", {"class": "RatingPage_rating__title___xoYR"})

    direction_name = abbr(script_tag.text)
    return direction_name


sheet_names = []
for url in urls:
    sheet_names.append(dir_name(url))
sheet_url = dict(zip(sheet_names, urls))


def parse_html(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    script_tag = soup.find("script", id="__NEXT_DATA__")
    if script_tag:
        json_data = json.loads(script_tag.string)
        programs = json_data["props"]["pageProps"]["programList"]["general_competition"]
        df = pd.DataFrame(programs)
        selected_columns = [
            "position",
            "sspvo_id",
            "exam_type",
            "exam_scores",
            "ia_scores",
            "total_scores",
            "diploma_average",
            "priority",
            "is_send_agreement",
            "status",
            "main_top_priority",
            "highest_passageway_priority",
        ]
        df = df[selected_columns]
        column_rename_map = {
            "exam_type": "Тип экзамена",
            "diploma_average": "Средний балл",
            "position": "Место",
            "priority": "Приоритет",
            "ia_scores": "ИД",
            "exam_scores": "Балл экзамена",
            "total_scores": "Сумма баллов",
            "is_send_agreement": "Согласие",
            "status": "Статус <?>",
            "sspvo_id": "ID",
            "main_top_priority": "Главный приоритет",
            "highest_passageway_priority": "Наивысший приоритет прохода",
        }
        df.rename(columns=column_rename_map, inplace=True)
        df.replace({True: "+", False: "-"}, inplace=True)
        df["Средний балл"] = df["Средний балл"].apply(
            lambda x: (
                f"{float(x):.4f}"
                if pd.notnull(x) and str(x).replace(".", "", 1).isdigit()
                else x
            )
        )
        exam_priority = {
            "ЯП": 1,
            "МегаОлимпиада ИТМО": 4,
            "КД": 5,
            "Мегашкола": 6,
            "КП": 7,
            "ЗИШ": 15,
            "Включи свет": 35,
            "ВЭ": 40,
            "ПИГА": 41,
        }
        df["exam_priority"] = df["Тип экзамена"].map(exam_priority)
        df["Средний балл (float)"] = pd.to_numeric(df["Средний балл"], errors="coerce")
        df.loc[~df["Тип экзамена"].isin(["ВЭ", "ПИГА"]), "Балл экзамена"] = 100
        df["Сумма баллов"] = pd.to_numeric(
            df["Балл экзамена"], errors="coerce"
        ) + pd.to_numeric(df["ИД"], errors="coerce")
        df.sort_values(
            by=["Сумма баллов", "exam_priority", "Средний балл (float)"],
            ascending=[
                False,
                True,
                False,
            ],  # баллы и средний — по убыванию, приоритет — по возрастанию
            inplace=True,
        )
        # Удаляем вспомогательные столбцы
        df.drop(columns=["exam_priority", "Средний балл (float)"], inplace=True)

    return df


def export_csv(df, shtnm):
    # Создаем имя файла на основе названия направления подготовки
    filename = f"{shtnm}.csv"
    # Сохраняем DataFrame в CSV файл
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    # print(f"Created file: {filename}")


for name in sheet_names:
    print(f"In production: {name}")
    df = parse_html(sheet_url[name])
    print(df.head(5))
    # export_csv(df, name)

print("All data parsed & exported to CSVs.")
