## Topic Modeling and Word Frequency Analysis of News Articles
import pandas as pd
from cnbc_web_scrapper import CnbcNewsScrapper
import re
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator



class Main:
    def __init__(self):
        self.cnbcWebScrapper = CnbcNewsScrapper()
        
    def data_preprocessing(self):
        data = self.cnbcWebScrapper.getArticleTexts()
        df = pd.DataFrame.from_dict(data=data, orient='index')
        df = df.reset_index()
        df = df.rename(columns={'index': 'article_title'})
        
        df['article_title_processed'] = df['article_title'].map(lambda x: re.sub('[,\.!?]', '', x))
        df['article_title_processed'] = df['article_title'].map(lambda x: x.lower())

        df['article_content_processed'] = df['article_content'].map(lambda x: re.sub('[,\.!?]', '', x))
        df['article_content_processed'] = df['article_content'].map(lambda x: x.lower())

        return df
    
    
    def createWordCloudArticleContent(self):
        df = self.data_preprocessing()
        
        for index, row in df.iterrows():
            print(f"Building WordCloud for {row['article_content_processed'][:30]}")
            wordcloud = WordCloud().generate(row['article_content_processed'])
            wordcloud.to_file(f"wordcloud/{row['article_content_processed'][:30]}.png")
            
    def getTop5MostFrequentWords(self):
        df = self.data_preprocessing()
        stopwords = set(STOPWORDS)
        for index, row in df.iterrows():
            words = [(i.replace("’s", "")) for i in row['article_content_processed'].split(" ") if i not in stopwords]
            df_words = pd.DataFrame({'word': words})
            top_5_words = df_words.value_counts().head(5)
            print(top_5_words)

        
        


    
        
        
        
if __name__ == "__main__":
    main = Main()
    main.createWordCloudArticleContent()
    main.getTop5MostFrequentWords()