from bs4 import BeautifulSoup
import urllib.request as req
#copy→copy-selecterを使えばcssセレクターをクリップボードにコピーできる
url = "https://www.aozora.gr.jp/index_pages/person148.html"
res = req.urlopen(url)
soup = BeautifulSoup(res, "html.parser")
li_list = soup.select("ol > li") #複数要素を取り出してリストで返す コピーしたcssセレクターを参照すると ol > liに情報が入っている
for li in li_list:
    a = li.a #.aはtag"a"のことかな？⇨多分それで確定
    if a != None:
        name = a.string
        href = a.attrs["href"]
        print(name, ">", href)



