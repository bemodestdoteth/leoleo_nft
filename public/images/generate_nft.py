import cv2
import numpy as np
from PIL import Image
import random
import os

'''
※ 참고
Generative Art를 어떤 식으로 만드냐에 따라 함수를 다르게 적어야 할 것 같다.
지금 이 방식은 trait마다 할당된 수치가 없이 weight만으로 generative art를 만든다. 그런데 우리 sample의 경우에는 sample size(image size)가 매우 작기 때문에 이렇게 만들면 rare trait이 나오지 않을 가능성도 존재한다. 이 경우를 막기 위해서 trait의 full list를 만들고 거기서 뽑아서 만드는 것이 괜찮아 보인다. 메모리는 많이 먹겠지만, 최선의 방법 같아 보인다.

# Images and its traits, weights must add up to 100%.
face = ['White', 'Black']
face_weights = [60, 40]
'''
'''
traits list:
"Background": "1",
"Body": "1",
"Outfit": "1",
"Hair": "1",
"Face": "1",
"Nose": "1",
"Eyebrow": "1",
"Eye": "1",
'''

# Generate traits
def generate_traits(weights):    
    trait = []

    for i in range(len(weights)):
        for j in range(weights[i]):
            trait.append(str(i + 1))
    
    return trait

# Recursive function to generate unique images
def generate_image():
    while(True):
        new_image = {}

        new_image['Background'] = random.choice(background)
        new_image['Body'] = random.choice(body)
        new_image['Outfit'] = random.choice(outfit)
        new_image['Hair'] = random.choice(hair)
        new_image['Face'] = random.choice(face)
        new_image['Nose'] = random.choice(nose)
        new_image['Eyebrow'] = random.choice(eyebrow)
        new_image['Eye'] = random.choice(eye)

        if new_image not in all_images:
            print(new_image)
            background.remove(new_image['Background'])
            body.remove(new_image['Body'])
            outfit.remove(new_image['Outfit'])
            hair.remove(new_image['Hair'])
            face.remove(new_image['Face'])
            nose.remove(new_image['Nose'])
            eyebrow.remove(new_image['Eyebrow'])
            eye.remove(new_image['Eye'])
            all_images.append(new_image)
        
        if len(all_images) == total_images:
            break

# Validate uniqueness
def validate_uniqueness(all_images):
    seen = []
    return not any(i in seen or seen.append(i) for i in all_images)

# Classify traits
background_files = {'1': 'background1'}
body_files = {'1': 'body1'}
outfit_files = {'1': 'outfit1'}
hair_files = {'1': 'hair1'}
face_files = {'1': 'face1'}
nose_files = {'1': 'nose1'}
eyebrow_files = {'1': 'eyebrow1'}
eye_files = {'1': 'eye1'}

# Total images and list for all images
total_images = 1 # 123
all_images = []
background = generate_traits([1])
body = generate_traits([1])
outfit = generate_traits([1])
hair = generate_traits([1])
face = generate_traits([1])
nose = generate_traits([1])
eyebrow = generate_traits([1])
eye = generate_traits([1])

# Generate unique combinations on trait weighings
generate_image()

if (not validate_uniqueness(all_images)):
    raise Exception("not unique image")

# Add tokenID to each image
for i in range(len(all_images)):
    all_images[i]['tokenID'] = i + 1
    i += 1

# 이렇게 만들면, 확률이 낮은 특정 trait이 누락될 일이 없다. 이미 개수를 정한 다음에 만들었으니까.

# Generate images
os.chdir('./public/images')

