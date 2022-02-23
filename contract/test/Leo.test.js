const { assert } = require('chai')
const _deploy_contracts = require('../migrations/2_deploy_contracts')

const Leo = artifacts.require('./Leo.sol')

require('chai')
    .use(require('chai-as-promised'))
    .should()

contract('Leo', (accounts) =>
{
    let contract

    before(async() =>
    {
        contract = await Leo.deployed()
    })

    describe('deployment', async () =>
    {
        it('deploys successfully', async () =>
        {
            const address = contract.address
            assert.notEqual(address, '')
            assert.notEqual(address, null)
            assert.notEqual(address, undefined)
            assert.notEqual(address, 0x0)
        })

        it('has a name', async () =>
        {
            const name = await contract.name()
            assert.equal(name, 'Leo')
        })

        it('has a symbol', async () =>
        {
            const symbol = await contract.symbol()
            assert.equal(symbol, 'LEO')
        })
    })

    describe('minting', async () => 
    {
        await contract.mint('213')
    })
})