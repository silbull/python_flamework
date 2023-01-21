#beautifulsoupの使い方
#ライブラリーを読み込む
from bs4 import BeautifulSoup

#解析したいHTML
html = '''
<html><body>
  <h1>スクレイピングって何?</h1>
  <p>Webページを解析すること.</p>
  <p>任意の箇所を抽出すること</p>
  <p id="subheading">それでは実際のコードを見て解説！</p>
  <ul>
  <li><a href="http://uta.pw">uta</a></li>
  <li><a href="http://uta.pw">oto</a></li>
  </ul>
</body></html>
'''

#HTMLの解析
soup = BeautifulSoup(html, 'html.parser') #BeautifulSoupのインスタンスの作成、第一引数は解析したいhtml,第二引数は解析を行うparser(構文解析器)

#任意の部分を抽出
h1 = soup.html.body.h1
p1 = soup.html.body.p
p2 = p1.next_sibling.next_sibling
p3 = soup.find(id="subheading") #任意のidを指定して要素を探す
links = soup.find_all("a")

#要素のテキストを表示
print("h1 = " + h1.string)
print("p = " + p1.string)
print("p = " + p2.string)
print("小見出し = " +p3.string)
#aタグの要素を全て抽出
for a in links:
    href =a.attrs['href'] #attrsプロパティでhref属性を取る
    text = a.string #説明テキストはstringプロパティで取る
    print(a.attrs) #attrsは属性と属性値の辞書型
    print(text, ">", href)