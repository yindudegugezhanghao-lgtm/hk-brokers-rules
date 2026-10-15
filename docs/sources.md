# 域名来源与核验记录

核验日期：2026-10-15。正式启用 **24 个主域名**。每条的机器可读记录见 [domains.json](domains.json)。下列依据为官网、官方文档、官方公开客户端网页或发行人披露；社区收录只作线索。

“官网链接/业务调用”代表合理确认使用关系，不等于独立 WHOIS 所有权审计。网页可能跳转、要求 JS 或对爬虫限流；这种情况结合官网入口、公开文档与披露核对，不将 HTTP 200 或域名相似作为归属证据。专用静态资源可收录，共享云和通用 CDN 不收录。主域规则也会覆盖该券商在该域下的其他官方功能，并不只限于交易 API。

| 券商 | 主域名 | 用途 | 官方依据与收录理由 |
| --- | --- | --- | --- |
| futu | `futuhk.com` | 官网 | [依据 1](https://www.futuhk.com/about-us) · [依据 2](https://ir.futuholdings.com/)。富途香港官网；发行人官网及公开披露可交叉核对。 |
| futu | `futuholdings.com` | 公司官网 / 投资者关系 | [依据 1](https://ir.futuholdings.com/) · [依据 2](https://www.futuhk.com/about-us)。富途控股官方投资者关系站，保留企业入口。 |
| futu | `futunn.com` | OpenAPI / 行情 / 交易文档 | [依据 1](https://openapi.futunn.com/futu-api-doc/intro/intro.html) · [依据 2](https://ir.futuholdings.com/)。官方 Futu API 文档承载域名；子域名由主域规则覆盖。 |
| futu | `futustatic.com` | 专用静态资源 | [依据 1](https://www.moomoo.com/) · [依据 2](https://cdn.futustatic.com/)。moomoo 官方页面引用 cdn.futustatic.com；是券商专用资源域，未扩大到共享 CDN。 |
| futu | `moomoo.com` | 官网 / 国际业务 | [依据 1](https://www.moomoo.com/) · [依据 2](https://ir.futuholdings.com/)。富途国际品牌官网；官方发行人资料说明 moomoo 业务。 |
| tiger | `itiger.com` | 官网 / 客户端下载 | [依据 1](https://www.itiger.com/sg/) · [依据 2](https://docs.itigerup.com/docs/intro)。老虎官方站与官方 OpenAPI 文档交叉核对。 |
| tiger | `itigerup.com` | 官网 / 开放平台 | [依据 1](https://docs.itigerup.com/docs/intro) · [依据 2](https://www.itigerup.com/help)。老虎官方开发文档及帮助中心。 |
| tiger | `laohu8.com` | 官方社区 / 行情内容 | [依据 1](https://www.itiger.com/sg/hans/marketing/Tigermerch) · [依据 2](https://ir.itigerup.com/static-files/a35fef98-aebf-46f1-a319-f1406d5919f3)。官网组件指向 laohu8.com/J/scoremall；发行人年报明确社区网站名称。 |
| tiger | `skytigris.cn` | 资讯 API | [依据 1](https://hkg.itiger.com/news/2673083458) · [依据 2](https://www.itiger.com/sg/)。官方资讯页公开 SSR 数据引用 stock-news.skytigris.cn/v3/news。仅据业务调用关系认定，未声称有注册人证明。 |
| tiger | `tigerfintech.com` | 客户端下载 | [依据 1](https://www.itiger.com/sg/) · [依据 2](https://www.itigerup.com/help)。官方站的桌面下载及应用商店跳转使用 download / da.tigerfintech.com。 |
| longbridge | `lbctrl.com` | 专用静态资源 | [依据 1](https://longbridge.com/hk) · [依据 2](https://longbridge.com/us)。两个地区官网引用 assets.lbctrl.com；未收录其底层共享云域。 |
| longbridge | `lbkrs.com` | 官方文件 / 业务资源 | [依据 1](https://longbridge.com/us) · [依据 2](https://assets.lbkrs.com/uploads/whale-site/LONGPORT%20Whale%E6%8A%80%E6%9C%AF%E6%9C%8D%E5%8A%A1%E9%80%9A%E7%94%A8%E6%9D%A1%E6%AC%BE.pdf)。长桥官网法律文件与长桥技术服务条款均由 assets.lbkrs.com 承载。 |
| longbridge | `longbridge.cn` | 行情 / 交易推送 | [依据 1](https://open.longbridge.com/zh-CN/docs/socket/hosts) · [依据 2](https://longbridge.com/hk)。官方业务地址文档列明 openapi-quote / openapi-trade.longbridge.cn。 |
| longbridge | `longbridge.com` | 官网 / OpenAPI / 行情交易 | [依据 1](https://open.longbridge.com/zh-CN/docs/socket/hosts) · [依据 2](https://longbridge.com/hk)。官网与官方业务地址交叉确认，覆盖 openapi 等子域。 |
| longbridge | `longportapp.com` | LongPort 平台 / 客户端服务 | [依据 1](https://support.longbridgewhale.com/topics/misc.disable/lp-user-agreement?locale=en) · [依据 2](https://longportapp.com/)。官方用户协议明确定义平台运营主体及 longportapp.com 网址；与长桥关联技术平台保持一致。 |
| huatai | `htsc.com.hk` | 官网 / 涨乐全球通 | [依据 1](https://www.htsc.com.hk/sc/service/software-download) · [依据 2](https://zlglobal.htsc.com.hk/zl/zh-hans/about/about-us.html)。华泰香港官网下载页与涨乐全球通品牌说明交叉确认。 |
| huatai | `zhangle.com` | 涨乐全球通下载 | [依据 1](https://www.htsc.com.hk/sc/service/software-download) · [依据 2](https://gb.zhangle.com/)。华泰香港官网的涨乐全球通下载入口直接指向 gb.zhangle.com。该主域也覆盖集团同品牌服务。 |
| usmart | `usmart.hk` | 官网旧入口 / 客服 | [依据 1](https://www.usmart.hk/zh-hk/download) · [依据 2](https://hk.usmartglobal.com/zh-hk)。旧官网跳转到现官网；现官网客服邮箱使用 usmart.hk。 |
| usmart | `usmartglobal.com` | 现官网 / 香港与新加坡入口 | [依据 1](https://hk.usmartglobal.com/zh-hk) · [依据 2](https://www.usmart.hk/zh-hk/download)。官方入口重定向到 hk.usmartglobal.com，站内列明持牌主体并链接新加坡子站。 |
| usmart | `usmartsecurities.com` | 旧官网 / 服务入口 | [依据 1](https://www.usmartsecurities.com/) · [依据 2](https://hk.usmartglobal.com/zh-hk/promotion-and-activities/detail/305)。旧入口重定向到现官网；现官网历史活动明确链接该域。 |
| fosun | `fosunwealth.com` | 官网旧入口 / 登录 | [依据 1](https://www.fosunwealth.com/contact) · [依据 2](https://www.fosunwealth.hk/)。旧入口跳转到现官网，现官网注册 / 登录仍链接 fosunwealth.com。 |
| fosun | `fosunwealth.hk` | 现官网 / 下载 | [依据 1](https://www.fosunwealth.hk/) · [依据 2](https://www.fosunwealth.hk/download/download)。官方站标注复星财富控股主体及星财富 App。 |
| fosun | `fotechwealth.com` | 星财富 App 服务入口 | [依据 1](https://www.fosunwealth.hk/) · [依据 2](https://h5.fotechwealth.com/m/?from=fosunwealth&langType=zhTc)。复星财富官网顶部的星财富 App 链接指向 h5.fotechwealth.com。 |
| fosun | `fotechwealth.com.cn` | 星财富存量客户下载入口 | [依据 1](https://www.fotechwealth.com.cn/) · [依据 2](https://www.fosunwealth.hk/download/download)。星财富官方下架公告说明存量客户更新与备用交易通道，页面主体为深圳星财智。 |

## 社区交叉检索（不是官方认证）

独立审查以下仓库相关规则，不复制其工程、注释或整份清单；依官方证据形成上述精简集合。部分仓库存在继承关系，多个仓库出现同一域名不能算多个独立证据。

- [forecho/broker-rules / Broker.list](https://github.com/forecho/broker-rules/blob/main/Broker.list)：提供六家相关线索，同时含其他券商、第三方、IP 与重复子域；均需独立过滤。
- [Arthur-vx/broker-rules / Broker.list](https://github.com/Arthur-vx/broker-rules/blob/main/Broker.list)：对照富途、老虎、长桥；排除其他券商、IP、追踪与重复子域。
- [LingJingMaster/Shadowrocket-Rules / HK_Broker.list](https://github.com/LingJingMaster/Shadowrocket-Rules/blob/main/HK_Broker.list)：对照同类域名，未将其收录当官方证明。
- [koo17173/rule-set / Stocks.list](https://github.com/koo17173/rule-set/blob/main/Stocks.list) 与 [BrokerHT](https://github.com/koo17173/rule-set/blob/main/BrokerHT)：辅助发现华泰线索；不采纳共享基础设施和大网段。
- [foreverchen9/personal_proxy_rules / foreverchen9_hk_broker.list](https://github.com/foreverchen9/personal_proxy_rules/blob/main/foreverchen9_hk_broker.list)：辅助发现 uSMART 与长桥旧入口；不采纳关键词规则和已覆盖子域。
- [blackmatrix7/ios_rule_script / TigerFintech.list](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Clash/TigerFintech/TigerFintech.list)：对照老虎条目；仍分别寻找官方用途依据。

## 修改记录

- 2026-10-15：首版启用上述 24 个主域名。理由逐条记录于表格和 JSON；其余线索见 [candidates.md](candidates.md)。
- 后续每次新增、删除都必须在此追加日期、域名、理由与证据；删除时保留旧记录或 Git 历史。CI 检查所有启用域名有元数据、日期及官方来源，但无法自动判断网页证据真实性；PR 必须人工核验。

