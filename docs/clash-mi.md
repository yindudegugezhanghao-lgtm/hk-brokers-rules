# Clash Mi：安装、生效与恢复

## 先保留现有配置

保留机场订阅及当前生效的覆写选择。安装前记录配置使用的是“内置-覆写”“内置-不覆写”还是自定义覆写；已有自定义脚本不要直接换掉。保持规则模式，不改 DNS、TUN、节点或现有通用分流。

仅添加“规则提供者”不会让流量自动命中它；实际配置还必须有 `RULE-SET,HK_Brokers,实际策略组名`。

## 方法一：提供者 + 一条规则

适用于能够编辑当前配置，或已经有保留原规则的追加机制的用户。

1. 在图形化“规则提供者”界面新增以下设置并保存。
2. 在当前配置或已有的安全追加机制中，将提供者加入 `rule-providers`，并在 `rules` 添加下面的一条引用。确认最终生效配置中两者都存在；不同版本中，图形界面的模板未必自动合并到当前配置。
3. 引用放在通用 GEOIP / GEOSITE / MATCH 前。若要覆盖机场原有同域规则，必须放在它们之前。保留原规则的顺序和内容。
4. 保存、重新加载配置或断开重连。检查连接详情中的匹配规则是否为 `RULE-SET / HK_Brokers`，并确认选中的是预期出口。

| 字段 | 值 |
| --- | --- |
| 名称 | `HK_Brokers` |
| Type | `http` |
| URL | `https://raw.githubusercontent.com/yindudegugezhanghao-lgtm/hk-brokers-rules/release/rules/HK_Brokers.mrs` |
| Format | `mrs` |
| Behavior | `domain` |
| 更新间隔 | 24 小时，若要求秒数则填 `86400` |

```yaml
rule-providers:
  HK_Brokers:
    type: http
    url: https://raw.githubusercontent.com/yindudegugezhanghao-lgtm/hk-brokers-rules/release/rules/HK_Brokers.mrs
    format: mrs
    behavior: domain
    path: ./rules/HK_Brokers.mrs
    interval: 86400

rules:
  - RULE-SET,HK_Brokers,PROXY_GROUP
  # 后面保留原有全部规则
```

这里的两个顶层段只用于展示应合并的内容；不要以此替换完整配置。`PROXY_GROUP` 必须替换为原配置中的真实策略组名，不能原样粘贴。不要固定写成某个节点名。

**不要开启“覆写规则”来绑定一个新模板。** 在本次检查的官方源码中，该路径设置 `OverWriteRules / OverWriteRuleProviders = true`，会替换原规则和提供者。项目不把“建模板 + 开启覆写”作为保留机场规则的安装方式。

## 方法二：可选 JS，自动追加

若原来只使用内置覆写、又不方便编辑配置，可使用这个通用脚本，免去手工添加提供者和 RULE-SET：

```text
https://raw.githubusercontent.com/yindudegugezhanghao-lgtm/hk-brokers-rules/main/examples/clash-mi.js
```

1. 打开“核心设置 → 覆写”，新增上面链接，类型选择 **JS**，名称可设为 `HK Broker Rules`。
2. 编辑该覆写的“追加-覆写”设置，保留安装前使用的内置模式：原来是“内置-覆写”就继续追加该模式，原来是“内置-不覆写”则继续相同模式。这样既有 App 核心设置仍按原方式处理；不要为本项目切换 DNS / TUN 设置。界面名称可能随版本变化，以当前版本为准。
3. 在当前机场配置的编辑页，将“核心覆写”选择为此脚本（仅应用到需要的配置）。保持原来的“覆写规则 / 覆写代理组”开关状态；如果这些开关已经启用并正在重建规则，应先把本项目追加逻辑整合到原机制，避免最终阶段把新增规则覆盖掉。
4. 保存并断开重连，在代理页面的 **`HK_Brokers_Policy`** 选择组中，选自己现有的策略组或节点。可以使用香港、日本、美国或其他可用出口。初次默认候选取自原配置顺序，并不代表推荐出口，请自行选择。
5. 在连接详情确认命中 `HK_Brokers`，并确认机场原有规则仍在。不要把能下载 MRS 当作已成功分流的证据。

