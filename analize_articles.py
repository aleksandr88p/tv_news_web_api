import json

import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import create_engine
from urllib.parse import quote
import datetime

nltk.download('punkt')
nltk.download('stopwords')

def connect_to_database(host, user, password, database):
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")
    return engine.connect()

def fetch_articles_from_tables(conn, table_names, days_ago):
    dataframes = []
    some_days_ago = (datetime.datetime.now() - datetime.timedelta(days=days_ago)).strftime('%Y-%m-%d %H:%M:%S')
    for table in table_names:
        sql_query = f"SELECT * FROM {table} WHERE parsing_date >= '{some_days_ago}'"
        df = pd.read_sql(sql_query, con=conn)
        df["source"] = table
        dataframes.append(df)
    return dataframes

def preprocess_articles(articles_df):
    stop_words = set(stopwords.words('english'))
    articles_df['article_text'] = articles_df['article_text'].apply(lambda x: ' '.join(
        [word for word in word_tokenize(x) if word.casefold() not in stop_words]
    ))
    vectorizer = TfidfVectorizer()
    article_vectors = vectorizer.fit_transform(articles_df['article_text'])
    return article_vectors

def find_similar_articles(all_articles, article_vectors, threshold):
    similarities = cosine_similarity(article_vectors)
    similar_articles_dict = {}
    for i in range(len(similarities)):
        for j in range(i + 1, len(similarities)):
            if similarities[i, j] > threshold:
                if all_articles.iloc[i]["url"] not in similar_articles_dict:
                    similar_articles_dict[all_articles.iloc[i]["url"]] = []
                similar_articles_dict[all_articles.iloc[i]["url"]].append(all_articles.iloc[j]["url"])
    return similar_articles_dict

def create_article_groups_dict(similar_articles_dict, all_articles):
    article_groups_dict = {}
    c = 0
    for key, val in similar_articles_dict.items():
        group = set(val + [key])
        sources = [all_articles.loc[all_articles['url'] == article_url]['source'].values[0] for article_url in group]
        if len(set(sources)) < 3:
            continue
        c += 1
        group_key = f"Articles group {c}"
        article_groups_dict[group_key] = [(article_url, all_articles.loc[all_articles['url'] == article_url]['article_text'].values[0]) for article_url in group]
    return article_groups_dict

def merge_groups(d):
    new_d = dict()
    merged_groups = []
    for group_id, articles in d.items():
        if group_id not in merged_groups:
            new_group_id = f"Articles group {len(new_d) + 1}:"
            new_d[new_group_id] = articles
            for other_group_id, other_articles in d.items():
                if other_group_id != group_id and not set(articles).isdisjoint(other_articles):
                    new_d[new_group_id].extend(other_articles)
                    merged_groups.append(other_group_id)
    return {k: list(set(v)) for k, v in new_d.items() if k not in merged_groups}

def get_article_groups(days_ago, host, user, password, database, table_names):
    conn = connect_to_database(host, user, password, database)
    articles_dfs = fetch_articles_from_tables(conn, table_names, days_ago)
    all_articles = pd.concat(articles_dfs, ignore_index=True)
    article_vectors = preprocess_articles(all_articles)
    similar_articles_dict = find_similar_articles(all_articles, article_vectors, 0.5)
    article_groups_dict = create_article_groups_dict(similar_articles_dict, all_articles)
    article_groups_dict = merge_groups(article_groups_dict)
    return article_groups_dict