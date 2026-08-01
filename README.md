# Navier–Stokes 开放研究日志

三维不可压缩 Navier–Stokes 存在性与光滑性问题的中文研究综述、可审计攻关计划与持续公开研究档案。

## 当前内容

- Clay 正式问题与尺度临界性
- 全局弱解、局部强解、临界小数据、部分正则性和弱解非唯一性综述
- 截至 2026 年的重要前沿及证据等级
- 七阶段研究计划与每一阶段的通过/停止条件
- 第一项研究任务：周期三维 NS 的临界能量与 Fourier 三波结构
- GitHub Pages 自动发布配置

静态 HTML 主文件位于：

```text
public/research-review.html
```

## 本地运行

需要 Node.js 22.13 或更高版本和 pnpm。

```bash
pnpm install
pnpm dev
pnpm test
```

## GitHub Pages

项目已包含 `.github/workflows/pages.yml`。详细步骤见
[`GITHUB_PAGES.md`](./GITHUB_PAGES.md)。

## 研究声明

本项目不声称已经解决 Navier–Stokes 千禧年问题。网页严格区分：

- 已发表或已复现定理
- 预印本主张
- 条件性结果
- 开放猜想
- 数值证据
- 已否定命题

任何实质结果都应给出完整假设、定义域、解类、证明、版本记录和可复现材料。
