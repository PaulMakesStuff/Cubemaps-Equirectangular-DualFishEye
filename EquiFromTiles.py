# -*- coding: utf-8 -*-

# revitToEquirectangular.py
#
# Takes a panoramic image exported from Revit and converts it into an equirectangular image for use in virtual reality applications
# Works with both panoramic images and combined stereo panoramic images
#
# For use with other cube maps this script will require further editing, for now remember that the script assumes the cube maps were originally in the following format:
#    
#	#
#      ####
#       #


from PIL import Image	# Python Imaging Library
import math		# Math functions
import sys		# allows us to extract the function args
import os		# allows us to split text for saving the file


def convertStrip(out):

    print('Converting:')
    increment = (dims*2)/100
    counter = 0
    percentCounter = 0

    for j in range(0,int(dims*2)):
        
		if(counter<=j):
			print(str(percentCounter)+'%')
			percentCounter+=1
			counter+=increment

		v = 1.0 - ((float(j)) / (dims*2))
		phi = v*math.pi
		
		for i in range(0,int(dims*4)):

			u = (float(i))/(dims*4)
			theta = u * 2 * math.pi
			
			# all of these range between 0 and 1
			x = math.cos(theta)*math.sin(phi)
			y = math.sin(theta)*math.sin(phi)
			z = math.cos(phi)
			
			a = max(max(abs(x),abs(y)),abs(z));
			
			# one of these will equal either -1 or +1
			xx = x / a;
			yy = y / a;
			zz = z / a;
			
            # format is left, front, right, back, bottom, top;
			# therefore negx, posz, posx, negz, negy, posy
			if(yy == -1):                   # square 1 left
			    xPixel = int(((-1*math.tan(math.atan(x/y))+1.0)/2.0)*dims)
			    yTemp = int(((-1*math.tan(math.atan(z/y))+1.0)/2.0)*(dims-1))
			    imageSelect = 1
			elif(xx == 1):			# square 2; front
			    xPixel = int(((math.tan(math.atan(y/x))+1.0)/2.0)*dims)
			    yTemp = int(((math.tan(math.atan(z/x))+1.0)/2.0)*dims)
			    imageSelect = 2
			elif(yy == 1):			# square 3; right
			    xPixel = int(((-1*math.tan(math.atan(x/y))+1.0)/2.0)*dims)
			    yTemp = int(((math.tan(math.atan(z/y))+1.0)/2.0)*(dims-1))
			    imageSelect = 3
			elif(xx == -1):			# square 4; back
			    xPixel = int(((math.tan(math.atan(y/x))+1.0)/2.0)*dims)
			    yTemp = int(((-1*math.tan(math.atan(z/x))+1.0)/2.0)*(dims-1))
			    imageSelect = 4
			elif(zz == 1):			# square 5; bottom
			    xPixel = int(((math.tan(math.atan(y/z))+1.0)/2.0)*dims)
			    yTemp = int(((-1*math.tan(math.atan(x/z))+1.0)/2.0)*(dims-1))
			    imageSelect = 5
			elif(zz == -1):			# square 6; top
			    xPixel = int(((-1*math.tan(math.atan(y/z))+1.0)/2.0)*dims)
			    yTemp = int(((-1*math.tan(math.atan(x/z))+1.0)/2.0)*(dims-1))
			    imageSelect = 6
			else:
			    print('error, program should never reach this point')
			    sys.exit(0)
			
			yPixel = (dims-1) if (yTemp>dims-1) else yTemp
			
			if(yPixel>dims-1):
				yPixel=dims-1
			if(xPixel>dims-1):
				xPixel=dims-1
			
			if(imageSelect==1):
				output.append(negx.getpixel((int(xPixel),int(yPixel))))
			elif(imageSelect==2):
				output.append(posz.getpixel((int(xPixel),int(yPixel))))
			elif(imageSelect==3):
				output.append(posx.getpixel((int(xPixel),int(yPixel))))
			elif(imageSelect==4):
				output.append(negz.getpixel((int(xPixel),int(yPixel))))
			elif(imageSelect==5):
				output.append(negy.getpixel((int(xPixel),int(yPixel))))
			elif(imageSelect==6):
				output.append(posy.getpixel((int(xPixel),int(yPixel))))
			else:
			    print('error, program should never reach this point')
			    sys.exit(0)
			

# begin main program code

negx = Image.open("negx.jpg")
posz = Image.open("posz.jpg")
posx = Image.open("posx.jpg")
negz = Image.open("negz.jpg")
negy = Image.open("negy.jpg")
posy = Image.open("posy.jpg")
dims = negx.size[0]

xPixel = 0
yPixel = 0
yTemp = 0
imageSelect = 0
outputHeight = 0
output = []
outputWidth = dims*4
outputHeight = dims*2
convertStrip(output)
	
img = Image.new("RGB", ((int(outputWidth)),(int(outputHeight))), None)
img.putdata(output)
img.save("pythonOutput.png") # output file name
img.show()
