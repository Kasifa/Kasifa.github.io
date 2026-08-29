# R0.73C 全站发布缺口矩阵

**审计日期：** 2026-08-30  
**基线提交：** `01af908`  
**公开端点：** v1.42 / R0.73B  
**审计范围：** 首页、研究笔记总索引、R0.60 后累计回顾、文献路线、发布清单、formal archive、双语资源和 GitHub Pages 实际页面。本文只记录审计结果；没有改动 `public/`、`scripts/` 或 `tests/`。

## 1. 结论

用户所说的“首页停在 R0.69V、研究笔记停在 R0.69W”描述了一个真实的**可发现性印象**，但不再是当前源码或线上页面的实际状态。

- 当前首页的顶部统计已经是 `178` 篇、最新 `R0.73B`。
- 首页正文同时存在且实际显示 `#r069v`、`#r069w`、`#r070a` 一直到 `#r073b`；R0.70A–R0.73B 共 80 张发布卡片。
- 独立的 `/notes/` 总索引有 178 条，R0.73B 位于第一条，R0.70A、R0.69W 和 R0.69V 都可直接找到。
- 当前累计回顾完整列出 R0.61–R0.73B 的 118 个节点；文献综述对本审计范围内的 82 个节点全部有研究笔记链接。
- 线上 `https://kasifa.github.io/`、`/notes/`、`/literature-review.html`、当前 recap 和 `site-version.json` 与本地 `public/` 对应文件逐字节一致。R0.70A、R0.73B 和当前 recap 均返回 HTTP 200。

当前真正存在的全站一致性缺口只有一个：根目录 `VERSION` 仍为 `1.41`，而 `public/site-version.json` 与 `research/release-manifest.json` 已为 `1.42`。R0.73C 发布时必须把三者同时推进到 `1.43`，并由 publication test 强制一致。

## 2. 为什么会看起来停在 R0.69V / R0.69W

证据不支持“R0.70A 以后未发布”这一解释。v1.42 之前的 v1.41 首页已经有 `#r070a` 和 `#r073b`，顶部也已经写明 178 篇和 R0.73B。问题主要出在入口和摘要层：

1. v1.41 没有 `public/notes/index.html`。首页“查看完整笔记”指向超长单页内部的 `#first-task`，而不是 latest-first 总索引。
2. v1.41 的当前路线标题仍停在“固定 \(M\) 的任意静态相位 Morse shape gate 已经闭合”，虽然同页后面已经有 R0.73B 卡片。这会让顶部路线看起来明显落后。
3. 首页在 R0.69W 后先插入 `#post-r060-recap`，再继续 R0.70A；加上完整首页超过十四万像素高，用户在 recap 处容易误以为逐节卡片已经结束。
4. 提交 `7879203`（`site: surface the complete post-R0.60 route`）新增 latest-first 总索引，把“查看完整笔记”改到 `/notes/`，增加直达 R0.73B 的入口，并把路线标题更新到 R0.73B。当前 `origin/main` 已包含该提交。

因此，最稳妥的判断是：曾经存在摘要/入口滞后，浏览器缓存或 Pages 部署时差可能放大了这个印象；但无法仅由仓库证明用户当时看到的具体缓存版本。当前浏览器实渲染已确认 R0.70A 和 R0.73B 为 `display:block`、`visibility:visible`，控制台无 warning/error。

## 3. R0.69V–R0.73B 发布矩阵

“首页”指详细研究卡片和首页路线链接；“recap”指当前 `public/recap-r0-61-r0-73b.html` 的完整节点索引；“文献”指 `public/literature-review.html` 的当前路线链接；“总索引”指 `public/notes/index.html`。

| 范围 | HTML / PDF | 首页 | recap | 文献 | 总索引 | 发布清单 / formal 状态 |
|---|---|---|---|---|---|---|
| R0.69V–W | 2/2 均有 | 均有 `id` 和链接 | 均有 | 均有 | 均有 | 早于 R0.70A formal inventory 合同；不进入 80/56/24 三个计数 |
| R0.70A–L | 12/12 均有 | 均有 | 均有 | 均有 | 均有 | 12 节全部 published；A–B 为 `missing-figure-directory`，C–L 为 `explanatory-package`，故列入 24 节 backlog |
| R0.70M–O | 3/3 均有 | 均有 | 均有 | 均有 | 均有 | published 且 formal-sealed |
| R0.70P–Z | 11/11 均有 | 均有 | 均有 | 均有 | 均有 | 全部 published；formal figure directory 未按现合同封存，列入 backlog |
| R0.71A | 1/1 均有 | 有 | 有 | 有 | 有 | published；列入 backlog |
| R0.71B–Z | 25/25 均有 | 均有 | 均有 | 均有 | 均有 | 全部 published 且 formal-sealed |
| R0.72A–Z | 26/26 均有 | 均有 | 均有 | 均有 | 均有 | 全部 published 且 formal-sealed |
| R0.73A–B | 2/2 均有 | 均有 | 均有 | 均有 | 均有 | 全部 published 且 formal-sealed |