脚本通过真实的 `main(config)` 接口接收配置，动态读取已有组、节点和 `proxy-providers`，只添加一个提供者、一个通用选择组和一条靠前规则，原规则顺序保持不变。原有 DNS、TUN、节点、原提供者及原组不被脚本重写。若已有同名选择组则保留并复用；若同名提供者指向不同资源或节点名称冲突，会明确报错。

脚本返回 JSON 字符串，Clash Mi 源码支持字符串作为最终 YAML 内容，JSON 也是有效 YAML。这避免 App 再序列化时丢失 DNS 通配符键引号。CI 检查通配符键、Unicode 组名、只有动态提供者的配置、重复应用及冲突处理，并用 Mihomo 校验生成配置。

**已有自定义 JS / YAML 覆写的用户：** 不要替换当前脚本。优先使用方法一，或将本脚本函数改名后，在原 `main(config)` 的最终返回前调用，并按两者返回类型正确解析/串联。合并逻辑需要结合原脚本，项目不声称能无条件合并任意自定义覆写。

## 停用与恢复

- 方法一：先删除/停用新增的 `RULE-SET,HK_Brokers,...` 引用，再删除项目提供者；重新加载。其余原配置保持不变。
- 方法二：把该机场配置的“核心覆写”切回安装前记录的选择，重新加载或断开重连；项目新增组、规则和提供者会随下一次配置生成消失。若采用了合并脚本，仅移除项目追加逻辑。不要删除原机场订阅。
- 若启动失败，先恢复原覆写并重连，再查看日志；提供者名错误、组名不存在、MRS 尚未下载、后续覆写又覆盖规则均可导致失败。需要更新规则时在提供者页刷新，通常每 24 小时自动拉取。

## 已核对的接口与实测边界

2026-10-15 检查 [KaringX/clashmi 官方源码提交 daef7be](https://github.com/KaringX/clashmi/tree/daef7be6c40d49a98a174a82c10599e163e71afd)。当时公开最新发行版为 [v1.0.31.1703](https://github.com/KaringX/clashmi/releases/tag/v1.0.31.1703)，App Store 版本可能不同。

- [提供者类型、格式及行为](https://github.com/KaringX/clashmi/blob/daef7be6c40d49a98a174a82c10599e163e71afd/lib/app/modules/diversion_template_manager.dart)：`http`、`mrs`、`domain`；间隔内部以秒保存。
- [JS 执行入口及返回值处理](https://github.com/KaringX/clashmi/blob/daef7be6c40d49a98a174a82c10599e163e71afd/lib/app/modules/profile_patch_manager.dart)：执行 `main(config)`；字符串直接作为配置内容。
- [原规则替换行为](https://github.com/KaringX/clashmi/blob/daef7be6c40d49a98a174a82c10599e163e71afd/lib/app/modules/clash_setting_manager.dart) 与 [界面开关](https://github.com/KaringX/clashmi/blob/daef7be6c40d49a98a174a82c10599e163e71afd/lib/screens/profile_settings_edit_screen.dart)。
- [内置覆写追加顺序](https://github.com/KaringX/clashmi/blob/daef7be6c40d49a98a174a82c10599e163e71afd/lib/app/local_services/vpn_service.dart)。

已实现 GitHub Actions 上的真实 Mihomo MRS / HTTP 提供者与匹配验证。未在真实 iPhone 的 Clash Mi 界面或已登录券商 App 环境完成测试；界面路径和 App 自身最终合并行为需以实际版本生效配置确认。分流规则不能保证所有交易流量覆盖，也不决定券商的账户或地区政策。
