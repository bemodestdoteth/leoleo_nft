import { cav, getContractInstance } from './caver'

export default class KlaytnService {

  constructor() {}

  async init () {
    const walletFromSession = sessionStorage.getItem('walletInstance')
    
    if (walletFromSession) {
      try {
        const address = JSON.parse(walletFromSession).address
        cav.klay.accounts.wallet.add(JSON.parse(walletFromSession))        
        
        return address
      } catch (e) {        
        sessionStorage.removeItem('walletInstance')
        return false
      }
    }
  }

  async getBlockNumber () {  	
    const blockNumber = await cav.klay.getBlockNumber()
    return blockNumber
  }

  async getBalance (address) {
    const balance = await cav.klay.getBalance(address)    
    return cav.utils.fromPeb(balance, "KLAY")
  }

  async loginWithKeystore (keystore, password) {  	
    const { privateKey: privateKeyFromKeystore } = cav.klay.accounts.decrypt(keystore, password)    
    await this.integrateWallet(privateKeyFromKeystore)
    return true
  }

  integrateWallet (privateKey) {
    const walletInstance = cav.klay.accounts.privateKeyToAccount(privateKey)
    cav.klay.accounts.wallet.add(walletInstance)
    sessionStorage.setItem('walletInstance', JSON.stringify(walletInstance))
    return true
  }
 
  removeWallet () {
    cav.klay.accounts.wallet.clear()
    sessionStorage.removeItem('walletInstance')
    return true
  }

  getWallet () {
    if (cav.klay.accounts.wallet.length) {
      return cav.klay.accounts.wallet[0]
    }
    return null
  }

  play (number, amount, dispatch, errorCb) {
    const walletInstance = cav.klay.accounts.wallet && cav.klay.accounts.wallet[0]
 
    if (!walletInstance) {
      console.log('no walletInstance')
      return
    }

    amount = cav.utils.toPeb(amount, "KLAY")

    const address = walletInstance.address
    getContractInstance().methods.play(number).send({
      from: address,
      gas: '100000000',
      value: amount
    })
     .once('transactionHash', (txHash) => {
        console.log(`
          Sending a transaction...
          txHash: ${txHash}
          `
        )
      })
      .once('receipt', (receipt) => {
        console.log(`
          Received receipt! (#${receipt.blockNumber} ,${receipt.transactionHash})
        `, receipt)

        dispatch(receipt)
      })
      .once('error', (error) => {
        errorCb(error.message)
      })
  }

}