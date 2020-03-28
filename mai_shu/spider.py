import requests
from bs4 import BeautifulSoup
import csv
import datetime

url = "https://www.bilibili.com/ranking"

# 发起网络请求
response = requests.get(url)
html_text = response.text
soup = BeautifulSoup(html_text, 'html.parser')

# 用来保存视频信息的对象
class Vedio:
    def __init__(self, title, rank, score, play, view, author, author_id, url):
        self.title = title
        self.rank = rank
        self.score = score
        self.play = play
        self.view = view
        self.author = author
        self.author_id = author_id
        self.url = url
        
    def to_csv(self):
        return [self.title, self.rank, self.score, self.play, self.view, self.author, self.author_id, self.url]
    
    @staticmethod
    def csv_title():
        return ['标题', '排名', '得分', '播放量', '观看量', '作者', '作者ID', '网址']

# 提取列表
items = soup.findAll('li', {'class':'rank-item'})
vedios = []

for item in items:
    title = item.find('a', {'class':'title'}).text
    score = item.find('div', {'class':'pts'}).find('div').text
    rank = item.find('div', {'class':'num'}).text
    data = item.find_all('span', {'class':'data-box'})
    play = data[0].text
    view = data[1].text
    author = data[2].text
    author_id = item.find_all('a')[2].get('href')[len('//space.bilibili.com/'):]
    url = item.find_all('a')[0].get('href')
    v = Vedio(title, rank, score, play, view, author, author_id, url)
    print(title, rank, score, play, view, author, author_id, url)
    vedios.append(v)

now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
file_name = 'top100_' + now + '.csv'
with open(file_name, 'w', newline = '') as f:
    pen = csv.writer(f)
    pen.writerow(Vedio.csv_title())
    for v in vedios:
        pen.writerow(v.to_csv())
    