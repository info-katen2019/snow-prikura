import face_recognition
import cv2
import numpy as np
import math
from datetime import datetime

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

#name,scale,adjでそれぞれのスタンプの情報を管理する
#usagi,neko,apple1,apple2
name = [[],[None,"usagi","neko","apple1","apple2"],[None,"tapi"]]
#スタンプの大きさ調整
scale = [[],[None,1.2,1.2,1.2,1.9],[None,1.2]]
#スタンプ位置調整
adj = [[],[None,0.4,0.4,0.2,0],[None,0.2]]

def main():
    #選ぶ選択の組み合わせ(初期設定) 下ひと桁が0のとき何も選ばない
    ch = [11,21]
    while True:
        #フレーム取得
        ret, frame = video_capture.read()
        #フレームの大きさを取得
        h, w, _  = frame.shape
        #顔パーツの座標群を取得
        locations = face_recognition.face_locations(frame)
        face_landmarks_list = face_recognition.face_landmarks(frame,face_locations=locations)

        #顔パーツを取得できたら画像を貼り付ける
        if face_landmarks_list:
            #顔認識できた数だけfor文を回す
            for face,parts in zip(locations,face_landmarks_list):
                #顔の縦幅,横幅を求める
                face_width = face[1] - face[3];
                face_height = face[2] - face[0];
                for i in ch:
                    #スタンプを貼らないとき 下ひと桁が0のとき何も貼らない
                    if i%10 == 0:
                        continue
                    #額付近のスタンプ
                    if i//10 == 1:
                        iti = math.floor(face[0] - face_height*adj[i//10][i%10])
                        pos = (math.ceil((face[3]+face[1])/2),math.ceil(iti))
                    #顎付近のスタンプ
                    elif i//10 == 2:
                        iti = math.floor(parts["chin"][8][1] + face_height*adj[i//10][i%10])
                        pos = (parts["chin"][8][0],math.ceil(iti))
                    
                    #スタンプを読み込んで大きさを取得
                    icon,icon_w,icon_h = load_icon("./stamp/"+name[i//10][i%10]+".png",face_width,i)
                    if is_put(pos,(w,h),(icon_w,icon_h)):
                        frame = merge_images(frame,icon,pos)
                    #デバッグ用 貼り付ける中心座標
                    #frame = cv2.circle(frame,pos, 5, (0,0,255), -1)
            
        #表示
        cv2.imshow('Video',frame)

        k = cv2.waitKey(1)&0xff # キー入力を待つ
        #簡易的な入力(キーボードから)
        if k == ord('q'):
            # 「q」キーが押されたら終了する
            break
        elif k == ord('p'):
            # 「p」キーで画像を保存
            save_image(frame)
        elif k == ord('0'):
            #ノーマル(何も表示しない)
            ch[0] = 10
            ch[1] = 10
        elif k == ord('1'):
            #usagi
            ch[0] = 11
        elif k == ord('2'):
            #neko
            ch[0] = 12
        elif k == ord('3'):
            #apple1
            ch[0] = 13
        elif k == ord('4'):
            #apple2
            ch[0] = 14
        elif k == ord('5'):
            #額付近のスタンプを外す
            ch[0] = 10
        elif k == ord('6'):
            #顎付近のスタンプを外す
            ch[1] = 20
        elif k == ord('7'):
            #tapi
            ch[1] = 21

    video_capture.release()
    cv2.destroyAllWindows()

#スタンプを置けるかどうか判定する関数
def is_put(pos,frame_size,icon_size):
    if math.ceil(pos[0]+icon_size[0]/2) <= frame_size[0] and math.floor(pos[0]-icon_size[0]/2) >= 0:
        if math.ceil(pos[1]+icon_size[1]/2) <= frame_size[1] and math.floor(pos[1]-icon_size[1]/2) >= 0:
            return True    
    return False

# アイコンを読み込む関数
def load_icon(path, distance,cho):
    icon = cv2.imread(path, -1)
    icon_height, icon_width  = icon.shape[:2]
    icon = img_resize(icon, float(scale[cho//10][cho%10]*distance/icon_width))
    icon_h, icon_w  = icon.shape[:2]

    return icon, icon_w, icon_h

# 画像をリサイズする関数
def img_resize(img, scale):
    h, w  = img.shape[:2]
    img = cv2.resize(img, (int(w*scale), int(h*scale)))
    return img

# 画像を合成する関数 posは貼り付けたい中心座標
def merge_images(bg, fg_alpha,pos):
    alpha = fg_alpha[:,:,3]  # アルファチャンネルだけ抜き出す(要は2値のマスク画像)
    alpha = cv2.cvtColor(alpha, cv2.COLOR_GRAY2BGR) # grayをBGRに
    alpha = alpha / 255.0    # 0.0〜1.0の値に変換

    fg = fg_alpha[:,:,:3]

    f_h, f_w, _ = fg.shape # アルファ画像の高さと幅を取得
    b_h, b_w, _ = bg.shape # 背景画像の高さを幅を取得
    s_x = math.floor(pos[0] - f_w/2)
    s_y = math.floor(pos[1] - f_h/2)

    # 画像の大きさと開始座標を表示
    #print("f_w:{} f_h:{} b_w:{} b_h:{} s({}, {})".format(f_w, f_h, b_w, b_h, s_x, s_y))

    bg[s_y:f_h+s_y, s_x:f_w+s_x] = (bg[s_y:f_h+s_y, s_x:f_w+s_x] * (1.0 - alpha)).astype('uint8') # アルファ以外の部分を黒で合成
    bg[s_y:f_h+s_y, s_x:f_w+s_x] = (bg[s_y:f_h+s_y, s_x:f_w+s_x] + (fg * alpha)).astype('uint8')  # 合成

    return bg

# 画像を保存する関数
def save_image(img):
    date = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = "./" + date + ".png"
    cv2.imwrite(path, img) # ファイル保存


if __name__ == '__main__':
    main()