# 验证与复现

本文档规定形式化工程的可复现构建、公理审计和完整性检查方法。

## 固定环境

| 组件 | 版本 |
| --- | --- |
| Lean | `4.31.0` |
| Hunter–Raudvere Lean 库 | `d45222190031d162feb1f6f3cf5fe2d11fab726d` |
| mathlib | `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f` |

Lean 工具链由 `lean-toolchain` 固定；直接依赖由 `lakefile.toml` 声明；完整依赖图由
`lake-manifest.json` 锁定。

## 完整构建

安装 [elan](https://github.com/leanprover/elan) 与 Git 后，在仓库根目录执行：

```bash
lake exe cache get
lake --rehash build
```

`PreimageChain` 与 `AxiomCheck` 均为默认构建目标。构建成功表示全部 Lean 模块已经
由固定工具链重新检查。

## 公理审计

执行：

```bash
lake env lean AxiomCheck.lean
```

`AxiomCheck.lean` 对证明链中的主要中间结论和最终公共定理运行 `#print axioms`。
下列四个最终定理仅依赖 `propext`、`Classical.choice` 与 `Quot.sound`：

- `PreimageChain.actual_reduced_pathwise_bound_closed`；
- `PreimageChain.pathwise_new_bound_closed`；
- `PreimageChain.superperm_new_bound_closed`；
- `PreimageChain.superperm_numerical_bounds_closed`。

审计输出不得包含 `sorryAx` 或项目自定义公理。

## 完整性扫描

使用 ripgrep 检查活动源码：

```bash
rg -n '\bsorry\b|\badmit\b|^\s*axiom\b' \
  --glob '*.lean' \
  --glob '!.lake/**' .
```

预期输出为空。

## Docker

也可以在隔离环境中执行同一验证流程：

```bash
docker build -t preimage-chain-verify .
docker run --rm preimage-chain-verify
```

镜像构建阶段获取固定依赖、编译全部证明、运行公理审计并拒绝任何未完成证明或
项目自定义公理。

## 信任边界

本项目依赖 Lean 内核、mathlib 以及固定版本的 Hunter Lean 库。底层排列、重叠图、
Hunter 变换和 Hunter–Raudvere 基线结果由 Hunter 依赖提供；本仓库验证论文新增的
无条件路径级下界、全局超排列下界及相应层级组合论证。
