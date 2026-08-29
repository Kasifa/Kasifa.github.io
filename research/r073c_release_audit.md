# R0.73C 发布架构只读审计

> **时间截面说明：** 本文第 2 节记录的是证明完成前的发布阻塞。后续
> `r073c_monodromy_proof.md`、双区间内核和独立 Decimal 复算已经闭合 C3/C4；
> C5 仍为 OPEN，C6 仍为 CONDITIONAL。最终状态以
> `r073c_report-source.md` 为准。

**审计日期：** 2026-08-30  
**基线提交：** `01af908`  
**基线端点：** public v1.42 / R0.73B  
**范围：** 列出 R0.73C 从 source stage 到 GitHub Pages 的文件、计数、生成顺序和测试门。本审计不修改 `public/` 或 `scripts/`。

## 1. 当前基线

我在当前 checkout 上运行了：

```bash
node scripts/run-release-publication-gate.mjs
python3 scripts/generate_note_index.py --check
```

两项均通过。发布 runner 当前解析为：

```text
latestCompletedRelease = r073b
mathematical gate      = tests/r073b-bloch-kinetic-gate.test.mjs
publication test       = tests/r073b-release.test.mjs
translation checker   = scripts/add-r073b-translations.mjs --check-only
```

当前可复核计数为：

| 项目 | 当前值 |
|---|---:|
| `public/site-version.json.version` | `1.42` |
| `research/release-manifest.json.siteVersion` | `1.42` |
| 最新公开节点 | `R0.73B` |
| `r0-*.html` 研究笔记 | 178 |
| 同名研究笔记 PDF | 135 |
| 历史 HTML-only 笔记 | 43 |
| R0.61 后 recap 节点 | 118 |
| R0.69P 后当前路线节点 | 88 |
| R0.70A 后已公开版本 | 80 |
| formal-sealed 版本 | 56 |
| legacy formal-figure backlog | 24 |

### 当前存在的一处版本不一致

根目录 `VERSION` 仍是 `1.41`，而 site-version 和 release manifest 已是
`1.42`。当前 publication runner 没有检查 `VERSION`，所以仍然通过。
R0.73C 不能继续复制这个漂移。最稳妥的处理是先把当前 baseline 的
`VERSION` 明确校正为 `1.42`，再由 R0.73C 发布事务统一推进到
`1.43`。至少，R0.73C 的 publication test 必须断言三处版本完全一致。

## 2. R0.73C 不能在数学结论冻结前发布

`research/r073c_problem_freeze.md` 仍把 C3--C5 列为 TO_PROVE，并把
C6 列为 conditional。现有 agent notes、screen 和 enclosure 脚本只能作为
工作输入，不能直接替代最终报告、独立审计或无限维证书。

发布前必须先把结果收敛成下列三类之一：

- 经证明的 `CLOSED`；
- 经证明的 `FALSE` 或严格 no-go；
- 保留为 `OPEN`，同时只发布本节已经证明的较弱结论。

有限 Fourier cutoff 收敛不能单独把 C4 改为 CLOSED；C5 也不能由
instantaneous numerical abscissa 推出。若 C4 或 vanishing-viscosity
Riesz package 未闭合，公开页面必须继续把 super-polynomial no-go 标为
conditional，而不能把它写成 R0.73C 的最终 theorem。

## 3. source stage 文件

### 3.1 必须作者化或综合的研究文件

最接近 R0.73B 合同的 R0.73C 文件集合是：

```text
research/r073c_problem_freeze.md
research/r073c_report-source.md
research/r073c_literature_audit.md
research/r073c_gap_matrix.md
research/r073c_<final-result>_proof.md
research/r073c_independent_analytic_audit.md
```

`<final-result>` 应在 C4/C5 的真实结论确定后命名。当前这些工作文件可作为
输入，但不应直接被宣告为 formal proof：

```text
research/r073c_fast_transfer_agent.md
research/r073c_rayleigh_analytic_agent.md
research/r073c_spectral_enclosure_agent.md
research/r073c_interval_monodromy.py
research/r073c_spectral_screen_agent.py
```

最终 `report-source` 需要一张稳定 claim ledger，明确哪些条目是
`ANALYTIC_PASS`、`FALSE`、`CONDITIONAL` 和 `OPEN`；不得留下
`TO_PROVE`/`TO_DISPROVE` 却同时推进公共计数。

### 3.2 source-stage manifest

只有在所有被引用路径已经存在后，才在
`research/release-manifest.json` 增加 `nextReleaseSourceStage`。在 source
stage，以下 live pointers 必须继续停在 R0.73B：

