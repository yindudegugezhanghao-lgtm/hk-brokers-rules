# Full 版数据和安全边界

更新时间：2026-10-16。本版本的使用者同意更广覆盖以减少全局代理，但不表示这些域名或 IP 全部专属于券商。

## 范围和数据

- 只涉及富途/moomoo、老虎、长桥、华泰/涨乐、盈立/uSMART、复星/星财富六个项目。
- 核心版 24 条经过官方资料交叉核验；Full 在此基础上增加108条社区域名，最终 **132条域名规则**。
- Full 添加 **94条 IPv4 CIDR**，共226条 Classical 规则。IP 来自公开专项券商规则及相关交易/行情清单。CIDR 可能相互覆盖，**94是原始去重的网段条数，不代表94段互不重叠**。
- 不包含其他券商、银行、宽泛 `DOMAIN-KEYWORD`、通用 CDN 基础域或整段网络运营商 ASN。
- 规则不会突破开户资格、账户地区或券商风控。

## 分组

| 券商 | 核心 | Full | 对照来源 |
| --- | ---: | ---: | --- |
| 富途/moomoo | 5 | 51 | forecho、proxyBug、V2Fly、LingJingMaster |
| 老虎 | 5 | 42 | blackmatrix7、proxyBug、V2Fly |
| 长桥 | 5 | 15 | V2Fly、forecho、koo17173 |
| 涨乐全球通 | 2 | 7 | koo17173、官方来源线索 |
| 盈立 | 3 | 11 | StricklandF、foreverchen9、官方来源线索 |
| 星财富 | 4 | 6 | forecho、官方网站资料 |

## 来源（不是全部官方背书）

- https://github.com/forecho/broker-rules （`Source/broker/*.conf`，2026-09-22 富途客户端审计）
- https://github.com/LingJingMaster/Shadowrocket-Rules （`HK_Broker.list`，2026-10-01 老虎增补）
- https://github.com/proxyBug/tigertrade-moomoo-rules （富途、老虎单独规则与 runtime 证据）
- https://github.com/v2fly/domain-list-community （`data/futu`, `data/itiger`, `data/longbridge`）
- https://github.com/blackmatrix7/ios_rule_script （`TigerFintech` 类别）
- https://github.com/koo17173/rule-set （`Stocks.list` 和 `BrokerHT`）
- https://github.com/StricklandF/Filter （`uSmart.list`）
- https://github.com/foreverchen9/personal_proxy_rules （券商候选补充）

## IP 风险

IP 原始源含精确 /32 与宽泛 /23、/24；一些为腾讯云、阿里云、海外云厂商共享网段。命中这些网段的无关应用请求可能绕行你的券商专用日本节点；也可能降低个别服务速度。Full Classical YAML 和 LIST **包括 IP**，MRS 与 domain YAML **不包括 IP**。

如果导入后网络不稳定，优先回退到不含 IP 的 Full MRS/domain YAML 或原24条精简版。不要把多个版本重复叠加。

## 更新方式

人工复核后提交到 `main`；Actions 通过后统一发布到 `release`，并重验稳定订阅链接。不会自动将上游新增的任意规则加入。手机端若将订阅转换成 `inline`，请单独确认刷新操作和自动更新行为。
