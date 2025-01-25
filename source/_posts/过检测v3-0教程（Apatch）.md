---
title: 过检测v3.0教程（Apatch）
date: 2024-08-02 23:34:45
tags:
- Android搞机
- 刷机
- 技术帖
categories:
- Android刷机
id: post5
cover: https://maxpcimg.cc/i/2024/09/29/66f8cb593bbd6.jpg
banner_img: https://maxpcimg.cc/i/2024/09/29/66f8cb593bbd6.jpg
index_img: https://maxpcimg.cc/i/2024/09/29/66f8cb593bbd6.jpg
---
本期教程是过检测教程，可以过 Native Test 25 和密钥认证 1.6 联网版的测试，效果如图：

![8e721a0b226cd2d1fa45f7f137315fa](https://img.picgo.net/2024/08/03/8e721a0b226cd2d1fa45f7f137315fa8e8511c021c5025a.jpg)

要求如下：

- 解锁 Bootloader
- 已刷入 Apatch 任意版本

本期的所有资源都会打包放在云盘里：https://cloud.189.cn/t/zyAbEzyU7NBn  （访问码<u>tdn6</u>）

下面教程开始。

------

## 安装、配置Bata版Apatch

### 安装

1. 打开云盘链接，下载压缩包并解压，文件目录如下
   > - Apatch 最新测试版和内核模块:
   >   	APatch10884 美化版.apk（来自[@酒次不会搞机](http://www.coolapk.com/u/24024215)）
   >   	cherish_peekaboo_1.4.2.kpm
   >
   > - LSPosed模块:
   >		隐藏应用列表_3.2.apk
   >
   > - 检测应用:
   >   	Applist Detector_2.4.apk'
   >   	Holmes_1.0.apk
   >   	Hunter_5.5.0.apk
   >   	Momo_4.4.1.apk
   >   	Native Test_Sad Minotaur_25.apk'
   >   	Ruru_1.1.1.apk
   >   	密钥认证_1.6.0（联网版）.apk
   >   	强度排行榜.txt
   >
   > - 系统模块:
   >   	LSPosed-1.9.3 去日志.zip
   >   	Tricky-Store-3.7.zip
   >   	Zygisk-Next-1.1.0-330-a1b0e69-release.zip
   >   	keybox.xml
   
2. 在文件管理器点击其中的 *APatch10884 美化版.apk* 进行安装

### 配置

3. 进入 Apatch，点击更新，设置好密钥后，点击**嵌入模块**，选择 *cherish_peekaboo_1.4.2.kpm* ，点击开始修补

   <img src="https://img.picgo.net/2024/08/02/APca3bd436b4c98c95.gif" alt="AP" style="zoom: 50%;" />

4. 重启手机



------



## 安装、配置模块

### 安装

1. 按顺序在 Apatch - 底栏 - 系统模块中安装以下模块：
   - *Zygisk-Next-1.1.0-330-a1b0e69-release.zip*
   - *LSPosed-1.9.3 去日志.zip*
   - *Tricky-Store-3.7.zip*

2. 重启手机

3. 打开通知，点击 LSPosed 的通知进入管理器，点击底栏的设置，关闭状态通知，点击创建快捷方式，关闭 Xposed API 调用保护

   <img src="https://img.picgo.net/2024/08/03/077d9ee925b2ebdfb77946f888bbc3798d3660fa63d0347.jpg" alt="077d9ee925b2ebdfb77946f888bbc37" style="zoom:33%;" />

4. 打开文件管理，安装 *隐藏应用列表_3.2.apk* ，打开隐藏应用列表

5. 重启手机

### 配置

6. 打开 MT 管理器，将把 *keybox.xml* 复制到 /data/adb/tricky_store/ （替换掉原来的）
7. 打开隐藏应用列表，点击<u>模板管理</u>，点击<u>创建白名单模板</u>，点击第一个<u>编辑列表</u>，随便选择一个无风险的应用，返回，点击第二个<u>编辑列表</u>，选择 *Applist Detector、Holmes、Native Test、Ruru* 和你需要过检测的应用
8. 打开一遍 Apatch



------



## 检查效果

1. 安装
   - *Applist Detector_2.4.apk'*
   - *Holmes_1.0.apk*
   - *Hunter_5.5.0.apk*
   - *Momo_4.4.1.apk*
   - *Native Test_Sad Minotaur_25.apk'*
   - *Ruru_1.1.1.apk*
   - *密钥认证_1.6.0（联网版）.apk* （需要挂梯子）
2. 打开各检测软件，根据没过的提示判断进行操作

