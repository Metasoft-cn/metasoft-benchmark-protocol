# Public Launch Check Report

> 生成时间：2026-09-27
> 检查范围：MBP repo 公开层完整性验证
> 基线 commit：`4fc1ecb` + 本轮未提交变更（README 重写 + 三篇文章完善）

## 检查结论

**PASS** — 公开层具备发布条件。3 项 minor gap 不阻塞发布，列为后续改进。

---

## 1. README Links

| Link | Target | 状态 |
|------|--------|------|
| `docs/BENCHMARK_PHILOSOPHY.md` | 内部文件 | ✅ 存在 |
| `METASOFT_BENCHMARK_ROADMAP.md` | 内部文件 | ✅ 存在 |
| `docs/REPOSITORY_MAP.md` | 内部文件 | ✅ 存在 |
| `CONTRIBUTING.md` | 内部文件 | ✅ 存在 |
| `LICENSE` | 内部文件 | ✅ 存在 |
| `https://github.com/Metasoft-cn/speech-follow-benchmark` | CSFB remote | ✅ URL 匹配 |
| `https://github.com/Metasoft-cn/ai-interview-benchmark` | AIB remote | ✅ URL 匹配 |
| `https://github.com/Metasoft-cn/metasoft-benchmark-protocol` | MBP remote | ✅ URL 匹配 |

**Gap (minor)**：`articles/` 目录在 Repository Map 中提及但未链接到具体文章。建议后续在 README 加 Articles 小节。

---

## 2. CI

`.github/workflows/test.yml` 存在。

| 项 | 值 |
|----|-----|
| 触发 | push / pull_request / workflow_dispatch |
| OS matrix | ubuntu-latest, windows-latest |
| Python matrix | 3.11, 3.12 |
| 工作目录 | benchmark-core |
| 步骤 | checkout → setup-python → pip install -e ".[dev]" → pytest |

**Gap (minor)**：CI 仅覆盖 `benchmark-core/` tests，未覆盖 schema 验证和 `examples/` 校验。可后续加一个 schema-validation job。

---

## 3. Examples

三层 examples 全部存在：

| 路径 | 内容 | 状态 |
|------|------|------|
| `examples/open-suite/` | benchmark-manifest.json, dataset-manifest.json, README.md, results.json | ✅ |
| `examples/hidden-suite/` | adapter.json, benchmark-manifest.json, dev-set.jsonl, README.md | ✅ |
| `benchmark-core/examples/` | aib_integration.py, csfb_retrofit.py | ✅ |

---

## 4. License

`LICENSE` 为完整 Apache-2.0 文本（187 行）。README License 小节正确标注 "Schemas and specification text are Apache-2.0; benchmarks adopting MBP keep their own licenses."

✅ PASS

---

## 5. Contributing

`CONTRIBUTING.md`（46 行）覆盖：

- 变更前检查清单（SPEC / philosophy / version bump / schema / tests）
- 变更类型分类（clarification / addition / breaking）
- benchmark-core API freeze 约束
- PR 验证要求
- 新 benchmark 接入流程
- 文档风格规范（无营销话术、无 emoji）

✅ PASS

---

## 6. Release Docs

`docs/RELEASE_CHECKLIST.md`（53 行）覆盖：

- MBP protocol release（9 项检查）
- Benchmark release（11 项检查）
- Freeze lifecycle gates：DRAFT→PREVIEW（5 项）、PREVIEW→FROZEN（6 项）、FROZEN→DEPRECATED（3 项）

✅ PASS

---

## 7. Schemas

`schemas/` 含 5 个 JSON Schema：

| Schema | 用途 |
|--------|------|
| `benchmark.schema.json` | benchmark manifest 验证 |
| `dataset-manifest.schema.json` | dataset manifest 验证 |
| `engine-adapter.schema.json` | adapter 配置验证 |
| `failure.schema.json` | failure case 验证 |
| `results.schema.json` | results 输出验证 |

✅ PASS

---

## 8. Tests

```
38 passed in 0.28s
```

`benchmark-core/` 全部测试通过。

✅ PASS

---

## 9. Protocol Docs

