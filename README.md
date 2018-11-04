# Artists Network Web版 [TBD]
アーティスト間の相関をネットワーク図でプロットします．

任意のアーティストから，関連するアーティストがたくさん表示されます．

![結果](https://github.com/saccho/artists-network/blob/feature/web/static/img/example_2.png)

Web公開に向けて開発中…

## 表示例
![sample](https://github.com/saccho/artists-network/blob/master/example_1.png)

## 準備
[Spotify for Developers](https://developer.spotify.com/) のAPIを使用しています．

conf/client.pyファイルを作成し，以下のパラメータを記述する．

```client.py
client_id = '<YOUR CLIENT ID>'
client_secret = '<YOUR CLIENT SECRET>'
```

## 使用方法
```
$ git clone https://github.com/saccho/artists-network
$ cd artists-network
$ python artists_network.py
```
標準入力に任意のアーティスト名を入力する．複数ヒットした場合は，アーティストの選択肢が表示されるので，自分の意図したアーティストを選択することで，ネットワーク図がプロットされる．
