# python内における「_」
_は繰り返し処理内において使わないということを示すための習慣

https://blog.pyq.jp/entry/Python_kaiketsu_180420#%E9%9D%9E%E5%85%AC%E9%96%8B%E3%81%AE%E3%83%A1%E3%82%BD%E3%83%83%E3%83%89%E3%81%AA%E3%81%A9%E3%82%92%E3%82%A2%E3%83%B3%E3%83%80%E3%83%BC%E3%82%B9%E3%82%B3%E3%82%A21%E3%81%A4%E3%81%A7%E9%96%8B%E5%A7%8B

# python内におけるzip関数
リストの要素をまとめる関数で、forループで複数のリストの要素を1度に取りたい時に使える
for x, target in zip(X, y)
https://note.nkmk.me/python-zip-usage-for/

#　　　np.whereの使い方
```python
np.where(条件式, x, y)
```
条件式が真ならx, 偽ならyを返す

# plt.legendとは
グラフにおける凡例の位置調整をする
bbox_to_anchorでは, 凡例の枠の, 図全体に対する相対的な位置を決定します。 図全体の左下を(0, 0), 右上を(1, 1)としたタプルで与えます。この位置のことをアンカーと呼ぶことにします。

locでは、アンカー(bbox_to_anchorで指定した位置)に, 凡例の枠のどの部分を合わせるかを決定します。loc='upper left'ではアンカーに枠の左上を合わせ、loc='center'では中心を合わせるなどの設定ができます。

borderaxespadでは、アンカーと、locで指定した枠の部分の間の距離を設定することができます。

https://qiita.com/matsui-k20xx/items/291400ed56a39ed63462

# plt.subplot、１つのプロットに複数のグラフを並べたりする

https://www.yutaka-note.com/entry/2020/01/02/232925
subplotsの方
fig, ax = plt.subplots() 引数を省力：１つのサブプロットを生成
fig, axes = plt.subplots(nrows, ncols)：nrows×ncols個のサブプロットを生成

https://www.yutaka-note.com/entry/matplotlib_subplots

# matplotlibはこれが一番わかりやすい
https://qiita.com/nkay/items/d1eb91e33b9d6469ef51

# enumerate関数
"""通常のforループに加えてindexも作れるs"""
for i, name in enumerate(l, 1):
    print(i, name)
# 1 Alice
# 2 Bob
# 3 Charlie
https://note.nkmk.me/python-enumerate-start/