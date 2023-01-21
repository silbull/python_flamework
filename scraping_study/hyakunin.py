#!/usr/bin/env python3

#ライブラリの読み込み
import sys
import urllib.request as req
import urllib.parse as parse

# コマンドライン引数を得る,コマンドライン引数は,sys/argvにリスト型で設定できる.sys.argv[0]にはスクリプトの名前が、sys.argv[1]以降に引数が設定される
if len(sys.argv)  <= 1: #長さが1以下ということは引数が書かれていない
    print("USAGE: hyakunin.py (keyword)")
    sys.exit() #pythonプログラムを中断
keyword = sys.argv[1]


#パラメータをurlエンコードする #エンコード...使えない文字(日本語とか)を使える文字に変更
API = "https://api.aoikujira.com/hyakunin/get.php"
query = {
    "fmt" : "ini",
    "key" : keyword
}
params = parse.urlencode(query) #パラメータをエンcオード
url = API+"?"+params
print("url=", url)

#ダウンロード
with req.urlopen(url) as r:
    b = r.read()
    data = b.decode("utf-8")
    print(data)