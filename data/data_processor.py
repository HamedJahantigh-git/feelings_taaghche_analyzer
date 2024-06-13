from typing import Tuple, List
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

"""
This class for crawl Taghche data for 
complecation dataset    name of the author,
                        name of the translator,
                        name of the book,
                        name of the publication
"""
class Crawler:
    
    def __init__(self, base_url: str) -> None:
        self._base_url = base_url
    
    def crawl(self, book_ids: list, book_names: str) -> List:
        author_list=[]
        translator_list=[]
        publisher_list=[]
        for index in tqdm(range(len(book_ids))):
            name = book_names[index].replace(" ", "_")
            id = str(int(book_ids[index]))
            url = self._base_url+"/"+id+"/"+name
            response = requests.get(url)
            if response.status_code == 200:
                page_content = response.content
                soup = BeautifulSoup(page_content, 'html.parser')
                book_data = soup.find_all(class_ = "bookHeader_detail__JY4wO")[0].get_text("|").split("|")
                author_list.append(book_data[book_data.index("نویسنده:")+1]
                                   if "نویسنده:" in book_data else "")
                translator_list.append(book_data[book_data.index("مترجم:")+1] 
                                       if "مترجم:" in book_data else "")
                publisher_list.append(book_data[book_data.index("انتشارات:")+1]
                                      if "انتشارات:" in book_data else "")
            else:
                print("Failed to retrieve the webpage url: "+ url)
        return [author_list, translator_list, publisher_list]

"""
This class do all process for data prepration.
Dataframe should have column name date, comment,
bookname, rate, bookID, and like 
"""
class DataProcessor:
    _required_columns = ["date", "comment", "bookname", "rate", "bookID", "like"]
    
    def __init__(self, data: pd.DataFrame) -> None:
        missing_columns = [col for col in self._required_columns if col not in data.columns]
        if missing_columns:
            raise Exception(f"DataFrame is missing required columns: {missing_columns}")
        data.dropna(inplace=True)
        data["rate"] = data["rate"].astype(int)
        data["bookID"] = data["rate"].astype(int)
        data["like"] = data["like"].astype(int)
        data["id"] = data.index
        self._data = data
        self._balance_df = None

    def get_df(self, balance_type = False) -> pd.DataFrame:
        return self._balance_df if balance_type else self._data

    def create_label(self, negative_boundary: int, positive_boundary: int) -> None:
        def label_sentiment(score):
            if score>=positive_boundary:
                return 2 #Positive Label
            elif score>negative_boundary:
                return 1 #Neutral Label
            else:
                return 0 #Negetive Label
        self._data["sentiment"] = self._data["rate"].apply(label_sentiment)
        
    def balance_data(self):
        positive = self._data[self._data['sentiment'] == 2]
        neutral = self._data[self._data['sentiment'] == 1]
        negative = self._data[self._data['sentiment'] == 0]

        # Find the size of the smallest class
        min_size = min(len(positive), len(neutral), len(negative))
        print("Positive Size: ", len(positive))
        print("Neutral Size: ", len(neutral))
        print("Negative Size: ", len(negative))
        # sample to balance classes
        positive = positive.iloc[:min_size]
        neutral =  neutral.iloc[:min_size]
        negative =  negative.iloc[:min_size]
        # Combine sampled classes
        self._balance_df =  pd.concat([positive, neutral, negative]).\
            sample(frac=1, random_state=42, replace=True).reset_index(drop=True)


    
      

class DataSpliter:
    
    def __init__(self, data: pd.DataFrame) -> None:
        self._data = data
    
    #TODO @Amir    
    def k_fold(self) -> List:
        pass
    
    # create train, validation, and test dataset for torch learning
    def dataset_train_val_test(self):
        train_data, temp_data = train_test_split(self._, test_size=0.2,  shuffle=False, stratify=balanced_data['sentiment'])

    
        
        