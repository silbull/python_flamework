---
title: matplotlibのめっちゃまとめ
tags: Python Python3 matplotlib
author: nkay
slide: false
---
# 0. はじめに

やりたいことがあるたびにいちいちGoogleや公式サイトで検索してそれっぽいのを探すのはもう面倒だ。
やっとそれっぽいのを見つけたのに、一行で済むようなことを「plt.なんちゃら」だの「set_なんちゃら」をたくさん並べましたなんてブログはもはや検索妨害だ。
Qiitaにすら僕のためのいい感じのまとめがないなんて……

よく考えたら自分が普段使うようなメソッドなんて限られているじゃないか。
もう自分でまとめるわ。自分のために。

というわけでインポート。

```py
import matplotlib as mpl
import matplotlib.pyplot as plt
```

ちなみに`mpl`は6.4.と6.5.でしか使わない。

# 1. 図（Figure）の作成

matplotlibの描き方は、まず台紙となる`Figure`をつくり、そこに付箋`Axes`を貼り、その付箋にプロットしていくというのが僕の中のイメージ。

![fig_and_axes.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/93e29905-fca2-d51d-8155-185356fbc5e3.jpeg)

したがってまず台紙を作る。これには`plt.figure()`を用いる。`plt.subplots()`もあるが後述。

## 1.1. plt.figure()

```py:plt.figure()の例
>>> fig = plt.figure()
<Figure size 432x288 with 0 Axes>

>>> fig = plt.figure(figsize=(6.4, 4.8), dpi=100,
...                  facecolor='w', linewidth=0, edgecolor='w')
<Figure size 640x480 with 0 Axes>
```

