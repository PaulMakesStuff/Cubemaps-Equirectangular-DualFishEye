# -*- coding: utf-8 -*-

from PIL import Image	# Python Imaging Library
import math		# Math functions
import sys		# allows us to extract the function args
import os		# allows us to split text for saving the file

def radtodeg(r):
  return r*180/math.pi
  
def degtorad(d):
  return d*math.pi/180
  
def scale(c,s):
  r = int(c[0]*s)
  g = int(c[1]*s)
  b = int(c[2]*s)
  return r, g, b
  
def add(a,b):
  r = int(a[0]+b[0])
  g = int(a[1]+b[1])
  b = int(a[2]+b[2])
  return r, g, b
  
def getrgb(image,size,r,t,face):
  xx = ((r * math.cos(t))+1)/2 # normalised betwen 0 and 1
  yy = ((r * math.sin(t))+1)/2 # normalised betwen 0 and 1
  xx *= size
  yy *= size  
  
  if(face=="rear"):
    xx+=size
  
  return image.getpixel((int(xx),int(yy)))

if(len(sys.argv)<1):
    print("function requires an input filename")
    sys.exit(0)
    
fisheye = Image.open(sys.argv[1]) # input file name
inputW, size = fisheye.size

output = []

W = 10000
H = 5000


frontlimit = degtorad(82.5)
blendlimit = degtorad(97.5)
blendsize = degtorad(15)
fov = degtorad(195)
semi = degtorad(180)


for j in range(0,H):

  phi = (1-(float(j)/H))*math.pi
  
  for i in range(0,W):

    theta = float(i)/W*2*math.pi
    
    # 3D normalised cartesian
    
    x = math.cos(theta)*math.sin(phi)
    y = math.sin(theta)*math.sin(phi)
    z = math.cos(phi)
    
    # normalised fisheye coordinates
    # a = angle from +x or -x axis
    # r = radius on fish eye to pixel
    # t = angle from +y or -y on fish eye to pixel
    
    a = math.atan2(math.sqrt(y*y+z*z),x)

    if a < frontlimit:    # front
    
      r = 2 * a / fov
      t = math.atan2(z,y)
      output.append(getrgb(fisheye,size,r,t,"front"))
      
    elif a < blendlimit:  # blend
    
      # fr
      r = 2 * a /fov
      t = math.atan2(z,y)
      bf = 1 - ((a-frontlimit)/blendsize)
      
      # re
      ar = semi-a
      rr = 2 * ar / fov
      tr = math.atan2(z,-1*y)
      bfr = 1 - bf
      
      output.append(add(scale(getrgb(fisheye,size,r,t,"front"),bf),scale(getrgb(fisheye,size,rr,tr,"rear"),bfr)))

    else:                     # rear
    
      r = 2 * (semi-a) / fov
      t = math.atan2(z,-1*y)
      output.append(getrgb(fisheye,size,r,t,"rear"))

img = Image.new("RGB", ((int(W)),(int(H))), None)
img.putdata(output)
img.save(os.path.splitext(sys.argv[1])[0]+"_EQUI.png") # output file name

      
      