逐项程序核对结果：在这 82 个节点中，note HTML、同名 PDF、首页 `id`、首页 note link、当前 recap link、文献路线 link 和 `/notes/` 索引条目均无缺失。

formal inventory 的 24 节 backlog 精确为：

```text
R0.70A–R0.70L
R0.70P–R0.70Z
R0.71A
```

formal-sealed 的 56 节精确为：

```text
R0.70M–R0.70O
R0.71B–R0.71Z
R0.72A–R0.72Z
R0.73A–R0.73B
```

这一区分很重要：`published` 表示公开材料存在；`formal-sealed` 还要求满足当前的正式附图与证据封存合同。不能把 backlog 写成“研究没有发布”。

## 4. 当前全站计数与 R0.73C 期望值

| 指标 | 当前 R0.73B | R0.73C 完整发布后 | 来源 / 选择器 |
|---|---:|---:|---|
| site version | 1.42 | 1.43 | `public/site-version.json.version`、`research/release-manifest.json.siteVersion`、首页 `html[data-site-version]`；根 `VERSION` 也必须同步 |
| 最新节点 | R0.73B | R0.73C | `public/site-version.json.latestRelease`、首页 `.status-meta`、`/notes/` 第一条 |
| 公开 HTML 研究笔记 | 178 | 179 | `public/notes/r0-*.html`；索引页自身不计数 |
| 同名研究笔记 PDF | 135 | 136 | `public/notes/r0-*.pdf` |
| 历史 HTML-only | 43 | 43 | HTML 数减同名 PDF 数 |
| R0.61 后 recap 节点 | 118 | 119 | 当前 recap 的 `.node-ref`；manifest `postR060RecapNodeCount` |
| 当前路线 R0.69P 后节点 | 88 | 89 | 首页 `.route-note-links a` |
| 首页 R0.70A 后发布卡片 | 80 | 81 | 首页 `[data-release]` |
| recap 阶段 | 37 | 38 | 当前 recap 的 `article.phase`；R0.73C 应独立成一阶段 |
| R0.70A 后 published | 80 | 81 | formal archive `publishedReleaseCount` |
| formal-sealed | 56 | 57 | formal archive `formalSealedReleaseCount` |
| legacy backlog | 24 | 24 | formal archive `legacyFormalFigureBacklogCount` |
| next release | r073c | r073d | `research/release-manifest.json.nextRelease` |

首页会新增第 83 个 `#r069v`–`#r073c` 范围内的详细卡片；其中 `[data-release]` 合同从 R0.70A 开始，因此该选择器应由 80 增到 81，而不是增到 83。

## 5. R0.73C 必须更新的入口和文字

### 5.1 首页 `public/research-review.html`

必须同时更新：

- `html[data-site-version="1.43"]`；
- `/i18n-en.js?v=1.43` 与 `/site-refresh.js?v=1.43`；
- `.status-meta` 的发布日期、v1.43、179、R0.73C；
- “我目前关注”、`Research topology · R0.1–R0.73C`；
- `.route-map-actions .route-map-latest` 指向 `#r073c`；
- 累计回顾链接改到 `/recap-r0-61-r0-73c.html`；
- 当前路线 range、标题、结论边界和 `<summary>` 的 89 节计数；
- `.route-note-links` 追加唯一的 `/notes/r0-73c.html`；
- `#post-r060-recap` 改为 119 / 179 / 81 / 57 / 24；
- 新增唯一 `<div id="r073c" data-release="r073c">`，并链接 note HTML/PDF、formal figure、certificate、report 和当前 recap；
- 页脚版本、日期与“上次综述”指针。

GitHub Pages workflow 会把该文件复制为 `_site/index.html`，所以仓库中没有 `public/index.html` 不是缺口。

### 5.2 研究笔记总索引 `public/notes/index.html`

用 `scripts/generate_note_index.py` 重建，而不是手工插入。验收点：

- R0.73C 是第一条；R0.73 series 从 2 篇变 3 篇；
- 179 HTML、136 PDF、43 HTML-only、latest R0.73C；
- recap 链接改到 R0.73C；
- v1.43 cache keys；
- `python3 scripts/generate_note_index.py --check` 通过。

### 5.3 累计回顾

新建并保留两套文件：

```text
public/recap-r0-61-r0-73c.html
public/recap-r0-61-r0-73c.pdf
```

旧的 R0.73B HTML/PDF 是历史端点，必须保持不变。新 recap 必须：

