import os
from itertools import chain
import requests #get request
import pandas as pd # dataframe handling, data manipulation, convert ke csv 
from bs4 import BeautifulSoup #parsing html

def parse_doc_dic(tr_tag):
    td_child = tr_tag.find_all('td')
    code = td_child[0].find('a').text.strip()
    name = td_child[1].text.strip() # strip() ngerapihin spasi
    high = td_child[2].text.strip().replace('.', '')
    low = td_child[3].text.strip().replace('.', '')
    close = td_child[4].text.strip().replace('.', '')
    volume = td_child[5].text.strip().replace('.', '')
    change = td_child[6].text.strip().replace('.', '')
    base_url = 'https://eoddata.com'
    code_url = td_child[0].find('a')['href']
    uri_col = base_url + code_url
    
    dic = {
        'Code' : code,
        'Name' : name,
        'High' : high,
        'Low' : low,
        'Close' : close,
        'Volume' : volume,
        'Change' : change,
        'Link' : uri_col
    }
    return dic

# LOOP all over alphabet

def scrape_stock(alpha_list):
    base_uri = 'https://eoddata.com/stocklist/INDEX/'
    df_all = []
    for i in range(len(alpha_list)):
        print(f'Get Resoonse of Index {alpha_list[i]}')
        print("---------------------------------------")
        data_uri = base_uri + alpha_list[i] + ".htm"
        response = requests.get(data_uri)
        page_content = response.text
        
        print(f'Parse HTML of Index {alpha_list[i]}')
        print("---------------------------------------")
        doc = BeautifulSoup(page_content, 'html.parser')
        tr_tag_odd = doc.find_all('tr', {'class' : 'ro'})
        tr_tag_even = doc.find_all('tr', {'class' : 're'})
        
        print(f'Get Records of Index {alpha_list[i]}')
        print("---------------------------------------")
        all_record_odd = [parse_doc_dic(tag) for tag in tr_parent_odd] # looping untuk seluruh baris ganjil
        all_record_even = [parse_doc_dic(tag) for tag in tr_parent_even]
        combine_records = list(chain.from_iterable(zip(all_record_odd, all_record_even)))
        df = pd.DataFrame(combine_records) 
        
        path = 'data'
        if not os.path.exists(path):
            os.makedirs(path)
        
        print(f'Saving Index {alpha_list[i]}')
        print("---------------------------------------")
        file_name = alpha_list[i] + ".csv"
        df.to_csv(f'{path}/{file_name}', index = False)
        
        print(f'Append Data from Stock {alpha_list[i]}')
        print("---------------------------------------")
        df_all.append(df) 
    
    df_all_combined = pd.concat(df_all, ignore_index=True)
    return df_all_combined