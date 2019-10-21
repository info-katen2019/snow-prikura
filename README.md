# snow-prikura
snowプリクラのリポジトリ
## 機能  
* カメラ機能  
* スタンプ機能  
* 顔認証を使った猫耳機能  
* グリーンバックで背景を合成  
* ペン機能  
## 使用ライブラリ
face_recognationを使う。
[詳しくはこれ](https://qiita.com/nonbiri15/items/f95b5fb01ae38980c9ce)
## ファイル 
- drawLandmark.py
  - webカメラで表示された顔に対して、顔認識を行い取得した顔パーツの座標を表示します。
- digitalMakeup.py
  - webカメラで表示された顔を複数認識し、顔を覆うように指定したスタンプを貼り付けます。
  (画像ファイルは透過機能が付いた画像ファイル(pngなど)のみ対応しています。)
## 参考文献
1. [顔を認識して笑い男画像をリアルタイムで貼り付ける](http://rikoubou.hatenablog.com/entry/2019/05/15/172615)
2. [背景画像にアルファ画像を合成する方法](http://rikoubou.hatenablog.com/entry/2019/05/14/145503)