- 覆盖 R0.61–R0.73C，而不是只补一段 R0.73C；
- 把总节点改为 119；
- 把公开 / sealed / backlog 改为 81 / 57 / 24；
- 在 timeline 中新增 R0.73C 独立 phase；
- 在 node index 末尾新增唯一 R0.73C；
- 更新 retained result、value、next、claims、reproduce，明确 C3/C4、C5、C6 与 Clay 的不同证据状态；
- 下一步改为 R0.73D。

历史 recap 快照从 R0.71A 才开始逐版保留，并且缺少 R0.71B 快照；这不是当前路线内容缺失，因为最新累计 recap 的 118 节索引完整覆盖 R0.61–R0.73B。未来继续遵守“每完成一节就生成新的累计 recap 并保留上一版”即可，不应重写旧快照。

### 5.4 文献综述 `public/literature-review.html`

必须更新：

- “本站 R0.69P–R0.73C 只列为研究笔记”；
- 当前 deck 的 endpoint、119 节 recap 链接和 R0.73C 路线判断；
- 新增含 `/notes/r0-73c.html` 的 route step；
- 新增唯一 `#r073c-boundary`，把主源、本站推导、有限计算和仍开放的外推分开；
- current recap 链接改到 C；
- footer 与 i18n cache 改到 v1.43。

### 5.5 manifest、archive、version

`research/release-manifest.json` 应变为：

```text
latestCompletedRelease                 r073c
siteVersion                            1.43
publicHtmlNoteCount                    179
postR060RecapNodeCount                 119
postR070APublishedReleaseCount         81
postR070AFormalSealedReleaseCount      57
legacyFormalFigureBacklogCount         24
nextRelease                            r073d
```

并把 latest mathematical gate、publication test 指针改到 R0.73C。`research/formal-archive-inventory.json` 必须只在两个 append-only 数组末尾各追加一次 `r073c`，latest 改 C、计数改 81/57，24 条 backlog 不变。

`public/site-version.json`、release manifest 和根 `VERSION` 必须统一为 `1.43`。当前 runner 没有捕捉根 `VERSION=1.41` 的漂移，R0.73C publication test 应补上该断言。

### 5.6 i18n

必须同步：

```text
translations/en.json
public/i18n-en.js
scripts/add-r073c-translations.mjs
scripts/i18n-snapshots/r073c-missing.json
```

R0.73C 中文与英文都要保留第一人称单数、证据边界和相同数学 token。当前双语全覆盖测试已通过；发布后必须再次证明 dictionary 对所有公开中文字符串无 missing key、无中文残留且 protected TeX/URL 不变。

## 6. 每完成一节后的固定发布清单

以后每一节都按同一事务完成，不让研究编号先于公开端点前进：

1. 冻结 analytic proof / negative result、claim ledger、gap matrix 与 literature audit；OPEN 项保持 OPEN。
2. 完成确定性证书、独立审计、实验 manifest/原始数据/进度日志、正式附图及 QA。
3. 生成 note HTML/PDF、formal figure 的 public byte-identical copies 和新的累计 recap HTML/PDF。
4. 同步首页 latest/progress/card、文献路线与 boundary、latest-first `/notes/` 索引。
5. 同步英文 dictionary、cache version、site-version、release manifest、formal archive 和根 `VERSION`。
6. 运行数学 gate、certificate source test、figure source test、release test、publication invariant、internal links、bilingual coverage、note-index check 和总 runner。
7. 合并到 `main` 后等待 Pages 完成，再核对根页、note、recap、literature、index、site-version 的 HTTP 200 和部署字节一致性。

本次只读审计实际运行的相关测试为：

```text
tests/bilingual-content.test.mjs
tests/release-publication-invariant.test.mjs
tests/site-route-current-boundary.test.mjs
tests/r073b-release.test.mjs
```

共 19 项全部通过。这证明当前 R0.73B 的公开入口、计数、recap endpoint、archive 分层和双语覆盖已经同步；它不替代 R0.73C 尚未完成的数学证书与发布门。

## 7. 线上逐字节核对

```text
homepage / research-review.html  d4bee04c7d38ff04ae3428c8a98e30e688b82bc05ebde02e4b4f8325c4e16abe
notes/index.html                  fcd7ee7f084e807ac3897af9db4c43990ed3549953a490b35310b3a375d3279b
literature-review.html            bed51c262c5974a04b10661c87cabdf54d48371ae3887be46b50ef26fb9ae429
recap-r0-61-r0-73b.html           5678a409d215d09857419cf7daf26f66d760755a833fbbc0e3fd054aff463a00
site-version.json                 d89777aa3813cdd5524d9186c8cb3af1b152f98c5bb5385d84fa8e0f752e3df6
```

以上每个 hash 的线上文件与本地文件相同。该结果只确认 2026-08-30 本次核验时的部署状态；R0.73C 发布后必须重新计算，不能沿用这些 hash。
