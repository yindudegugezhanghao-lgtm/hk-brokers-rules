# HK Broker Rules

[![Build](https://github.com/yindudegugezhanghao-lgtm/hk-brokers-rules/actions/workflows/build.yml/badge.svg)](https://github.com/yindudegugezhanghao-lgtm/hk-brokers-rules/actions/workflows/build.yml)
[![Domains](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fyindudegugezhanghao-lgtm%2Fhk-brokers-rules%2Frelease%2Frules%2Fmanifest.json&query=%24.domain_count&label=domains)](https://raw.githubusercontent.com/yindudegugezhanghao-lgtm/hk-brokers-rules/release/rules/manifest.json)

HK Broker Rules 是一个面向 Mihomo / Clash 系列客户端的免费开源券商域名分流规则项目。整理券商官方及相关业务主域名，提供轻量、透明、可自动更新的规则集，方便用户根据自己的网络环境选择分流策略。

Free, open-source domain routing rules for six Hong Kong brokerage platforms. Reviewed sources, transparent provenance, and real Mihomo MRS builds on GitHub Actions. Choose your own routing policy.

## 覆盖范围

首版 **24 个主域名**，全部采用 `DOMAIN-SUFFIX` 语义；当前发布数量见上方动态徽章及 [构建清单](https://raw.githubusercontent.com/yindudegugezhanghao-lgtm/hk-brokers-rules/release/rules/manifest.json)。完整启用清单和逐条官方依据见 [来源记录](docs/sources.md)。

| 券商 | 源文件 | 首版数量 |
| --- | --- | ---: |
| 富途牛牛 / Futu / moomoo | [futu.txt](source/futu.txt) | 5 |
| 老虎证券 / Tiger Brokers | [tiger.txt](source/tiger.txt) | 5 |
| 长桥证券 / Longbridge | [longbridge.txt](source/longbridge.txt) | 5 |
| 涨乐全球通 / 华泰国际 | [huatai.txt](source/huatai.txt) | 2 |
| 盈立证券 / uSMART | [usmart.txt](source/usmart.txt) | 3 |
| 星财富 / 复星财富 | [fosun.txt](source/fosun.txt) | 4 |

仅维护上述六家，不含银行、其他券商、IP、关键词、共享云、通用 CDN、广告追踪或独立第三方金融平台。主域覆盖所有子域，不重复维护已覆盖的 API 子域。主域规则也可能覆盖券商自身资讯、社区及静态资源。未确认项不默认启用。

## 下载与订阅

| 文件 | 稳定 HTTPS 地址 | 提供者参数 |
| --- | --- | --- |
| **MRS（推荐）** | [HK_Brokers.mrs](https://raw.githubusercontent.com/yindudegugezhanghao-lgtm/hk-brokers-rules/release/rules/HK_Brokers.mrs) | `behavior: domain` · `format: mrs` |
| YAML | [HK_Brokers.yaml](https://raw.githubusercontent.com/yindudegugezhanghao-lgtm/hk-brokers-rules/release/rules/HK_Brokers.yaml) | `behavior: domain` · `format: yaml` |
| 原始 LIST | [HK_Brokers.list](https://raw.githubusercontent.com/yindudegugezhanghao-lgtm/hk-brokers-rules/release/rules/HK_Brokers.list) | `behavior: classical` · `format: text` |
| 校验和 / 测试 | [SHA256SUMS](https://raw.githubusercontent.com/yindudegugezhanghao-lgtm/hk-brokers-rules/release/rules/SHA256SUMS) · [validation.json](https://raw.githubusercontent.com/yindudegugezhanghao-lgtm/hk-brokers-rules/release/rules/validation.json) | [Actions 运行记录](https://github.com/yindudegugezhanghao-lgtm/hk-brokers-rules/actions) |

`release` 分支始终保留最近一次验证通过的整套文件；`main` 用于人工维护源文件。MRS 为官方 Mihomo **v1.19.32** 工具生成的二进制；YAML 的 `+.example.com` 与 LIST 的 `DOMAIN-SUFFIX,example.com` 含义相同。

这些文件是规则集，不是节点订阅，也不是完整代理配置。GitHub 链接可达性取决于用户网络；首次下载可使用现有可用连接。配置文件中的 `type: http` 同样支持 HTTPS URL。

## iPhone Clash Mi

完整步骤、版本依据及恢复方法见 **[Clash Mi 安装说明](docs/clash-mi.md)**。

已有配置编辑入口时，只需新增一个规则提供者，再新增一条引用规则，无需逐个输入域名：

| 图形界面字段 | 值 |
| --- | --- |
| 名称 | `HK_Brokers` |
| Type | `http` |
| URL | `https://raw.githubusercontent.com/yindudegugezhanghao-lgtm/hk-brokers-rules/release/rules/HK_Brokers.mrs` |
| Format | `mrs` |
| Behavior | `domain` |
| 更新间隔 | 24 小时（配置文本为 `86400` 秒） |

提供者必须在实际生效配置的 `rules` 中被引用：

```yaml
- RULE-SET,HK_Brokers,PROXY_GROUP
```

把 `PROXY_GROUP` 换成自己配置中实际存在的策略组名，放在通用 GEOIP、GEOSITE 和 MATCH 前面；如果更早有命中的 DOMAIN 规则，也需要调整优先级。保持规则模式，保留所有原规则、DNS、TUN 和节点。

**不要为安装本规则开启 Clash Mi 的“覆写规则”开关**：所检查源码中该开关会替换原规则集合。不能安全追加时，可使用项目提供的 [可选 JS 覆写](examples/clash-mi.js)：自动加入提供者、一条规则和通用选择组 `HK_Brokers_Policy`，用户从已有组或节点中选择出口，不按地区猜测。已有自定义 JS 的用户请按文档合并，避免覆盖原脚本。

## 通用 Mihomo 示例

把以下字段合并进现有配置，不要复制成完整配置替换订阅：

```yaml
rule-providers:
  HK_Brokers:
    type: http
    behavior: domain
    format: mrs
    url: https://raw.githubusercontent.com/yindudegugezhanghao-lgtm/hk-brokers-rules/release/rules/HK_Brokers.mrs
    path: ./rules/HK_Brokers.mrs
    interval: 86400

rules:
  - RULE-SET,HK_Brokers,PROXY_GROUP
  # 保留原有规则，通用兜底放在此规则之后
```

可选择现有香港、日本、美国或其他可用出口；项目不规定地区或节点。域名匹配不会保证券商账户资格、业务可用性或出口被券商接受。只使用 IP 的连接、未核验新域名及第三方服务可能不覆盖。

## 自动更新和验证

源文件变更推送到 `main` 时，GitHub Actions 自动构建；PR 只校验，不发布、不自动合并。支持 Actions 页面手动运行。工具版本和官方压缩包 SHA256 固定在 [tools.lock.json](tools.lock.json)，Actions 依赖固定到提交 SHA。

云端先检查格式、类型、重复、主域层级及来源记录，再生成 LIST / YAML / MRS，运行 MRS 还原比较和实际 Mihomo 加载与路由测试。测试通过才向 `release` 分支原子提交；之后从公开 HTTPS 下载并复验。失败不发布未通过验证的文件，源变更不依赖定时抓取社区清单。用户侧每 24 小时拉取已审核发布；上游券商域名变化仍需人工审查，不会自动采纳候选。

全部 MRS 构建、测试和发布限定于 GitHub 托管 Actions；无需在用户电脑安装 Mihomo 或运行构建工具。详见 [构建说明](docs/build.md)。

## 参与维护

欢迎免费使用、订阅、Fork、提交 Issue / PR 或改善兼容性。新增域名请注明所属券商、官方证据、用途、为何需要主域规则，以及可能误匹配的影响；未核验项进入 [候选清单](docs/candidates.md)。新增、删除都保留理由与记录。

误匹配或失效请提供域名、客户端和版本、脱敏后的匹配规则及复现说明。不要上传账户、交易资料、节点、订阅或完整配置。贡献流程见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 兼容性边界

云端验证包含 LIST / YAML / MRS、HTTP MRS 提供者、实际规则匹配及可选 JS 的配置保留测试。Clash Mi 接口依据官方公开源码核对；未在真实 iPhone 或登录券商账户环境完成端到端测试。旧版 Clash 内核可能不支持 MRS，应选择其支持的 YAML classical/text 形式；本项目 YAML 是 **domain**，不要误填 classical。

MIT License。与券商或客户端官方无隶属关系。