<code>[plt.figure()](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.figure.html#matplotlib.pyplot.figure)</code>を実行すると、無地の台紙`Figure`が戻り値として返される。このときパラメータを入力すると図の設定ができる。

| 主な引数             | 説明                                                 |
| :------------------- | :--------------------------------------------------- |
| *figsize*            | `Figure`のサイズ。横縦を`(float, float)`で指定。 |
| *dpi*                | dpi。整数で指定。                                    |
| *facecolor*          | 図の背景色。Jupyterだと透過色になってたりする。      |
| *linewidth*          | 図の外枠の太さ。デフォルトは`0`（枠なし）。        |
| *edgecolor*          | 図の外枠の色。`linewidth`を指定しないと意味ない。    |
|                      |                                                      |
| *subplotpars*        | `AxesSubplot`の基準を指定する。                    |
| *tight_layout*       | `True`にするとオブジェクトの配置が自動調整される。 |
| *constrained_layout* | `True`にするとオブジェクトの配置が自動調整される。 |

- `figsize`×`dpi`の値が、画像として出力した際の`Figure`のピクセルサイズになる。
- 上記パラメータのうち、`dpi`から`edgecolor`は`Figure.get_XXX(AAA)`で取得でき、`Figure.set_XXX(AAA)`で後から変更できる。`figsize`を取得変更するときは`figwidth`と`figheight`を用いる。
- Tight Layoutにすると、オブジェクト同士が重なっていたらそれを避け、また無駄な余白があればそれを埋めるように各オブジェクトの配置が自動調整される。
- Constrained LayoutはTight Layoutより柔軟らしいが試験中のモード。

```py:figsizeとfigwidth/figheight
>>> fig = plt.figure(figsize=(6, 4), dpi=72)
>>> print(fig.get_figsize())
AttributeError: 'Figure' object has no attribute 'get_figsize'

>>> print(fig.get_figwidth(), fig.get_figheight())
6.0 4.0
```

以下、例（`plt.figure()`だけでは画像出力できないので`Axes`オブジェクトを作成する作業を加えている）。

```py:1-1_a
fig = plt.figure(figsize=(6, 4), dpi=72,
                 facecolor='skyblue', linewidth=10, edgecolor='green')
ax = fig.add_subplot(111)

fig.savefig('1-1_a.png',
            facecolor=fig.get_facecolor(), edgecolor=fig.get_edgecolor())
```

>![1-1_a.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/99bbf22f-94dd-365f-1233-b4f8604c0505.png)

## 1.2. plt.subplots()

2.2.を参照。

# 2. グラフ（Axes）の作成

1.で作った`Figure`に`Axes`を追加する。いろいろ方法がある。

- `Axes`が1つ ⇒ `Figure.add_subplot(111)`（`Figure.add_axes((0, 0, 1, 1))`でも可）
- 同じ大きさの`Axes`を並べる ⇒ `Figure.add_subplot()`
- いろいろな大きさの`Axes`を並べる ⇒ GridSpec
- グラフの大きさ、位置をとにかく自由に決めたい ⇒ `Figure.add_axes()`

## 2.1. Figure.add_subplot()

```py:Figure.add_subplot()の例
>>> ax = fig.add_subplot(1, 1, 1)

>>> ax1 = fig.add_subplot(2, 1, 1)
... ax2 = fig.add_subplot(2, 1, 2)
```

<code>[Figure.add_subplot(nrows, ncols, index)](https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure.add_subplot)</code>を実行すると、無地の付箋`Axes`（正確には`AxesSubplot`オブジェクト）が戻り値として返される。
`nrows`，`ncols`，`index`は位置と大きさを決めるパラメータで、整数を入れる。台紙`Figure`を、縦`nrows`分割・横`ncols`分割したうちの`index`番目の位置に配置された`Axes`が返される。グラフを1つしか作らないときは`(1, 1, 1)`で良い。
`nrows`，`ncols`，`index`が全て一桁のときは、カンマを省略して三桁の整数を一つ指定する書き方（`pos`引数）もできる。

```py:posの例
>>> ax = fig.add_subplot(111)

>>> ax1 = fig.add_subplot(211)
... ax2 = fig.add_subplot(212)
```

このほかパラメータを入力するとグラフ枠の設定ができる。

| 主な引数      | 説明                                                             |
| :------------ | :--------------------------------------------------------------- |
| *title*       | グラフのタイトル。                                               |
| *facecolor*   | グラフの背景色。`fc`でも可。                                   |
| *alpha*       | グラフの透明度を0～1で指定。                                     |
| *zorder*      | オブジェクトが重なっていた時この値が大きい方が前面に描画される。 |
|               |                                                                  |
| *xlabel*      | 横軸名。                                                         |
| *xmargin*     | データの最小値・最大値から横軸の最小値・最大値までのサイズ。     |
| *xlim*        | 横軸の最小値・最大値を`(float, float)`で指定。                 |
| *xticks*      | 横軸の目盛線を表示する値をリストで指定。                         |
| *xticklabels* | 横軸の目盛のラベルをリストで指定。                               |
| *sharex*      | 横軸を共有する`Axes`を指定。                                   |

- 横軸パラメータ名の「x」を「y」に変えると縦軸の設定も同様にできる。

例

```py:2-1_a
fig = plt.figure(facecolor='skyblue')
ax1 = fig.add_subplot(2, 3, 1)  # 2行3列の1番目
ax2 = fig.add_subplot(2, 2, 3)  # 2行2列の3番目
ax3 = fig.add_subplot(1, 4, 4)  # 1行4列の4番目

fig.savefig('2-1_a.png', facecolor=fig.get_facecolor())
```

>![2-1_a.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/e719f00d-6220-8234-3e3f-896ec6c55a59.png)

```py:2-1_b
fig = plt.figure(facecolor="skyblue", tight_layout=True)
ax1 = fig.add_subplot(
    211,
    title="ax1",
    fc="gray",
    ylabel="y1",
    xticks=[2, 4, 8],
    xticklabels=["two", "4", "hachi"],
)
ax2 = fig.add_subplot(223, title="ax2", ylim=(-1, 0), ylabel="y2a")
ax3 = fig.add_subplot(224, title="ax3", sharey=ax2, ylabel="y2b")

fig.savefig("2-1_b.png", facecolor=fig.get_facecolor())
```

>![2-1_b.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/5ff11ab1-6855-c15a-f2f3-14863af8768c.png)

## 2.2. `plt.subplots()`

```py:plt.subplots()の例
>>> fig, ax = plt.subplots()

>>> fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)

>>> fig, axes = plt.subplots(2, 2, sharey='row')
... ax1 = axes[0, 0]
... ax2 = axes[0, 1]
```

<code>[plt.subplots(nrows, ncols)](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots.html#matplotlib.pyplot.subplots)</code>を実行すると、無地の台紙`Figure`と、無地の付箋`Axes`（複数の場合はそのリスト）が戻り値として返される。
`nrows`，`ncols`は`Axes`の配置を決めるパラメータで、指定すると`Figure`を縦`nrows`分割、横`ncols`分割した全ての位置の`Axes`の行列が返される。
`sharex`をTrueにすると全ての横軸が共有される。`sharex`を`col`にすると同じ列同士で横軸が共有される。
このほか`plt.figure()`と同じようにパラメータを入力すると`Figure`の設定ができる（1.1.を参照）。また、`subplot_kw=dict()`内に`Axes`のパラメータを指定できる（2.1.を参照）。

例

```py:2-a_a
fig, axes = plt.subplots(facecolor="skyblue", subplot_kw=dict(facecolor="gray"))

fig.savefig("2-2_a.png", facecolor=fig.get_facecolor())
```

> ![2-2_a.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/dfd1358a-fbc3-5ddd-dc4d-41916f1d6985.png)

```py:2-2_b
fig, axes = plt.subplots(
    2,
    3,
    facecolor="skyblue",
    sharex="col",
    sharey=True,
    subplot_kw=dict(facecolor="gray"),
)

axes[0, 0].set_xlim(0, 10)  # 一番左上のグラフのx軸の範囲を0～10に設定
axes[1, 2].set_xlim(2, 3)  # 一番右下のグラフのx軸の範囲を2～3に設定
axes[0, 1].set_ylim(0, 100)  # 上段中央のグラフのy軸の範囲を0～100に設定

fig.savefig("2-2_b.png", facecolor=fig.get_facecolor())
```

> ![2-2_b.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/bf844e72-d3d9-7d25-e383-0b0365bdd462.png)

## 2.3. GridSpec

```py:GridSpecの例
>>> gs = fig.add_gridspec(2, 4)
... ax1 = fig.add_subplot(gs[0, 0])
... ax2 = fig.add_subplot(gs[1, 1:3])
... ax3 = fig.add_subplot(gs[:, 3])
```

<code>[Figure.add_gridspec(nrows, ncols)](https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure.add_gridspec)</code>を実行すると、`GridSpec`オブジェクトが戻り値として返される。`GridSpec`は`Figure`を分割するマス目のようなもの。
`nrows`と`ncols`は分割基準を決めるパラメータで、指定すると`Figure`を縦`nrows`分割、横`ncols`分割する`GridSpec`が返される。
`Figure.add_subplot(pos)`（2.1.参照）の第一引数に`GridSpec`オブジェクトのスライスを渡すことで、その大きさ・位置の`Axes`を得ることができる。
また、デフォルトでは`Figure`を等分割するが、`width_ratios`，`height_ratios`に縦横の分割の比率のリストを渡すことができる。

例

```py:2-3_a
fig = plt.figure(facecolor="skyblue", tight_layout=True)
gs = fig.add_gridspec(2, 3)
ax1 = fig.add_subplot(gs[0, 0:2], facecolor="gray")
ax2 = fig.add_subplot(gs[1, 0:2], facecolor="lightgreen")
ax3 = fig.add_subplot(gs[:, 2])

fig.savefig("2-3_a.png", facecolor=fig.get_facecolor())
```

>![2-3_a.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/b95f640b-64d2-8923-f28b-202e9ddd3200.png)

```py:2-3_b
fig = plt.figure(facecolor="skyblue")
gs = fig.add_gridspec(2, 2, width_ratios=[2, 1])
ax1 = fig.add_subplot(gs[0], facecolor="gray")
ax2 = fig.add_subplot(gs[2], facecolor="lightgreen")
ax3 = fig.add_subplot(gs[:, 1])

fig.savefig("2-3_b.png", facecolor=fig.get_facecolor())
```

> ![2-3_b.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/83601478-e2b1-0f94-4e68-bf5f29ffdaa0.png)

## 2.4. Figure.add_axes()

```py:Figure.add_axes()の例
>>> ax = fig.add_axes((0, 0, 1, 1))

>>> ax1 = fig.add_axes((0, 1/2, 1/4, 1/2))
... ax2 = fig.add_axes((0, 0.1, 0.5, 0.2))
... ax3 = fig.add_axes((3/4, 0, 1/4, 1))
```

<code>[Figure.add_axes((left, bottom, width, height))](https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure.add_axes)</code>を実行すると、無地の付箋`Axes`が戻り値として返される。
`left`，`bottom`，`width`，`height`は位置と大きさを決めるパラメータで、`Figure`の縦横を1とした相対サイズで指定する。`left`，`bottom`で`Axes`の左下隅の位置座標を指定し、`width`，`height`で`Axes`のサイズを指定する。`(0, 0, 1, 1)`で台紙`Figure`いっぱいにグラフを描く。
このほかパラメータを入力するとグラフ枠の設定ができる（2.1.の表を参照）。

例

```py:2-4_a
fig = plt.figure(facecolor="skyblue")
ax = fig.add_axes((0, 0, 1, 1), facecolor="gray")

fig.savefig("2-4_a.png", facecolor=fig.get_facecolor())
```

> ![2-4_a.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/f02d82d9-7f39-2956-a48a-c1a28cf9d283.png)

```py:2-4_b
fig = plt.figure(facecolor="skyblue")
ax1 = fig.add_axes((0.1, 0.1, 0.4, 0.8), facecolor="gray", ylim=(0, 100))
ax2 = fig.add_axes((0.5, 0.1, 0.4, 0.8), facecolor="lightgreen", sharey=ax1)

ax2.tick_params(
    # 縦軸目盛を右側に表示
    left=False,
    right=True,
    # 縦軸目盛ラベルを右側に表示
    labelleft=False,
    labelright=True,
)

fig.savefig("2-4_b.png", facecolor=fig.get_facecolor())
```

> ![2-4_b.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/9d42cd83-18d9-9ff7-74df-1f01250890ec.png)

## 2.5. Figure.subplot_mosaic()

<code>[Figure.subplot_mosaic(layout)](https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure.subplot_mosaic)</code>を実行すると、`Axes`（正確には`AxesSubplot`オブジェクト）を要素とする、辞書が戻り値として返される。
第一引数`layout`に、`Axes`のラベル名を要素とする行列（リストのリスト）を渡すことで、等間隔に`Axes`を並べることができる。

```python:2-5_a
fig = plt.figure(facecolor="skyblue")
axes = fig.subplot_mosaic(
    [
        ["A", "B"],
    ],
    subplot_kw=dict(facecolor="green"),
)

fig.savefig("2-5_a.png", facecolor=fig.get_facecolor())
```

> ![2-5_a.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/c13f6203-1303-105d-cb0e-820bc734ea31.png)

```python:2-5_b
fig = plt.figure(facecolor="skyblue")
axes = fig.subplot_mosaic(
    [
        ["A"],
        ["B"],
    ],
    subplot_kw=dict(facecolor="green"),
)

fig.savefig("2-5_b.png", facecolor=fig.get_facecolor())
```

> ![2-5_b.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/1f482684-b55f-a152-fcbb-9797383b21a0.png)

隣接する`Axes`のラベル名に同じ名前が指定されていると結合される。また`'.'`を指定するとその部分は余白になる。

```python:2-5_c
fig = plt.figure(facecolor="skyblue")
axes = fig.subplot_mosaic(
    [
        ["A", ".", "C"],
        ["B", "B", "C"],
    ],
    subplot_kw=dict(facecolor="green"),
)

fig.savefig("2-5_c.png", facecolor=fig.get_facecolor())
```

> ![2-5_c.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/a1fbf174-6c57-3df2-3416-05819c388597.png)

リストではなく文字列で表現することも可能。

```python:2-5_c2
fig = plt.figure(facecolor="skyblue")
axes = fig.subplot_mosaic(
    """
    A.C
    BBC
    """,
    subplot_kw=dict(facecolor="green"),
)

fig.savefig("2-5_c2.png", facecolor=fig.get_facecolor())
```

> ![2-5_c2.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/479467d9-3ae7-d0b5-7934-ea4060046525.png)

# 3. プロットする

2.で作った`Axes`に各種メソッドを適用して点や線をプロットしていく。
基本的に第一引数`x`に横軸の値の配列、第二引数`y`に縦軸の値の配列を渡す。値に文字列型の配列を渡した場合は[0, 1, 2, ..., N-1]（`x=range(len(x))`）として扱われる。

ここでは、2022年7月の東京・札幌・那覇の気象データ（平均気温・降水量・平均雲量）を例に用いる。[気象庁のサイト](https://www.data.jma.go.jp/gmd/risk/obsdl/)よりダウンロードの後、ヘッダを変更した。

```text:data.csv
,Tokyo,Tokyo,Tokyo,Sapporo,Sapporo,Sapporo,Naha,Naha,Naha
date,Temperature,Precipitation,CloudCover,Temperature,Precipitation,CloudCover,Temperature,Precipitation,CloudCover
2022/7/1,30.4,0,0.5,20.4,0.0,8.8,27.1,7.0,9.5
2022/7/2,29.5,0,5.0,21.5,0.0,7.5,26.8,26.5,9.5
2022/7/3,28.9,0.0,8.3,25.9,0,5.0,26.5,33.5,9.0
2022/7/4,26.5,3.5,9.3,24.8,0.0,8.0,28.9,0.0,7.3
2022/7/5,26.2,2.0,9.8,23.6,0.0,7.0,28.7,0.5,6.5
（以下略）
```

```python:CSVファイルをpd.DataFrameとして読み込み
import pandas as pd

df = pd.read_csv("data.csv", header=[0, 1], index_col=[0])
df.index = pd.to_datetime(df.index)
print(df.head())
```

| <br>date   | Tokyo<br>Temperature | Tokyo<br>Precipitation | Tokyo<br>CloudCover | Sapporo<br>Temperature | Sapporo<br>Precipitation | Sapporo<br>CloudCover | Naha<br>Temperature | Naha<br>Precipitation | Naha<br>CloudCover |
| :--------- | -------------------: | ---------------------: | ------------------: | ---------------------: | -----------------------: | --------------------: | ------------------: | --------------------: | -----------------: |
| 2022-07-01 |                 30.4 |                      0 |                 0.5 |                   20.4 |                        0 |                   8.8 |                27.1 |                     7 |                9.5 |
| 2022-07-02 |                 29.5 |                      0 |                   5 |                   21.5 |                        0 |                   7.5 |                26.8 |                  26.5 |                9.5 |
| 2022-07-03 |                 28.9 |                      0 |                 8.3 |                   25.9 |                        0 |                     5 |                26.5 |                  33.5 |                  9 |
| 2022-07-04 |                 26.5 |                    3.5 |                 9.3 |                   24.8 |                        0 |                     8 |                28.9 |                     0 |                7.3 |
| 2022-07-05 |                 26.2 |                      2 |                 9.8 |                   23.6 |                        0 |                     7 |                28.7 |                   0.5 |                6.5 |

## 3.1. 折れ線グラフ(`Axes.plot()`)

```py:Axes.plot()の例
>>> ax.plot(x, y1, "rs:", label="line_1")
... ax.plot(y2, color="C0", marker="^", linestyle="-", label="line_2")
```

折れ線グラフは<code>[Axes.plot()](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html#matplotlib.axes.Axes.plot)</code>。
第一引数`x`（横軸の値）は省略可能。省略すると[0, 1, 2, ..., N-1]（`x=range(len(y))`）として扱われる。
第三引数`fmt`には、`color`，`marker`，`linestyle`をひとまとめにして記述できる。

| 主な引数          | 説明                                                             |
| :---------------- | :--------------------------------------------------------------- |
| *label*           | プロットのラベル。凡例に表示される。                             |
| *color*           | 折れ線の色。`c`でも可。                                        |
| *dashes*          | 折れ線の実線部分と空白部分の長さをリストで指定。                 |
| *linestyle*       | 折れ線の線種。`ls`でも可。`dashes`が指定されていると無効。   |
| *linewidth*       | 折れ線の太さ。`lw`でも可。                                     |
| *alpha*           | 透明度を0～1で指定。                                             |
| *zorder*          | オブジェクトが重なっていた時この値が大きい方が前面に描画される。 |
|                   |                                                                  |
| *marker*          | マーカーの形状。`None`でマーカーなし。                         |
| *markersize*      | マーカーのサイズ。`ms`でも可。                                 |
| *markerfacecolor* | マーカーの色。`mfc`でも可。                                    |
| *markeredgewidth* | マーカーの縁の太さ。`mew`でも可。                              |
| *markeredgecolor* | マーカーの縁の色。`mec`でも可。                                |

戻り値は`Line2D`オブジェクトのリスト。

```python:折れ線グラフ1-単純な例
fig = plt.figure(facecolor="white")
ax = fig.add_subplot(111, xlabel="xlabel", ylabel='ylabel')

# xの値のリストとyの値リストを個別に与える
x = [0, 2, 3, 4, 10]
y = [8, 5, 3, 4, 1]
ax.plot(x, y, marker="o", label="blue")

# xの値を与えない場合
y = [1, 3, 2, 5, 4, 3, 6, 5, 8, 7, 9]
ax.plot(y, marker="o", label="orange")

ax.legend()  # 凡例表示
fig.savefig("3-1_a.png")  # 画像保存
```

> ![3-1_a.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/524c1ba3-ae2e-0761-61fe-0b0bb8f59b8b.png)


```python:折れ線グラフ2-データフレームの読み込み例
fig = plt.figure(facecolor="white")
ax = fig.add_subplot(111, xlabel="date", ylabel="Temperature [℃]")

data = df.swaplevel(0, 1, axis=1)["Temperature"]
ax.plot(data, label=data.columns, lw=2)

ax.legend()
ax.grid(axis="y", lw=0.5)
ax.tick_params(rotation=20)
fig.savefig("3-1_b.png")
```

> ![3-1_b.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/a9ed1618-0c20-6f67-1c50-909ef78c1a31.png)

```python:折れ線グラフ3-線とマーカーのカスタマイズ例
fig = plt.figure(facecolor="white")
ax = fig.add_subplot(
    111,
    ylabel="Temperature [℃]",
    xlim=(pd.Timestamp("2022-07-10"), pd.Timestamp("2022-07-17")),
)

data = df.swaplevel(0, 1, axis=1)["Temperature"]
ax.plot(data["Tokyo"], lw=5, alpha=0.5, label="Tokyo")
ax.plot(data["Sapporo"], marker="^", linestyle="-.", mfc="black", label="Hokkaido")
# fmt="rs:"はcolor="r(ed)", marker="s(quare)", linestyle=":" の意味
ax.plot(data["Naha"], "rs:", ms=10, mew=5, mec="green", label="Okinawa")

ax.legend()
ax.grid(axis="y", lw=0.5)
ax.tick_params(axis="x", rotation=20)
fig.savefig("3-1_c.png")
```

> ![3-1_c.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/401c4eb4-9969-f765-db81-4596f52b224e.png)

```python:折れ線グラフ4-応用例
# 軸の中間を省略するということはできないので、
# 省略の前後と中央部を作って擬似的に作成する
fig = plt.figure()
ax1 = fig.add_axes(
    (0.1, 0.1, 0.35, 0.8),
    fc="gainsboro",
    xlim=tuple(pd.to_datetime(["2022-07-01", "2022-07-10"])),
    xticklabels=range(1, 11),
    ylabel="Total Precipitation [mm]",
)
ax2 = fig.add_axes(
    (0.55, 0.1, 0.35, 0.8),
    fc="gainsboro",
    xlim=tuple(pd.to_datetime(["2022-07-20", "2022-07-30"])),
    xticklabels=range(20, 31),
    sharey=ax1,
)
fig.suptitle("Jump plot")
fig.text(0.5, 0, "date", horizontalalignment="center")

ax1.plot(df[("Tokyo", "Precipitation")].cumsum())
ax2.plot(df[("Tokyo", "Precipitation")].cumsum())

ax0 = fig.add_axes((0.45, 0.1, 0.1, 0.8), fc="white", xticks=[], yticks=[])
ax1.spines["right"].set_visible(False)
ax0.spines["left"].set_visible(False)
ax0.spines["right"].set_visible(False)
ax2.spines["left"].set_visible(False)
ax2.tick_params(left=False, labelleft=False)

ax0.spines["top"].set_linestyle((0, (5, 7)))
ax0.spines["bottom"].set_linestyle((0, (5, 7)))

fig.savefig("3-1_d.png")
```

> ![3-1_d.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/7a4b6e47-3a91-894b-03a4-126d7649386e.png)

## 3.2. 散布図（`Axes.scatter()`）

```py:Axes.scatter()の例
>>> ax.scatter(x, y, marker="o")
```

散布図は<code>[Axes.scatter()](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.scatter.html#matplotlib.axes.Axes.scatter)</code>。

| 主な引数     | 説明                                                             |
| :----------- | :--------------------------------------------------------------- |
| *marker*     | マーカーの形状。                                                 |
| *s*          | マーカーのサイズ。                                               |
| *c*          | マーカーの色。`facecolor`，`facecolors`でも可。              |
| *linewidths* | マーカーの縁の太さ。全て同じ場合は`linewidth`，`lw`でも可。  |
| *edgecolors* | マーカーの縁の色。デフォルトは`'face'`（`c`と同じ色）。      |
|              |                                                                  |
| *label*      | プロットのラベル。凡例に表示される。                             |
| *alpha*      | 透明度を0～1で指定。                                             |
| *zorder*     | オブジェクトが重なっていた時この値が大きい方が前面に描画される。 |

- マーカーに関するパラメータは、データ数と同じ要素数のリストを渡すと各点ごとに設定できる。

戻り値は`PathCollection`オブジェクト。

```python:散布図1-単純な例
fig = plt.figure()
ax = fig.add_subplot(111, xlabel="CloudCover", ylabel="Temperature [℃]")

ax.scatter(df[("Tokyo", "CloudCover")], df[("Tokyo", "Temperature")])

fig.savefig("3-2_a.png")
```

> ![3-2_a.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/2ee34c85-9a29-46a3-f427-54c05c5249fa.png)

```python:散布図2-データによってマーカーサイズを変更する例
fig = plt.figure()
ax = fig.add_subplot(111, xlabel="CloudCover", ylabel="Temperature [℃]")

ax.scatter(df[("Tokyo", "CloudCover")], df[("Tokyo", "Temperature")], s=df[("Tokyo", "CloudCover")]**2)
ax.scatter(df[("Sapporo", "CloudCover")], df[("Sapporo", "Temperature")], s=df[("Sapporo", "CloudCover")]**2)
ax.scatter(df[("Naha", "CloudCover")], df[("Naha", "Temperature")], s=df[("Naha", "CloudCover")]**2)

fig.savefig("3-2_b.png")
```

> ![3-2_b.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/9783fa2a-3934-ebd2-4d17-7e12c6899f65.png)

```python:散布図3-データによってマーカー色を変更する例
fig = plt.figure()
ax = fig.add_subplot(111, xlabel="CloudCover", ylabel="Temperature [℃]")

color_label = {"0mm": "#BBBBFF", "1-10mm": "#7777FF", ">10mm": "#0000FF"}
colors = pd.cut(
    df[("Tokyo", "Precipitation")],
    [0, 1, 10, 100],
    right=False,
    labels=color_label.keys(),
)
for color, data in df["Tokyo"].groupby(colors):
    ax.scatter(
        data["CloudCover"], data["Temperature"], c=color_label[color], label=color
    )

ax.legend(title="Precipitation")
fig.savefig("3-2_c.png")
```

> ![3-2_c.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/d17504c5-b405-a637-469c-dcfa13c2562f.png)

## 3.3. 棒グラフ（`Axes.bar()`）

```py:Axes.bar()の例
>>> ax.bar(x, height)
```

棒グラフは<code>[Axes.bar()](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.bar.html#matplotlib.axes.Axes.bar)</code>。

| 主な引数    | 説明                                                                                                                 |
| :---------- | :------------------------------------------------------------------------------------------------------------------- |
| *width*     | 棒の幅（太さ）。横軸の値で指定。デフォルトは`0.8`。                                                                |
| *bottom*    | 棒の下端。主に積み上げ棒グラフにするときに用いる。                                                                   |
| *align*     | 棒の横位置。デフォルトは`'center'`（`x`の値に棒の中心が来る）。<br>`'edge'`にすると`x`の値に棒の左端が来る。 |
| *color*     | 棒の色。`facecolor`，`fc`でも可。                                                                                |
| *hatch*     | 棒の網掛け。                                                                                                         |
| *linewidth* | 棒の縁の太さ。`lw`でも可。                                                                                         |
| *edgecolor* | 棒の縁の色。`ec`でも可。                                                                                           |
| *alpha*     | 透明度を0～1で指定。                                                                                                 |
| *zorder*    | オブジェクトが重なっていた時この値が大きい方が前面に描画される。                                                     |

- `x`の値に棒の右端が来るようにする場合は、`width`を負にして`align='edge'`とする。

戻り値は`BarContainer`オブジェクト。

```python:棒グラフ1-単純な例
fig = plt.figure()
ax = fig.add_subplot(111, xlabel="date", ylabel="Precipitation [mm]")

ax.bar(df.index, df[("Tokyo", "Precipitation")])

ax.tick_params(axis="x", rotation=20)
fig.savefig("3-3_a.png")
```

> ![3-3_a.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/5a2e48c9-6541-546e-edfb-f1c6ab47d8f4.png)

```python:棒グラフ2-棒が複数ある例
fig = plt.figure(figsize=(12, 4))
ax = fig.add_subplot(
    111,
    xlabel="date",
    ylabel="CloudCover",
    xlim=tuple(pd.to_datetime(["2022-06-30 12:00", "2022-07-08 12:00"])),
)

data = df.xs("CloudCover", level=1, axis=1)

w = pd.Timedelta("6H")
[
    ax.bar(data.index - w * (i - 1), data[cityname], label=cityname, width=w, zorder=10)
    for i, cityname in enumerate(data.columns)
]

ax.tick_params(bottom=False)
ax.grid(axis="y", c="gainsboro", zorder=9)
[ax.spines[side].set_visible(False) for side in ["right", "top"]]
ax.legend()
fig.savefig("3-3_b.png")
```

> ![3-3_b.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/c73e7894-99d3-07ad-23f1-04ee07500d5b.png)

### 3.3.1. 横持ち棒グラフ（`Axes.barh()`）

```py:Axes.barh()の例
>>> ax.barh(y, width)
```

横棒グラフは<code>[Axes.barh()](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.barh.html#matplotlib.axes.Axes.barh)</code>。
使い方はほぼ`Axes.bar()`と同じだが、第一引数に横軸の値・第二引数に縦軸の値を渡す。

```python:横持ち棒グラフ2-棒が複数ある例
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(
    111,
    xlabel="CloudCover",
    ylabel="date",
    ylim=tuple(pd.to_datetime(["2022-07-08 12:00", "2022-06-30 12:00"])),
)

data = df.xs("CloudCover", level=1, axis=1)

w = pd.Timedelta("6H")
[
    ax.barh(data.index - w * (i - 1), data[cityname], label=cityname, height=w, zorder=10)
    for i, cityname in enumerate(data.columns)
]

ax.tick_params(bottom=False)
ax.grid(axis="x", c="gainsboro", zorder=9)
[ax.spines[side].set_visible(False) for side in ["right", "bottom"]]
ax.legend()
fig.savefig("3-3_b_2.png")
```

> ![3-3_b_2.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/37dd248e-50a9-7374-023a-112be90b51ca.png)

### 3.3.2. 積み上げ棒グラフ

積み上げ棒グラフを直接描くようなメソッドはない。トリックを使う必要がある。

以下は曜日別の降水量の例である。一番上に位置する月曜日のデータ値を全体の合計にし、火曜日のデータ（実際には火曜日から日曜日までの合計）の棒を月曜日の棒の上から描くことで、積み上げ棒グラフを再現している。欠点としては棒の塗りを半透明にしたい場合は（実際には棒が重なっているので）変になってしまう。

```python:積み上げ棒グラフ1-積算による重ね描き
fig = plt.figure()
ax = fig.add_subplot(111, xlabel="City", ylabel="Precipitation [mm]", xlim=(-0.6, 3.3))

data = df.xs("Precipitation", level=1, axis=1).groupby(df.index.weekday).sum()
data_cumsum = data.loc[::-1].cumsum()

day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
for i in data.index:
    ax.bar(data.columns, data_cumsum.loc[i], label=day_names[i], zorder=10+i)

ax.tick_params(bottom=False)
ax.grid(axis="y", c="gainsboro", zorder=9)
[ax.spines[side].set_visible(False) for side in ["right", "top"]]
ax.legend()
fig.savefig("3-3_c_1.png")
```

> ![3-3_c_1.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/995323bb-72af-a4d0-dec6-7324a64d5e6c.png)

次の例は`Axes.bar`の`bottom=`引数を用いる方法である。これは月曜日のデータの下端（`bottom=`引数）に火曜日から日曜日までの合計値を指定している。

```python:積み上げ棒グラフ2-底上げする方法
fig = plt.figure()
ax = fig.add_subplot(111, xlabel="City", ylabel="Precipitation [mm]", xlim=(-0.6, 3.3))

data = df.xs("Precipitation", level=1, axis=1).groupby(df.index.weekday).sum()

day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
for i in data.index:
    ax.bar(
        data.columns,
        data.loc[i],
        bottom=data.loc[i + 1 :].sum(axis=0),
        label=day_names[i],
        zorder=10,
    )

ax.tick_params(bottom=False)
ax.grid(axis="y", c="gainsboro", zorder=9)
[ax.spines[side].set_visible(False) for side in ["right", "top"]]
ax.legend()
fig.savefig("3-3_c_2.png")
```

> ![3-3_c_2.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/0ac059c5-c9aa-d264-d72e-67e8c06aaba8.png)


## 3.4. ヒストグラム（`Axes.hist()`）

```py:Axes.hist()の例
>>> ax.hist(x)

>>> n, bins, patches = ax.hist([x1, x2], bins=10, range=(x.min(), x.max()))
```

ヒストグラムは<code>[Axes.hist()](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.hist.html#matplotlib.axes.Axes.hist)</code>。第一引数に`x`にデータ配列を渡す（集計は自動で行われる）。

| 主な引数      | 説明                                                                                         |
| :------------ | :------------------------------------------------------------------------------------------- |
| *bins*        | ビン（柱）の本数。デフォルトは`10`。<br>各階級区間（境界）のリストを指定することもできる。 |
| *range*       | 対象範囲を`(float, float)`で指定。デフォルトは`(x.min(), x.max())`。                     |
| *density*     | `True`：`n`（下記参照）の合計が1になるように正規化する。                                 |
| *cumulative*  | `True`：グラフを累積分布にする。                                                           |
| *histtype*    | グラフの種類（下記参照）。デフォルトは`'bar'`。                                            |
| *align*       | 柱の横位置。デフォルトは`'mid'`（区間の中央）。`'left'`，`'right'`が選べる。           |
| *orientation* | デフォルトは`'vertical'`。`'horizontal'`にすると横持ちになる。                           |
|               |                                                                                              |
| *color*       | ビンの色。リストで系列毎に指定可。                                                           |
| *label*       | 系列名。リストで系列毎に指定可。                                                             |
|               |                                                                                              |
| *facecolor*   | ビンの色。`fc`でも可。`color`とは違いリスト不可（全系列同色）。                          |
| *hatch*       | ビンの網掛け。                                                                               |
| *linewidth*   | ビンの縁の太さ。`lw`でも可。                                                               |
| *edgecolor*   | ビンの縁の色。`ec`でも可。                                                                 |
| *alpha*       | 透明度を0～1で指定。                                                                         |
| *zorder*      | オブジェクトが重なっていた時この値が大きい方が前面に描画される。                             |

`histtype`ではグラフの種類を以下から指定する。

- `'bar'`：デフォルト。通常のヒストグラム。系列が複数ある場合は、横に並べて表示する。
- `'barstacked'`：系列が複数ある場合、各ビンが積み上げ棒グラフになる。
- `'step'`：ステップ折れ線グラフ。
- `'stepfilled'`：ステップ折れ線グラフ（塗りつぶし）。系列が複数ある場合は重なって背面に来た系列は見えなくなるので、`alpha`を同時に設定することを推奨。

`Axes.hist()`の戻り値は3つ。グラフオブジェクトのほか、度数のデータを取得することができる。

- 第一戻り値`n`は、各階級の度数（＝各ビンの高さ）の配列（系列が2つ以上の場合は配列のリスト）。
- 第二戻り値`bins`は、各階級区間（境界）の配列。
- 第三戻り値`patches`は、`Patch`オブジェクトのリスト。

```python:ヒストグラム1-単純な例
fig = plt.figure(figsize=(8, 4))
ax = fig.add_subplot(
    111, xticks=range(18, 35, 1), xlabel="Temperature [℃]", ylabel="Days"
)

data = df.xs("Temperature", level=1, axis=1).stack()
n, bins, patches = ax.hist(data, bins=range(18, 35, 1))

# 度数を棒の頭に表示
texts = [
    ax.text(bin + 0.5, num + 0.3, int(num), horizontalalignment="center")
    for num, bin in zip(n, bins)
    if num
]

[ax.spines[side].set_visible(False) for side in ["right", "top"]]
fig.savefig("3-4_a.png")
```

> ![3-4_a.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/002d7a99-6f6a-4fa2-fb25-cee92ce8e0d3.png)

```python:ヒストグラム2-複数のヒストグラムを重ねる例
fig = plt.figure(figsize=(8, 4))
ax = fig.add_subplot(
    111, xticks=range(18, 35, 1), xlabel="Temperature [℃]", ylabel="Days"
)

data = df.xs("Temperature", level=1, axis=1)
n, bins, patches = ax.hist(
    [data["Sapporo"], data["Naha"]],
    bins=range(18, 35, 1),
    label=["Sapporo", "Naha"],
    align="left",
    histtype="stepfilled",
    alpha=0.5,
)

[ax.spines[side].set_visible(False) for side in ["right", "top"]]
ax.legend(title="City")
fig.savefig("3-4_b.png")
```

> ![3-4_b.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/92c650fa-ddba-f8e5-f309-d16fd17af828.png)

## 3.5. 箱ひげ図（`Axes.boxplot()`）

```python:Axes.boxplot()の例
>>> ax.boxplot(x)

>>> ax.boxplot([x1, x2], notch=True, sym="b+", labels=["x1", "x2"])
```

箱ひげ図は<code>[Axes.boxplot()](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.boxplot.html#matplotlib.axes.Axes.boxplot)</code>。第一引数に`x`にデータ配列を渡す（集計は自動で行われる）。

| 主な引数       | 説明                                                                                                                                                           |
| :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| *notch*        | `True`：箱を切れ目ありにする。95%信頼区間が可視化される。                                                                                                    |
| *sym*          | 外れ値のマーカーの色と形状を文字列型で指定。`''`で非表示。                                                                                                   |
| *vert*         | `False`：グラフを横持ちにする。                                                                                                                              |
| *whis*         | 外れ値の境界をIQR=1とした値で指定。デフォルトは`1.5`。<br>また`[5, 95]`のようにするとパーセンタイル区間でも指定可。`'range'`にすると外れ値を考慮しない。 |
| *widths*       | 箱の幅（太さ）。横軸の値で指定。デフォルトは`0.5`。                                                                                                          |
| *labels*       | 系列名（x軸目盛りラベルに表示される）をリストで指定。                                                                                                          |
| *showmeans*    | `True`：平均値を表すマーカーを表示。<br>なお、`meanline=True`を指定しているとマーカーではなく線になる。                                                    |
| *patch_artist* | `True`：箱を`Line2D`オブジェクトではなく`Patch`オブジェクトで描画する。                                                                                  |
| *zorder*       | オブジェクトが重なっていた時この値が大きい方が前面に描画される。                                                                                               |
|                |                                                                                                                                                                |
| *capprops*     | 最大値・最小値を表す線のスタイルを辞書型で指定。                                                                                                               |
| *boxprops*     | 箱のスタイルを辞書型で指定。                                                                                                                                   |
| *whiskerprops* | ひげ線のスタイルを辞書型で指定。                                                                                                                               |
| *medianprops*  | 中央値を表す線のスタイルを辞書型で指定。                                                                                                                       |
| *flierprops*   | 外れ値のマーカーのスタイルを辞書型で指定。`sym`を指定している場合は無効。                                                                                    |
| *meanprops*    | 平均値のマーカーのスタイルを辞書型で指定。                                                                                                                     |

- `capprops`，`boxprops`，`whiskerprops`，`medianprops`に渡すキーワードは`color`（色），`linewidth`（太さ），`linestyle`（線種）など。なお、`c`，`lw`などは不可。
- `patch_artist=True`時に`boxprops`に渡すキーワードは`facecolor`（色），`color`（縁色），`linewidth`（縁の太さ）など。なお、`fc`，`lw`などは不可。
- `flierprops`，`meanprops`に渡すキーワードは`marker`（形状），`markeresize`（大きさ），`markerfacecolor`（色），`markeredgecolor`（縁色）など。なお、`ms`，`mfc`などは不可。

戻り値は複数の`Line2D`（`patch_artist=True`時は箱のみ`Patch`オブジェクト）オブジェクトからなる辞書。

```python:箱ひげ図1-単純な例
fig = plt.figure()
ax = fig.add_subplot(111, xlabel="City", ylabel="Temperature [℃]")

data = df.xs("Temperature", level=1, axis=1)
ax.boxplot(data, labels=data.columns, zorder=10)

ax.grid(axis="y", c="gainsboro", zorder=9)
fig.savefig("3-5_a.png")
```

> ![3-5_a.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/cf2b9d93-b985-cd8e-6831-b9f5d5ed590f.png)

```python:箱ひげ図2-カスタマイズ例
fig = plt.figure()
ax = fig.add_subplot(111, xlabel="Pref", ylabel="Temperature [℃]")

data = df.xs("Temperature", level=1, axis=1)
result = ax.boxplot(
    [data["Sapporo"], data["Tokyo"], data["Naha"]],
    labels=["Hokkaido", "Tokyo", "Okinawa"],
    whis=[5, 95],
    patch_artist=True,
    boxprops=dict(facecolor="skyblue"),  # 箱を水色に
    medianprops=dict(color="blue"),  # 中央値を示す横線を青色に
    flierprops=dict(marker="x", markeredgecolor="orange"),  # 外れ値を橙色に
    zorder=10,
)

# オブジェクトをあとから個別に変更する例
result["fliers"][2].set_markeredgecolor("red")  # 那覇の外れ値を赤に
result["boxes"][1].set_facecolor("green")  # 東京の箱を緑に
# 北海道のひげ下側と最小値を太い紫に
[result[p][0].set(color="purple", linewidth=4) for p in ["caps", "whiskers"]]

ax.grid(axis="y", c="gainsboro", zorder=9)
fig.savefig("3-5_b.png")
```

> ![3-5_b.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/4242c0a9-7250-3eac-8592-9bad4cca2b7d.png)

## 3.6. バイオリン図（`Axes.violinplot()`）

```py:Axes.violinplot()の例
>>> ax.violinplot([x1, x2], [1, 2])
```

バイオリン図は<code>[Axes.violinplot()](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.violinplot.html#matplotlib.axes.Axes.violinplot)</code>。

第一引数`dataset`に各データ、第二引数`positions`（オプション）にy軸の位置を与える。すなわち`dataset`と`positions`の長さは一致していなければならない。

主な引数は以下の通り。x軸目盛りラベルや、色・線の太さ、`zorder`が指定できないなどオプション引数が少ない。

| 主な引数      | 説明                                                            |
| :------------ | :-------------------------------------------------------------- |
| *vert*        | `False`：バイオリンを横向きにする。                             |
| *widths*      | バイオリンの最大幅（太さ）。横軸の値で指定。デフォルトは`0.5`。 |
| *showmeans*   | `True`：平均値を表す横線を表示。                                |
| *showextrema* | `False`：縦線と、最大値と最小値を表す短い横線を非表示。           |
| *showmedians* | `True`：中央値を表す横線を表示。                                |
| *quantiles*   | 短い横線を表示するパーセンタイル値（0～1）をデータごとに指定。  |

- `quantiles`は例えば`[[.25], [.25, .5, .75]]`のように指定すると、1つ目のデータは25%タイル値、2つ目のデータは25%・50%・75%タイル値を表す短い横線が表示される。`dataset`と同じ長さでなければならない。

戻り値は複数の`Line2D`オブジェクトからなる辞書。線や色を変更する場合はこれを用いる。

```python:バイオリン図の例
fig = plt.figure()
ax = fig.add_subplot(111, xlabel="City", ylabel="Temperature [℃]")

data = df.xs("Temperature", level=1, axis=1)
ax.violinplot(data, showmedians=True)

# x軸目盛りラベルを設定
ax.set_xticks(range(1, data.shape[1] + 1), labels=data.columns)

ax.grid(axis="y", c="gainsboro")
fig.savefig("3-6_a.png")
```

> ![3-6_a.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/3edf4af8-6559-6cce-9082-ed51f51f9810.png)

# 4. 文字・注釈を入れる

## 4.1. 文字列の挿入（`Figure.text()`，`Axes.text()`）

```py:Figure.text()，Axes.text()の例
>>> fig.text(0.1, 0.1, 'fig_text')
Text(0.1, 0.1, 'fig_text')

>>> ax.text(0.1, 0.1, 'ax_text')
Text(0.1, 0.1, 'ax_text')
```

図中に文字列を挿入する場合は[`Figure.text()`](https://matplotlib.org/api/_as_gen/matplotlib.figure.Figure.html#matplotlib.figure.Figure.text)，[`Axes.text()`](https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.text.html#matplotlib.axes.Axes.text)を用いる。第一引数`x`に横位置・第二引数`y`に縦位置・第三引数`s`に文字列を渡す。
`Figure.text()`は`Figure`の左下を(0, 0)・右上を(1, 1)とした座標で`x`，`y`を指定する。`Axes.text()`はグラフの値で`x`，`y`を指定する。
なお、文字列中の改行は`'\n'`。

| 主な引数              | 説明                                                                                    |
| :-------------------- | :-------------------------------------------------------------------------------------- |
| *horizontalalignment* | 左右揃え。`ha`でも可。`'left'`，`'center'`，`'right'`から指定。                 |
| *verticalalignment*   | 上下揃え。`va`でも可。`'top'`，`'center'`，`'bottom'`，`'baseline'`から指定。 |
| *rotation*            | 回転角度。90度の場合は`90`のほか`'vertical'`でも指定可能。                          |
| *rotationmode*        | `'anchor'`：(x, y)の値を中心に文字列を回転する。`ha`や`va`の挙動が変わる。        |
|                       |                                                                                         |
| *fontfamily*          | フォント。                                                                              |
| *fontname*            | フォント。                                                                              |
| *fontsize*            | 大きさ。`size`でも可。                                                                |
| *fontweight*          | ウェイト。0～1000の数値，或いはウェイトネームの文字列を指定。                           |
| *fontstyle*           | `'italic'`：斜体。                                                                    |
| *color*               | 色。                                                                                    |
| *bbox*                | 図形スタイルを辞書形式で指定（4.5.参照）。                                              |
| *alpha*               | 透明度を0～1で指定。                                                                    |
| *zorder*              | オブジェクトが重なっていた時この値が大きい方が前面に描画される。                        |
|                       |                                                                                         |
| *withdash*            | `True`：文字列から(x, y)に向かって線を伸ばす。                                        |
| *dashlength*          | 線の長さ。                                                                              |
| *dashdirection*       | 線の方向。`0`：文字列の右側。`1`：文字列の左側。                                    |
| *dashrotation*        | 線の角度。(x, y)から見て反時計回りに0～180で指定。0未満や180以上も可能だが非推奨。      |
| *dashpad*             | 線の端と文字列の間の余白の距離。デフォルトは`3`。                                     |
| *dashpush*            | 線の端と(x, y)の間の余白の距離。                                                        |

戻り値は`Text`オブジェクト。

```py:4-1_a
fig = plt.figure(facecolor='skyblue')
ax1 = fig.add_axes((0.1, 0.1, 0.4, 0.8), facecolor='lightgreen', ylim=(0, 100))
ax2 = fig.add_axes((0.5, 0.1, 0.4, 0.8), facecolor='lightblue', sharey=ax1)
ax2.tick_params(left=False, right=True, labelleft=False, labelright=True)
ax1.grid()
ax2.grid()

# 基本
ax1.text(0.2, 80, 'text')
ax1.text(0.2, 60, 'left', ha='left')
ax1.text(0.2, 40, 'center', ha='center')
ax1.text(0.2, 20, 'right', ha='right')
ax1.text(0.4, 80, 'top', va='top')
ax1.text(0.6, 80, 'center', va='center')
ax1.text(0.8, 80, 'bottom', va='bottom')

# 回転
ax1.text(0.4, 60, 'r90b', rotation='vertical', va='bottom')
ax1.text(0.6, 60, 'r90c', rotation='vertical', va='center')
ax1.text(0.8, 60, 'r90t', rotation='vertical', va='top')
ax1.text(0.4, 40, 'r270b', rotation=270, va='bottom')
ax1.text(0.6, 40, 'r270c', rotation=270, va='center')
ax1.text(0.8, 40, 'r270t', rotation=270, va='top')

# fig
fig.text(0, 0, 'leftbottom')
fig.text(1, 0, 'rightbottom', ha='right')
fig.text(0, 1, 'lefttop', va='top')
fig.text(1, 1, 'righttop', ha='right', va='top')

# withdash
[ax2.text(0.5, 50, 'd_rot'+str(r), withdash=True, dashlength=45,
          dashrotation=r, dashpush=r/10, color='C'+str(int(r/30)))
 for r in range(0, 180, 30)]
[ax2.text(0.5, 50, 'd_rot'+str(r+180), withdash=True, dashlength=45,
          dashdirection=1, dashrotation=r, dashpush=(r+180)/10)
 for r in range(0, 180, 30)]

fig.savefig('4-1_a.png', facecolor=fig.get_facecolor())
```

>![4-1_a.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/be930e71-765b-54b8-63b3-77b67b07540d.png)

## 4.2. 図タイトル（`Figure.suptitle()`）

```py:Figure.suptitle()の例
>>> fig.suptitle('title')
Text(0.5, 0.98, 'title')
```

図`Figure`全体に対してにタイトルを挿入する場合は、[`Figure.suptitle()`](https://matplotlib.org/api/_as_gen/matplotlib.figure.Figure.html#matplotlib.figure.Figure.suptitle)に文字列を渡すのが容易。
なお、個別のグラフ`Axes`に対してにタイトルを挿入する場合は、作成時に`title`で指定する（2.参照）のが容易だが、後から追加変更する場合は`Axes.set_title()`で可能。

| 主な引数 | 説明    |
| :------- | :------ |
| `x`    | x座標。 |
| `y`    | y座標。 |

- その他のパラメータは4.1.を参照。

戻り値は`Text`オブジェクト。`Figure.text()`，`Axes.text()`に専用のデフォルトパラメータが与えられているだけのようである。

```py:4-2_a
# py:4-2_a
fig = plt.figure()
fig.subplots_adjust(wspace=0.5)
ax1 = fig.add_subplot(131)
ax2 = fig.add_subplot(132)
ax3 = fig.add_subplot(133)

fig.suptitle('figtitle')
ax1.set_title('ax1title')
ax2.set(title='ax2title')
ax3.update(dict(title='ax3title'))

fig.savefig('4-2_a.png')
```

>![4-2_a.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/b07ee254-5368-a312-8464-cb744609c80e.png)

## 4.3. 矢印（`Axes.arrow()`）

```py:Axes.arrow()の例
>>> ax1.arrow(0, 1, 1, 3, width=0.1)
```

矢印の挿入は[`Axes.arrow()`](https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.arrow.html#matplotlib.axes.Axes.arrow)で行う。第一引数`x`・第二引数`y`に始点の座標、第三引数`dx`・第四引数`dy`に矢の長さを、グラフの座標系で渡す。

| 主な引数               | 説明                                                                                      |
| :--------------------- | :---------------------------------------------------------------------------------------- |
| *width*                | 矢柄の太さ。                                                                              |
| *head_width*           | 矢尻の太さ。デフォルトでは`width`に依存。                                               |
| *head_length*          | 矢尻の長さ。デフォルトでは`head_width`に依存。                                          |
| *overhang*             | 矢尻の返しの長さ。デフォルトは`0`（返しなし）。                                         |
| *shape*                | `left`，`right`で縦半分のみの表示。                                                   |
| *length_includes_head* | `True`：(dx, dy)を矢印の先端にする。デフォルトは`False`（(dx, dy)に矢尻後端がくる）。 |
|                        |                                                                                           |
| *facecolor*            | 色。`fc`でも可。                                                                        |
| *hatch*                | 網掛け。                                                                                  |
| *linewidth*            | 縁の太さ。`lw`でも可。                                                                  |
| *edgecolor*            | 縁の色。`ec`でも可。                                                                    |
| *alpha*                | 透明度を0～1で指定。                                                                      |
| *zorder*               | オブジェクトが重なっていた時この値が大きい方が前面に描画される。                          |

戻り値は`FancyArrow`オブジェクト。

```py:4-3_a
fig = plt.figure()
ax1 = fig.add_subplot(111, xlim=(0, 7), ylim=(0, 6))
ax1.grid(zorder=5)

ax1.arrow(0, 1, 1, 3, zorder=10, width=0.1, fc='red')
ax1.arrow(1, 1, 1, 3, zorder=10, width=0.1, fc='blue',
          head_width=0.1)
ax1.arrow(2, 1, 1, 3, zorder=10, width=0.1, fc='orange',
          head_length=1)
ax1.arrow(3, 1, 1, 3, zorder=10, width=0.1, fc='brown',
          overhang=0.3)
ax1.arrow(4, 1, 1, 3, zorder=10, width=0.1, fc='gray',
          shape='left')
ax1.arrow(5, 1, 1, 3, zorder=10, width=0.1, fc='gray',
          shape='right')
ax1.arrow(6, 1, 1, 3, zorder=10, width=0.1, fc='green',
          length_includes_head=True)

fig.savefig('4-3_a.png')
```

>![4-3_a.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/f088c58d-8ccd-3f5b-42c6-6f41dce595dd.png)

## 4.4. 座標に対して文字・矢印（`Axes.annotate()`）

```py:Axes.annotate()の例
>>> ax1.annotate('Text', (0, 1))
Text(0, 1, 'Text')

>>> ax1.annotate('Text', (1, 1), (2, 4),
...              arrowprops=dict(arrowstyle='->'))
Text(1, 1, 'Text')
```

ある座標に対して文字、或いは文字と矢印を指し示す場合は[`Axes.annotate()`](https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.annotate.html#matplotlib.axes.Axes.annotate)を用いる。第一引数`s`に文字列・第二引数`xy`に座標位置をタプルで渡す。
第三引数`xytext`に座標位置を渡すと、文字列が`xytext`の位置に、矢印の先が`xy`の位置になる。

| 主な引数            | 説明                                                                                                                                            |
| :------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------- |
| *xytext*            | 文字列の座標を`(float, float)`で指定。                                                                                                        |
| *xycoords*          | `xy`の座標の指定方法。デフォルトは`data`（グラフのデータの値）。<br>`'figure fraction'`：`Figure`左下を(0, 0)，右上を(1, 1)とした座標。 |
| *textcoords*        | `xytext`の座標の指定方法。デフォルトは`xycoords`に従う。                                                                                    |
|                     |                                                                                                                                                 |
| *arrowprops*        | 矢印に関するパラメータを辞書型で指定。                                                                                                          |
| ┣ *arrowstyle*      | 矢印のスタイル（下記参照）。デフォルトは`'simple'`。                                                                                          |
| ┣ *mutation_scale*  | 矢印の大きさ。                                                                                                                                  |
| ┣ *connectionstyle* | 矢柄のスタイル（下記参照）。デフォルトは`'arc3'`。                                                                                            |
| ┣ *shrinkA*         | 文字列と矢印後端の間の余白の距離。                                                                                                              |
| ┣ *shrinkB*         | 矢印先端と`xy`の間の余白の距離。                                                                                                              |
| ┗ **kwargs          | ほか`fc`，`hatch`，`lw`，`ec`，`alpha`，`zorder`など指定可（4.2.参照）。                                                            |

- このほか、文字列に関するパラメータは4.1.を参照。
- Arrow Style，Connection Styleはスタイル名を文字列で渡すが、それに続けて細かい設定を指定することも可能。複雑になるのでここでは詳述しない。

戻り値は`Annotation`オブジェクト。

```py:4-4_a
fig = plt.figure(figsize=(12, 4))
ax = fig.add_subplot(111, title='Arrow Styles',
                     xlim=(-0.2, 14.4), ylim=(-0.1, 1.2))

arrstyles = ['-', '->', '-[', '-|>', '<-',
             '<->', '<|-', '<|-|>', ']-', ']-[',
             'fancy', 'simple', 'wedge', '|-|']

[ax.annotate(arrstyle, (i, 0), (i+1, 1), zorder=10, ha='center', size=14,
             arrowprops=dict(arrowstyle=arrstyle, mutation_scale=20))
 for i, arrstyle in enumerate(arrstyles)]

fig.savefig('4-4_a.png')
```

>![4-4_a.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/50b675fc-07a3-cba7-9fc3-d6b3c0ce69b7.png)

```py:4-4_b
fig = plt.figure(figsize=(10, 4))
ax = fig.add_subplot(111, title='Connection Styles',
                     xlim=(-0.2, 10.4), ylim=(-0.1, 1.3))

constyles = ['angle', 'angle3', 'arc', 'arc3', 'bar']

[ax.annotate(constyle, (i*2, 0), (i*2+2, 1), zorder=10, ha='center', size=14,
             arrowprops=dict(arrowstyle='-|>', mutation_scale=20,
                             connectionstyle=constyle))
 for i, constyle in enumerate(constyles)]

fig.savefig('4-4_b.png')
```

>![4-4_b.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/7e3f9adf-c951-fad4-722f-1359fabf94fd.png)

## 4.5. 図形の設定（Bbox）

```py:Bboxの例
>>> ax.text(1, 1, 'TextWithBox', bbox=(dict(boxstyle='circle')))
Text(1, 1, 'TextWithBox')
```

引数`bbox`に辞書形式でパラメータを指定することで、文字列を任意の図形で囲む事ができる。

| 主な引数    | 説明                                                             |
| :---------- | :--------------------------------------------------------------- |
| *boxstyle*  | 図形のスタイル（下記参照）。                                     |
|             |                                                                  |
| *color*     | 背景と縁の色。                                                   |
| *facecolor* | 背景色。`fc`でも可。                                           |
| *hatch*     | 網掛け。                                                         |
| *linewidth* | 縁の太さ。`lw`でも可。`color`を指定していると無効。          |
| *edgecolor* | 縁の色。`ec`でも可。`color`を指定していると無効。            |
| *alpha*     | 透明度を0～1で指定。                                             |
| *zorder*    | オブジェクトが重なっていた時この値が大きい方が前面に描画される。 |

- [Box Style](https://matplotlib.org/api/_as_gen/matplotlib.patches.BoxStyle.html#matplotlib.patches.BoxStyle)はスタイル名を文字列で渡すが、それに続けて細かい設定を指定することも可能。複雑になるのでここでは詳述しない。

```py:4-5_a
fig = plt.figure(figsize=(10, 2))
fig.suptitle('Box Styles')
ax = fig.add_axes((0.04, 0.1, 0.92, 0.8))

bstyles = ['circle', 'darrow', 'larrow', 'rarrow', 'round',
           'round4', 'roundtooth', 'sawtooth', 'square']

[fig.text(i*0.1, 0.5, bstyle, color='w', bbox=(dict(
    boxstyle=bstyle, fc=f'C{i}')))
 for i, bstyle in enumerate(bstyles, 1)]

fig.savefig('4-5_a.png')
```

>![4-5_a.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/daa44c54-b3be-b4b6-56b5-8910d08bfe9b.png)

# 5. 凡例の設定

## 5.1. 凡例の追加

凡例は<code>[Figure.legend()](https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure.legend)</code>あるいは<code>[Axes.legend()](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.legend.html#matplotlib.axes.Axes.legend)</code>を用いる。このときパラメータを入力すると凡例の設定ができる。

| 主な引数         | 説明                                                                |
| :--------------- | :------------------------------------------------------------------ |
| *handles*        | 凡例に載せるデータ（5.2.参照）。                                    |
| *labels*         | 各系列の表示名前（5.2.参照）。                                      |
| *loc*            | 凡例の位置（5.3.参照）。                                            |
| *bbox_to_inches* | 凡例の位置と大きさ（5.4.参照）。                                    |
| *mode*           | `'expand'`：幅を横いっぱいに広げる（5.4.も参照）。                |
|                  |                                                                     |
| *shadow*         | `True`：凡例ボックスの影を表示。                                  |
| *framealpha*     | 凡例ボックスの透明度を0～1で指定。                                  |
| *facecolor*      | 凡例ボックスの背景色。                                              |
| *edgecolor*      | 凡例ボックスの縁の色。                                              |
|                  |                                                                     |
| *title*          | 凡例のタイトル名。                                                  |
| *title_fontsize* | 凡例のタイトルのフォントサイズ。                                    |
| *ncol*           | 凡例の列数。デフォルトは`1`。                                     |
| *fontsize*       | 凡例のフォントサイズ。                                              |
|                  |                                                                     |
| *numpoints*      | マーカーの数（折れ線グラフのとき）。                                |
| *scatterpoints*  | マーカーの数（散布図のとき）。                                      |
| *markerscale*    | マーカーの多大きさ。                                                |
|                  |                                                                     |
| *borderpad*      | 凡例の文字とボックス縁の間の余白を、`fontsize`を1とした値で指定。 |
| *labelspacing*   | 凡例の行間を、`fontsize`を1とした値で指定。                       |
| *handlelength*   | 凡例の線の長さを、`fontsize`を1とした値で指定。                   |
| *handletextpad*  | 凡例の線と系列名の間の余白を、`fontsize`を1とした値で指定。       |
| *columnspacing*  | 凡例の列間を、`fontsize`を1とした値で指定。                       |

- `zorder`引数は指定できない。前後の位置を指定する場合は、凡例オブジェクトの`.set_zorder()`メソッド（`.set(zorder=)`でも可）を用いる。

## 5.2. 表示データの設定

`Figure.legend()`あるいは`Axes.legend()`を用いると、自動で`Figure`或いは`Axes`内にある`Artist`オブジェクト（プロット）をかきあつめて凡例に表示してくれる。このときオブジェクトに`label`が指定されていれば、それが表示名となる。
データを自分で設定する場合は引数`handles`に`Artist`オブジェクトのリストを渡し、表示名を自分で設定する場合は引数`labels`に表示名のリストを渡す。

```python:凡例を変更した例
fig = plt.figure()
ax = fig.add_subplot(111, xlabel="City", ylabel="Precipitation [mm]", xlim=(-0.5, 4))

data = df.xs("Precipitation", level=1, axis=1).groupby(df.index.weekday).sum()

bars = [
    ax.bar(
        data.columns,
        data.loc[i],
        bottom=data.loc[i + 1 :].sum(axis=0),
        zorder=10,
    )
    for i in data.index
]

ax.tick_params(bottom=False)
ax.grid(axis="y", c="gainsboro", zorder=9)
[ax.spines[side].set_visible(False) for side in ["right", "top"]]

day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
ax.legend(
    handles=bars,
    labels=[f"{day_names[i]} = {data.loc[i].sum()}" for i in range(7)],
)
fig.savefig("3-3_c_2.png")
```

> ![3-3_c_2 (1).png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/5825c486-81bc-d6f6-1200-0ef600a13f3a.png)


## 5.3. 凡例の位置設定

引数`loc`に特定の文字列・数値を渡すことで凡例の位置を指定できる。

| 文字列         | 数字 | 説明                     |
| :------------- | :--- | :----------------------- |
| 'best'         | 0    | 以下から自動で位置を決定 |
| 'upper right'  | 1    | 右上                     |
| 'upper left'   | 2    | 左上                     |
| 'lower left'   | 3    | 左下                     |
| 'lower right'  | 4    | 右下                     |
| 'right'        | 5    | 右中央                   |
| 'center left'  | 6    | 左中央                   |
| 'center right' | 7    | 右中央                   |
| 'lower center' | 8    | 中央下                   |
| 'upper center' | 9    | 中央上                   |
| 'center'       | 10   | 中央                     |

- `'center right'`と`'right'`は同じ。
- 左下を(0, 0)・右上を(1, 1)とする座標を`(float, float)`の形で渡すことで、凡例左下隅の位置を任意に指定可能。

## 5.4. 凡例の位置と大きさを細かく設定

引数`bbox_to_inches`に、左下を(0, 0)・右上を(1, 1)とする座標を`(float, float)`の形で渡すことで、`loc`で指定した凡例の隅がその位置にくる。
また、横位置・縦位置に続けて幅・高さを加えた`(float, float, float, float)`の形にすることで、大きさを指定することもできる。

`mode`引数のデフォルトは`None`になっている。これが`None`のとき、凡例の横幅は表示文字列に合わせて自動調整される。
`mode='expand'`とすることで、内容にかかわらず凡例の幅を`bbox_to_inches`で指定した値にすることができる。

# 6. 軸の設定

グラフの軸は、横軸`Axes.xaxis`と縦軸`Axes.yaxis`と、グラフの枠`Axes.spines`でできている。

## 6.1. グラフの枠（`Axes.spines`）の設定

グラフの枠`Axes.spines`は、上下左右それぞれの枠線`Spine`オブジェクトの集合（辞書形式になっている）。キー`'left'`，`'right'`，`'top'`，`'bottom'`でそれぞれ取り出せる。
`Spine.set(XXX=AAA)`或いは`Spine.update(dict(XXX=AAA))`或いは`Spine.set_XXX(AAA)`でパラメータを変更することができる。

| 主な引数    | 説明                                                                                      |
| :---------- | :---------------------------------------------------------------------------------------- |
| *position*  | 枠の位置を`(position type, amount)`あるいは`'zero'`，`'center'`で指定（下記参照）。 |
|             |                                                                                           |
| *color*     | 色。`edgecolor`，`ec`でも可。                                                         |
| *dashes*    | 実線部分と空白部分の長さをリストで指定。                                                  |
| *linestyle* | 線種。`ls`でも可。`dashes`が指定されていると無効。                                    |
| *linewidth* | 太さ。`lw`でも可。                                                                      |
| *alpha*     | 透明度を0～1で指定。                                                                      |
| *zorder*    | オブジェクトが重なっていた時この値が大きい方が前面に描画される。                          |
| *visible*   | `False`：非表示。                                                                       |

`position`で指定できる`position type`は以下の通り。

- `'outward'`：`amount`pxだけ`Axes`の外側に配置。`amount`を負にすると`Axes`の内側に配置。
- `'axes'`：`Axes`左下を(0, 0)・右上を(1, 1)とした座標の位置に配置。
- `'data'`：データの座標位置に配置。
- `position='zero'`或いは`position=('data', 0)`で0のところに軸を配置できる。
- `position='center'`或いは`position=('axes', 0.5)`で`Axes`の中心に軸を配置できる。

```py:6-1_a
fig = plt.figure(figsize=(12, 4))
ax1 = fig.add_subplot(141, fc='skyblue', xlim=(-5, 10), title='axis1')
ax1.spines['left'].set(position=('outward', 10))
ax1.spines['bottom'].set(position=('outward', 10))

ax2 = fig.add_subplot(142, fc='skyblue', xlim=(-5, 10), title='axis2')
ax2.spines['left'].set(position=('axes', 0.2))
ax2.spines['bottom'].set(position=('axes', 0.2))

ax3 = fig.add_subplot(143, fc='skyblue', xlim=(-5, 10), title='axis3')
ax3.spines['left'].set(position=('data', -3))
ax3.spines['bottom'].set(position=('data', 0.1))

ax4 = fig.add_subplot(144, fc='skyblue', xlim=(-5, 10), title='axis4')
ax4.spines['left'].set(position='zero')
ax4.spines['bottom'].set(position='center')

fig.savefig('6-1_a.png')
```

>![6-1_a.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/cb0ff987-2a27-1e62-eb4b-58745ffe17ce.png)

## 6.2. 軸ラベルの設定

グラフの軸ラベルは、`Axes`作成時に`xlabel`，`ylabel`で指定する（2.参照）のが容易だが、後から追加変更する場合は`Axes.set_xlabel('横軸ラベル名')`，`Axes.set_ylabel('縦軸ラベル名')`を用いる。この時4.1.のパラメータを用いて文字のスタイルを指定可能。
縦軸横軸のラベル名を同時に変更する場合は，`Axes.set(xlabel='横軸ラベル名', ylabel='縦軸ラベル名')`あるいは`Axes.update(dict(xlabel='横軸ラベル名', ylabel='縦軸ラベル名'))`で一行で書ける。

```py:6-2_a
fig = plt.figure()
fig.subplots_adjust(wspace=1)

ax1 = fig.add_subplot(131, xlabel='x1', ylabel='y1')

ax2 = fig.add_subplot(132)
ax2.set_xlabel('x2', size=20, color='red')
ax2.set_ylabel('y\n2', rotation=0, ha='center', color='g',
               bbox=dict(boxstyle='circle', fc='orange'))

ax3 = fig.add_subplot(133)
ax3.set(xlabel='x3', ylabel='y3')

fig.savefig('6-2_a.png')
```

>![6-2_a.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/1f11f294-a4c8-0b3a-221d-546a49c5e29b.png)

## 6.3. 軸の最小値・最大値の設定

軸の最小値・最大値は、`Axes`作成時に`xlim`，`ylim`で指定する（2.参照）のが容易だが、後から追加変更する場合は`Axes.set_xlim(left, right)`，`Axes.set_ylim(bottom, top)`を用いる。
縦軸横軸の最小値・最大値を同時に変更する場合は，`Axes.set(xlim=(left, right), ylim=(bottom, top))`あるいは`Axes.update(dict(xlim=(left, right), ylim=(bottom, top)))`で一行で書ける。

`Axes.set_xlim(auto=True)`，`Axes.set_ylim(auto=True)`とすると、データの最小値・最大値から自動で軸の最小値・最大値が決定される。`Axes`作成時に`xmargin`，`ymargin`を指定していると、「(データの最大値 - データの最小値) * margin」が左右の余白の幅になる（デフォルトは`0.05`）。

```py:6-3_b
fig = plt.figure(figsize=(10, 4))

# デフォルト（margin=0.05）
ax1 = fig.add_subplot(131)
ax1.plot([[1, 0], [0, 1]])

# margin=0
ax2 = fig.add_subplot(132, xmargin=0, ymargin=0)
ax2.plot([[1, 0], [0, 1]])

# margin=1
ax3 = fig.add_subplot(133, xmargin=1, ymargin=1)
ax3.plot([[1, 0], [0, 1]])

fig.savefig('6-3_b.png')
```

>![6-3_b.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/5f94df92-c927-2599-37d2-18a01e02fefc.png)

## 6.4. 軸の目盛の設定

軸の目盛は`Axis.set_major_locator()`（大目盛）と`Axis.set_minor_locator()`（補助目盛）に各種`Locator`を渡すことで変更可能。`Locator`は`mpl.ticker.XXXLocator()`で作成・取得する。
デフォルトでは`major_locator`（大目盛）は`AutoLocator`，`minor_locator`（補助目盛）は`NullLocator`になっている（っぽい）。

```py:6-4_a
fig = plt.figure()
ax = fig.add_axes((0.2, 0.2, 0.6, 0.6))
ax.plot([0, 5])

ax.set_xlabel(str(type(ax.xaxis.get_major_locator())) + '\n'
              + str(type(ax.xaxis.get_minor_locator())))
ax.set_ylabel(str(type(ax.yaxis.get_major_locator())) + '\n'
              + str(type(ax.yaxis.get_minor_locator())))

fig.savefig('6-4_a.png')
```

>![6-4_a.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/cb5e6f19-6ab1-2cfa-2827-f2d79aa687c0.png)

### 6.4.1. 目盛なし（`NullLocator`）

`NullLocator`で目盛なしにできるが、`Axes.set_xticks([])`，`Axes.set_yticks([])`の方が簡単（6.4.8.参照）。

```py:6-4_b
fig = plt.figure()
ax = fig.add_axes((0.2, 0.2, 0.6, 0.6))
ax.plot([0, 5])

ax.xaxis.set_major_locator(mpl.ticker.NullLocator())
ax.yaxis.set_major_locator(mpl.ticker.NullLocator())

ax.set(xlabel=type(ax.xaxis.get_major_locator()),
       ylabel=type(ax.yaxis.get_major_locator()))
fig.savefig('6-4_b.png')
```

>![6-4_b.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/d8d5d766-15f3-bd92-3df2-9cc3020b1666.png)

### 6.4.2. 自動で目盛りを設定（`AutoLocator`）

`AutoLocator`にすると自動で目盛りを設定する。後から`xlim`，`ylim`が変わってもそれに合わせてくれる。

```py:6-4_c
fig = plt.figure()
ax = fig.add_axes((0.2, 0.2, 0.6, 0.6))

ax.xaxis.set_major_locator(mpl.ticker.AutoLocator())
ax.yaxis.set_major_locator(mpl.ticker.AutoLocator())

ax.set(xlim=(0, 3.14), ylim=(0, 0.01))

ax.set(xlabel=type(ax.xaxis.get_major_locator()),
       ylabel=type(ax.yaxis.get_major_locator()))
fig.savefig('6-4_c.png')
```

>![6-4_c.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/e08c1494-5aad-831a-d19d-42e66ed455c3.png)

### 6.4.3. 特定の値の整数倍に目盛（`MultipleLocator`）

`MultipleLocator(base)`に数値を渡すことで、その値の整数倍の箇所に目盛りを入れることができる。デフォルトは`base=1.0`。なお、0以下にするとエラーになる。

```py:6-4_d
fig = plt.figure()
ax = fig.add_axes((0.2, 0.2, 0.6, 0.6))
ax.plot([-3, 3])

ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(0.3))

ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator())  # 1.0
ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(0.2))

ax.set(xlabel=type(ax.xaxis.get_major_locator()),
       ylabel=type(ax.yaxis.get_major_locator()))
fig.savefig('6-4_d.png')
```

>![6-4_d.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/9bdc4c1b-b857-3990-25a3-e04eb2521889.png)

### 6.4.4. 等差数列の目盛を配置（`IndexLocator`）

`IndexLocator(base, offset)`に数値を渡すことで、「base×n＋offset」の位置に目盛りを入れることができる。`offset=0`のとき`MultipleLocator`と同じ。
なお、デフォルト値はないので数値を与えないとエラーになる。なお、`base`を0にするとエラーになる。

```py:6-4_e
fig = plt.figure()
ax = fig.add_axes((0.2, 0.2, 0.6, 0.6))
ax.plot([-3, 3])

ax.xaxis.set_major_locator(mpl.ticker.IndexLocator(0.3, 0.1))

ax.yaxis.set_major_locator(mpl.ticker.IndexLocator(1, -0.2))

ax.set(xlabel=type(ax.xaxis.get_major_locator()),
       ylabel=type(ax.yaxis.get_major_locator()))
fig.savefig('6-4_e.png')
```

>![6-4_e.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/82b087f4-7cf4-26bd-02cf-e871b406c0b1.png)

### 6.4.5. 特定の個数だけ目盛を配置（`LinearLocator`）

`LinearLocator(numticks)`に数値を渡すことで，グラフ最大値～最小値をnumticks-1等分する位置に目盛を配置することができる。

```py:6-4_f
fig, axes = plt.subplots(1, 12, figsize=(12, 4), tight_layout=True,
                         subplot_kw=dict(xticks=[], ylim=(-5, 5)))

for i in range(len(axes)):
    axes[i].set_title(str(i))
    axes[i].yaxis.set_major_locator(mpl.ticker.LinearLocator(i))

fig.savefig('6-4_f.png')
```

>![6-4_f.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/de65d9b6-09f2-bae8-4e4a-18d7d98bddea.png)

### 6.4.6. `MaxNLocator`

`MaxNLocator(nbins)`に値を渡すと、「目盛の間」の数が`nbins`以内で最大となるように、かつ`steps`にある値の倍数の位置に目盛を配置する（？）。`integer=True`にすると整数の値のみに目盛を配置する。
ちなみに`AutoLocator`は`MaxNLocator('auto', steps=[1, 2, 2.5, 5, 10])`と同じらしい。

```py:6-4_g
fig, axes = plt.subplots(1, 11, figsize=(12, 4), tight_layout=True,
                         subplot_kw=dict(xticks=[], ylim=(-5, 10)))

for i in range(len(axes)):
    axes[i].set_title(str(i+1))
    axes[i].yaxis.set_major_locator(mpl.ticker.MaxNLocator(i+1))

fig.savefig('6-4_g.png')
```

>![6-4_g.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/d6217c5f-9420-9bd1-6a3e-8b2df38c307a.png)

### 6.4.7. 対数軸

`Axes`のパラメータ`xsclae`, `yscale`を`'log'`にすると対数軸にできる（通常の軸スケールは`'linear'`）。後から追加変更する場合は`Axes.set_xscale()`，`Axes.set_yscale()`を用いる。`Axes.set_xscale()`，`Axes.set_yscale()`は`base`で対数の底を指定可能（デフォルトは`10`）。
このとき`Locator`は`LogLocator`になる。

```py:6-4_h
import math

y = [math.exp(i/10) for i in range(50)]
fig = plt.figure(figsize=(10, 4), tight_layout=True)

ax1 = fig.add_subplot(131, title='linear')
ax1.plot(y)
ax1.set_ylabel(type(ax1.yaxis.get_major_locator()))

ax2 = fig.add_subplot(132, title='log, 10', yscale='log')
ax2.plot(y)
ax2.set_ylabel(type(ax2.yaxis.get_major_locator()))

ax3 = fig.add_subplot(133, title='log, 2')
ax3.set_yscale('log', base=2)
ax3.plot(y)
ax3.set_ylabel(type(ax3.yaxis.get_major_locator()))

fig.savefig('6-4_h.png')
```

>![6-4_h.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/5a1af3cb-0703-e72a-84e2-ae4e400464e2.png)

### 6.4.8. 目盛りの位置を自由に設定（`FixedLocator`）

`Axes`のパラメータ`xticks`, `yticks`に数値のリストを渡すと、その値の箇所にだけ目盛を配置することができる。後から変更する場合は`Axes.set_xticks()`，`Axes.set_yticks()`を用いる。`[]`にすると目盛がなくなる。
このとき`Locator`は`FixedLocator`になる。

```py:6-4_i
fig, axes = plt.subplots(1, 3, figsize=(10, 4), tight_layout=True,
                         subplot_kw=dict(xlim=(0, 1), ylim=(-5, 10)))

axes[0].set_xticks([])
axes[0].set_yticks([-4, -3, -1, 0.5, 9.98])

axes[1].set(xticks=[1/3], yticks=range(10))

axes[2].xaxis.set_major_locator(mpl.ticker.FixedLocator([]))
axes[2].yaxis.set_major_locator(mpl.ticker.FixedLocator([0]))
axes[2].yaxis.set_minor_locator(mpl.ticker.FixedLocator(range(-5, 11)))

fig.savefig('6-4_i.png')
```

>![6-4_i.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/605cb3bd-776e-2ef5-0324-8382b8219610.png)

## 6.5. 軸の目盛ラベルの設定

軸の目盛は`Axis.set_major_formatter()`（大目盛）と`Axis.set_minor_formatter()`（補助目盛）に各種`Formatter`を渡すことで変更可能。`Formatter`は`mpl.ticker.XXXFormatter()`で作成・取得する。

```py:6-5_a
fig = plt.figure()
ax = fig.add_axes((0.2, 0.2, 0.6, 0.6))
ax.plot([-3, 3])

ax.set_xlabel(str(type(ax.xaxis.get_major_formatter())) + '\n'
              + str(type(ax.xaxis.get_minor_formatter())))
ax.set_ylabel(str(type(ax.yaxis.get_major_formatter())) + '\n'
              + str(type(ax.yaxis.get_minor_formatter())))

fig.savefig('6-5_a.png')
```

>![6-5_a.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/33956d3b-3bcb-0031-5001-08d191da723c.png)

### 6.5.1. 目盛ラベルなし（`NullFormatter`）

`NullFormatter`で目盛ラベルなしにできるが、`Axes.set_xticklabels([])`，`Axes.set_yticklabels([])`の方が簡単（6.5.参照）。

```py:6-5_b
fig = plt.figure()
ax = fig.add_axes((0.2, 0.2, 0.6, 0.6))
ax.plot([0, 5])

ax.xaxis.set_major_formatter(mpl.ticker.NullFormatter())
ax.yaxis.set_major_formatter(mpl.ticker.NullFormatter())

ax.set(xlabel=type(ax.xaxis.get_major_formatter()),
       ylabel=type(ax.yaxis.get_major_formatter()))
fig.savefig('6-5_b.png')
```

>![6-5_b.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/cfca85c6-dedf-e3b5-55fa-ea487b5d18b6.png)

### 6.5.2. 値をそのまま表示（`ScalarFormatter`）

`ScalarFormatter()`は、値をそのまま表示する。

- 第一引数`useOffset`に数値を渡すと、その数だけ目盛ラベルの値が引かれる。
- 単位として表示される「e」を用いた表記は、`useMathText=True`すると「×10^」を用いた表記になる。

```py:6-5_c
fig, axes = plt.subplots(1, 4, figsize=(10, 4), tight_layout=True,
                         subplot_kw=dict(xlim=(-0.1, 1.1), ylim=(-5, 10)))
[ax.plot([0, 8]) for ax in axes]

axes[1].xaxis.set_major_formatter(mpl.ticker.ScalarFormatter(2))
axes[1].yaxis.set_major_formatter(mpl.ticker.ScalarFormatter(2))

axes[2].xaxis.set_major_formatter(mpl.ticker.ScalarFormatter(-1/4))
axes[2].yaxis.set_major_formatter(mpl.ticker.ScalarFormatter(-0.5))

axes[3].xaxis.set_major_formatter(
    mpl.ticker.ScalarFormatter(-1/4, useMathText=True))
axes[3].yaxis.set_major_formatter(
    mpl.ticker.ScalarFormatter(-0.5, useMathText=True))

fig.savefig('6-5_c.png')
```

>![6-5_c.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/97d19480-509b-af24-8592-4bad1dac5516.png)


### 6.5.3. パーセント表示（`PercentFormatter`）

目盛ラベルをパーセント表示するときは`PercentFormatter`を用いる。

- 第一引数`xmax`：100%とみなす値。デフォルトは`100`。
- 第二引数`decimals`：少数第何位まで表示するか。デフォルトは`None`（自動）。
- 第三引数`symbol`：接尾辞。数字の後につける文字列。デフォルトは`'%'`。

```py:6-5_d
fig, axes = plt.subplots(1, 3, figsize=(10, 4), tight_layout=True,
                         subplot_kw=dict(xlim=(-0.1, 1.1), ylim=(-5, 10)))
[ax.plot([0, 8]) for ax in axes]

axes[1].xaxis.set_major_formatter(mpl.ticker.PercentFormatter(1))
axes[1].yaxis.set_major_formatter(mpl.ticker.PercentFormatter(10))

axes[2].xaxis.set_major_formatter(mpl.ticker.PercentFormatter(1, 0, 'pct'))
axes[2].yaxis.set_major_formatter(mpl.ticker.PercentFormatter(5, 2))

fig.savefig('6-5_d.png')
```

>![6-5_d.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/ca854a09-ffac-6561-33ea-df95c190d084.png)

### 6.5.4. フォーマット文字列で指定（`StrMethodFormatter`）

`StrMethodFormatter()`に文字列を渡すと、`str.format()`で変換した結果が得られる。
`{x}`は目盛の値を表し、`{pos}`は目盛の位置（何番目か）を表す。

```py:6-5_e
fig, ax = plt.subplots(1, 1)
ax.plot([-1000000, 1000000])

ax.xaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('({pos:~^3})'))
ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:+,.0f}'))

fig.savefig('6-5_e.png')
```

なお、バージョン3.3.0からは`set_major_formatter()`に直接フォーマット文字列を渡すことができるようになった。

```py:6-5_e
fig, ax = plt.subplots(1, 1)
ax.plot([-1000000, 1000000])

ax.xaxis.set_major_formatter('({pos:~^3})')
ax.yaxis.set_major_formatter('{x:+,.0f}')

fig.savefig('6-5_e.png')
```

>![6-5_e.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/f7e29b1a-b94b-51fb-e017-d6de5bcdcf95.png)

### 6.5.5. 定義した関数で表示を指定（`FuncFormatter`）

`FuncFormatter()`に関数を渡すと、その関数に`x`（目盛の値），`pos`（目盛の位置）を渡した結果が表示される。引数の数が2つでない関数を指定するとエラーになる。
（自由度が高いが良い使い道が思いつかなかった（検索しても`StrMethodFormatter`等で済むことをわざわざ`FuncFormatter`で行っている例が多かった））

```py:6-5_f
fig, ax = plt.subplots(1, 1)
ax.plot([-1000000, 1000000])

ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda x, pos: x/(pos-5)))

fig.savefig('6-5_f.png')
```

>![6-5_f.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/ea36ca78-24c8-c67b-d343-fb79f716cf88.png)

### 6.5.6. 目盛ラベルを自由に設定（`FixedFormatter`）

`Axes`のパラメータ`xticklabels`, `yticklabels`に数値のリストを渡すと、その値の箇所にだけ目盛を配置することができる。`[]`にすると目盛ラベルがなくなる。
後から変更する場合は`Axes.set_xticklabels()`，`Axes.set_yticklabels()`を用いる。このとき第二引数以降に文字列に関するパラメータを指定可能（4.1.参照）。
このとき`Formatter`は`FixedFormatter`になる。

```py:6-5_g
fig = plt.figure(figsize=(10, 4))
ax = fig.add_axes((0.1, 0.4, 0.8, 0.5))

tick_l = [0, 21.3, 44.4, 65.8, 86.7, 107.5]
label_l = ['Otemachi', 'Tsurumi', 'Totsuka',
           'Hiratsuka', 'Odawara', 'Ashinoko']

ax.set(title='Tokyo ~ Hakone',
       xlabel='Km', xticks=tick_l, yticklabels=[])

ax.set_xticklabels(label_l, rotation=45, ha='right')

fig.savefig('6-5_g.png')
```

>![6-5_g.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/d5767472-7c4e-b26f-18d7-16a9c8eadc43.png)

## 6.6. 補助線の設定

グラフエリアに罫線を引く方法。

### 6.6.1. 方眼線（`Axes.grid()`）

[`Axes.grid()`](https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.grid.html#matplotlib.axes.Axes.grid)を用いるとグラフに方眼線（罫線）を引くことができる。

| 主な引数 | 説明                                                                                                     |
| :------- | :------------------------------------------------------------------------------------------------------- |
| *which*  | 方眼線を引く基準の目盛を`'major'`，`'minor'`，`'both'`から指定。デフォルトは`'major'`。          |
| *axis*   | 方眼線を引く方向を`'x'`（横軸），`'y'`（縦軸），`'both'`（両方）から指定。デフォルトは`'both'`。 |

- そのほかの設定は3.1.参照。

```py:6-6_a
fig, ax = plt.subplots(1, 1)

ax.grid(axis='x', color='red', lw=0.5)
ax.grid(axis='y', color='green', lw=2, ls='--')

fig.savefig('6-6_a.png')
```

>![6-6_a.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/6fc7bb76-e573-d4f7-334b-5660e6bfacdc.png)

### 6.6.2. 特定の位置に直線

方眼線は目盛と連動しているため、目盛と無関係に線を引きたいときには折れ線グラフを引くしか無い。
`Axes.plot()`を用いてもよいが、直線を引くには[`Axes.axhline()`](https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.axhline.html#matplotlib.axes.Axes.axhline)（横線），[`Axes.axvline()`](https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.axvline.html#matplotlib.axes.Axes.axvline)（縦線）を用いるのが容易。
第一引数に線の位置座標を渡す。第二引数と第三引数に0～1の値を渡すと線を短くできる。`Axes.axhline()`（横線）の場合は以下のようになる。

| 主な引数 | 説明                                        |
| :------- | :------------------------------------------ |
| *y*      | 線のy座標。縦の位置。デフォルトは`0`。    |
| *xmin*   | 線の始点（左端）の位置。デフォルトは`0`。 |
| *xmax*   | 線の終点（右端）の位置。デフォルトは`1`。 |

- `xmin`，`xmax`は、`Axes`の左下を(0, 0)・右上を(1, 1)とする座標で指定する。
- そのほかの設定は3.1.参照。

```py:6-6_b
fig = plt.figure()
ax = fig.add_subplot(111, ylim=(-5, 5))

ax.axhline(c='r')
ax.axvline(0.5, 0.1, 0.4, c='skyblue')
ax.axvline(0.5, 0.6, 0.9, c='blue')

fig.savefig('6-6_b.png')
```

>![6-6_b.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/742ba80a-4396-eaf3-f7f0-1096f3c05cc4.png)

[`Axes.hlines()`](https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.hlines.html#matplotlib.axes.Axes.hlines)（横線），[`Axes.vlines()`](https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.vlines.html#matplotlib.axes.Axes.vlines)（縦線）を用いると複数の位置に同時に線を引くことができる。`Axes.hlines()`（横線）の場合は以下のようになる。

| 主な引数     | 説明                                                             |
| :----------- | :--------------------------------------------------------------- |
| *y*          | 線のy座標。縦の位置。                                            |
| *xmin*       | 線の始点（左端）の位置。                                         |
| *xmax*       | 線の終点（右端）の位置。                                         |
| *colors*     | 線の色。リストを渡すと一本ごとに決められる。                     |
| *linestyles* | 線の種類。リストを渡すと一本ごとに決められる。                   |
| *zorder*     | オブジェクトが重なっていた時この値が大きい方が前面に描画される。 |

- `y`，`xmin`，`xmax`は、データの座標で指定する。

```py:6-6_c
fig = plt.figure()
ax = fig.add_subplot(111, ylim=(0, 10))

ax.hlines(5, 0, 1)
ax.vlines([0.5, 0.5], [1, 6], [4, 9], colors=['skyblue', 'blue'])

fig.savefig('6-6_c.png')
```

>![6-6_c.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/7ddd7c9f-293a-12cf-53ff-fe5e9863aa20.png)

## 6.7. 軸目盛の一括設定

`Locator`，`Formatter`以外の軸目盛の設定は[`Axes.tick_params()`](https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.tick_params.html#matplotlib.axes.Axes.tick_params)を用いるのが容易。
第一引数`axis`には設定対象の軸名`'x'`（横軸），`'y'`（縦軸），`'both'`（両方）のいずれかを指定する（デフォルトは`'both'`）。

| 主な引数         | 説明                                                                                    |
| :--------------- | :-------------------------------------------------------------------------------------- |
| *reset*          | `True`：指定していないパラメータを全てデフォルト値に変更する。                        |
| *colors*         | 目盛線と目盛ラベルの色。`color`，`labelcolor`が指定されている場合はそちらが優先。   |
| *zorder*         | オブジェクトが重なっていた時この値が大きい方が前面に描画される。                        |
|                  |                                                                                         |
| *which*          | 設定対象の目盛を`'major'`，`'minor'`，`'both'`から指定。デフォルトは`'major'`。 |
| *direction*      | 目盛の向きを`'in'`（内側），`'out'`（外側），`'inout'`（両方）から指定。          |
| *length*         | 目盛線の長さ。                                                                          |
| *width*          | 目盛線の太さ。                                                                          |
| *color*          | 目盛線の色。                                                                            |
| *pad*            | 目盛線と目盛ラベルの間隔。                                                              |
| *labelsize*      | 目盛ラベルのフォントサイズ。                                                            |
| *labelcolor*     | 目盛ラベルの色。                                                                        |
| *labelrotation*  | 目盛ラベルの角度。                                                                      |
|                  |                                                                                         |
| *grid_color*     | 方眼線の色。                                                                            |
| *grid_alpha*     | 方眼線の透明度を0～1で指定。                                                            |
| *grid_linewidth* | 方眼線の太さ。                                                                          |
| *grid_linestyle* | 方眼線の線種。                                                                          |

- `top`，`bottom`，`left`，`right`に、`True`／`False`を渡すことで、上下左右の目盛線の表示／非表示を指定可能。
- `labeltop`，`labelbottom`，`labelleft`，`labelright`に、`True`／`False`を渡すことで、上下左右の目盛ラベルの表示／非表示を指定可能。

# 7. 画像出力

```py:Figure.savefig()の例
>>> fig.savefig('filename.png')
```

図`Figure`を画像として保存するには[`Figure.savefig()`](https://matplotlib.org/api/_as_gen/matplotlib.figure.Figure.html#matplotlib.figure.Figure.savefig)を用いる。第一引数`fname`にファイル名を指定する。このときパラメータを入力すると画像の設定ができる。

| 主な引数      | 説明                                                                          |
| :------------ | :---------------------------------------------------------------------------- |
| *figsize*     | `Figure`のサイズ。横縦を`(float, float)`で指定。                          |
| *dpi*         | dpi。整数で指定。`'figure'`にすると`Figure`のパラメータを引き継ぐ。       |
| *quality*     | JPEGの品質を0～100で指定。                                                    |
| *facecolor*   | 図の背景色。`Figure`のパラメータは無視される。                              |
| *edgecolor*   | 図の枠の色。`Figure`のパラメータは無視される。                              |
| *bbox_inches* | `'tight'`：`Figure`ではなく、オブジェクトが配置されている部分を出力する。 |

# 8. スタイルの設定に関して

## 8.1. linestyle一覧

```py:8-1_a
fig = plt.figure()
ax = fig.add_subplot(111, xlim=(0, 1), ylim=(4, -1))

ls_list = ['-', '--', ':', '-.']

for i, ls in enumerate(ls_list):
    ax.text(0.1, i, ls, size=30, va='center')
    ax.plot([0.2, 1], [i, i], ls=ls)

fig.savefig('8-1_a.png')
```

>![8-1_a.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/eaac8691-415f-c9ed-d888-35fa1c6efc3b.png)

## 8.2. markerstyle一覧

```py:8-2_a
fig = plt.figure(figsize=(12, 4))
ax = fig.add_subplot(111, xlim=(-0.2, 38), ylim=(0, 1))

m_list = ['.', ',', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', '8', 's',
          'p', '*', 'h', 'H', '+', 'P', 'x', 'X', 'D', 'd', '|', '_',
          0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, '']
plot = [0.1, 0.6, 0.8]

for i, m in enumerate(m_list):
    ax.plot([i+p for p in plot], plot, c='gainsboro',
            marker=m, ms=10, mfc='orange', mew=1.5, mec='green')
    ax.text(i+0.75, 0.9, m, size=15, ha='center')

fig.savefig('8-2_a.png')
```

>![8-2_a.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/394333/dc0365ea-a90f-1e5d-f558-e6e846eaaab7.png)

`$...$`で囲むと数式をマーカーにできる。

## 8.3. colorname一覧

名前がついている色一覧。
[⇒公式](https://matplotlib.org/gallery/color/named_colors.html)
