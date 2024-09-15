import os


# dataset is a dictionary with the following structure:
# {
#     "category_name": [
#         {
#             "title": "article_title",
#             "url": "article_url",
#             "date": "article_date",
#             "time": "article_time",
#             "author": "article_author"
#             "content": "article_content"
#         }
#     ]

def save_articles_dataset(dataset):
    # Create folder for each category
    for category in dataset.keys():
        # create folder for each category
        category_folder = f"data/{category}"
        os.makedirs(category_folder, exist_ok=True)

        # create file for each article
        for article in dataset[category]:
            # the name of the file is the number of the article
            article_file = f"{category_folder}/{dataset[category].index(article)}.txt"
            with open(article_file, "w") as f:
                f.write(f"Title: {article['title']}\n")
                # f.write(f"URL: {article['url']}\n")
                # f.write(f"Date: {article['date']}\n")
                # f.write(f"Time: {article['time']}\n")
                # f.write(f"Author: {article['author']}\n")
                f.write(f"Content: {article['content']}\n")

    print("Dataset saved successfully!")
