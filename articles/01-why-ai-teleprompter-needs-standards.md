# 为什么 AI 提词器需要行业标准？

> 技术文章骨架 — 基于 CSFB (Chinese Speech Follow Benchmark)

## 引言

传统 teleprompter 只做一件事：滚动文本。

AI 提词器要做的事完全不同：

- **跟读**：知道用户说到哪里了
- **跳读**：用户跳过了一段，能跟上
- **忘词**：用户卡住了，能提示
- **即兴**：用户偏离了，能拉回来
- **时间控制**：剩余时间不够了，能压缩

这些能力目前没有行业标准。每个产品自己定义"跟读正确"是什么意思。

## 问题

### 1. "跟读准确率 95%" 是什么意思？

没有标准 dataset，这个数字无法比较。

- 什么算"跟读正确"？
- 什么场景？正常跟读？跳读？忘词？
- 什么语言？中文？英文？混合？
- 什么难度？短文本？长文本？技术术语？

### 2. 跳读检测没有基准

用户从第 3 段跳到第 7 段，AI 应该：

- 检测到跳转
- 不报错
- 从第 7 段继续

但"检测到跳转"的准确率怎么测？没有标准答案。

### 3. 恢复能力无法量化

用户忘词了，AI 提示后用户恢复。恢复时间多久？恢复到正确位置了吗？这些都没有 benchmark。

## CSFB 的回答

Chinese Speech Follow Benchmark (CSFB) 是第一个面向中文语音跟随的公开 benchmark。

### 数据集

- 6,629 cases / 48,851 events
- 覆盖：正常跟读、跳读、忘词、重复、混合语言、技术术语
- 每个事件有 expected segment index（标准答案）

### 评估维度

不是单一"准确率"，而是多维度：

| 维度 | 含义 |
|------|------|
| event_accuracy | 每个事件的 segment 预测是否正确 |
| final_accuracy | 最终位置是否正确 |
| false_jump | 误报跳转的次数 |
| skip_detection | 跳读检测准确率 |
| recovery_latency | 恢复到正确位置的延迟 |
| by_language | 按语言分组的准确率 |
| by_region | 按区域（spoken/non-spoken）分组的准确率 |

### 失败案例优先

CSFB 不只给一个分数。它暴露失败案例：

- 哪些场景所有 baseline 都失败？
- 哪些场景只有部分 baseline 失败？
- 失败模式是什么？（wrong-backward? false-jump? lost-recovery?）

## 为什么需要标准

### 对产品团队

有了标准，"我们的跟读准确率 95%" 可以变成 "在 CSFB v0.2 上 event_accuracy=0.95, false_jump=0.02"。

可比较，可复现，可信任。

### 对用户

用户可以问："这个提词器在 CSFB 上得过多少分？"

而不是听营销话术。

### 对行业

当多个产品在同一 benchmark 上比较，整个行业有了进步方向。

## CSFB 现状

- **版本**: v0.2.0-preview.1
- **模式**: OPEN_SUITE（公开可复现）
- **CI**: Ubuntu/Windows × Python 3.11/3.12
- **数据集 SHA256**: `242a5937…95fcdf`
- **仓库**: https://github.com/Metasoft-cn/speech-follow-benchmark

## 结论

AI 提词器不是"滚动文本 + ASR"。它是一个实时决策系统：跟读、跳转检测、恢复、时间控制。

这些能力需要标准化的评测。CSFB 是第一次尝试。

---

*本文基于 CSFB v0.2.0-preview.1，数据集冻结于 2026-09-23。*
