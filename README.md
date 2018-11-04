# Artists Network API
アーティスト間の関係をネットワーク図でプロットします．サーバサイドのプログラムです．
アーティスト情報をjson形式で返します．

Webページでは任意のアーティストから，関連するアーティストがたくさん表示されます．

Webページの構想図
![結果](https://github.com/saccho/artists-network/blob/feature/web/static/img/example_2.png)

## 準備
[Spotify for Developers](https://developer.spotify.com/) のAPIを使用しています．

.envファイルを作成し，以下のパラメータを記述する(.env_sample参照)．

```.env
CLIENT_ID = "<YOUR CLIENT ID>"
CLIENT_SECRET = "<YOUR CLIENT SECRET>"
```

## 使用方法
```
$ git clone https://github.com/saccho/artists-network
$ cd artists-network
$ python app.py
```

## ルーティング
/genres => ジャンルと対応する値を返します．

/source-artists/<artist_name> => artist_nameをSpotifyから検索し，ヒットしたアーティストの情報を返します．

/related-artists/<artist_id> => artist_idに対応したアーティストの情報と，関連アーティストの情報を返します．
