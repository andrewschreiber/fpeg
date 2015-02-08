import requests
import json
from PIL import Image

import os


filename="got.jpg"

im=Image.open(filename)

apikey="9e91cb08-3b8c-4c0e-a0fa-256c75fe2f07"
url="https://api.idolondemand.com/1/api/sync/detectfaces/v1"


headers={"Content-Type" : "multipart/related"}

files={"file": (filename, open(filename,"rb"),"image/jpeg",headers)}

args={"apikey":apikey}
response=requests.post(url,files=files,data=args)
print response.content

faces=json.loads(response.content)
face_regions=[]
face_coords=[]
for face in faces['face']:
    face_tuple=(face["left"],face["top"],face["left"]+face["width"],face["top"]+face["height"])
    face_coords.append(face_tuple)
    region=im.crop(face_tuple)
    face_regions.append(region)
    
im.save("tmp.jpg",quality=10)

im_compressed=Image.open("tmp.jpg")

for i in range(len(face_regions)):
    im_compressed.paste(face_regions[i],face_coords[i])


im_compressed.show()
