# GitHub Pages 发布说明

这个项目已经包含可直接部署的静态研究站点：

- 网页源文件：`public/research-review.html`
- 自动发布工作流：`.github/workflows/pages.yml`

## 推荐发布方式

1. 在 GitHub 创建仓库：
   - 个人主页：`你的用户名.github.io`
   - 或项目站点：`navier-stokes-research`
2. 把本项目推送到仓库的 `main` 分支。
3. 打开仓库 `Settings → Pages`。
4. 在 `Build and deployment → Source` 中选择 `GitHub Actions`。
5. 打开 `Actions` 页面确认 `Deploy static research site to GitHub Pages` 成功。

个人主页地址为：

```text
https://你的用户名.github.io/
```

项目站点地址通常为：

```text
https://你的用户名.github.io/navier-stokes-research/
```

## 发布前检查

- 填写作者姓名与联系信息。
- 确认所有预印本都明确标注为“预印本”。
- 不要把私人笔记、密钥、未授权论文 PDF 或本地路径提交到公开仓库。
- 建议为正文选择 CC BY 4.0，为代码选择 MIT；在确认前不必添加许可文件。
