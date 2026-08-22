# 怎么让 GitHub 主页显示出来

GitHub 规定：只有 **用户名同名的公开仓库** 里的 `README.md` 才会出现在个人主页。

你的用户名是 `BigQ749`，所以仓库必须叫 `BigQ749/BigQ749`。

## 1. 把头像换上

仓库里有 `assets/readme/avatar.jpg`（圆形毛笔字「齐」）。

GitHub → Settings → Profile → 上传这张图。

简介可以写成：

```text
硬件能拿在手里。工具能马上跑起来。
```

## 2. 建同名公开仓库并推上去

在本目录执行：

```powershell
cd D:\APP\github-profile-BigQ749
git init
git add .
git commit -m "Add GitHub profile README."
gh repo create BigQ749 --public --source=. --remote=origin --push
```

推上去之后打开 https://github.com/BigQ749 就能看到主页。

不要把仓库改成 private，private 的 profile README 不会显示。

## 3. 本地预览

双击 `preview.html`，或：

```powershell
Start-Process "D:\APP\github-profile-BigQ749\preview.html"
```

改完视觉后重新出图：

```powershell
python D:\APP\github-profile-BigQ749\scripts\render_assets.py
```
