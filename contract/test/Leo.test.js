const { assert } = require('chai')
const _deploy_contracts = require('../migrations/2_deploy_contracts')

const Leo = artifacts.require('./Leo.sol')

require('chai')
    .use(require('chai-as-promised'))
    .should()

contract('Color', (accounts)) =>
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
            const name = await constact.name()
        })
    })
}