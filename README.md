PythonによるWebアプリケーションのdemo
=================
## 概要
脆弱性情報サイトよりデータを収集し管理する。

https://jvndb.jvn.jp/

## 完成度合い
- そこそこ(学習のためなので)

一覧画面  
<img src="https://user-images.githubusercontent.com/22115777/58462471-f2b65f00-816c-11e9-9e21-9e5677bed6c1.png" width=50%>  
集計画面  
<img src="https://user-images.githubusercontent.com/4899700/47139528-fb050c80-d2f6-11e8-8427-eeb267a43f9f.png" width=50%>  
グラフ画面  
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
- ブラウザよりアクセス(http://localhost:8002/)
- User/Passwordにadmin/adminを入力してログイン
<img src="https://user-images.githubusercontent.com/22115777/65844320-ba1fcf80-e370-11e9-8c36-3f0aa0ef9059.png" width=50%>
<img src="https://user-images.githubusercontent.com/22115777/65844449-521db900-e371-11e9-9586-4b995d1c781b.png" width=50%>

## JVNデータの更新
```
docker exec jvn_web python3 /var/www/jvn/jvn_db_register.py
```

## JVNデータのバックアップ
```
docker exec jvn_postgres pg_dump -v -U jvn jvn_db | gzip -c > /tmp/jvn_dump.sql.gz
python /home/hideki/jvn/tool/jvn_dropbox.py  --token=${YOUR_DROPBOX_APIKEY}
```

## 接続テストのためpsqlを構築
```
docker run -it --name psql --network jvn_default governmentpaas/psql
```
## phppgadminの構築
```
docker run -d --name phppgadmin --network jvn_default -p 8081:80 -e PHP_PG_ADMIN_SERVER_HOST=192.168.1.3 dockage/phppgadmin
```
## pgadminの構築
```
docker run --name=pgadmin -d -p 8081:80 --network jvn_default \ 
  -e PGADMIN_DEFAULT_EMAIL=hoge@hoge.com \
  -e PGADMIN_DEFAULT_PASSWORD=hoge \
   dpage/pgadmin4
```
