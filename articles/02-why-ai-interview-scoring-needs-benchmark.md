# AI 面试评分为什么需要 Benchmark？

> 技术文章骨架 — 基于 AIB (AI Interview Benchmark)

## 引言

AI 面试评分系统越来越多。但一个核心问题没人回答：

> 这个评分系统本身靠谱吗？

## 问题

### 1. 评分一致性

同一个候选人，同一段回答，问两次：

```
第一次：85 分
第二次：60 分
```

为什么？因为 LLM 有随机性。但用户不知道。

### 2. 关键词匹配 vs 理解

问题："你最大的优势是什么？"

回答 A："我擅长后端开发，有五年经验，做过高并发系统。"
回答 B："我的后端开发能力比较强，从业五载，曾处理过高并发场景。"

A = 85, B = 45？

如果评分系统只是在数关键词，那它不是在"理解"，是在"匹配"。

### 3. 排序一致性

面试官知道回答 A 比回答 B 好。评分系统给 A = 70, B = 75？

排序都做不对，绝对分数有什么意义？

### 4. 证据溯源

评分系统给 85 分。凭什么？

- 引用了哪些证据？
- 候选人说的哪些点被认可了？
- 还是凭空打分？

没有证据溯源，评分不可审计。

## AIB 的回答

AI Interview Benchmark (AIB) 不测"AI 面试官多聪明"。它测"AI 面试官的评分有多可信"。

### 六个评测维度

| 维度 | 测什么 | 为什么重要 |
|------|--------|-----------|
| ranking_consistency | 好答案分数 > 差答案分数 | 排序都错，绝对分数无意义 |
| MAE | 评分与标准答案的偏差 | 偏差大 = 评分标准不准 |
| stability_sigma | 重复评分的标准差 | 不稳定 = 不可信 |
| level_bias | 按难度分组的偏差 | 是否对某个难度系统性偏高/偏低 |
| evidence_grounding | 引用证据的覆盖率 | 无证据 = 凭空打分 |
| paraphrase_score_drift | 同义改写后分数漂移 | 漂移大 = 关键词匹配非理解 |

### 四个核心资产

#### 1. Dataset Split

```
train (8)      → 参与者校准用
dev (16)       → 开发用
public_test (30) → 公开评分
hidden_test (30) → 内部验证评分（不公开）
```

防止针对公开测试集调参。

#### 2. Perturbation Generator

同一道题，不同表达方式：

```
原题：请用一分钟介绍你自己

扰动：
- 做个自我介绍吧
- 能简单介绍一下你的背景吗
- 让我了解一下你是谁
```

保持语义意图，改变表面形式。

如果评分系统对不同表达给差异很大的分数，说明它只是在关键词匹配。

#### 3. Invariance Test（MBP 招牌特性）

同一个能力，不同问法 → 分数应该接近。

```
能力：沟通能力

问题 A → 评分 8.5
问题 B → 评分 8.4
问题 C → 评分 8.6

正常。
```

```
问题 A → 评分 9.0
问题 B → 评分 4.0
问题 C → 评分 8.0

异常。说明评分系统不理解能力，只匹配关键词。
```

#### 4. Hidden Holdout

公开分数 vs 验证分数：

- **MBP Public Score**: 在 public_test 上的分数，任何人可复现
- **MBP Verified Score**: 在 hidden_test 上的分数，不公开

类似 community edition + enterprise verification。

## 为什么 perturbation generator 是确定性的

AIB 的 perturbation generator 不依赖 LLM。

原因：如果生成器依赖某个 LLM，别人会质疑 benchmark 本身被那个模型影响。

确定性生成器（固定种子 + 模板）更容易审计，更可信。

## AIB 现状

- **版本**: v0.2.0-preview.1
- **总 cases**: 108 (24 curated + 60 generated + 24 invariance)
- **模式**: OPEN_SUITE + HIDDEN_HOLDOUT
- **CI**: Ubuntu/Windows × Python 3.11/3.12
- **仓库**: https://github.com/Metasoft-cn/ai-interview-benchmark

## 结论

AI 面试评分不是"给个分数"。它是一个需要可信度验证的评测系统。

AIB 用六个维度 + 四个核心资产回答："这个评分系统本身靠谱吗？"

---

*本文基于 AIB v0.2.0-preview.1，冻结于 2026-09-27。*
