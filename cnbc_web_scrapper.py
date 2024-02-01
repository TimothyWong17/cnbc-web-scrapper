import requests 
from bs4 import BeautifulSoup
import csv
import pandas as pd


class CnbcNewsScrapper:
    def __init__(self):
        self.url = 'https://www.cnbc.com/business/'
        self.data = {}
        
    
    def getCurrentArticles(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, 'html.parser')
        articles = soup.findAll("div", {"class": "Card-standardBreakerCard"})
        print("Scraping CNBC Article Metadata")
        for article in articles:
            if article.find("div", {"class": "Card-titleContainer"}) is not None:
                content = article.find("div", {"class": "Card-titleContainer"})
                #print(content.a.text, content.a['href'])
                self.data[content.a.text] = {"article_link": content.a['href']}
                
        return self.data
    
    
    def getArticleTexts(self):
        self.getCurrentArticles()
    
        for article_title, data in self.data.items():
            print(f"Scraping content from {data['article_link']}")
            r = requests.get(data['article_link'])
            soup = BeautifulSoup(r.text, 'html.parser')
            page = soup.find("div", {"class": "ArticleBody-articleBody"})
            main_content = page.find("div", {"class": "group"})
            paragraphs = main_content.findAll("p")
            article_content = ""
            for paragraph in paragraphs:
                article_content += paragraph.text.strip()
            data['article_content'] = article_content
            
            
        with open(f'data/cnbc_articles.csv', 'w', newline='') as csvfile:
            columns = ['article_title', 'article_link', 'article_content']
            writer = csv.DictWriter(csvfile, fieldnames=columns)

            # Write header
            writer.writeheader()

            # Write data
            print("Writing Data to CSV")
            for row_key, inner_dict in self.data.items():
                row_data = {'article_title': row_key, **inner_dict}
                writer.writerow(row_data)


        return self.data

            
    
    
    
        
        
        
        
if __name__ == "__main__":
    cnbcNewsScrapper = CnbcNewsScrapper()
    cnbcNewsScrapper.getArticleTexts()