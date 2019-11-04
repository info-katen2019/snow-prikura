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
**drawLandmark.py**
- webカメラで表示された顔に対して、顔認識を行い取得した顔パーツの座標を表示します。
 
**digitalMakeup.py**
- webカメラで表示された顔を複数認識し、指定したスタンプを貼り付けます。
 
  画像ファイルは透過機能が付いた画像ファイル(pngなど)のみ対応しています。
   
  [digitalMakeup.pyの使い方について](/digitalMakeupDoc.md)

## 使用例
以下に、**digitalMakeup.py**を使用して、画像を保存した場合の例を示します.
 
>[acworksさん](https://www.photo-ac.com/profile/43626)による[写真AC](https://www.photo-ac.com/)からの写真
 
![20191026_171503](https://user-images.githubusercontent.com/24364250/67629854-7614e180-f8c0-11e9-96ea-b7122ffc3114.png)
![20191026_171740](https://user-images.githubusercontent.com/24364250/67629873-becc9a80-f8c0-11e9-89be-32fda7c85c52.png)
## 参考文献
1. [face_recognition](https://github.com/ageitgey/face_recognition)
2. [顔を認識して笑い男画像をリアルタイムで貼り付ける](http://rikoubou.hatenablog.com/entry/2019/05/15/172615)
3. [背景画像にアルファ画像を合成する方法](http://rikoubou.hatenablog.com/entry/2019/05/14/145503)