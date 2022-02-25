from PIL import Image
import json
import os
import random

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
        new_image['Face'] = random.choice(face)
        new_image['Eye'] = random.choice(eye)
        new_image['Nose'] = random.choice(nose)
        new_image['Eyebrow'] = random.choice(eyebrow)
        new_image['Hair'] = random.choice(hair)
        new_image['Accessories'] = random.choice(accessories)

        if new_image not in all_images:
            print(new_image)
            background.remove(new_image['Background'])
            body.remove(new_image['Body'])
            outfit.remove(new_image['Outfit'])
            face.remove(new_image['Face'])
            eye.remove(new_image['Eye'])
            nose.remove(new_image['Nose'])
            eyebrow.remove(new_image['Eyebrow'])
            hair.remove(new_image['Hair'])
            accessories.remove(new_image['Accessories'])
            all_images.append(new_image)
        
        if len(all_images) == total_images:
            break

# Validate uniqueness
def validate_uniqueness(all_images):
    seen = []
    return not any(i in seen or seen.append(i) for i in all_images)

# Classify traits
background_files = {'1': 'background1', '2': 'background2'}
body_files = {'1': 'body1'}
outfit_files = {'1': 'outfit1', '2': 'outfit2'}
face_files = {'1': 'face1'}
eye_files = {'1': 'eye1', '2': 'eye2'}
nose_files = {'1': 'nose1', '2': 'nose2'}
eyebrow_files = {'1': 'eyebrow1', '2': 'eyebrow2'}
hair_files = {'1': 'hair1', '2': 'hair2'}
accessories_files = {'1': 'accessories1'}

# Total images and list for all images
total_images = 5 # 123
all_images = []
background = generate_traits([5, 5])
body = generate_traits([123])
outfit = generate_traits([5, 5])
face = generate_traits([123])
eye = generate_traits([5, 5])
nose = generate_traits([5, 5])
eyebrow = generate_traits([5, 5])
hair = generate_traits([5, 5])
accessories = generate_traits([123])

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

for item in all_images:
    im1 = Image.open("./parts/background/{}.png".format(background_files[item["Background"]])).convert('RGBA')
    im2 = Image.open("./parts/body/{}.png".format(body_files[item["Body"]])).convert('RGBA')
    im3 = Image.open("./parts/outfit/{}.png".format(outfit_files[item["Outfit"]])).convert('RGBA')
    im4 = Image.open("./parts/face/{}.png".format(face_files[item["Face"]])).convert('RGBA')
    im5 = Image.open("./parts/eye/{}.png".format(eye_files[item["Eye"]])).convert('RGBA')
    im6 = Image.open("./parts/nose/{}.png".format(nose_files[item["Nose"]])).convert('RGBA')
    im7 = Image.open("./parts/eyebrow/{}.png".format(eyebrow_files[item["Eyebrow"]])).convert('RGBA')
    im8 = Image.open("./parts/hair/{}.png".format(hair_files[item["Hair"]])).convert('RGBA')
    im9 = Image.open("./parts/accessories/{}.png".format(accessories_files[item["Accessories"]])).convert('RGBA')

    # Create each composite
    com1 = Image.alpha_composite(im1, im2)
    com2 = Image.alpha_composite(com1, im3)
    com3 = Image.alpha_composite(com2, im4)
    com4 = Image.alpha_composite(com3, im5)
    com5 = Image.alpha_composite(com4, im6)
    com6 = Image.alpha_composite(com5, im7)
    com7 = Image.alpha_composite(com6, im8)
    com8 = Image.alpha_composite(com7, im9)

    rgb_im = com8.convert('RGB')
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
    token["attributes"].append(getAttribute("Face", i["Face"]))
    token["attributes"].append(getAttribute("Eye", i["Eye"]))
    token["attributes"].append(getAttribute("Nose", i["Nose"]))
    token["attributes"].append(getAttribute("Eyebrow", i["Eyebrow"]))
    token["attributes"].append(getAttribute("Hair", i["Hair"]))
    token["attributes"].append(getAttribute("Accessories", i["Accessories"]))

    with open(metadata_url + str(token_id) + ".json", 'w') as outfile:
        json.dump(token, outfile, indent=4)
f.close()