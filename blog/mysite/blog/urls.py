from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'), #作成した urls.py の中身はこのように変更することで、先程 views.py で作成した関数（＝index.htmlを呼び出す処理）のルーティングを設定します。


]
#ちなみに name='index' を設定しておくことで「blog:index」という名前を使ってこの url を逆引きで呼び出すことができるようになります。