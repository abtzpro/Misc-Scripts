import requests
from bs4 import BeautifulSoup

def get_topic():
    topic = input("Please enter a topic: ")
    return topic

def get_article(topic):
    url = f"https://www.wikipedia.org/wiki/{topic}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    article = soup.find_all('p')
    return article

def write_article(article):
    with open('article.txt', 'w') as file:
        for p in article:
            file.write(p.text)

def main():
    topic = get_topic()
    article = get_article(topic)
    write_article(article)

if __name__ == "__main__":
    main()