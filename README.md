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

**精简版**仅维护上述六家，不含银行、其他券商、IP、关键词、共享云、通用 CDN、广告追踪或独立第三方金融平台。主域覆盖所有子域，不重复维护已覆盖的 API 子域。主域规则也可能覆盖券商自身资讯、社区及静态资源。未确认项不默认启用。

## 可选全量版 Full（域名 + IP）

为希望只代理六家券商相关流量、避免整机全局代理的使用者提供 **Full 全量候选版**。精简版保留24条经过官方资料交叉核验的主域名；Full 基于精简版额外整理社区候选，包含 **132个域名后缀 + 94条 IP-CIDR（共226条）**。

> Full 里的 IP 段可能是共享云厂商，可能匹配其他 App 的连接；也不能保证覆盖券商所有请求或改变账户所属地区。此清单来自公开社区与部分客户端审计，并非所有主域都有最新官方归属证明。

| 版本 | 地址 | 用途 |
| --- | --- | --- |
| **Full Classical YAML（新版 iPhone Clash 推荐）** | [HK_Brokers_Full_classical.yaml](https://raw.githubusercontent.com/yindudegugezhanghao-lgtm/hk-brokers-rules/release/rules/HK_Brokers_Full_classical.yaml) | **132域名 + 94 IP**；`behavior: classical` |
| Full LIST | [HK_Brokers_Full.list](https://raw.githubusercontent.com/yindudegugezhanghao-lgtm/hk-brokers-rules/release/rules/HK_Brokers_Full.list) | **132域名 + 94 IP**；`behavior: classical` |
| Full YAML（domain only） | [HK_Brokers_Full.yaml](https://raw.githubusercontent.com/yindudegugezhanghao-lgtm/hk-brokers-rules/release/rules/HK_Brokers_Full.yaml) | **132域名，无IP**；`behavior: domain` |
| Full MRS（domain only） | [HK_Brokers_Full.mrs](https://raw.githubusercontent.com/yindudegugezhanghao-lgtm/hk-brokers-rules/release/rules/HK_Brokers_Full.mrs) | **132域名，无IP**；`behavior: domain` |

**重要**：Full 是可选的独立订阅，精简版旧地址保持不变。若要切换，请先移除当前配置里的精简版规则引用，再加入 Full 规则集，以免两份重复；需要保留原机场分流和原节点设置。新版 Clash 显示为 `inline` 时，不能仅凭下载链接推断定时刷新已经生效，必要时在界面手动重新下载。

完整原始候选、上游仓库、审查边界见 [Full 数据说明](docs/full-sources.md)；`source-full/` 为人工维护的候选增量，不自动从上游拉取。

## 下载与订阅

| 文件 | 稳定 HTTPS 地址 | 提供者参数 |
| --- | --- | --- |
| **MRS（推荐）** | [HK_Brokers.mrs](https://raw.githubusercontent.com/yindudegugezhanghao-lgtm/hk-brokers-rules/release/rules/HK_Brokers.mrs) | `behavior: domain` · `format: mrs` |
| YAML | [HK_Brokers.yaml](https://raw.githubusercontent.com/yindudegugezhanghao-lgtm/hk-brokers-rules/release/rules/HK_Brokers.yaml) | `behavior: domain` · `format: yaml` |
| **Classical YAML（新版 Clash 规则集合）** | [HK_Brokers_classical.yaml](https://raw.githubusercontent.com/yindudegugezhanghao-lgtm/hk-brokers-rules/release/rules/HK_Brokers_classical.yaml) | `behavior: classical` · `format: yaml` |
| 原始 LIST | [HK_Brokers.list](https://raw.githubusercontent.com/yindudegugezhanghao-lgtm/hk-brokers-rules/release/rules/HK_Brokers.list) | `behavior: classical` · `format: text` |
| 校验和 / 测试 | [SHA256SUMS](https://raw.githubusercontent.com/yindudegugezhanghao-lgtm/hk-brokers-rules/release/rules/SHA256SUMS) · [validation.json](https://raw.githubusercontent.com/yindudegugezhanghao-lgtm/hk-brokers-rules/release/rules/validation.json) | [Actions 运行记录](https://github.com/yindudegugezhanghao-lgtm/hk-brokers-rules/actions) |

`release` 分支始终保留最近一次验证通过的整套文件；`main` 用于人工维护源文件。MRS 为官方 Mihomo **v1.19.32** 工具生成的二进制；原有 YAML 的 `+.example.com` 与 LIST 的 `DOMAIN-SUFFIX,example.com` 含义相同。另提供 Classical YAML，其 `payload` 为 `DOMAIN-SUFFIX,example.com`，适合要求 classical 规则语法的客户端规则集导入页面。

这些文件是规则集，不是节点订阅，也不是完整代理配置。GitHub 链接可达性取决于用户网络；首次下载可使用现有可用连接。配置文件中的 `type: http` 同样支持 HTTPS URL。

## iPhone Clash Mi

完整步骤、版本依据及恢复方法见 **[Clash Mi 安装说明](docs/clash-mi.md)**，包含以下四种方式：

| 方式 | 操作概要 | 适用条件 |
| --- | --- | --- |
| [分流模板 → 提供者订阅](docs/clash-mi.md#native-templates) | 建 MRS 提供者 → 建 RULE-SET 模板 → 在当前配置绑定已有策略组 | 已使用完整模板分流；首次从机场规则切换须先承接原分流 |
| [现有配置追加](docs/clash-mi.md#configuration) | 追加一个提供者和一条 RULE-SET，支持 MRS / YAML / LIST | 能编辑配置或已有可靠追加机制 |
| [JS 自动追加](docs/clash-mi.md#javascript) | 导入项目 JS，自动创建提供者、引用和选择组 | 当前使用内置覆写，不另外用模板重建全部规则 |
| [本地静态文件](docs/clash-mi.md#offline) | 下载规则文件，在支持的本地配置中引用 | 手动更新，不依赖在线提供者 |

**你要找的提供者订阅入口：核心设置 → 分流模板 → 规则提供者 → ＋。** 填写：

| 图形界面字段 | 值 |
| --- | --- |
| 名称 | `HK_Brokers` |
| Type | `http` |
| URL | `https://raw.githubusercontent.com/yindudegugezhanghao-lgtm/hk-brokers-rules/release/rules/HK_Brokers.mrs` |
| Format | `mrs` |
| Behavior | `domain` |
| 更新间隔 | 24 小时（配置文本为 `86400` 秒） |

原生模板方式还需返回 **分流模板 → 规则模板 → ＋**，取名 `券商分流`，新增 **Type: RULE-SET → 规则提供者: HK_Brokers**。模板内无需填写出口，保存后在 **配置 → 当前机场配置 → 编辑 → 规则** 中为该模板绑定已有策略组，并把券商模板排在通用兜底模板前面。仅添加提供者不会自动生效；模板绑定的前提和开关影响详见上方教程 A。

在配置文本中，最终生效引用为：

```yaml
- RULE-SET,HK_Brokers,PROXY_GROUP
```

把 `PROXY_GROUP` 换成自己配置中实际存在的策略组名，放在通用 GEOIP、GEOSITE 和 MATCH 前面；如果更早有命中的 DOMAIN 规则，也需要调整优先级。保持规则模式，保留所有原规则、DNS、TUN 和节点。

**普通机场原配置用户不要只建券商模板后就开启“覆写规则”**：所核对源码对模板规则和提供者设置替换标志，不能据此保证保留原机场全部分流。已采用完整模板体系的人可在原体系内增加并绑定券商模板；否则使用配置追加或 [JS 自动追加](examples/clash-mi.js)。JS 使用通用选择组 `HK_Brokers_Policy`，不按地区猜测出口；已有自定义覆写的人需合并，避免覆盖原脚本。规则 URL 不是机场节点订阅，也不是整套分流模板的一键导入链接。

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
