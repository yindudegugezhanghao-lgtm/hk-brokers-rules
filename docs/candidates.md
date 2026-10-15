# 候选与排除记录

检查日期：2026-10-15。这里的域名均 **不在正式规则中**。候选表示本次证据不足，不代表有害、已失效或不属于券商。不能因社区清单出现、名字相似或 DNS 能解析就启用。

| 线索 | 状态 | 本次处理与所需补充 |
| --- | --- | --- |
| `futufin.com`、`futuhn.com`、`futu0.com` 至 `futu9.com` | 待核验 | 社区存在业务线索；尚缺当前官方域名用途或关联证据。API 子域线索应追溯到可信官方资料，不能一律扩大到主域。 |
| `moomoobull.com`、`futuhkapp.com`、`moomoo.com.hk` | 待核验 | 可提供官网交叉链接、官方客户端下载或官方隐私声明以补充。 |
| `tigerbbs.cn`、`tigerbrokers.net`、`zhijianfengyi.cn`、`zhijianfengyi.com` | 待核验 | 未充分核对当前用途、归属及必要性；不凭拼写推断。 |
| `longbridge.global`、`longbridgeapp.com`、`longbridgehk.com`、`longbridge.cloud`、`wbrks.com` | 待核验 | 社区线索保留；需要官方当前业务端点或受控资源证据。 |
| `zhangleglobal.com`、`ihtfin.com` | 待核验 | 华泰社区规则线索，当前官方核验不足。 |
| `htsc.com`、`htsc.com.cn`、`htzq.com.cn` | 暂不收录 | 集团或内地业务线索；本次未证明对华泰国际 / 涨乐全球通分流的必要性。 |
| `usmart8.com`、`usmart-app.com`、`usmart.sg` | 待核验 | 需要当前官方 SDK、客户端下载或条款中明确的服务关系。 |
| `mfosunhani.com` | 待核验 | 复星社区业务线索，未确认当前业务角色；不因含有品牌字符而启用。 |
| `htisec.com` | 排除 | 海通国际，与华泰国际不是同一券商，不能混淆。 |
| `appsflyersdk.com`、`play-analytics.com`、`googletagmanager.com` | 排除 | 统计、归因或追踪服务，不满足规则范围。 |
| `qcloud.com`、`myqcloud.com`、`amazonaws.com`、`cloudfront.net`、`b-cdn.net` | 排除 | 共享云或通用 CDN；即便客户端会用到某个租户子域，也不收录其主域。 |
| `tradingview.com` 及其独立服务域 | 排除 | 独立第三方金融平台。 |
| 其他券商、银行、IP-CIDR、IP-ASN 和关键词规则 | 排除 | 超出项目约定范围，不作为候选自动采纳。 |

已由正式主域覆盖的 `api.futunn.com`、`cdn.futustatic.com`、`api.lbkrs.com`、`openapi-quote.longbridge.com` 等不另列规则。客户端未来使用新域名或直连 IP 的情况，需要脱敏观察后重新核验；规则不承诺全流量覆盖。
