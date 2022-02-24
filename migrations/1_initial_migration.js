// 파일 이름에 붙은 숫자: truffle에서 이해하는 js code 실행 순서.
// 컨트랙 path를 truggle-config에 적어놔서 파일명만 적어도 된다.
const Migrations = artifacts.require("Migrations");

// Contract deploy할 때마다 Migration 코드도 동시에 돌리게 한다.
module.exports = function(deployer)
{
    deployer.deploy(Migrations);
}