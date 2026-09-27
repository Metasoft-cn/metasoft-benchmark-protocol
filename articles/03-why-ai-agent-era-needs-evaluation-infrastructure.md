# 为什么 AI Agent 时代需要 Evaluation Infrastructure

> 技术文章骨架 — 基于 MBP (Metasoft Benchmark Protocol)

## 引言

AI Agent 时代，每个人都在建 Agent。

但一个没人问的问题：

> 这个 Agent 到底行不行？

不是"demo 看起来很酷"。而是"在什么标准下，它行？"

## 当前问题

### 1. 每个 AI 产品自己当裁判

```
产品 A："我们的 AI 准确率 95%"
产品 B："我们的 AI 准确率 98%"
```

谁验证？用什么数据集？什么指标？

没有标准。每个产品自己定义"准确率"是什么意思。

### 2. Benchmark = 测试集 + 排行榜 的误解

很多人以为 benchmark 就是：

```
测试集 → 跑模型 → 出分数 → 排名
```

但好的 benchmark 要回答：

- 什么场景？什么失败模式？
- 分数能复现吗？
- 会不会被针对优化（刷榜）？
- 单一分数还是多维度？
- 失败案例在哪里？

### 3. 评测代码不可复用

每个 AI 项目都自己写：

```
runner.py      # 跑测试
metrics.py     # 算分数
report.py      # 出报告
provenance.py  # 记录版本
```

四个项目的 runner 互不相同，metric 定义略有差异，report 格式不一样。

这不是评测基础设施，是四个孤岛。

## MBP 的回答

Metasoft Benchmark Protocol (MBP) 不是又一个 benchmark。它是"怎么做 benchmark"的工程协议。

### 两个层次

```
公开层（MBP）：
  Protocol    — 怎么定义 benchmark
  Schemas     — manifest / results / failure 的 JSON schema
  benchmark-core — 统一运行时
  Methodology — dataset split / perturbation / invariance / hidden holdout

私有层（产品）：
  各产品用 MBP 做内部评测
  护城河组件不公开
```

### benchmark-core：统一运行时

```
benchmark-core/
├─ adapter/     # 被测系统接口（in-process / subprocess）
├─ metric/      # 指标注册 + 计算
├─ dataset/     # 数据集加载 + split + hash
├─ runner/      # 执行引擎
├─ report/      # results.schema.json 输出
├─ provenance/  # SHA256 + 版本 + 可复现性
└─ hidden_evaluator/ # 隐藏评测边界
```

一个 benchmark 接入 MBP 只需：

1. 定义 adapter（被测系统怎么调）
2. 注册 metrics（怎么算分）
3. 提供 dataset（测试数据）

runner / report / provenance 不用自己写。

### 评测方法论

MBP 不只是代码。它定义了四个评测方法论资产：

#### 1. Dataset Split

```
train / dev / public_test / hidden_test
```

防止针对公开测试集调参。

#### 2. Perturbation Generator

保持语义意图，改变表面形式。测试系统是否真正理解。

#### 3. Invariance Test

同一能力，不同表达 → 分数应该接近。大漂移 = 关键词匹配。

这是 MBP 的招牌特性。

#### 4. Hidden Holdout

公开分数 vs 验证分数。类似 community edition + enterprise verification。

### 核心原则

```
能公开复现的，尽量公开复现。
必须防刷榜的，使用隐藏评测。
先定义指标，再比较系统。
优先暴露失败模式，而不是只给一个总分。
比较前必须冻结评测。
禁止为了某个被测系统修改 Benchmark。
```

## 已落地的 benchmark

| Benchmark | 领域 | 版本 | Cases | 模式 |
|-----------|------|------|-------|------|
| CSFB | 语音跟随 | v0.2.0-preview.1 | 6,629 | OPEN_SUITE |
| AIB | 面试评分 | v0.2.0-preview.1 | 108 | OPEN_SUITE + HIDDEN_HOLDOUT |
| Website | AI 建站 | 设计阶段 | — | — |
| Quant | 量化策略 | 设计阶段 | — | HIDDEN_SUITE |

## 为什么不是又一个框架

市面上有很多 ML 测试框架。MBP 不同在于：

1. **不是通用 ML 测试**：MBP 面向 AI Agent / AI 系统的评测，不是 model accuracy benchmark
2. **强调失败案例**：不只给分数，优先暴露失败模式
3. **强调防刷榜**：hidden holdout + invariance test
4. **强调可复现**：SHA256 + seed + version + provenance
5. **公开/私有分离**：protocol 公开，产品护城河不公开

## MBP 现状

- **版本**: v0.1.0-draft (protocol) + benchmark-core 0.1.0.dev1 (runtime)
- **Phase 1**: benchmark-core ✅ COMPLETE
- **Phase 2**: AIB v0.2 methodology ✅ COMPLETE
- **Phase 3**: Adaptive Speaking Engine (private) — design phase
- **仓库**: https://github.com/Metasoft-cn/metasoft-benchmark-protocol

## 结论

AI Agent 时代不需要又一个 leaderboard。

它需要的是：

- 可复现的评测
- 多维度的指标
- 失败案例的暴露
- 防刷榜的机制
- 统一的运行时

这就是 MBP 在做的事。

---

*本文基于 MBP v0.1.0-draft + benchmark-core Phase 1 + AIB v0.2.0-preview.1。*
