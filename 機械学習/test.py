# coding: utf-8
# Your code here!
import numpy as np
import matplotlib.pyplot as plt

def plot_ap(func,theta): # 振幅特性と位相特性を描く
    # Figure
    fig=plt.figure(figsize = (10, 5))

    # ax1 振幅特性
    ax1=fig.add_subplot(121)
    ax1.grid()

    gain=abs(func)

    # 表示範囲を設定
    lim=[-np.pi, np.pi]
    ax1.set_xlim(lim)
    ax1.set_ylim(0,1.05*np.max(gain))

    # x軸のラベルを設定
    ax1.set_xlabel("$\omega$")
    # タイトルを設定
    ax1.set_title("amplitude characteristic")

    # x軸の目盛りを[-pi/T,pi/T]仕様に
    xt=[-np.pi,-np.pi/2,0,np.pi/2,np.pi]
    ax1.set_xticks(xt)
    xl=["$-\pi/T$","$-\pi/2T$",0,"$\pi/2T$","$\pi/T$"]
    ax1.set_xticklabels(xl)

    ax1.plot(theta,gain)

    # ax2 位相特性
    ax2=fig.add_subplot(122)
    ax2.grid()

    # 表示範囲を設定
    ax2.set_xlim(lim)
    ax2.set_ylim(lim)

    # x軸のラベルを設定
    ax2.set_xlabel("$\omega$")
    # タイトルを設定
    ax2.set_title("phase characteristic")

    # x軸の目盛りを[-pi/T,pi/T]仕様に
    ax2.set_xticks(xt)
    ax2.set_xticklabels(xl)

    # y軸の目盛りを[-pi,pi]仕様に
    ax2.set_yticks(xt)
    yl=["$-\pi$","$-\pi/2$",0,"$\pi/2$","$\pi$"]
    ax2.set_yticklabels(yl)

    ax2.plot(theta,np.arctan2(np.imag(func),np.real(func)))

    # 出力
    plt.show()


PI=np.pi
x=np.linspace(-PI,PI,1000)
func2=1/3*(1+np.exp(-1j*x)+np.exp(-2j*x))
#func=1/3*(1+np.cos(x)+np.cos(2*x)-1j(np.sin(x)+np.sin(2*x)))
plot_ap(func2,x)