```text
latestCompletedRelease = r073b
latestReleaseGate = tests/r073b-bloch-kinetic-gate.test.mjs
latestReleasePublicationTest = tests/r073b-release.test.mjs
publicHtmlNoteCount = 178
postR060RecapNodeCount = 118
postR070APublishedReleaseCount = 80
postR070AFormalSealedReleaseCount = 56
```

R0.73C block 至少应绑定：

```text
release                  = r073c
stage                    = source-freeze
publicationStatus        = pending-formal-certificate-figure-and-publication
publicCountersAdvanced   = false
report                   = research/r073c_report-source.md
problemFreeze            = research/r073c_problem_freeze.md
literatureAudit          = research/r073c_literature_audit.md
gapMatrix                = research/r073c_gap_matrix.md
analyticProof            = research/r073c_<final-result>_proof.md
independentAudit         = research/r073c_independent_analytic_audit.md
independentAnalyticAudit = research/r073c_independent_analytic_audit.md
producer                 = research/certificates/r073c/generate_certificate.py
independentProducer      = research/certificates/r073c/independent_recompute.py
comparator               = research/certificates/r073c/validate_certificate.py
certificateDirectory     = research/certificates/r073c
experimentDirectory      = experiments/r073c
figureDirectory          = figures/r073c/<figure-package>
generator                = scripts/generate_r073c_release.py
translationScript        = scripts/add-r073c-translations.mjs
translationSnapshot      = scripts/i18n-snapshots/r073c-missing.json
releaseGate              = tests/r073c-<claim>-gate.test.mjs
publicationTest          = tests/r073c-release.test.mjs
certificateSourceTest    = tests/r073c-deterministic-certificate-source.test.mjs
figureSourceTest         = tests/r073c-<figure>-figure-source.test.mjs
```

全局 invariant 会访问其中的核心路径；过早写入一个尚不存在的路径会使
当前 R0.73B 发布 runner 立即失败。这是预期的 fail-closed 行为。

## 4. formal evidence 文件

### 4.1 确定性证书

新建：

```text
research/certificates/r073c/
  README.md
  generate_certificate.py
  independent_recompute.py
  validate_certificate.py
  command.txt
  environment.txt
  progress.ndjson
  certificate.json
  independent_recompute.json
  crosscheck.json
  validation.json
  manifest.json
  SHA256SUMS
```

证书必须区分：解析恒等式、interval/tail enclosure、有限维诊断和未证明的
无限维结论。若 C4 采用 Fourier-tail enclosure，tail estimate、rounding
mode、区间库版本和独立 validator 必须进入 manifest 与 hash ledger。

沿用 R0.73B 的 lifecycle：先 `--source-stage`，在绑定源文件形成真实
40-hex commit 后再 `--formal --source-commit <commit>`；最后运行
`validate_certificate.py --require-formal`。`SHA256SUMS` 必须覆盖目录中
所有普通文件且不得覆盖目录外路径。

### 4.2 数值实验

新建 `experiments/r073c/`。确切 CSV/JSON 名称应由最终 C4/C5 screen
决定，但至少保留：

```text
README.md
command.txt
requirements.txt
environment.json
contract.json
manifest.json
progress.ndjson
summary.json
validation.json
<solver-or-screen>.py
<independent-validator>.py
<raw-or-lossless-data files>
```

manifest 应记录 cutoff、精度、步长、参数网格、线程数、硬件、wall time、
source hash 和每个输出的 bytes/SHA-256。若只做有限矩阵，必须保留
`finiteDimensionalOnly=true`，且 claim boundary 明确否认无限维谱证明。

### 4.3 正式附图

新建：

```text
figures/r073c/<figure-package>/
```

最接近 R0.73B 的 source inventory 是：

```text
README.md
caption.md
command.txt
config.json
contract.json
environment.txt
figure-contract.md
manifest-draft.json
plot.py
qa-protocol.md
requirements.txt
validate.py
```

formal render 后增加：

```text
figure.pdf
figure.svg
figure.png
data.csv                  # 或 manifest 声明的等价原始数据
results.json
validation.json
manifest.json
SHA256SUMS
qa-final-size.png
qa-grayscale.png
qa-pdf.png
qa-report.md
```

最终 master 仍应为 178 mm 双栏向量 PDF/SVG 和 600 dpi PNG，除非
figure contract 明确选择 85 mm 单栏。formal manifest 必须记录人工最终
尺寸、灰度和 PDF raster QA。公开的 PDF/SVG/PNG 必须与 archival master
逐字节一致。

