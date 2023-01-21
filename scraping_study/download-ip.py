import urllib.request

#データの取得
url = "https://api.aoikujira.com/ip/ini"
res = urllib.request.urlopen(url)
data = res.read()

#バイナリーを文字列に変換
text = data.decode("utf-8")
print(text)