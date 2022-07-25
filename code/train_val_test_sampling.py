import shutil
import random
import json
from tqdm import tqdm

ANIMAL_NAME_KOR_LIST = ['고라니', '멧돼지', '오소리', '노루']
ANIMAL_NAME_ENG_LIST = ['waterdeer', 'wildpig', 'badger', 'roedeer']
ANIMAL_NAME_ABR_LIST = ['WD', 'WP', 'BG', 'RD']

data = {
    'all_images': [],
    'classified_images': {'__': []},
    'train_images': [],
    'val_images': [],
    'test_images': [],
    'detection_categories': {'5': '__'}
}

# Retrieve data
with open('../../json/result.json', 'r', encoding='utf-8') as f:
    tmp = json.load(f)['images']
    for image in tmp:
        if image['max_detection_conf'] != 0:
            image['file'] = image['file'].split('/')[-1]
            data['all_images'].append(image)

# Classify for each animal classes
for idx, key in enumerate(ANIMAL_NAME_ABR_LIST):
    data['classified_images'][key] = []
    data['detection_categories'][str(idx+1)] = key

# For each image...
for image in data['all_images']:
    # For each class...
    for animal_idx, animal_name_kor in enumerate(ANIMAL_NAME_KOR_LIST):
        classified = False
        if animal_name_kor in image['file']:
            for detection in image['detections']:
                detection['category'] = str(animal_idx+1)
            data['classified_images'][ANIMAL_NAME_ABR_LIST[animal_idx]].append(image)
            classified = True
            break
    if not classified:
        data['classified_images']['__'].append(image)
        for detection in image['detections']:
            detection['category'] = '5'  # Assign "Otherwise"

# Verify the number of images by assertion
num_of_classified_images = 0
for key in data['classified_images'].keys():
    num_of_classified_images += len(data['classified_images'][key])
assert num_of_classified_images == len(data['all_images'])

sampling_params = {}

# Set num of train/val/test images of each class for sampling
for key in data['classified_images'].keys():
    current_classified_images = data['classified_images'][key]
    num_all = len(current_classified_images)
    num_train = round(num_all*0.8)
    num_val = round(num_all*0.1)
    num_test = round(num_all*0.1)
    num_sum = num_train + num_val + num_test
    num_diff = num_all - num_sum
    num_train += num_diff
    print('# of Train/Val/Test images of category ' + key)
    print((num_train, num_val, num_test))
    assert num_all == num_train + num_val + num_test
    sampling_params[key] = {
        'num_all': num_all,
        'num_train': num_train,
        'num_val': num_val,
        'num_test': num_test
    }

# Randomly sample train/val/test images
for key in data['classified_images'].keys():
    current_classified_images = data['classified_images'][key]
    image_train_list = random.sample(population=current_classified_images, k=sampling_params[key]['num_train'])
    for image in image_train_list:
        current_classified_images.remove(image)
    image_val_list = random.sample(population=current_classified_images, k=sampling_params[key]['num_val'])
    for image in image_val_list:
        current_classified_images.remove(image)
    image_test_list = current_classified_images

    data['train_images'].extend(image_train_list)
    data['val_images'].extend(image_val_list)
    data['test_images'].extend(image_test_list)

# Save train/val/test annotation data
for key in ['train', 'val', 'test']:
    new_data = {
        'images': data[key+'_images'],
        'detection_categories': data['detection_categories']
    }
    for image in tqdm(new_data['images']):
        fname = image['file']
        shutil.copy(
            '../../images/image/%s' % fname,
            '../../images/%s/%s' % (key, fname)
        )
    with open('../../json/%s/result.json' % key, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False)

# Save data dictionary
with open('../../json/result_train_val_test.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)
