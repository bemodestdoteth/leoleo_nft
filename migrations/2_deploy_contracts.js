// 컨트랙 path를 truggle-config에 적어놔서 파일명만 적어도 된다.
const LeoLeo_mint = artifacts.require("LeoLeo_mint");

// Anonymous function with async
module.exports = async function(deployer)
{
    await deployer.deploy(LeoLeo_mint);
};
// Async: 기다린다?: C#에서 썼을 때는 기다리는 동안에 다른 코드를 실행할 수 있도록 만들어주는 장치라고 들었다. 마치 음식 하나를 렌지를 돌리는 동안 다른 음식 준비를 하는 것처럼.