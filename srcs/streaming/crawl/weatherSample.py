import requests
from bs4 import BeautifulSoup
import re

url = "https://weather.naver.com"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

temperture = soup.find('strong', {'class': 'current'})
temperature = float(temperture.text[6:-2])
temperture = soup.find('span', {'class': 'lowest'})

weekly_list = soup.find('ul', {'class': 'week_list'})
weekly_list_text = weekly_list.text.strip().split('\n')

weekly_text = []
for i in range(len(weekly_list_text)):
    if weekly_list_text[i] != '':
        weekly_text.append(weekly_list_text[i])

weekly_temp = []
daily_temp = []
for i in range(len(weekly_text)):
    if "최고기온" in weekly_text[i] or "최저기온" in weekly_text[i]:
        daily_temp.append(weekly_text[i][4:-1])
        if len(daily_temp) == 2:
            weekly_temp.append(daily_temp)
            daily_temp = []

day = "월화수목금토일"
weekly_dict = {}
for i in range(len(weekly_temp[3:])):
    weekly_dict[day[i]] = weekly_temp[3:][i]

print(weekly_dict['월'][1])

