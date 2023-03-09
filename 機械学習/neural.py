import numpy as np
import matplotlib.pyplot as plt

#10*10の(x,y)座標
X = np.arange(-1.0, 1.0, 0.2)
Y = np.arange(-1.0, 1.0, 0.2)
#出力グリッド
Z = np.zeros((10, 10))
#中間層と出力層の重みw_m, w_o
w_m = np.array([[3.0, 3.0], [3.0, 3.0]])
w_o = np.array([[1.0], [-1.0]])
#中間層と出力層のバイアスb_m, b_o
b_m = np.array([2.5, -2.5])
b_o = np.array([0.0])
#中間層の活性化関数はシグモイド関数
def middle_layer(x, w, b):
    u = np.dot(x, w) + b
    return 1/(1+np.exp(-u))
#出力層の活性化関数は恒等関数
def output_layer(x, w, b):
    u = np.dot(x, w) + b
    return u
#ニューラルネットワークの演算
for i in range(10):
    for j in range(10):
        inp = np.array([X[i], Y[j]]) #入力(x, y)
        mid = middle_layer(inp, w_m, b_m) #中間層の演算
        out = output_layer(mid, w_o, b_o) #出力層の演算
        Z[j][i] = out #演算結果を格納
#結果の表示
plt.imshow(Z, cmap = "gist_gray", vmin = 0.0, vmax = 1.0)
plt.colorbar()
plt.show()
