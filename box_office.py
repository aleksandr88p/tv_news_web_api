
import mysql.connector
import openai
from retrying import retry
import mysql.connector
# from main import db_host, db_user, db_name, db_password

def connect_to_database(host, user, password, database):
    # Установка соединения с базой данных
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    return connection

def get_article_dates(conn):
    cursor = conn.cursor()
    # Выполнение запроса SELECT для выборки поля article_date
    sql_query = "SELECT article_date FROM box_office_articles"
    cursor.execute(sql_query)

    # Получение результатов запроса
    results = cursor.fetchall()

    # Закрытие курсора и соединения
    cursor.close()
    conn.close()
    # Возвращение результатов
    return sorted([row[0].strftime('%Y-%m-%d') for row in results], reverse=True)


def get_last_dates(count, conn):
    all_dates = get_article_dates(conn)
    return all_dates[:count]


def get_article_by_date(conn, article_date):
    # Создание соединения с базой данных
    connection = conn

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

def generate_summary_BO(api_key, article_content, query=None):
    openai.api_key = api_key

    default_query = """Summarize this text in a direct, chatty tone. List in bullet points all the notable movies at the box office this past weekend mentioned in this text and summarize how they performed at the box office. Categorize each film under either the subheading "hit" or "flop" depending on how they performed. Bold film titles (without quotations) and include relevant emojis:\n\n"""

    full_query = f"{query}: \n\n" if query else default_query
    prompt = full_query + article_content

    @retry(stop_max_attempt_number=3, wait_fixed=30 * 1000)  # Retry 3 times with a 30-second wait between attempts
    def request_summary():
        try:
            print('***************************************')
            print(f'from try, len prompt is {len(prompt)}')
            # print(prompt)
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


