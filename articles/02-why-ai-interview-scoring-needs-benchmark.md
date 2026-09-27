# Evaluating the Evaluators: Benchmark Infrastructure for AI Interview Scoring

> 基于 AIB (AI Interview Benchmark) — 测的不是"AI 面试官多聪明"，而是"AI 面试官的评分有多可信"。

## 引言

AI 面试评分系统越来越多。但一个核心问题没人回答：

> 这个评分系统本身靠谱吗？

## LLM Judge 的三种不可靠

当前主流的 AI 面试评分方案是 "LLM as Judge"：用一个 LLM 给候选人的回答打分。
但 LLM Judge 本身有三个系统性不可靠来源。

### 不可靠 1：Prompt Sensitivity

同一个候选人回答，同一个 judge 模型，只改 judge 的 prompt 措辞：

```
Prompt A: "请给这个回答打分，1-10 分"
→ 8.5 分

Prompt B: "请评估这个回答的质量，1-10 分，严格要求"
→ 6.0 分

Prompt C: "你是一位资深面试官，请给这个回答打分"
→ 9.0 分
```

分数差异 3 分，但候选人回答没变。

**问题**：如果 benchmark 用固定 prompt 评测，被测系统可以针对那个 prompt 优化。
如果 benchmark 不固定 prompt，结果不可复现。

### 不可靠 2：Score Drift

同一个 judge，同一个 prompt，同一个回答，不同时间运行：

```
Run 1 (temperature=0):   8.5
Run 2 (temperature=0):   8.5  (确定性)
Run 3 (temperature=0.7): 7.8
Run 4 (temperature=0.7): 9.1
```

temperature=0.7 时分数漂移 1.3 分。

**问题**：很多产品用 temperature > 0 追求"评分多样性"，
但这意味着评分本身不可复现。候选人今天 85 分，明天可能 78 分。

### 不可靠 3：Keyword Bias

```
回答 A: "我擅长后端开发，有五年经验，做过高并发系统。"
回答 B: "我的后端开发能力比较强，从业五载，曾处理过高并发场景。"
```

A 和 B 语义相同，但 A 包含 "擅长""五年""高并发" 等常见关键词，
B 用了 "从业五载" 这种少见表达。

LLM Judge 给 A = 85, B = 45。

**问题**：judge 不是在评估能力，是在数关键词。
换一种表达方式，分数就崩了。

### 这三种不可靠的共同后果

没有 invariance test，这些不可靠不会被发现。
因为每个产品只测"平均分""通过率"这种聚合指标，
分数漂移被平均掉了，prompt sensitivity 被隐藏了，keyword bias 被同质化测试集掩盖了。

这就是为什么 AIB 的核心是 invariance test。

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
train (8)        → 参与者校准用
dev (16)         → 开发用
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

这正是上面三种不可靠的检测器：
- prompt sensitivity → invariance test 用固定 judge prompt，隔离被测系统的 prompt 依赖
- score drift → invariance test 要求多次运行取统计量
- keyword bias → invariance test 用同义改写暴露关键词匹配

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

LLM Judge 的 prompt sensitivity、score drift、keyword bias 三种不可靠，
在传统聚合指标下隐形，只有 invariance test 能系统化暴露。

AIB 用六个维度 + 四个核心资产回答："这个评分系统本身靠谱吗？"

---

*本文基于 AIB v0.2.0-preview.1，冻结于 2026-09-27。*
