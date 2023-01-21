from bs4 import BeautifulSoup
import urllib.request as req
url = "https://finance.yahoo.co.jp/quote/USDJPY=X"
res = req.urlopen(url)

soup=BeautifulSoup(res, "html.parser")

price = soup.select_one("._3BGK5SVf").string #参照したいデータのCSSセレクターは検証を押して開発者ツールを利用すればわかる
print("usd/jpy= " , price)
