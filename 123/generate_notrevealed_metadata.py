import json
import os

os.chdir("./public/images")

# Dump metadata
local_metadata = "./notrevealed/"
total_images = 5 # 123
notrevealed = []

for i in range(total_images):
    notrevealed.append({})
    notrevealed[i]["Not Revealed"] = "Coming Soon!"
    notrevealed[i]["tokenID"] = i + 1

with open(local_metadata + "notrevealed.json", 'w') as file:
    json.dump(notrevealed, file, indent = 4)

# Generate metadata for each image
def getAttribute(key, value):
    return {
        "trait_type": key,
        "value": value
    }

f = open(local_metadata + "notrevealed.json") 
data = json.load(f)

## Art before reveal
CID = "QmZB28X9r5EB1s4pyh3dxeaUN5dbEdbRAyWdqivU42EKL1"
metadata_URI = "https://ipfs.io/ipfs/" + CID + "/"

for i in data:
    token_id = i['tokenID']
    token = {
        "name": "LeoLeo #" + str(token_id),
        "description": "LeoLeo NFT in KyungHee University.",
        "tokenId": token_id,
        "image": metadata_URI + 'notrevealed.png',
        "attributes": []
    }
    token["attributes"].append(getAttribute("Not Revealed", "Coming Soon!"))

    with open(local_metadata + str(token_id) + ".json", 'w') as outfile:
        json.dump(token, outfile, indent=4)
f.close()