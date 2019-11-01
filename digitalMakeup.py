import face_recognition
import cv2
import numpy as np
import math
from datetime import datetime
import time
import multiprocessing as mp
import os
import subprocess
import passwd

#パスワードリスト
passwd_list = passwd.gen_passwd(5000)

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

#name,scale,adjでそれぞれのスタンプの情報を管理する
name = [[],[None,"usagi","neko","apple1","apple2","vr","sento"],[None,"tapi","mazai"],[None,"aika","gogo"], [None, "num_1", "num_2", "num_3"]]
#スタンプの大きさ調整
scale = [[],[None,1.2,1.2,1.2,1.9,1.5,3],[None,1.2,0.8],[None,1.1,1.1], [None, 1, 1, 1]]
#y座標のスタンプ位置調整
adj_y = [[],[None,0.4,0.4,0.2,0,-0.25,-0.4],[None,-0.2,-0.25],[None,0.2,0.8]]
#x座標のスタンプ位置調整
adj_x = [[],[None,0,0,0,0,0,0.35],[None,0,0],[None,-0.5,-0.5]]

def main():
    #選ぶ選択の組み合わせ(初期設定) 下ひと桁が0のとき何も選ばない
    ch = [11,21,31]

    print("キーボードのキーを押すと,スタンプが切り替わります.\n")
    print("<各キーの説明>\n\n[システム]----\nQ:プログラムの終了,P:画像の保存")
    print("----\n\n[顔全体]----\nA:顔全体スタンプの消去")
    print("W:ウサ耳,E:ネコ耳,R:りんご1\nT:りんご2,Y:VRゴーグル,U:せんとくん\n----\n")
    print("[口付近]----\nZ:口付近スタンプの消去")
    print("D:タピオカ,F:モンスターエナジー\n----\n")
    print("[右頬付近]----\nS:右頬付近のスタンプの消去")
    print("C:I科展ふきだし,V:ゴゴゴ\n----\n")

    while True:
        #1フレーム毎に処理
        process_frame = process(ch)
        #1つ前のch[0]を保存
        ch_tmp = ch[0]
        #キーボード入力処理
        ch = input_key(ch)
        if ch[0] == -1:
            break
        elif ch[0] == -2:
            ch[0] = ch_tmp
            '''
            p = mp.Process(target=count_down, args=(process_frame,))
            p.start()
            '''
            save_image(process_frame)
            
        #映像表示
        cv2.imshow('Video', process_frame)
    video_capture.release()
    cv2.destroyAllWindows()


