PythonによるWebアプリケーションのdemo
=================
## 概要
脆弱性情報サイトよりデータを収集し管理する。

https://jvndb.jvn.jp/

## 完成度合い
- そこそこ(学習のためなので)

- 一覧画面
<img src="https://user-images.githubusercontent.com/22115777/58462471-f2b65f00-816c-11e9-9e21-9e5677bed6c1.png" width=50%>
- 集計画面
<img src="https://user-images.githubusercontent.com/4899700/47139528-fb050c80-d2f6-11e8-8427-eeb267a43f9f.png" width=50%>
- グラフ画面
<img src="https://user-images.githubusercontent.com/22115777/52532776-3d060280-2d6d-11e9-9c66-ca9e8ed2844d.png" width=50%>

## インストールの方法、動かし方
- 下記コマンドを実行
```
cd ${WHERE}
git clone https://github.com/hidekuno/jvn
cd jvn
docker-compose build
docker-compose up -d
```
- User/Passwordをadmin/adminでログイン
<img src="https://user-images.githubusercontent.com/22115777/65844320-ba1fcf80-e370-11e9-8c36-3f0aa0ef9059.png" width=50%>
<img src="https://user-images.githubusercontent.com/22115777/65844449-521db900-e371-11e9-9586-4b995d1c781b.png" width=50%>