正式 figure 通常需要 distinct source commit 与 certificate commit；所以
提交顺序不能压成一个未封存的 working-tree 快照。

## 5. R0.73C 发布时新建的文件

最终 claim slug 和 figure ID 尚未冻结，以下用占位符表示，但固定部分是
确定的。

### 5.1 发布脚本与测试

```text
scripts/generate_r073c_release.py
scripts/add-r073c-translations.mjs
scripts/i18n-snapshots/r073c-missing.json
tests/r073c-<claim>-gate.test.mjs
tests/r073c-release.test.mjs
tests/r073c-deterministic-certificate-source.test.mjs
tests/r073c-<figure>-figure-source.test.mjs
```

### 5.2 公共输出

```text
public/notes/r0-73c.html
public/notes/r0-73c.pdf
public/recap-r0-61-r0-73c.html
public/recap-r0-61-r0-73c.pdf
public/assets/r073c/<figure-id>.pdf
public/assets/r073c/<figure-id>.svg
public/assets/r073c/<figure-id>.png
```

旧的 `recap-r0-61-r0-73b.*` 必须保留为历史端点。GitHub Pages workflow
会在部署时把 `public/research-review.html` 复制为 `_site/index.html`；仓库
中不需要另建 `public/index.html`。

## 6. R0.73C 发布时修改或重新生成的文件

| 文件 | R0.73C 更新点 |
|---|---|
| `public/research-review.html` | v1.43/cache/date；179 笔记；latest R0.73C；完整路线新增 C；current route 89；新增唯一 `data-release="r073c"` card；累计回顾改到 119；NEXT 改为 R0.73D；链接新 note/PDF/figure/certificate/report/recap |
| `public/literature-review.html` | cache/footer v1.43；route 把“开放接口 R0.73C”改为有证据标签的 R0.73C；新增“开放接口 R0.73D”；新增 `id="r073c-boundary"`；recap/link/count 改到 C/119 |
| `public/notes/index.html` | 由 `generate_note_index.py` 重建；R0.73C 必须第一；R0.1 仍最后；179 HTML、136 PDF、43 HTML-only；recap 链接指向 C；v1.43 |
| `public/i18n-en.js` | 由 R0.73C translation script 重建完整 live dictionary |
| `public/site-version.json` | `version=1.43`、`latestRelease=R0.73C`、`publicHtmlNoteCount=179`、实际发布日期 |
| `translations/en.json` | 追加稳定 `r073cNNN` 条目；保留全部旧条目 |
| `research/release-manifest.json` | latest=C；siteVersion=1.43；179/119/81/57/24；next=D；latest gate/publication pointers 改为 C；移除 `nextReleaseSourceStage` |
| `research/formal-archive-inventory.json` | `publishedReleases` 与 `formalSealedReleases` 各 append `r073c`；latest=C；counts 81/57；backlog 仍 24 |
| `VERSION` | 与 canonical site version 同步为 `1.43` |
| `tests/site-route-current-boundary.test.mjs` | 当前 route/literature 边界由 R0.73B 改为 R0.73C，并保留“每个 note route 只出现一次”的断言 |

在当前动态架构下，通常**不需要**修改：

```text
scripts/generate_note_index.py
scripts/i18n-lib.mjs
tests/release-publication-invariant.test.mjs
tests/internal-public-links.test.mjs
tests/bilingual-content.test.mjs
.github/workflows/pages.yml
.github/workflows/release-publication-gate.yml
```

这些文件已从 manifest 或实际 `r0-*.html` inventory 推导 endpoint。只有
当 R0.73C 改变发布合同本身时才应修改它们。

## 7. 预期计数

若 R0.73C 按当前 formal contract 完整发布，并且同名 PDF 同步生成，
最终计数应为：

```text
siteVersion                         1.43
latestCompletedRelease             r073c
latestRelease                      R0.73C
publicHtmlNoteCount                179
same-name note PDFs                136
historical HTML-only notes         43
postR060RecapNodeCount             119
current route R0.69P–R0.73C        89
postR070APublishedReleaseCount      81
postR070AFormalSealedReleaseCount   57
legacyFormalFigureBacklogCount      24
nextRelease                         r073d
```

若累计回顾为 R0.73C 新增一个独立 phase，phase 数将从 37 变为 38；该值
应由实际 `<article class="phase">` 计数验证，而不是先假定后填文案。

总索引页本身不计入 179。note count 必须继续使用 `r0-*.html` 或
`/^r0-[0-9a-z]+\.html$/`，不能恢复为 `*.html`，否则
`public/notes/index.html` 会被误计为第 180 篇。

