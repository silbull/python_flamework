import urllib.request
#URLと保存パスを指定
url = "https://uta.pw/shodou/img/28/214.png"
savename = "test.png"

#ダウンロード
urllib.request.urlretrieve(url, savename) #urlをsavenameとして保存
print("保存しました")