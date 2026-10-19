"""Losslessly convert LuizMelo's CC0 Pet Cats Pack pixels to SVG row runs.

Developer tool only (requires Pillow); normal builds use the generated JSON.
Source archive: assets/pet-cats-pack.zip, downloaded from the author's free page.
"""
from pathlib import Path
from hashlib import sha256
from io import BytesIO
import json
import zipfile
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'assets'/'companions'/'pet-cats'
CHARACTERS={'classic_cat':3,'tuxedo_cat':2,'orange_cat':1,
            'spotted_cat':4,'fluffy_cat':5,'brown_cat':6}
ACTIONS=('Walk','Idle','Run','Meow','Laying','Itch','Sleeping1','Sleeping2',
         'Sitting','Licking 1','Licking 2','Stretching')


def convert():
    archive=ROOT/'assets'/'pet-cats-pack.zip'
    data={'source':'https://luizmelo.itch.io/pet-cat-pack','license':'CC0-1.0',
          'archive_sha256':sha256(archive.read_bytes()).hexdigest(),
          'origin':[12,14],'cell_size':50,'characters':{}}
    with zipfile.ZipFile(archive) as pack:
        for character,number in CHARACTERS.items():
            actions={}
            for action in ACTIONS:
                filename=f'Pet Cats Pack/Cat-{number}/Cat-{number}-{action}.png'
                if filename not in pack.namelist():
                    continue  # The author's Cat-3 has no Itch sheet.
                png=pack.read(filename)
                sheet=Image.open(BytesIO(png)).convert('RGBA')
                assert sheet.height==50 and sheet.width%50==0
                frames=[]
                for index in range(sheet.width//50):
                    frame=sheet.crop((index*50,0,(index+1)*50,50))
                    pixels=frame.load();runs=[]
                    for y in range(50):
                        x=0
                        while x<50:
                            rgba=pixels[x,y]
                            if not rgba[3]:
                                x+=1;continue
                            end=x+1
                            while end<50 and pixels[end,y]==rgba:end+=1
                            color='#%02x%02x%02x'%rgba[:3]
                            if rgba[3]!=255:color+='%02x'%rgba[3]
                            runs.append([x-12,y-14,end-x,color])
                            x=end
                    # Verify that the conversion preserves every original pixel.
                    recovered=Image.new('RGBA',(50,50))
                    for x,y,length,color in runs:
                        rgb=tuple(bytes.fromhex(color[1:]))
                        if len(rgb)==3:rgb+=(255,)
                        for px in range(x+12,x+12+length):recovered.putpixel((px,y+14),rgb)
                    # PNGs may retain arbitrary RGB under fully transparent pixels.
                    expected=[px if px[3] else (0,0,0,0) for px in frame.get_flattened_data()]
                    assert list(recovered.get_flattened_data())==expected, filename
                    frames.append(runs)
                actions[action]={'source':filename,'sha256':sha256(png).hexdigest(),'frames':frames}
            data['characters'][character]={'cat':number,'actions':actions}
        (DEST/'LICENSE.txt').write_bytes(pack.read('Pet Cats Pack/License.txt'))
    (DEST/'frames.json').write_text(json.dumps(data,separators=(',',':'))+'\n',encoding='utf-8')


if __name__=='__main__':
    DEST.mkdir(parents=True,exist_ok=True)
    convert()
