# Hitokoto Home Assistant Integration

精选句子集成，定时获取一言API的精选句子。

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://hacs.xyz/docs/faq/custom_repositories)


## 功能特性

- ✅ 支持配置句子分类（动画、漫画、游戏、文学等）
- ✅ 支持自定义更新间隔（分钟、小时、天）

## 安装

将`hitokoto`文件夹复制到Home Assistant的`custom_components`目录下。

## 配置

通过Home Assistant的集成界面添加：

1. 进入 配置 -> 设备与服务
2. 点击 添加集成
3. 搜索 "Hitokoto"
4. 选择分类和更新间隔

## 实体属性

实体提供以下属性：
- `from`: 句子来源
- `from_who`: 作者
- `type`: 类型
- `creator`: 创建者
- `uuid`: 唯一标识符


## 添加卡片
```
type: markdown
content: >
  > {{ states('sensor.hitokoto_yi_yan') }} —— {{
  state_attr('sensor.hitokoto_yi_yan', 'from_who') or '' }}
title: 每日一言

```