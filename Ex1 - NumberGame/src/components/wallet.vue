<template>
<div>
  <h2>Connect to Wallet</h2>
  <div>
    <template v-if="walletInstance">
      <div>        
        <h2>Integrated</h2>
        <div class="balance">Balance: {{balance}} Klay</div>
        <div class="address">{{walletInstance.address}}</div>
        <button class="btnSubmit" @click="this.handleRemoveWallet">REMOVE WALLET</button>
      </div>
    </template>
    <template v-else>
      <div>
        <label for="keystore">Keystore:</label>
        <input type="file" name="keystore" v-on:change="this.handleImport" />        

        <label for="password">Password:</label>
        <input
          name="password"
          v-model="password"          
          type="password"          
          required
        ></input>        

        <h3>OR</h3>

        <label for="privateKey">Private Key:</label>  
        <input
          v-model="privateKey"
          name="privateKey"
          type="password"
          required
        ></input>

        <p>
          <button class="btnSubmit" @click="this.handleAddWallet">ADD WALLET</button>
        </p>
      </div>
    </template>  
  </div>
</div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'

export default {
  data: () => ({ 
    keystore: null,
    password: '',
    privateKey: null,
    walletInstance: null
  }),
  computed: {
    ...mapGetters('wallet', [
      'klaytn',
      'balance'
    ])
  },
  methods: {
    ...mapMutations('wallet', [ 
      'setIsConnectWallet',
      'setMyAddress',
      'setBalance'
    ]),

    handleImport (e) {
      const keystore = e.target.files[0]
      
      const fileReader = new FileReader()
      fileReader.onload = (e) => {
        try {
          if (!this.checkValidKeystore(e.target.result)) {            
            alert('Invalid keystore file.')
            return
          }

          this.keystore = e.target.result
                  
        } catch (e) {
          alert('Invalid keystore file.')          
          return
        }
      }
      fileReader.readAsText(keystore)
    },

    async handleAddWallet () {
      try {
        if(this.privateKey) {
          await this.klaytn.integrateWallet(this.privateKey)          
        } else {
          await this.klaytn.loginWithKeystore(this.keystore, this.password)
        }
        this.getWalletInfo()
      } catch (e) {        
        alert(`Password or private key doesn't match.`)        
      }
    },

    async getWalletInfo () {
      this.walletInstance = this.klaytn.getWallet() 
      const address = this.walletInstance.address
      if(address) {
        this.setMyAddress(address)
        const balance = await this.klaytn.getBalance(address)        
        this.setBalance(balance)
        this.setIsConnectWallet(true)
      } else {
        this.setIsConnectWallet(false)
      }
    },

    checkValidKeystore (keystore) {
      const parsedKeystore = JSON.parse(keystore)
      const isValidKeystore = parsedKeystore.version &&
        parsedKeystore.id &&
        parsedKeystore.address &&
        parsedKeystore.crypto

      return isValidKeystore
    },

    async handleRemoveWallet () {
      await this.klaytn.removeWallet()
      this.setIsConnectWallet(false)
      this.walletInstance = null
    }
  },
  mounted () {
    if(this.klaytn) {
      this.walletInstance = this.klaytn.getWallet()
    }    
  }
}

</script>

<style scoped>


</style>