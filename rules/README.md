# 构建产物

`main` 保存人工审核的源文件。LIST、YAML、MRS、校验和及测试报告仅在 GitHub Actions 构建，验证通过后整体提交到 `release` 分支的本目录。

- [HK_Brokers.mrs](https://raw.githubusercontent.com/yindudegugezhanghao-lgtm/hk-brokers-rules/release/rules/HK_Brokers.mrs)
- [HK_Brokers.yaml](https://raw.githubusercontent.com/yindudegugezhanghao-lgtm/hk-brokers-rules/release/rules/HK_Brokers.yaml)
- [HK_Brokers.list](https://raw.githubusercontent.com/yindudegugezhanghao-lgtm/hk-brokers-rules/release/rules/HK_Brokers.list)
- [validation.json](https://raw.githubusercontent.com/yindudegugezhanghao-lgtm/hk-brokers-rules/release/rules/validation.json)

不要手工编辑或改名伪造 MRS；构建失败会保留上次成功发布。
