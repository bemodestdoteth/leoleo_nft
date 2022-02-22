
const state = {
  klaytn: null,  
  isConnectWallet: false,
  myaddress: '',
  balance: 0
}

const getters = {
  klaytn: (state) => state.klaytn,  
  isConnectWallet: (state) => state.isConnectWallet,
  myaddress: (state) => state.myaddress,
  balance: (state) => state.balance
}

const mutations = {
  setKlaytn(state, klaytn) {
    state.klaytn = klaytn
  },  
  setIsConnectWallet(state, isConnected) {    
    state.isConnectWallet = isConnected
  },
  setMyAddress(state, address) {
    state.myaddress = address
  },
  setBalance(state, balance) {
    state.balance = balance
  }
}

const actions = {
  
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}