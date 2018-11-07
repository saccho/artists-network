# Artists Network API
SpotifyAPIから得られたアーティスト情報を変換（ジャンルを数値に変換，アーティストと関連アーティストの情報を結合など）してjson形式で返します．

Webページでは任意のアーティストから，関連するアーティストがたくさん表示され，そこから伸びるノードから次のアーティストにリンクできるようにする予定です．

Webページの構想図
![例](https://github.com/saccho/artists-network/blob/master/static/img/example_2.png)

## 準備
[Spotify for Developers](https://developer.spotify.com/) のAPIを使用しています．

.envファイルを作成し，以下のパラメータを記述する(.env.sample参照)．

```.env
CLIENT_ID = "<YOUR CLIENT ID>"
CLIENT_SECRET = "<YOUR CLIENT SECRET>"
```

## 使用方法
```
$ git clone https://github.com/saccho/artists-network-api
$ cd artists-network-api
$ python app.py
```

## ルーティング
/genres → ジャンルと対応する値を返します．

/source-artists/&lt;market&gt;/<artist_name> → artist_nameをSpotifyから検索し，ヒットしたアーティストの情報を返します．

/related-artists/<artist_id> → artist_idに対応したアーティストの情報と，関連アーティストの情報を返します．