## 8. 最接近的 generator

### 8.1 full release generator

最接近模板是 `scripts/generate_r073b_release.py`。它已经包含：

- exact baseline preflight；
- source-stage manifest equality；
- certificate、experiment、figure fail-closed validation；
- formal figure 与 public assets 的 byte identity；
- note、recap、homepage、literature、manifest/archive 的顺序更新；
- `required`、`once`、`section`、`assert_clean`、MathJax 检查和 flat hash
  ledger helpers；
- `R073B_RELEASE_ROOT` 的 fixture-root 模式。

R0.73C 应复制结构而不是运行旧脚本，并至少改为：

```text
R073C_RELEASE_ROOT
R073B_RELEASE_BASELINE = v1.42 / 178 / 118 / 80 / 56 / 24
SOURCE_STAGE_CONTRACT.release = r073c
input and claim tokens = final C4/C5 decision
output note = public/notes/r0-73c.html
output recap = public/recap-r0-61-r0-73c.html
site version = 1.43
next release = r073d
```

preflight 还应断言 R0.73C note/PDF、recap/PDF 和 public asset directory 均
不存在，首页没有 `data-release="r073c"`，当前 recap 恰有 118 个唯一
节点。所有输入验证必须在第一次 public write 之前完成。

历史 R0.73B generator 仍写 v1.41；这是一次性历史生成器，不能拿它重跑
当前 v1.42 tree。

### 8.2 note index generator

`scripts/generate_note_index.py` 是可直接复用的 generator：

```bash
python3 scripts/generate_note_index.py
python3 scripts/generate_note_index.py --check
```

它读取 `public/site-version.json`，所以必须在 site-version 已推进到 R0.73C
后运行。它也按同名 PDF 是否存在决定链接；因此最终一次生成必须放在
`public/notes/r0-73c.pdf` 已经生成之后，否则会把 R0.73C 错标为
HTML-only，并把 43 临时变成 44。

### 8.3 PDF renderer

full release generator 故意不嵌入 Playwright/Chromium PDF 生成。最接近的
既有用法是先服务 `public/`，再调用：

```bash
python3 -m http.server 8000 --directory public

node scripts/render-note-pdf.mjs \
  http://127.0.0.1:8000/notes/r0-73c.html \
  public/notes/r0-73c.pdf

node scripts/render-note-pdf.mjs \
  http://127.0.0.1:8000/recap-r0-61-r0-73c.html \
  public/recap-r0-61-r0-73c.pdf
```

PDF 要在中文模式、MathJax 和字体加载完成后生成，并检查页数、文件头、
链接、公式断行和打印版布局。

### 8.4 i18n generator

复制 `scripts/add-r073b-translations.mjs` 为 R0.73C 版本。active pages 应
至少是：

```text
literature-review.html
notes/index.html
notes/r0-73c.html
recap-r0-61-r0-73c.html
research-review.html
```

脚本应要求这些页加载 `/i18n-en.js?v=1.43`，把 exact missing-string
顺序冻结到 `scripts/i18n-snapshots/r073c-missing.json`，追加
`r073cNNN` IDs，并同时写 `translations/en.json` 与
`public/i18n-en.js`。最终执行：

```bash
node scripts/add-r073c-translations.mjs
node scripts/add-r073c-translations.mjs --check-only
```

snapshot 必须在 note、recap、home、literature、index 的最终中文字符串
稳定后生成；否则任何后续文案修改都会触发 snapshot drift。

## 9. 测试门

### 9.1 R0.73C 专属门

`tests/r073c-<claim>-gate.test.mjs` 应检查：

- 最终 analytic/negative claim 的准确公式、量词和 norm；
- C4 与 C5、finite enclosure 与 infinite-dimensional theorem 的边界；
- positive/negative \(\Lambda\) 和 fixed \(\gamma_*\) 的限定；
- source-stage manifest 不推进公共计数；
- experiment/certificate claim boundary；
- `TO_PROVE` 不会混进已完成 claim。

`tests/r073c-release.test.mjs` 应检查：

- generator 的 fail-closed 输入验证先于 public writes；
- source stage 与 final stage 两种 lifecycle；
- final counts 179/119/81/57/24 和 next R0.73D；
- `VERSION`、site-version、manifest、所有 active cache tags 都为 1.43；
- note、recap、home、literature、index 的链接和唯一 current gate；
- note/recap PDF；
- formal figure/public asset byte identity；
- exact English coverage、protected TeX token 和 CLOSED/FALSE/OPEN boundary。