| 文件 | 状态 |
|------|------|
| `SPEC.md` | ✅ |
| `VERSIONING.md` | ✅ |
| `REPRODUCIBILITY.md` | ✅ |
| `SECURITY.md` | ✅ |
| `CHANGELOG.md` | ✅ |
| `METASOFT_BENCHMARK_ROADMAP.md` | ✅ |
| `METASOFT_BENCHMARK_PORTFOLIO.md` | ✅ |
| `METASOFT_BENCHMARK_ASSET_INVENTORY.md` | ✅ |
| `PUBLIC_FOUNDATION_REPORT.md` | ✅ |

`docs/` 含 12 个文件：BENCHMARK_PHILOSOPHY / REPOSITORY_MAP / RELEASE_CHECKLIST / METRIC_POLICY / FREEZE_POLICY / OPEN_VS_HIDDEN / ANTI_GAMING / SEPARATION_POLICY / FAILURE_CORPUS / REFERENCE_IMPLEMENTATIONS / EVALUATION_ENGINE_DESIGN / case-studies/

✅ PASS

---

## 10. Articles

三篇技术文章已从 skeleton 完善为正式版：

| 文章 | 标题 | 状态 |
|------|------|------|
| `01-why-ai-teleprompter-needs-standards.md` | The Case for Standardized Evaluation of AI Teleprompters | ✅ 正式版 |
| `02-why-ai-interview-scoring-needs-benchmark.md` | Evaluating the Evaluators: Benchmark Infrastructure for AI Interview Scoring | ✅ 正式版 |
| `03-why-ai-agent-era-needs-evaluation-infrastructure.md` | From Unit Tests to Agent Evaluation Protocols: Building Trustworthy AI Agent Infrastructure | ✅ 正式版 |

本轮补充内容：
- 文章 1：新增"传统提词器的三种失败模式"（跳读/忘词/即兴具体案例）
- 文章 2：新增"LLM Judge 的三种不可靠"（prompt sensitivity / score drift / keyword bias）并连接到 invariance test
- 文章 3：新增"评测的三个时代"（Unit Test → ML Benchmark → Agent Evaluation Protocol 演进 + 对比表）

✅ PASS

---

## 11. .gitignore

```
__pycache__/
*.py[cod]
.venv/
.pytest_cache/
*.egg-info/
build/
dist/
benchmark-core/aib_output/
benchmark-core/csfb_output/
```

**Gap (minor)**：MBP repo `.gitignore` 未排除 hidden_test 相关文件。但 MBP repo 本身不持有 hidden_test（hidden_test 在 AIB repo 中，AIB 的 `.gitignore` 已排除）。当前 MBP repo 无泄露风险。

---

## 12. No Private Content

- `ADAPTIVE_SPEAKING_ENGINE_DESIGN.md` 位于 `D:\03_Others\Desktop\提词器\`，在 MBP repo 之外 ✅
- MBP repo 内无提词器设计文档、无内部实现代码 ✅
- `git log` 无含密钥/凭证的 commit ✅

✅ PASS

---

## 汇总

| 检查项 | 结果 |
|--------|------|
| README links | ✅ PASS (1 minor gap: articles 未链接) |
| CI | ✅ PASS (1 minor gap: 无 schema validation job) |
| Examples | ✅ PASS |
| License | ✅ PASS |
| Contributing | ✅ PASS |
| Release docs | ✅ PASS |
| Schemas | ✅ PASS |
| Tests (38) | ✅ PASS |
| Protocol docs | ✅ PASS |
| Articles (3) | ✅ PASS |
| .gitignore | ✅ PASS (1 minor gap: MBP 本身无 hidden_test) |
| No private content | ✅ PASS |

**总体：PASS — 可公开发布。**

3 项 minor gap 不阻塞发布，列为后续改进：
1. README 加 Articles 小节，链接到三篇文章
2. CI 加 schema validation job
3. （无需行动）MBP repo 本身不持有 hidden_test，无泄露风险

---

## 未提交变更

本轮 4 个文件已修改，待一次性 commit + push：

```
modified:   README.md
modified:   articles/01-why-ai-teleprompter-needs-standards.md
modified:   articles/02-why-ai-interview-scoring-needs-benchmark.md
modified:   articles/03-why-ai-agent-era-needs-evaluation-infrastructure.md
new file:   PUBLIC_LAUNCH_CHECK_REPORT.md  (本文件)
```