'''
def composite(fore, back):
    # kernel = np.ones((1, 1), np.uint8)
    kernel = np.ndarray((0), np.uint8)
    fore = cv2.cvtColor(fore, cv2.COLOR_RGB2BGR)
    back = cv2.cvtColor(back, cv2.COLOR_RGB2BGR)

    fore_gray = cv2.cvtColor(fore, cv2.COLOR_BGR2GRAY)

    ret, mask = cv2.threshold(fore_gray, 200, 255, cv2.THRESH_BINARY)

    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    output = np.zeros(fore.shape, dtype=fore.dtype)

    for i in range(3):
        output[:, :, i] = back[:, :, i] *(opening/255) + fore[:, :, i] *(1-opening/255)

    output = cv2.cvtColor(output, cv2.COLOR_BGR2RGBA)
    cv2.waitKey(0)
    return output

for item in all_images:
    im1 = cv2.imread("./parts/background/{}.jpg".format(background_files[item["Background"]]))
    im2 = cv2.imread("./parts/body/{}.jpg".format(body_files[item["Body"]]))
    im3 = cv2.imread("./parts/outfit/{}.jpg".format(outfit_files[item["Outfit"]]))
    im4 = cv2.imread("./parts/hair/{}.jpg".format(hair_files[item["Hair"]]))
    im5 = cv2.imread("./parts/face/{}.jpg".format(face_files[item["Face"]]))
    im6 = cv2.imread("./parts/nose/{}.jpg".format(nose_files[item["Nose"]]))
    im7 = cv2.imread("./parts/eyebrow/{}.jpg".format(eyebrow_files[item["Eyebrow"]]))
    im8 = cv2.imread("./parts/eye/{}.jpg".format(eye_files[item["Eye"]]))

    # Create each composite
    com1 = composite(im2, im1)
    com2 = composite(im3, com1)
    com3 = composite(im5, com2)
    com4 = composite(im8, com3)
    com5 = composite(im6, com4)
    com6 = composite(im7, com5)
    com7 = composite(im4, com6)

    file_name = str(item["tokenID"]) + ".jpg"
    cv2.imwrite('./leoleo/' + file_name, com7)
'''
for item in all_images:
    im1 = Image.open("./parts/background/{}.png".format(background_files[item["Background"]])).convert('RGBA')
    im2 = Image.open("./parts/body/{}.png".format(body_files[item["Body"]])).convert('RGBA')
    im3 = Image.open("./parts/outfit/{}.jpg".format(outfit_files[item["Outfit"]])).convert('RGBA')
    im4 = Image.open("./parts/hair/{}.jpg".format(hair_files[item["Hair"]])).convert('RGBA')
    im5 = Image.open("./parts/face/{}.jpg".format(face_files[item["Face"]])).convert('RGBA')
    im6 = Image.open("./parts/nose/{}.jpg".format(nose_files[item["Nose"]])).convert('RGBA')
    im7 = Image.open("./parts/eyebrow/{}.jpg".format(eyebrow_files[item["Eyebrow"]])).convert('RGBA')
    im8 = Image.open("./parts/eye/{}.jpg".format(eye_files[item["Eye"]])).convert('RGBA')

    # Create each composite
    com1 = Image.alpha_composite(im1, im2)
    com2 = Image.alpha_composite(com1, im3)
    com3 = Image.alpha_composite(com2, im5)
    com4 = Image.alpha_composite(com3, im8)
    com5 = Image.alpha_composite(com4, im6)
    com6 = Image.alpha_composite(com5, im7)
    com7 = Image.alpha_composite(com6, im4)

    rgb_im = com1.convert('RGB')
    file_name = str(item["tokenID"]) + ".png"
    rgb_im.save('./leoleo/' + file_name)

# Dump metadata
metadata_file = './metadata/leo_metadata.json'
with open(metadata_file, 'w') as file:
    json.dump(all_images, file, indent = 4)

# Generate metadata for each image
def getAttribute(key, value):
    return {
        "trait_type": key,
        "value": value
    }

f = open(metadata_file) 
data = json.load(f)

metadata_url = "https://leometadata.s3.ap-northeast-2.amazonaws.com/images/metadata/"
peoject_name = "LeoLeo"

for i in data:
    token_id = i['tokenID']
    token = {
        "name": peoject_name + str(token_id),
        "description": "LeoLeo nft in KyungHee University.",
        "tokenId": token_id,
        "image": metadata_url + str(token_id) + '.png',
        "attributes": []
    }
    token["attributes"].append(getAttribute("Background", i["Background"]))
    token["attributes"].append(getAttribute("Body", i["Body"]))
    token["attributes"].append(getAttribute("Outfit", i["Outfit"]))
    token["attributes"].append(getAttribute("Hair", i["Hair"]))
    token["attributes"].append(getAttribute("Face", i["Face"]))
    token["attributes"].append(getAttribute("Nose", i["Nose"]))
    token["attributes"].append(getAttribute("Eyebrow", i["Eyebrow"]))
    token["attributes"].append(getAttribute("Eye", i["Eye"]))

    with open(metadata_url + str(token_id) + ".json", 'w') as outfile:
        json.dump(token, outfile, indent=4)
f.close()