# Preimage-Chain Lower Bounds for Superpermutations

本仓库提供论文 *Preimage-Chain Corrections, Primitive-Block Rigidity, and New
Lower Bounds for Superpermutations* 的 Lean 4 形式化工程。项目证明修正后的无条件
路径级下界，并将其传递为超排列长度的全局下界及 `k = 5,…,14` 的直接数值推论。

形式化工程使用 Lean 4.31.0，并通过锁定的 Lake 依赖精确固定 Hunter–Raudvere
基线与 mathlib 版本。

## 主要结论

公共入口 [`PreimageChain.lean`](PreimageChain.lean) 导出以下最终定理：

| Lean 定理 | 内容 |
| --- | --- |
| `PreimageChain.actual_reduced_pathwise_bound_closed` | 每条 `σ²` 约化 Hamilton 路径满足修正后的路径级下界 |
| `PreimageChain.pathwise_new_bound_closed` | 任意 Hamilton 路径满足无条件 `PathwiseNewBound` |
| `PreimageChain.superperm_new_bound_closed` | 对所有 `k ≥ 5`，得到无条件全局超排列下界 |
| `PreimageChain.superperm_numerical_bounds_closed` | 直接给出论文数值表中 `k = 5,…,14` 的十项下界 |

全局定理的形式化陈述为：

```lean
theorem superperm_new_bound_closed
    {k : ℕ} (hk : 5 ≤ k) :
    Numerics.hunterBound k + Numerics.gamma k hk ≤ Hunter.Ssuper k
```

数值推论已经闭合为：

| `k` | `Ssuper k` 下界 | `k` | `Ssuper k` 下界 |
| ---: | ---: | ---: | ---: |
| 5 | 153 | 10 | 4,033,080 |
| 6 | 869 | 11 | 43,916,235 |
| 7 | 5,892 | 12 | 522,610,764 |
| 8 | 46,118 | 13 | 6,746,523,219 |
| 9 | 408,418 | 14 | 93,890,256,441 |

## 论文

- [英文版 PDF](paper/pdfs/Preimage_Chain_New_Lower_Bounds_EN_Academic_Polished.pdf)
- [中文版 PDF](paper/pdfs/Preimage_Chain_New_Lower_Bounds_ZH_Academic_Polished.pdf)
- [中英双语合订版 PDF](paper/pdfs/Preimage_Chain_New_Lower_Bounds_Bilingual_EN_then_ZH_Academic_Polished.pdf)
- [形式化与确定性计算审计补充材料](anc/Preimage_Chain_New_Lower_Bounds_Supplement_v4_Lean.zip)

补充材料版本为 `4.0.1-lean-formalized-release`，SHA-256 为
`8ce335b549b5c52c4ffbbe91f1a75528ebdbd8d9e3de49d21002c32d14a0dd65`。

## 固定环境

| 组件 | 固定版本 |
| --- | --- |
| Lean | `4.31.0` |
| Hunter–Raudvere Lean 库 | `d45222190031d162feb1f6f3cf5fe2d11fab726d` |
| mathlib | `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f` |

`lean-toolchain`、`lakefile.toml` 和 `lake-manifest.json` 共同固定完整构建环境。
Hunter 与 mathlib 由 Lake 获取，不作为 vendored 源码纳入本仓库。

## 复现验证

安装 [elan](https://github.com/leanprover/elan) 与 Git 后，在仓库根目录运行：

```bash
lake exe cache get
lake --rehash build
lake env lean AxiomCheck.lean
```

检查活动 Lean 源码不存在 `sorry`、`admit` 或项目自定义 `axiom`：

```bash
rg -n '\bsorry\b|\badmit\b|^\s*axiom\b' \
  --glob '*.lean' \
  --glob '!.lake/**' .
```

该命令的预期输出为空。也可以使用 Docker 执行隔离验证：

```bash
docker build -t preimage-chain-verify .
docker run --rm preimage-chain-verify
```

GitHub Actions 工作流通过 `workflow_dispatch` 手动触发，并执行同一套构建、
公理审计和占位符扫描。

## 信任边界

[`AxiomCheck.lean`](AxiomCheck.lean) 对主要中间结论和最终公共定理执行
`#print axioms`。四个最终定理的审计结果均只包含：

```text
propext
Classical.choice
Quot.sound
```

活动源码中不存在未完成证明或本项目新增的公理。底层排列、重叠图、Hunter 变换
及 Hunter–Raudvere 基线结果由固定提交的 Hunter Lean 库提供。因此，本仓库的
准确声明是：论文新增的无条件路径级下界、全局超排列下界及相应层级组合论证已经
形式化；不宣称 Lean 内核、mathlib、Hunter 库或所有外部软件均由本项目重新验证。

更完整的验证范围和复现规范见 [`VERIFICATION.md`](VERIFICATION.md)。

## 仓库结构

```text
PreimageChain/       形式化定义、中间引理与最终证明模块
PreimageChain.lean   统一公共入口
AxiomCheck.lean      公理依赖审计入口
lean-toolchain       Lean 版本固定文件
lakefile.toml        Lake 项目与直接依赖声明
lake-manifest.json   完整依赖锁定清单
Dockerfile           隔离复现环境
VERIFICATION.md      构建、公理与占位符审计规范
CITATION.cff         软件引用元数据
paper/               英文、中文与双语合订论文 PDF
anc/                 形式化证明与确定性计算审计补充材料
```

## 引用

引用本形式化工程时，请使用 [`CITATION.cff`](CITATION.cff) 提供的元数据，并同时
引用相应论文版本。

## 许可证

除另有说明的第三方材料外，本仓库中的原创代码、文档与论文材料均
采用 [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)
（CC BY 4.0）许可。版权所有 © 2026 Xiaolong Liu。完整条款见 [`LICENSE`](LICENSE)。

第三方依赖不属于本仓库的许可范围，继续适用其各自的许可证。
