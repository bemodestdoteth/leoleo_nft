import Vue from 'vue'
import Vuex from 'vuex'

import wallet from '@/store/modules/wallet'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
  	wallet
  }
})
