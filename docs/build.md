# 云端构建与验证

所有 MRS 构建、测试和发布都在 **GitHub 托管 Actions** 中执行。脚本检查 `GITHUB_ACTIONS` 与 `RUNNER_ENVIRONMENT`，本地调用构建流程会拒绝执行；无需在用户电脑安装、下载或运行 Mihomo。

## 数据流

1. `brokers.json` 登记券商；当前仅六家。`source/<broker>.txt` 是唯一人工规则源，`docs/domains.json` 是逐条证据元数据。
2. `scripts/build.py` 严格检查语法、主域层级、大小写、重复、IP、规则类型、来源与券商对应；合并使用集合确保产物唯一。发现重复源条目时失败，要求维护者消除歧义。
3. LIST 输出 `DOMAIN-SUFFIX`，YAML 输出 `payload` 下的 `+.domain`，供 `behavior: domain` 使用。
4. 下载 [Mihomo v1.19.32 官方 release](https://github.com/MetaCubeX/mihomo/releases/tag/v1.19.32) 的 Linux amd64 compatible 压缩包，先核对锁文件中的 SHA256 再解压执行。
5. 使用官方命令生成二进制，并重新读取 MRS 还原为 domain 文本，与源集合逐项比较。

```text
mihomo convert-ruleset domain yaml HK_Brokers.yaml HK_Brokers.mrs
mihomo convert-ruleset domain mrs HK_Brokers.mrs roundtrip.txt
```

命令已依据该版本的 [mrs_converter.go](https://github.com/MetaCubeX/mihomo/blob/v1.19.32/rules/provider/mrs_converter.go) 核对。官方 [提供者文档](https://wiki.metacubex.one/en/config/rule-providers/) 说明 MRS 支持 domain / ipcidr，本项目只生成 domain。MRS 是含版本标记的压缩二进制，不是重命名文本。

## 真实验证

`scripts/validate_runtime.py` 启动真实 Mihomo，检查 API 提供者数量并经 HTTP 代理发送请求：

- `classical/text` LIST 文件提供者。
- `domain/yaml` 文件提供者。
- `domain/mrs` 文件提供者。
- `domain/mrs` HTTP 提供者，通过 HTTP 实际下载 MRS。
- 每个主域、`api` 子域及多层子域必须命中；相似前缀、主域后追加其他后缀必须不命中。
- 银行、其他券商、共享云、追踪及独立金融平台作为负例。
- 损坏的 MRS 必须被官方解析器拒绝。

所有测试目标只映射到 runner 内部回环地址，无需登录、访问券商账户或下单。正例只有经券商规则进入测试选择组才可返回特定内容，兜底为 REJECT；负例还检查没有到达回环测试服务。测试覆盖规则语义，不能代替真实 iPhone 或券商客户端完整业务测试。

可选 JS 用独立 fixture 检查原配置字段、原规则次序、动态节点来源、同名冲突、Unicode、通配符 DNS 键及幂等，并使用同一 Mihomo 校验其输出配置。

## 发布与失败处理

`main` 推送或手动运行可发布；`pull_request` 只校验。Actions 固定到提交 SHA，Mihomo 固定版本和压缩包哈希；升级必须通过 PR 审查。流水线无付费服务器和自定义 API 密钥，只使用 GitHub 自带 `GITHUB_TOKEN`。

先完成全部生成及测试，再把 `.build/rules` 作为一次 Git 提交推送至 `release` 分支；LIST / YAML / MRS 不会分批发布。发布前检查源分支头，跳过过时构建，且串行化发布。若生成或测试失败，不更新发布分支；公开下载复核若因 GitHub 传播或网络故障失败，已提交的文件仍是此前通过验证的完整集合，工作流报告失败供排查。

发布后 `scripts/verify_published.py` 从 GitHub 公共 HTTPS 下载订阅文件，逐字节比较，再用下载文件重做真实路由测试。裸链接 CDN 可能有短时缓存；复核使用带运行号的查询参数防止读到旧缓存，正式稳定链接不需要参数。

`manifest.json` 包含域名数量、分券商列表、来源提交、工具版本、构建时间、Actions 地址和文件哈希；`validation.json` 包含测试结果，`SHA256SUMS` 用于内容校验。每个发布提交可回溯和恢复。

## 维护规则

通过 PR 修改源文件、证据元数据与 `docs/sources.md` 的变更记录。CI 不会自动抓取、启用候选或自动合并 PR。人类维护者必须核对证据真实性与范围。

未来新增券商时，登记 `brokers.json`、新增源文件与证据，更新文档；无需更改合并器。为避免把子域误当主域，当前明确允许的公共后缀是 `com / cn / hk / com.hk / com.cn`；如新域使用其他后缀，应先依据 [Public Suffix List](https://publicsuffix.org/list/) 更新脚本中的已审查后缀集合。该有限后缀集不是完整 PSL 数据库。

客户端以 86400 秒更新频率下载最近一次审核发布；不是自动扩张规则范围。Fork 用户需修改 README、示例 JS 与示例配置内的仓库路径，并在自己的 Actions 权限中允许工作流写入发布分支。
