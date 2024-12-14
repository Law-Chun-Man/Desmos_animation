import os
from paths import jpg, pnm, svg


def jpg_to_svg():
    num = 0
    for filename in os.listdir(jpg):
        jpg_path = os.path.join(jpg, filename)
        if os.path.isfile(jpg_path):
            pnm_path = f"{pnm}/frame_{num:05d}.pnm"
            svg_path = f"{svg}/frame_{num:04d}.svg"
            os.system(f'magick {jpg_path} {pnm_path}')
            os.system(f'potrace {pnm_path} -s -o {svg_path}')
            num +=1
    print("Finished converting to svg")