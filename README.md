# leoleo_nft
민팅 컨트랙 완성했습니다. 혼자서 테스트 하실 수 있게끔 간단하게 설명 적으려고 합니다. 테스트 하면서 궁금하신 거나 이상한 점 발견하시면 바로 연락 주세요.

## **1. Generative art**
　`image` 폴더에 리빌 이후 이미지&메타데이터, 리빌 이전 이미지&메타데이터가 저장되어 있어요. 이거 그대로 `pinata`에 올리셔도 되고 각각 이미지랑 메타데이터 만드는 파이썬 코드도 있으니 테스트 해보고 싶으시면 테스트 가능해요.

　그것도 귀찮으시면 `Image_URI` 파일에 제가 `pinata`에 올려둔 링크가 있으니 이것 활용하시면 됩니다. `pinata`에 올라간 메타데이터 파일 이름은 로컬에 있는 것과 똑같아요.

## **2. Minting Contract**
　클레이튼 IDE로 컴파일 및 배포 가능합니다. `LeoLeo_beforereveal.sol`이 리빌 전 이미지를 담을 컨트랙트, `LeoLeo_afterreveal.sol`에 리빌 함수와 리빌 이후 nft를 담을 컨트랙트에요.

### LeoLeo_beforereveal.sol
　`constructor`가 인수를 받는데 리빌 전 메타데이터 ipfs 주소를 넣으시면 돼요. 모르겠으면 `Image_URI`파일 참고하시면 됩니다. 

　`batchMint` 함수로 민팅을 진행합니다. 누구에게 보내는지, 몇 개를 민팅할지만 적어서 실행하면 nft 번호는 컨트랙에서 알아서 지정해줘요. 민팅 완료하셨으면 `totalsupply()` 함수로 현재 민팅된 갯수 확인 가능해요. `burn()`으로 nft 소각도 가능합니다.

### LeoLeo_afterreveal.sol
　`beforereveal` 컨트랙에서 민팅 완료하셨으면 `afterreveal` 함수를 배포합니다. `constructor`가 인수를 2개 받는데 리빌 후 메타데이터 ipfs 주소, 그리고 배포한 `beforereveal`컨트랙 주소 넣으시면 돼요.

　`afterreveal` 컨트랙은 따로 민팅 함수를 만들지 않고 `migrate()` 이용해서 리빌 전 nft와 갈아끼우기를 진행합니다. 리빌 전 nft를 민팅 완료한 상태에서  `triggerMigration()` 누르시면 리빌 전 nft는 자동으로 소각되고 리빌 후 nft가 자동으로 민팅이 돼요. 참고로 `triggerMigration()` 함수는 컨트랙이 블록체인에 올라가고 100블록 이후부터 작동합니다.