certificate/figure source tests 应检查独立重算、无 producer import、source
bindings、commit lineage、self-test zero-write、准确 package inventory、vector
PDF/600-dpi PNG 和视觉边界。

### 9.2 当前 canonical runner

final manifest 改到 R0.73C 后，下面命令会动态切换到 C：

```bash
node scripts/run-release-publication-gate.mjs
```

顺序是：

1. `tests/release-publication-invariant.test.mjs`；
2. manifest 指向的 R0.73C mathematical gate；
3. `tests/r073c-release.test.mjs`；
4. `scripts/add-r073c-translations.mjs --check-only`；
5. `tests/site-route-current-boundary.test.mjs`；
6. `tests/internal-public-links.test.mjs`；
7. `tests/bilingual-content.test.mjs`；
8. `tests/release-publication-gate-runner.test.mjs`。

### 9.3 当前 runner 的覆盖缺口

R0.73B 的 source-stage contract 声明了 `certificateSourceTest` 和
`figureSourceTest`，但 `scripts/run-release-publication-gate.mjs` 当前只执行
main mathematical gate 与 publication test，并不会自动执行这两个独立
source test。R0.73C 不能把“文件存在”误报成“CI 已执行”。有两种可靠做法：

1. 把 certificate/figure source assertions 并入 R0.73C main gate 或
   publication test；或
2. 扩展 manifest/runner，让它显式解析并执行附加 source tests，同时更新
   `tests/release-publication-gate-runner.test.mjs` 和两个 GitHub workflow 的
   runner contract。

在 runner 扩展完成前，至少必须显式运行：

```bash
node --test tests/r073c-deterministic-certificate-source.test.mjs
node --test tests/r073c-<figure>-figure-source.test.mjs
```

## 10. 推荐发布顺序

1. 冻结最终数学结论、claim IDs、figure ID 和下一问题 R0.73D。
2. 完成 report、proof、literature、gap matrix、independent audit 和测试源。
3. 所有 source-stage 路径存在后再声明 `nextReleaseSourceStage`；确认 live
   counters 仍停在 R0.73B。
4. 运行 experiment 与独立 validator，保留 progress、raw data、manifest、
   hashes。
5. 形成绑定源文件的 commit；生成 source-stage certificate，再生成 formal
   certificate 并验证。
6. 形成 certificate commit；生成 formal figure、完成视觉 QA、验证 archive，
   复制 byte-identical public masters。
7. 以 v1.42/R0.73B 为 exact baseline 运行
   `scripts/generate_r073c_release.py`，生成 note/recap 并更新 home、literature、
   manifests 和 cache tags。
8. 本地服务页面，生成 note PDF 与 recap PDF，做视觉检查。
9. 在 PDF 存在后生成 `public/notes/index.html`，再运行 `--check`。
10. 冻结 R0.73C i18n snapshot，生成 `translations/en.json` 和
    `public/i18n-en.js`，运行 `--check-only`。
11. 运行两个独立 source tests、canonical publication runner、
    `python3 scripts/audit_public_site.py --json` 与 `git diff --check`。
12. 仅当所有门通过后提交并推送；Pages workflow 会再次运行同一 publication
    runner，随后把 `public/` 发布到 `https://kasifa.github.io/`。

## 11. 最终发布 QA 清单

- [ ] `VERSION`、manifest、site-version、home、literature、latest note、latest
      recap、note index 的版本与 cache query 一致。
- [ ] R0.73C HTML/PDF 同时存在；总索引显示 179/136/43，C 在第一条。
- [ ] 首页完整路线恰含 179 个唯一 note links；R0.69P 后 current block 为 89。
- [ ] 首页每个 R0.70A+ release 恰有一个 progress card；R0.73C 不重复 note
      route link。
- [ ] recap node index 为 119 个唯一节点，末项 R0.73C；旧 recap 未删除。
- [ ] literature 有直接 R0.73C note link、`r073c-boundary` 和唯一 R0.73D open
      interface。
- [ ] public figure PDF/SVG/PNG 与 formal archive master hash 完全相同。
- [ ] note/recap PDF 不是旧页面缓存，公式、中文字体、页数和内部链接通过。
- [ ] `translations/en.json` 无重复 `id`/`zh`，English 无中文残留，protected
      TeX/URL 和 CLOSED/FALSE/OPEN 顺序不漂移。
- [ ] internal links、fragments、GitHub source links、voice boundary 全通过。
- [ ] C4/C5 若未闭合，页面没有把 conditional super-polynomial no-go 改写成
      theorem，更没有 nonlinear 或 Clay 外推。
