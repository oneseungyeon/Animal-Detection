import json
import datetime
from skimage.io import imread
import os
from math import trunc
from tqdm import tqdm

ANIMAL_NAME_KOR_LIST = ['고라니', '멧돼지', '오소리', '노루']
ANIMAL_NAME_ENG_LIST = ['waterdeer', 'wildpig', 'badger', 'roedeer']
ANIMAL_NAME_ABR_LIST = ['WD', 'WP', 'BG', 'RD']

with open('../../json/val/result.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

coco = {
    'info': {
        'year': 2021,
        'version': '1.0',
        'description': 'KNPS animal detection dataset - snapshots',
        'contributor': 'KNPS, UOS',
        'url': '',
        'date_created': str(datetime.datetime.now())
    },
    'images': [],
    'annotations': [],
    'licenses': [
        {
          "id": 0,
          "name": "Unknown License",
          "url": ""
        }
    ],
    'categories': []
}

for animal_name_idx, animal_name_abr in enumerate(ANIMAL_NAME_ABR_LIST):
    coco['categories'].append({
        'supercategory': 'animal',
        'id': animal_name_idx + 2,
        'name': animal_name_abr
    })
coco['categories'].append({
    'supercategory': 'animal',
    'id': 1,
    'name': '__'
})

for idx, image in tqdm(enumerate(data['images'])):
    file_name = image['file']
    file_path = os.path.join('../../images/val', file_name)
    im_array = imread(file_path)
    height = im_array.shape[0]
    width = im_array.shape[1]

    coco_image = {
        'id': idx,
        'width': width,
        'height': height,
        'file_name': file_name,
        'license': 0,
        'date_captured': ''
    }

    coco_annotation = {
        'bbox': None,
        'image_id': idx,
        'category_id': None
    }

    coco['images'].append(coco_image)

    for detection in image['detections']:
        rel_coord = detection['bbox']  # x, y, width, height
        abs_coord = [
            trunc(rel_coord[0]*width),
            trunc(rel_coord[1]*height),
            trunc(rel_coord[2]*width),
            trunc(rel_coord[3]*height)
        ]
        coco_annotation['bbox'] = abs_coord
        coco_annotation['category_id'] = int(detection['category'])

        coco['annotations'].append(coco_annotation)

with open('../../json/val/result_COCO.json', 'w', encoding='utf-8') as f:
    json.dump(coco, f, ensure_ascii=False)