#描画プロセス
def process(ch):
    #フレーム取得
    ret, frame = video_capture.read()
    #フレームの大きさを取得
    h, w, _  = frame.shape
    #1/4サイズのフレーム（高速化用）
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    #顔パーツの座標群を取得
    locations = face_recognition.face_locations(small_frame)
    face_landmarks_list = face_recognition.face_landmarks(small_frame, face_locations=locations)
    
    #顔パーツを取得できたら画像を貼り付ける
    if face_landmarks_list:
        #顔認識できた数だけfor文を回す
        for face, parts in zip(locations, face_landmarks_list):
            #顔の縦幅,横幅を求める
            face_width = (face[1] - face[3]) * 4;
            face_height = (face[2] - face[0]) * 4;
            #print("aa",ch)
            for i in ch:
                base = list()
                #スタンプを貼らないとき 下ひと桁が0のとき何も貼らない
                if i%10 == 0:
                    continue
                #額付近のスタンプ
                if i//10 == 1:
                    base = (int((face[3]+face[1])/2), face[0])
                #顎付近のスタンプ
                elif i//10 == 2:
                    base = parts["chin"][8]
                #右頬付近のスタンプ
                elif i//10 == 3:
                    base = parts["chin"][13]
                #スタンプを貼る中心座標を設定
                pos = (abs(base[0]*4 - face_width*adj_x[i//10][i%10]), abs(base[1]*4 - face_height*adj_y[i//10][i%10]))
                #スタンプを読み込んで大きさを取得
                icon, icon_w, icon_h = load_icon("./stamp/" + name[i//10][i%10] + ".png", face_width, i)
                if is_put(pos, (w, h), (icon_w, icon_h)):
                    frame = merge_images(frame, icon, pos)
                #デバッグ用 貼り付ける中心座標
                #frame = cv2.circle(frame,pos, 5, (0,0,255), -1)
    #1フレームを出力
    return frame    

#キーボードの入力処理を行う関数
def input_key(ch):
    dic = {ord('q'):-1,ord('p'):-2,ord('a'):10,ord('z'):20,
    ord('s'):30,ord('w'):11,ord('e'):12,ord('r'):13,ord('t'):14,
    ord('y'):15,ord('u'):16,ord('d'):21,ord('f'):22,ord('c'):31,
    ord('v'):32}

    #キー入力を待つ
    k = cv2.waitKey(1)&0xff 

    if k in dic:
        if dic[k] < 0:
            ch[0] = dic[k]
        else:
            ch[dic[k]//10-1] = dic[k]
    
    return ch

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

def load_icon_easy(path):
    icon = cv2.imread(path, -1)
    icon_h, icon_w  = icon.shape[:2]

    return icon, icon_w, icon_h

# 画像をリサイズする関数
def img_resize(img, scale):
    h, w  = img.shape[:2]
    img = cv2.resize(img, (int(w*scale), int(h*scale)))
    return img

# 画像を合成する関数 posは貼り付けたい中心座標
def merge_images(bg, fg_alpha, pos):
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
    #1番目
    if(os.path.isfile("img_num.dat") == False):
        write_num(0)
    num = read_num() + 1
    write_num(num)
    path = "./" + str(num) + ".png"
    img = img_resize(img, 0.5)
    cv2.imwrite(path, img) # ファイル保存
    gen_basic()
    htaccess()
    

#連番生成
def write_num(num):
    with open("img_num.dat", 'w') as w_file:
        w_file.write(str(num))
#連番読み取り        
def read_num():
    with open("img_num.dat", 'r') as r_file:
        n = r_file.readline()
        return int(n)

#.htpsswd生成
def gen_basic():
    num = read_num()
    #パスワード生成
    #password = ''.join([secrets.choice(string.ascii_letters + string.digits) for i in range(8)])
    password = passwd_list[num]
    #パスワードとIDを書き込み
    with open("pass_list.txt", "a") as w_file:
        w_file.write("ID: "+str(num)+"  PASS: "+password+"\n")
     #.htpasswdの生成   
    subprocess.call(["htpasswd", "-c",  "-b", "/home/ryuto/"+str(num)+".htpasswd", str(num), password])
    
#.htaccess作成    
def htaccess():
    num = read_num()
    with open(".htaccess", "a") as w_file:
        w_file.write(
            "<Files "+str(num)+".png>\n"+
                "AuthType basic\n"+
                "AuthUserFile /home/ryuto/"+str(num)+".htpasswd\n"+
                "AuthName \"secret\"\n"+
                "require valid-user\n"+
            "</Files>\n"
            )
    subprocess.call(["cp", ".htaccess", "/home/ryuto/public_html"])
    subprocess.call(["cp", "./"+str(num)+".png", "/home/ryuto/public_html"])
   
'''
def count_down(frame):
    start = time.time()
    while True:
        t = time.time() - start
        if t >= 1 and t < 2:
            icon, icon_w, icon_h = load_icon_easy("./stamp/" + name[4][3] + ".png")
            pos = (int(icon_w/2), int(icon_h/2))
            merge_images(frame, icon, pos)
        elif t >= 2 and t < 3:
            icon, icon_w, icon_h = load_icon_easy("./stamp/" + name[4][2] + ".png")
            pos = (int(icon_w/2), int(icon_h/2))
            merge_images(frame, icon, pos)
        elif t >= 3 :
            icon, icon_w, icon_h = load_icon_easy("./stamp/" + name[4][1] + ".png")
            pos = (int(icon_w/2), int(icon_h/2))
            merge_images(frame, icon, pos)
            break
'''    

if __name__ == '__main__':
    main()