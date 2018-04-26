# https://stackoverflow.com/questions/6605006/convert-pdf-to-image-with-high-resolution#6605085
# https://stackoverflow.com/questions/291813/recommended-way-to-embed-pdf-in-html?rq=1
# https://www.amazon.com/Definitive-Guide-ImageMagick/dp/1590595904

import subprocess, os
os.system('clear')
params = ['convert', ' -density 300 -resize 220x205', ' abc.pdf', ' thumb.jpg']
cmd = "convert  -verbose -density 150 abc.pdf -quality 100 -sharpen 0x1.0 thumb.jpg"
# cmd = "convert  -verbose -density 150 -trim abc.pdf -quality 100 -flatten -sharpen 0x1.0 thumb.jpg"
# subprocess.check_call(params)
os.system(cmd)
print(cmd)
print("Done converting")



# import PythonMagick
# from os import listdir
# from os.path import isfile, join
# source_files = [f for f in listdir("./") if isfile(join("./", f))]

# counter = 0
# for pdf in source_files:
#     counter += 1
#     img = PythonMagick.Image()
#     img.density("300")
#     img.quality(100)
#     img.read(join("./", pdf))
#     img.crop(PythonMagick.Geometry(470, 900, 1130, 650))
#     img.rotate(90)
#     img.write("./output/new_%s.png" % counter)

