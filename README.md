# Artists Network
アーティスト間の相関をネットワーク図でプロットします．

任意のアーティストから，関連するアーティストが10人表示され，さらにそこから10人の関連アーティストが表示されます．

## 表示例
![sample](https://github.com/saccho/artists-network/blob/master/example_1.png)

## 準備
[Spotify for Developers](https://developer.spotify.com/) のAPIを使用しています．

client_config.pyファイルを作成し，以下のパラメータを記述する．

```client_config.py
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
