# 稀疏雷达论文一区实验补强执行计划 进度回填

日期：2026-07-28  
用途：把 `C:\Users\刘子轩\Desktop\稀疏雷达论文一区实验补强执行计划_20260728.md` 与当前可验证证据对齐，避免把“计划存在”误认成“任务已完成”。

## 1. 计划文件本身的机械统计

- 计划文件中共有 **63 个 checkbox 项**
- 当前机械统计结果：**0/63 已勾选，63/63 未勾选**
- 结论：这份计划文档本身还没有被回填成进度表，仍是执行蓝图

## 2. 证据层面的真实进度

以下状态来自现有状态文档和冻结包，而不是来自这份计划的勾选状态。

| 区块 | 当前状态 | 证据摘要 | 结论 |
|---|---|---|---|
| Phase 0 方法身份 / 协议 / 证据治理 | 部分完成 | `paper_experiment_status.md` 明确写到 Gate 1 仍是 partial，Gate 2 仍是 incomplete；`final_experiment_audit_and_manuscript_plan.md` 也指出 Gate 1 还缺最终 split/evaluator hash packet，Gate 2 还未把基线策略冻结为单一政策 | 不是空白，但未闭合 |
| Phase A 现有预测高收益实验 | 大部分已有证据 | 已有投票公平对照、proposal 诊断、校准、效率、定性图、统计/复算等材料；但真实腐蚀大矩阵和统一口径仍未完全收口 | 已经推进很远，但仍有未定稿项 |
| Phase B 短训筛选 / 多种子闭环 | 部分完成 | formal 3-seed main comparison、strict route 12/12 positive、high-performance formal comparison 等已经有完整证据；当前 fair_ablation 结果表已推进到 311/322，剩余 11 条全部是 `error=True` 的失败证据或外部阻塞 | 核心主结果已成，筛选闭环未全满 |
| Phase C 完整数据 / 外部有效性 | 未完成 | 完整 MAN / VoD / TJ4DRadSet / full K-Radar / 多类别 / LODO / 少样本 / worst-group 仍主要停留在计划层 | 这是当前最大的缺口之一 |
| 高价值加分实验 | 混合完成 | 点丢失、投票敏感性、校准、效率、定性图等已有结果；但并非全部都达到主文级冻结 | 可写进论文的部分已经不少 |
| 不建议继续投入的实验 | 已确定 | 计划中已明确列出不要再做的大量细搜和无效扩种子 | 这部分属于决策完成，不是实验完成 |
| 预注册验收标准 | 未满足 | 主性能、模块贡献、鲁棒性、校准、跨域、效率的总验收线尚未全部闭合 | 仍不能宣称整体 paper-ready |
| 最终论文表图 | 部分完成 | 主文/补充材料的结构和边界已有冻结文件，但最终版仍需要和剩余闭环项同步 | 可用框架已有，最终收口未完 |
| 排期 / 清单 | 未完成 | 推荐排期和 completion checklist 仍未被回填成完成状态 | 仍是待执行项 |

## 3. 当前已经可以视为“有实证支撑”的部分

这些内容已经不是纯计划，属于可直接拿来写论文或做冻结边界的材料。

- 严格路线在 4 数据集 × 3 种子上有 **12/12 正增益**
- 高性能路线 `q55rpa50_kprior` 已经能作为高性能分支讨论
- 点丢失、投票敏感性、校准、效率、定性 BEV 这些证据已存在
- `paper_experiment_status.md`、`final_experiment_audit_and_manuscript_plan.md`、`table_and_caption_freeze.md` 等文件已经把主文/补充/内部边界分开
- `submission_audit_bundle.md`、`independent_recomputation_bundle_manifest.md`、`dataset_protocol_bundle.md` 等冻结包已经存在，但 Gate 1 / Gate 2 仍未完全终局化

## 4. 当前仍然没做完或没法闭合的部分

### 4.1 仍缺协议闭环

- final split/evaluator hash packet 未完全归档
- baseline roster 仍未冻结成唯一 manuscript-facing 政策
- 方法身份注册表还没有变成唯一、不可混用的最终记录

### 4.2 仍缺完整外部有效性

- 完整 MAN / VoD / TJ4DRadSet / full K-Radar
- 多类别主结果
- LODO / 少样本
- 自然恶劣天气最坏组
- 真正意义上的完整官方 SOTA 表

### 4.3 仍缺部分筛选闭环

- M3 / M4 的单种子 go/no-go 还没有把所有分支收束到一个统一结论
- 少数模块和分支仍停在 screening 或 partial evidence
- 当前只剩 11 条缺口，其中 9 条是 `error=True` 的失败证据，2 条是外部阻塞

## 5. 冻结矩阵里的 T1-T15 进展

当前冻结矩阵不是全部完成，但已经有 4 个条目进入 `supported`。

| T项 | 状态 | 含义 |
|---|---|---|
| T1 | supported | 四数据集主对比已冻结，可写主文，但还需要最终呈现语言 |
| T2 | partial | 顺序消融已重建，但 M3/M4 在部分数据集仍不完整 |
| T3 | supported | 四数据集交互闭环已存在，可作为执行证据 |
| T4 | partial | 组件消融仍是 screening |
| T5 | partial | RGPC 族仍是 screening |
| T6 | partial | range 分析还缺最终接受表 |
| T7 | partial | sparsity 分析还缺 bootstrap CI 闭环 |
| T8 | partial | 物理分析仍未形成最终包 |
| T9 | partial | point dropout 还缺斜率最终化 |
| T10 | partial | corruption grid 仍未全闭合 |
| T11 | supported | 效率和延迟证据已足够支撑当前结论 |
| T12 | supported | 校准链路与四模块/四数据集证据已闭合 |
| T13 | partial | convergence 还缺最终包 |
| T14 | partial | 定性图还缺最终筛选和排序 |
| T15 | partial | 敏感性还缺全局共享包 |

## 6. 适合继续推进的顺序

1. 先把 `Gate 1` 的协议包补成能冻结的最终版本
2. 再把 `Gate 2` 的基线名册和比较政策冻结成单一口径
3. 把可闭合的 `Phase A / B` 材料回填到主文或补充材料框架
4. 把无法继续推进的分支显式标成 `blocked` 或 `screen-only`
5. 最后再判断是否还有必要补 `Phase C` 的完整官方数据路线

## 7. 现有 fair_ablation 残余缺口

The module-level residual map is now separated into a dedicated note:

- [fair_ablation_remaining_gap_map_20260728.md](C:/Users/刘子轩/radar_experiment_configs/results/fair_ablation_remaining_gap_map_20260728.md)

That map records:

- 11 incomplete rows remaining in `fair_ablation_seed_results.csv`
- 9 failed-model rows with `error=True`
- 2 blocked rows with empty / mismatched Astyx splits
- no retryable rows remain
- `bevgate_replay10 / kradar / 2028` has completed rerunning on GPU0
- `corner / truckscenes / 2028` has completed rerunning on GPU1
- `rccg / kradar / 2028` has completed rerunning on GPU2

This means the remaining work is no longer just “unknown missing runs”; it is
now partitioned into `blocked` and `failed evidence` classes.

## 8. 一句话结论

这份计划不是“做完了”，而是“已有相当一部分证据成熟，但计划层和冻结层还没有完全闭合”。  
如果只看计划勾选，当前是 **0/63**；如果看实证材料，**主线证据已经推进到可以写论文的程度，但完整一区闭环还差协议冻结、基线冻结和完整外部有效性**。当前 fair_ablation 结果表已经推进到 **311/322**，剩余 11 条中有 9 条是失败证据，2 条是外部阻塞。
