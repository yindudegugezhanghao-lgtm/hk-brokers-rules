// Optional Clash Mi main(config) override. No region or subscription is assumed.
// Existing proxy groups/nodes remain available in HK_Brokers_Policy.
function main(config) {
  if (!config || typeof config !== "object" || Array.isArray(config)) {
    throw new Error("HK Broker Rules: expected a parsed configuration object");
  }
  var providerName = "HK_Brokers";
  var policyName = "HK_Brokers_Policy";
  var url = "https://raw.githubusercontent.com/yindudegugezhanghao-lgtm/hk-brokers-rules/release/rules/HK_Brokers.mrs";
  var providers = config["rule-providers"] || {};
  if (providers[providerName] &&
      (providers[providerName].url !== url || providers[providerName].format !== "mrs" ||
       providers[providerName].behavior !== "domain" || providers[providerName].type !== "http")) {
    throw new Error("HK Broker Rules: provider name HK_Brokers already has different settings");
  }
  var groups = config["proxy-groups"] || [];
  var nodes = config.proxies || [];
  if (!Array.isArray(groups) || !Array.isArray(nodes) ||
      (config.rules !== undefined && !Array.isArray(config.rules))) {
    throw new Error("HK Broker Rules: invalid groups, proxies or rules");
  }
  if (nodes.some(function (node) { return node.name === policyName; })) {
    throw new Error("HK Broker Rules: policy name collides with an existing node");
  }
  var existing = groups.some(function (group) { return group.name === policyName; });
  var members = [];
  groups.concat(nodes).forEach(function (entry) {
    var name = entry.name;
    if (typeof name === "string" && name !== policyName && name !== "GLOBAL" &&
        members.indexOf(name) === -1) members.push(name);
  });
  var uses = Object.keys(config["proxy-providers"] || {});
  if (!existing && !members.length && !uses.length) {
    throw new Error("HK Broker Rules: no existing proxy groups, nodes or providers available");
  }
  var result = Object.assign({}, config);
  result["rule-providers"] = Object.assign({}, providers);
  result["rule-providers"][providerName] = {
    type: "http", url: url, format: "mrs", behavior: "domain",
    path: "./rules/HK_Brokers.mrs", interval: 86400
  };
  result["proxy-groups"] = groups.slice();
  if (!existing) {
    var group = {name: policyName, type: "select", proxies: members};
    if (uses.length) group.use = uses;
    result["proxy-groups"].push(group);
  }
  var brokerRule = "RULE-SET," + providerName + "," + policyName;
  var oldRules = (config.rules || []).filter(function (rule) { return rule !== brokerRule; });
  // Priority is explicit: prepend only this rule, preserve all original rule order.
  result.rules = [brokerRule].concat(oldRules);
  // Clash Mi accepts a string result as YAML. JSON is valid YAML and preserves
  // wildcard DNS keys without depending on the App's YAML re-serialization.
  return JSON.stringify(result);
}
