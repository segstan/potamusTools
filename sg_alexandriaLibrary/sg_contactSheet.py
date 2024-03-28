import os
from PIL import Image,ImageFont,ImageDraw

try:
	import OpenImageIO as oiio
	ImageBufLoaded = True
except:
	ImageBufLoaded = False
	pass

def makeContactSheet(images,padding,nCols,nRows,outputW,outputH,margins,outpath):
	#Read and Resize all the images 
	#imgs = [Image.open(img).resize((outputW,outputH)) for img in images]
	print(" --- Gathering Images for CS --- ")
	imgs =[]
	list32bits = ["exr","hdr","tif"]

	marl = margins[0] 
	mart = margins[1]
	marr = margins[2]
	marb = margins[3]
	
	for pic in images:
		if pic.split('.')[-1] not in list32bits:
			basename = os.path.basename(pic)
			print("Opening Image: " + str(basename))
			img=Image.open(pic)

			width,height=img.size

			#Calculate new format, with maintain ratio
			aspectOriginal = float(width)/float(height)
			if aspectOriginal >= 1.0:
				newHeight = int(height*outputH/width)
				newWidth =  outputW
			else:
				newWidth = int(width*outputW/height)
				newHeight =outputH

			# Resize image
			resized=img.resize((newWidth,newHeight))

			size = max(outputH,newWidth,newHeight)
			outSize = (size,size)

			# Create the new image
			bg = (0,0,0,255)
			frame = Image.new('RGBA',outSize,bg)
			bbox = ( int((size-newWidth)/2),int((size-newHeight)/2) )
			
			# Copy in new frame
			frame.paste(resized,bbox)
			#Add Text
			font = ImageFont.truetype("arial.ttf",int(newWidth*0.05))
			addTextImg= ImageDraw.Draw(frame)
			addTextImg.text((5,int(size-(size*0.07))),basename,(255,255,255),font)
			
			imgs.append(frame)
		
		else:
			if ImageBufLoaded == True:
				print("32 bits Convertion Started")
				previewImage = os.path.join(outpath,basename.split(".")[0]+".png")
				img =  oiio.ImageBuf(pic)
				spec= img.spec()
				## Reformat
				width = spec.width
				height = spec.height
				#Calculate new format, with maintain ratio
				aspectOriginal = float(width)/float(height)
				if aspectOriginal >= 1.0:
					newHeight = int(height*outputH/width)
					newWidth =  outputW
				else:
					newWidth = int(width*outputW/height)
					newHeight =outputH

				# Convert Color Space 
				colorspace =oiio.ImageBufAlgo.colorconvert(img,img,"Linear","sRGB")
				# Resize
				imgResized = oiio.ImageBuf(oiio.ImageSpec(newWidth,newHeight,spec.nchannels,oiio.FLOAT))
				oiio.ImageBufAlgo.resize(imgResized,img)
				# Save a png
				imgResized.write(previewImage)
				# Add back to the list to iterate again
				images.append(previewImage)
			else:
				print("Break")
				break

	# Calculate the size of the output frame
	marW = marl+marr
	marH = mart+marb

	padW = (nCols-1)*padding
	padH = (nRows-1)*padding
	isize = (nCols*outputW+marW+padW,nRows*outputH+marH+padH)

	# Create the new image
	bg = (0,0,0,255)
	iNew = Image.new('RGBA',isize,bg)

	# Insert every pic
	for iRow in range(nRows):
		for iCol in range(nCols):
			left = marl + iCol*(outputW+padding)
			right = left + outputW
			upper = mart + iRow*(outputH+padding)
			lower = upper + outputH
			bbox = (left,upper,right,lower)
			try:
				img = imgs.pop(0)
			except:
				break
			iNew.paste(img,bbox)

	path = os.path.join(outpath ,"result.png")
	result = iNew.save(path)

	print(" --- Contact Sheet Saved --- ")

	return path
