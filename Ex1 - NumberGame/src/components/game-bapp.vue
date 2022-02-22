<template>
  <div>
    <Wallet />
    <BettingComponent v-on:complete-choose-number="onCompleteChooseNum" />
  </div>
</template>
<script>
import { mapGetters, mapMutations } from 'vuex'
import KlaytnService from '@/klaytn/klaytnService'

import Wallet from '@/components/wallet'
import BettingComponent from '@/components/betting-component'

export default {
  name: 'game-bapp',  
  components: {
    Wallet,
    BettingComponent
  },
  async mounted () {
    await this.connect()	
  },

  computed: {
    ...mapGetters('wallet', [
      'klaytn',
      'myaddress'
    ])
  },

  methods: {
    ...mapMutations('wallet', [
      'setKlaytn',
      'setIsConnectWallet',
      'setMyAddress',
      'setBalance'
    ]),

    async connect () {
      const klaytn = new KlaytnService()
      this.setKlaytn(klaytn)
      const address = await klaytn.init()      

      if (address) {
        this.setMyAddress(address)

        this.getBalance()
        this.setIsConnectWallet(true)
      } else {
        this.setIsConnectWallet(false)
      }
    },
    
    async getBalance () {
      if (this.myaddress) {        
        const balance = await this.klaytn.getBalance(this.myaddress)        
        this.setBalance(balance)
      }
    },

    onCompleteChooseNum () {
      this.getBalance()
    }
  }
}
</script>