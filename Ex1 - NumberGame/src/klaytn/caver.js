
import Caver from 'caver-js'

const deployedABI = require('./deployedABI.json')

const TEST_NET = 'https://api.baobab.klaytn.net:8651'

export const config = {
  rpcURL: TEST_NET
}

const DEPLOYED_ADDRESS = '0xa3e9E54627C6B7ED0986E5A9d1ecd7f8A0D013f2' // testnet

const cav = new Caver(config.rpcURL)

const getContractInstance = () => {  
  const contractInstance = deployedABI
  && DEPLOYED_ADDRESS
  && new cav.klay.Contract(deployedABI, DEPLOYED_ADDRESS)
  return contractInstance
}

export {cav, getContractInstance}
