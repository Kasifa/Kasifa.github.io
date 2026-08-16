# Navier–Stokes 开放研究日志

这是我整理三维不可压缩 Navier–Stokes 存在性与光滑性问题的公开研究日志，包括综述、工作计划和计算笔记。

## 当前内容

- Clay 正式问题与尺度临界性
- 全局弱解、局部强解、临界小数据、部分正则性和弱解非唯一性综述
- 截至 2026 年的重要前沿及证据等级
- 分阶段的研究计划与每一步的检查条件
- 第一份研究笔记：周期三维 NS 的临界能量与 Fourier 三波结构
- 第二份研究笔记：dyadic 非局部尾与螺旋三波
- 第三份研究笔记：近对角螺旋核的零点集与精确极值
- 第四份研究笔记：稠密近对角频率包的尺度下界
- 第五份研究笔记：临界频率包的短时失相与频谱泄漏
- 第六份研究笔记：固定注入下的频谱泄漏优化
- 第七份研究笔记：全六模态泄漏下界与 2D3C 调制
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

R0.5 的 Fourier–Galerkin 动力学计算另外需要 Python 3 与 NumPy：

```bash
python3 -m pip install -r requirements-research.txt
python3 research/critical_packet_dynamics.py
python3 research/triad_leakage_variation.py
python3 research/optimized_packet_dynamics.py
python3 research/six_mode_coercivity.py
python3 research/six_mode_modulation.py
python3 research/dense_packet_mode_budget.py
```

## GitHub Pages

项目已包含 `.github/workflows/pages.yml`。详细步骤见
[`GITHUB_PAGES.md`](./GITHUB_PAGES.md)。

## 研究声明

这个项目没有解决 Navier–Stokes 千禧年问题。我在网页中区分：

- 已发表或已复现定理
- 预印本主张
- 条件性结果
- 开放猜想
- 数值证据
- 被算例排除的说法

如果以后得到实质结果，我会写清假设、定义域、解类、证明、版本记录和复现材料。
