import urllib.request
import urllib.parse  #リクエスト用のパラメータを作るのに必要

API = "https://api.aoikujira.com/zip/xml/get.php"

#パラメータをURlエンコードする,下記２行はapi側から指定されていること
values = {
    'fmt' : 'xml',
    'zn': '8190367'
}
params = urllib.parse.urlencode(values)

#リクエスト用のURLを作成
url = API + "?" + params #この形⇨パラメータ付きのURLの作り方、パラメータが少ない時はこの形からいきなりurlを作っても良い(パラメータとは外部から投入されるデータ)
print("url=", url)

#ダウンロード
data = urllib.request.urlopen(url).read()
text = data.decode("utf-8")
print(text)