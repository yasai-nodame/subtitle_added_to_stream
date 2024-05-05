# Twitch Live Stream Subtitle Embedder

## 概要

Twitchのライブ配信のm3u8形式のURLを取得し、m3u8_download.pyのURLに記述します。このスクリプトは、取得したライブ配信をリアルタイムでダウンロードし、字幕を埋め込んで視聴することができます。

## 実行手順

1. コマンドプロンプトを開きます。
2. `start python m3u8_download.py & start python vlc_regeneration.py` を実行します。
3. m3u8_download.pyがライブ配信をダウンロードし続け、vlc_regeneration.pyが字幕を埋め込んだ動画をVLCでリアルタイムに再生します。

## 注意事項

- 大容量の動画ファイルをダウンロードする場合は、十分なディスク容量を確保してください。
- このスクリプトはTwitchのライブ配信に対応しています。他の動画ストリーミングプラットフォームには対応していません。
- ディレクトリのPATHはご自身のPATHに置き換えてください。
- URLはTwichのネットワークタブからm3u8を取得してください。
