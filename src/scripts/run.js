// Require and Initialize
const CaverExtKAS = require('caver-js-ext-kas');
const Keys = require('../../private-keys.js');
const accessKeyId = Keys.accessKeyId;
const secretAccessKey = Keys.secretAccessKey;
const chainId = 1001 //Baobab

// Init KAS and kip17
const caver = new CaverExtKAS(chainId, accessKeyId, secretAccessKey)
const kip17 = new caver.kct.kip17('0x7a5a559dad539bec801b17b5395b03da07d7c8d7');
const _variableBaseUris = "ipfs://QmT2jysS5eGFfrHyAvbaERJngY21CbAGKAH2UZuijMGneH/";

const ABI = "";
// const NFTcontract = new KIP17(ABI);
// const result = await caver.kas.kip17.getContractList();