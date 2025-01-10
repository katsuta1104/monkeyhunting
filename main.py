!pip install APNG
from math import sin,cos,tan,atan,sqrt,radians,degrees
from apng import APNG
from PIL import Image,ImageDraw,ImageFont,ImageOps
import IPython

g = 9.80665


def check(h,l,theta):
  rad = radians(theta)
  tangent = tan(rad)
  if abs(tangent - h/l) < 10**-2:
    return True
  return False

def start():
  v0,L,H,theta = input("v(初速),L(距離),H(高さ),θ(投射角)の順に半角空白区切り").split()
  if not(v0.isdigit() and L.isdigit() and H.isdigit() and theta.isdigit()):
    print("整数値で入力してください")
    start()
  v0 = int(v0) ; L = int(L) ; H = int(H) ; theta = int(theta)
  if not (0<theta<90):
    print("1以上90未満の値を入力してください")
    start()
  if not (v0>0 and L>0 and H>0):
    print("0よりも大きい整数値を入力してください")
    start()

  uhen = sqrt(g*(L**2+H**2)/2*H)
  flag = check(H,L,theta)

  if v0>uhen:
    print("この値は不等式を満たします。よろしいですか？")
    ans = input("良いなら何も入力せず、そうでないなら何かを入力してください")
    if ans == "":
      print("承知しました")
      print("角度良し！" if flag else "角度だめ")
      return v0,L,H,theta
    else:
      print("再度やり直します")
      start()
  else:
    print("この値は不等式を満たしません。よろしいですか？")
    ans = input("良いなら何も入力せず、そうでないなら何かを入力してください")
    if ans == "":
      print("承知しました")
      print("角度良し！" if flag else "角度だめ")
      return v0,L,H,theta
    else:
      print("再度やり直します")
      start()


v0,L,H,theta = start()
"""
テスト用
g = 9.8 #[m/s]
L = 10 #[x軸方向に対する両者の距離]
theta = 45 #[kodoho]
rad = radians(theta) #[rad]
H = 10 #[お猿さんの高さ]
v0 = 7 #[初速]
"""

rad = radians(theta)
#print(rad)
x = v0 * cos(rad)
y = v0 * sin(rad)
scale = 1.2 #scale倍する

def culcurate_v(time):
  way_y = y - g*time
  way_x = x
  radian = atan(way_y / way_x)
  a = tan(radian) #傾き
  return (float("{:.4f}".format(a)))

def culcurete_maxtime():
  a = L*scale / x #弾丸が1.2L倍を超える時
  b = 2*y / g #弾丸が地面の下に行く
  return min(a,b)

def culcurete_maxheight():
  t = y/g
  p = L*scale/x
  if t >= p:
    a = y*p - g*p**2/2
  else:
    a = y*t - g*t**2/2
  return max(a,H)


max_time = culcurete_maxtime()
max_y = culcurete_maxheight()
max_x = L
#print(max_x,max_y)
#横をx,高さをyとして800,400がマックスになるように調整する
pixel_x = 800/(max_x*scale)
pixel_y = 400/(max_y*scale)
#print(pixel_x,pixel_y)

def save(time,x1,y1,x2,y2):
  filename = "file%06d.png" % (time*100)

  tangent = culcurate_v(time)
  plaspixel_x = int(100*pixel_x)
  plaspixel_y = int(tangent*100*pixel_y)
  #print(plaspixel_x,plaspixel_y,tangent)

  #print(filename)
  im = Image.new("RGB",(800,400),(255,255,255))
  draw = ImageDraw.Draw(im)


  monkey_x = int(x1*pixel_x)
  monkey_y = int(y1*pixel_y)
  bullet_x = int(x2*pixel_x)
  bullet_y = int(y2*pixel_y)
  #print(monkey_x,monkey_y)


  draw.ellipse((monkey_x-10,monkey_y-10,monkey_x+10,monkey_y+10),fill=(255,0,0),outline=(0,0,0))
  draw.ellipse((bullet_x-10,bullet_y-10,bullet_x+10,bullet_y+10),fill=(0,255,0),outline=(0,0,0))
  #print((tangent*100))
  draw.line(((bullet_x,bullet_y),(bullet_x+plaspixel_x,bullet_y+plaspixel_y)),fill=(0,0,255))
  #print(bullet_x,bullet_y)



  im_flip = ImageOps.flip(im)

  draw_mi = ImageDraw.Draw(im_flip)
  draw_mi.text((monkey_x-20,400-monkey_y-20),str("{:.3f}".format(x1))+"   "+str("{:.3f}".format(y1)),'black')
  draw_mi.text((bullet_x-20,400-bullet_y-20),str("{:.3f}".format(x2))+"   "+str("{:.3f}".format(y2)),'black')
  draw_mi.text((100,100),"Time  =  "+str("{:.3f}".format(time)),'black')



  im_flip.save(filename)
  return filename

ims = []
files = []
now_time = 0
while now_time < max_time:
  now_time += 0.01
  monkeyX = L
  monkeyY = (H-(g*now_time**2/2))
  bulletX = x*now_time
  bulletY = y*now_time - g*now_time**2 / 2
  files.append(save(now_time,monkeyX,monkeyY,bulletX,bulletY))

#print(files)
APNG.from_files(files,delay=1).save('animation.png')
IPython.display.Image('animation.png')

#入力例1 [10 5 5 45] 不等式を満たさない
#入力例2 [45,5,5,45] 不等式を満たす
#入力例3 [150,12,13,80] 不等式を満たす、が………?
