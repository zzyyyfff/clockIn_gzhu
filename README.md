# 广州大学gzhu健康打卡脚本

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [广州大学gzhu健康打卡脚本](#广州大学gzhu健康打卡脚本)
  - [感谢](#感谢)
  - [使用方法](#使用方法)
  - [详细教程(仅供参考，因为用的别人的图)](#详细教程仅供参考因为用的别人的图)

<!-- /code_chunk_output -->

## 感谢

感谢situ2001让我发现了白嫖github action服务器的新思路
[他的项目链接](https://github.com/situ2001/gzhu_no_clock_in)

本来没打算自己写的，主要是因为我用他写的脚本老是打卡失败，，，

那就自己写一个打卡脚本吧，这种重复性的劳动就应该交给自动化来做！

## 使用方法

设置两个repository secrets：XUHAO和MIMA
它们的值分别对应你的学号和密码。

脚本会在每天早上7点自动运行。

## 详细教程(仅供参考，因为用的别人的图)

首先把该项目Fork一份（在网页右上角，点Fork前记得顺便点个Star哦~），然后去到你fork下来的仓库里。

接着，按照如图所示操作。

虽然图中是STUID和STUPWD，但是名称应该设置为 XUHAO 和 MIMA
它们的值分别对应你的学号和密码。

![Setsecrets](/assets/set_secrets.png)

Action会在每日7点运行，如果需要手动运行Action，可根据下图进行操作

图中第二步的workflow的名字是scrape（和图中GZHU Auto Clock In在同一位置）

![Runw workflow](/assets/run_workflow.png)

如果fork下来的仓库在未来需要更新，点击Fetch upstream并fetch and merge即可
