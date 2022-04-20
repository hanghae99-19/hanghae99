import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=M&rtm=N&ymd=20210701', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')


music_chart = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
for music in music_chart:
    rank = music.select_one('td.number').text[:2].strip()
    title = music.select_one('td.info > a.title.ellipsis').text.strip()
    artist = music.select_one('td.info > a.artist.ellipsis').text.strip()
    print(rank, title, artist)


