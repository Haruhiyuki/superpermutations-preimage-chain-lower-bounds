# Second-order macro-packing research bundle

本目录研究最小超排列一般下界的二阶、支撑敏感方向。

- `SECOND_ORDER_MACRO_PACKING_RESEARCH_NOTE.md`：数学归约、宏谱、打包证据与主猜想。
- `verify_second_order_macro_packing.py`：仅使用 Python 标准库的确定性审计。
- `second_order_macro_packing_summary.json`：紧凑机器可读结果与证书索引。

复现：

```bash
python3 verify_second_order_macro_packing.py
```

完整的逐实例审计报告保存在随研究包发布的 `second_order_macro_packing_report.json` 中；仓库保留紧凑摘要，以避免提交一兆字节以上的派生数据。摘要记录了完整报告的 SHA-256、下载研究包的 SHA-256，以及仓库中验证程序的 Git blob SHA。

有限审计不替代研究笔记中标明尚待完成的任意 `k` 证明。本目录不声称已经得到新的任意 `k` 下界；其目标是建立跨越现有 `(k-4)!` 修正层级的全局研究框架。