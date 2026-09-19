---
name: editorial-publishing-engine
description: 出版级编辑排版引擎。把已写好的长文（尤其是《西方哲学，从0开始》这类知识文章）转换为 1080×1440 的高端编辑型图片轮播（editorial carousel）。反AI感是最高优先级硬门槛；内容默认冻结（preserve），视觉目标为杂志/文化刊物级 editorial feeling。
---

# Editorial Publishing Engine（出版级编辑排版引擎）

> 不是普通小红书卡片生成器。目标观感：高端杂志 / 文化刊物 / 高级金融杂志的 editorial feeling。
> 参考 Vogue 的标题与留白纪律、T Magazine 的文化感与图文克制、The New Yorker 的文章感与文字优先、高端金融杂志的结构与来源严谨；**不复制任何具体杂志的版式、logo、masthead 或专有视觉**。

## 何时使用本 Skill

- 输入是一篇**已写好的长文**（正文已批准/接近批准），需要变成一组 3:4 竖版编辑型图片轮播。
- 输出是 1080×1440 的 PNG 序列 + contact sheet，用于发布到竖版内容平台。
- 用户要求“编辑感 / 杂志感 / 高级感 / 不要 AI 知识卡感”时。
- 默认适配《西方哲学，从0开始》（见 `references/PHILOSOPHY_ADAPTER.md`），也可适配其他知识长文（换主题词典即可）。

## 核心工作流

```text
FINAL COPY
  → intent mode
  → semantic structure analysis
  → page plan
  → master assignment
  → art direction
  → HTML
  → Playwright PNG
  → ANTI-AI GATE
  → visual QA
  → contact sheet
  → targeted revision
  → final export
```

## 四种内容意图（intent mode）

| intent | 默认 | 允许 | 禁止 |
|---|---|---|---|
| preserve | ✅ | 冻结正文，只分页排版 | 改字、删判断、加解释 |
| compress | | 压缩句子表达 | 改变判断、条件、不确定性 |
| rewrite | | 用户明确允许时改写 | 擅自改写 |
| visualize | | 把已有关系转成图 | 发明数据、新增关系 |

**已批准正文默认冻结（preserve）**。压缩的底线：压缩的是句子，不是论证。

## 最高优先级硬规则

1. 已批准正文默认冻结；局部反馈 → 局部修改。
2. 不因为“统一视觉”重做整套。
3. 不按平均字数机械分页；每页只承担一个主要思想动作。
4. 内容决定布局；图片必须有信息功能；没图比乱加图好。
5. whitespace 是结构，不是剩余空间。
6. **ANTI-AI 是 HARD GATE**。
7. Philosophy 300 常规发布目标为 **8–10 页，原则上不超过 10 页**；需要控制页数时，优先合并相邻认知动作和提高页面利用率，不得删掉冻结论证。
8. KNOW / CORRECT / TOOL / PERSON 是后台验收维度，不要求前台逐项做成独立栏目或“方法页”。

## MASTER TEMPLATE SYSTEM v1.1

旧 12 layouts 仅保留为兼容层；正式页面统一落在 5 个 MASTER：essay / statement / evidence / cover / credits。

### 固定 Section Marker

- 常规内容页使用两位阿拉伯数字：`01 / 02 / 03 ...`，不再使用“一 · / 二 · / 三 ·”。
- 推荐结构：`<span class="section-no">01</span><span class="section-title">泰勒斯是谁</span>`。
- 数字使用该页强调色；章节名固定近黑。
- 数字约 26px，章节名约 23px；不得退回 13px 轻量 kicker。
- 只用间距分隔，不使用 `·` 作为编号分隔符。
- 同一 deck 连续编号，不得逐页改样式。

### 固定账号 Chrome

每一页必须显示 `@每天读一点哲学`。默认页脚左侧固定为：
`《西方哲学，从0开始》 · @每天读一点哲学`；右侧固定为 `NNN / 300 · PAGE NN`。
账号名属于出版身份，不是正文，不得随页面内容变化。

### Source / Colophon

- “资料来源”只展示读者需要的真实文献来源。
- 内部工程文件名、冻结版本、渲染器版本、测试版本不出现在读者前台。
- 如需保存内部出版信息，留在 HTML metadata、repo、audit 或内部 colophon 文件，不占常规发布页。

## 目录结构

```text
skills/editorial-publishing-engine/
├── SKILL.md
├── README.md
├── references/
├── schemas/
├── layouts/
├── masters/
├── renderer/
├── qa/
└── tests/
```

## 默认配置

`config/philosophy_300_editorial.yaml`：canvas 1080×1440 / 3:4、content_mode preserve、
literary-editorial 主 + fashion-intellectual 次、近黑文字、单一低饱和强调色、
禁止渐变/圆角卡/阴影/emoji 装饰/等宽栅格/默认居中 hero/纸张纹理/假数据。

## 修订纪律

- 用户只提某一页 → 只改那一页。
- 改完重建 contact sheet，复核整组节奏与相邻页衔接。
- 正文在 preserve 模式下改动 = 内容锁校验失败，必须显式升级 intent 才能动正文。
