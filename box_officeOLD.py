import json

import mysql.connector
import nltk
nltk.download('punkt')
import openai
from retrying import retry

def create_connection():
    # Параметры подключения к базе данных
    host = "185.51.121.22"
    user = "user_for_tv_and_news"
    password = "mY@we$omeP@$$w0rd"
    database = "tv_news"

    # Установка соединения с базой данных
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    return connection

def get_article_dates():
    # Создание соединения с базой данных
    connection = create_connection()

    # Создание курсора для выполнения запросов
    cursor = connection.cursor()

    # Выполнение запроса SELECT для выборки поля article_date
    query = "SELECT article_date FROM box_office_articles"
    cursor.execute(query)

    # Получение результатов запроса
    results = cursor.fetchall()

    # Закрытие курсора и соединения
    cursor.close()
    connection.close()

    # Возвращение результатов
    return [row[0] for row in results]

d = get_article_dates()
print(sorted(d))
"""
[datetime.date(2023, 6, 4), datetime.date(2023, 5, 29), datetime.date(2023, 5, 21), datetime.date(2023, 5, 15), datetime.date(2023, 5, 7), datetime.date(2023, 5, 1), datetime.date(2023, 4, 24), datetime.date(2023, 4, 17), datetime.date(2023, 4, 9), datetime.date(2023, 4, 3), datetime.date(2023, 3, 26), datetime.date(2023, 3, 20), datetime.date(2023, 3, 13), datetime.date(2023, 3, 6), datetime.date(2023, 2, 27), datetime.date(2023, 6, 11)]
[datetime.date(2023, 2, 27), datetime.date(2023, 3, 6), datetime.date(2023, 3, 13), datetime.date(2023, 3, 20), datetime.date(2023, 3, 26), datetime.date(2023, 4, 3), datetime.date(2023, 4, 9), datetime.date(2023, 4, 17), datetime.date(2023, 4, 24), datetime.date(2023, 5, 1), datetime.date(2023, 5, 7), datetime.date(2023, 5, 15), datetime.date(2023, 5, 21), datetime.date(2023, 5, 29), datetime.date(2023, 6, 4), datetime.date(2023, 6, 11)]

"""


def get_article_by_date(article_date):
    # Создание соединения с базой данных
    connection = create_connection()

    # Создание курсора для выполнения запросов
    cursor = connection.cursor()

    # Выполнение запроса SELECT для выборки поля article_content по указанной дате
    query = "SELECT article_content FROM box_office_articles WHERE article_date = %s"
    cursor.execute(query, (article_date,))

    # Получение результатов запроса
    result = cursor.fetchone()

    # Закрытие курсора и соединения
    cursor.close()
    connection.close()

    if result:
        return result[0]
    else:
        return None


# article_text = get_article_by_date('2023-06-11')


def generate_summary(api_key, article_content, query=None):
    openai.api_key = api_key

    default_query = """Summarize this text in a direct, chatty tone. List in bullet points all the notable movies at the box office this past weekend mentioned in this text and summarize how they performed at the box office. Categorize each film under either the subheading "hit" or "flop" depending on how they performed. Bold film titles (without quotations) and include relevant emojis:\n\n"""

    full_query = f"{query}: \n\n" if query else default_query
    prompt = full_query + article_content

    @retry(stop_max_attempt_number=3, wait_fixed=30 * 1000)  # Retry 3 times with a 30-second wait between attempts
    def request_summary():
        try:
            print('***************************************')
            print(f'from try, len prompt is {len(prompt)}')
            print(prompt)
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                temperature=0.4,
                max_tokens=500
            )
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"Error generating summary: {e}")
            raise  # Re-raise the exception to trigger a retry

    summary = request_summary()
    return summary


# Пример использования функции
# api_key = "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"
# article = article_text
#
# generated_summary = generate_summary(api_key, article)

# try:
#     if generated_summary:
#         print("Сгенерированное краткое содержание:")
#         print(generated_summary)
# except Exception as e:
#
#     print(f"Ошибка при генерации краткого содержания {e}")


