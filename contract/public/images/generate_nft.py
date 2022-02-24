from PIL import Image
import random
import json
import os

'''
※ 참고
Generative Art를 어떤 식으로 만드냐에 따라 함수를 다르게 적어야 할 것 같다.
지금 이 방식은 trait마다 할당된 수치가 없이 weight만으로 generative art를 만든다. 그런데 우리 sample의 경우에는 sample size(image size)가 매우 작기 때문에 이렇게 만들면 rare trait이 나오지 않을 가능성도 존재한다. 이 경우를 막기 위해서 trait의 full list를 만들고 거기서 뽑아서 만드는 것이 괜찮아 보인다. 메모리는 많이 먹겠지만, 최선의 방법 같아 보인다.

# Images and its traits, weights must add up to 100%.
face = ['White', 'Black']
face_weights = [60, 40]

and other traits...
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

        new_image['Face'] = random.choice(face)
        new_image['Background'] = random.choice(background)
        '''
        and other traits...
        '''

        if new_image not in all_images:
            print(new_image)
            face.remove(new_image['Face'])
            background.remove(new_image['Background'])
            all_images.append(new_image)
        
        if len(all_images) == total_images:
            break

# Validate uniqueness
def validate_uniqueness(all_images):
    seen = []
    return not any(i in seen or seen.append(i) for i in all_images)

'''
and other traits...
'''

# Classify traits
face_files = {
    '1': 'face_black',
    '2': 'face_white',
    '3': 'face_gray',
    '4': 'face_red',
    '5': 'face_gold'
}

background_files = {
    '1': 'background_black',
    '2': 'background_white',
    '3': 'background_gray',
    '4': 'background_red',
    '5': 'background_gold'
}

'''
and other traits...
'''

# Total images and list for all images
total_images = 10
all_images = []
face = generate_traits([9, 9, 5, 1, 1])
background = generate_traits([9, 9, 5, 1, 1])

# Generate unique combinations on trait weighings
generate_image()

if (not validate_uniqueness(all_images)):
    raise Exception("not unique image")

# Add tokenID to each image
for i in range(len(all_images)):
    all_images[i]['tokenID'] = i + 1
    i += 1

# 이렇게 만들면, trait 개수를 체크할 필요가 없다. 이미 개수를 정한 다음에 만들었으니까.

# Generate images
os.chdir('./contract/public/images')

for item in all_images:
    im1 = Image.open("./parts/face/{}.png".format(face_files[item["Face"]])).convert('RGBA')
    im2 = Image.open("./parts/background/{}.png".format(background_files[item["Background"]])).convert('RGBA')

    # Create each composite
    com1 = Image.alpha_composite(im1, im2)

    # Convert to RGB
    rgb_im = com1.convert('RGB')
    file_name = str(item["tokenID"]) + ".png"
    rgb_im.save('./leos/' + file_name)

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

metadata_url = "./metadata/"
peoject_name = "LeoLeo"

for i in data:
    token_id = i['tokenID']
    token = {
        "image": metadata_url + str(token_id) + '.png',
        "tokenId": token_id,
        "name": peoject_name + ' ' + str(token_id),
        "attributes": []
    }
    token["attributes"].append(getAttribute("Face", i["Face"]))
    token["attributes"].append(getAttribute("Background", i["Background"]))

    with open(metadata_url + str(token_id) + ".json", 'w') as outfile:
        json.dump(token, outfile, indent=4)
f.close()