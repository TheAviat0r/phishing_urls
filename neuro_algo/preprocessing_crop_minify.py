from PIL import Image
import os
import numpy as np
from collections import defaultdict


folder = os.path.dirname(os.path.abspath(__file__))

def crop_minify(filepath):
    im = Image.open(filepath)
    rgb_im = im.convert('RGB')
    rgb_im = rgb_im.crop((0,0,1024,128))
    result = rgb_im.resize((320,40), Image.LANCZOS)
    result.save(filepath.replace('.png', '.jpg'))

