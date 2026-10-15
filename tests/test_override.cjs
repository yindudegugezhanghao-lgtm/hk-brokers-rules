const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const context = vm.createContext({});
vm.runInContext(fs.readFileSync('examples/clash-mi.js', 'utf8'), context);
function apply(config) { return JSON.parse(context.main(config)); }
const original = {
  dns: {'nameserver-policy': {'*.example.com': ['https://example.invalid/dns-query']}},
  tun: {enable: true}, proxies: [{name: 'Any node', type: 'socks5', server: '127.0.0.1', port: 1}],
  'proxy-groups': [{name: '自选 🌏', type: 'select', proxies: ['Any node']}],
  'rule-providers': {original: {type: 'inline', behavior: 'domain', payload: ['example.com']}},
  rules: ['DOMAIN-SUFFIX,example.com,DIRECT', 'MATCH,自选 🌏']
};
const snapshot = JSON.parse(JSON.stringify(original));
const result = apply(original);
assert.deepEqual(original, snapshot, 'must not mutate original config');
for (const key of ['dns', 'tun', 'proxies']) assert.deepEqual(result[key], snapshot[key]);
assert.deepEqual(result['rule-providers'].original, snapshot['rule-providers'].original);
assert.deepEqual(result['proxy-groups'][0], snapshot['proxy-groups'][0]);
assert.deepEqual(result.rules.slice(1), snapshot.rules);
assert.equal(result.rules[0], 'RULE-SET,HK_Brokers,HK_Brokers_Policy');
assert.deepEqual(apply(result), result, 'must be idempotent');
assert.equal(result['proxy-groups'][1].proxies[0], '自选 🌏');
const onlyProvider = apply({'proxy-providers': {Dynamic: {type: 'http'}}, rules: ['MATCH,DIRECT']});
assert.deepEqual(onlyProvider['proxy-groups'][0].use, ['Dynamic']);
assert.throws(() => apply({'rule-providers': {HK_Brokers: {url: 'https://example.invalid'}}}));
assert.throws(() => apply({}));
assert.throws(() => apply({proxies: [{name: 'HK_Brokers_Policy'}]}));
if (process.argv.includes('--fixture')) {
  fs.mkdirSync('.build', {recursive: true});
  fs.writeFileSync('.build/override-fixture.json', JSON.stringify(result));
}
console.log('Override preservation, dynamic provider, conflict and idempotency tests passed');
