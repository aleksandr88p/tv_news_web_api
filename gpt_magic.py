import time
import random
import openai
from retrying import retry

def generate_summary(api_key, article_groups, query=None):
    openai.api_key = api_key
    summaries = {}

    for group_key, group_articles in article_groups.items():
        # Choose the shortest article and get the link as well
        shortest_article = min(group_articles, key=lambda x: len(x[1]))
        article_to_summarize, link = shortest_article[1], shortest_article[0]

        default_query = "Summarize the following text in 3-8 sentences written a conversational, direct, casual, accessible, chatty and down-to-earth, but catered to insider industry professionals. Give it a catchy title (not in quotations) that includes important keywords and relevant emojis. Bold the most important phrases or key takeaways, write all important names in uppercase, and include emojis where relevant: \n\n"
        # query = f"{query}: \n\n" if query else default_query
        # query += ''
        # prompt = query + article_to_summarize
        full_query = f"{query}: \n\n" if query else default_query
        full_query += ''
        prompt = full_query + article_to_summarize
        # @retry(stop_max_attempt_number=3, wait_fixed=30 * 1000)  # Retry 3 times with a 30-second wait between attempts
        def request_summary():
            for attempt in range(3):
                try:
                    print('***************************************')
                    print(f'from try, len promt is {len(prompt)}')
                    print(prompt)
                    response = openai.Completion.create(
                        engine="text-davinci-003",
                        prompt=prompt,
                        temperature=0.4,
                        max_tokens=500
                    )
                    return response.choices[0].text.strip()
                except Exception as e:
                    print(f"Error generating summary for {group_key}: {e}")


        summary = request_summary()

        if not summary:
            summary = link  # Fall back to the original article if no summary was generated

        summaries[group_key] = summary
        print(f"\nSummary generated for {group_key} based on the article: {link}\n")

    return summaries