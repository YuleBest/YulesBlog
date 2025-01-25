---
title: Android部分机型修改开机第一屏logo
date: 2024-10-22 01:09:47
tags:
- Android搞机
- 刷机
- 技术帖
categories:
- Android刷机
id: post14
cover: https://maxpcimg.cc/i/2024/10/22/6716bada8b5a5.png
banner_img: https://maxpcimg.cc/i/2024/10/22/6716bada8b5a5.png
index_img: https://maxpcimg.cc/i/2024/10/22/6716bada8b5a5.png
---
# Android 部分机型修改开机第一屏

[TOC]

------

## 0	确认手机系统版本

**有以下情况之一的不可以修改**

- 手机系统 OS 为 MIUI 13 以及 MIUI 13 以上版本的（包括澎湃）

  手机为小米 10s 或红米 K40 之后发布的机型

  - 小米在上述版本系统/机型中为 logo / splash 分区添加了签名验证

- 不能解锁 Bootloader 锁（BL 锁）的
  - 修改系统分区需要解锁 BL

- 其余未列出情况请自测

------

## 1	解锁

首先你需要将手机的 BL 锁进行解锁，最好可以获取 Root 权限

------

## 2	备份 logo 或 splash 分区镜像文件

### 2.1	方法 1：Root 提取法

1. 将手机 Root

2. 在手机上下载安装 [MT 管理器](https://mt2.cn/)

3. 下载 [我制作的脚本](https://www.123684.com/s/iBeVVv-KqhV)

4. 打开 MT 管理器，使用 Root 权限执行脚本

   <img src="https://maxpcimg.cc/i/2024/10/22/67168e5e03cd2.jpg" style="zoom:33%;" />

6. 观察下图界面，是否有 logo 或 splash 分区

    <img src="https://maxpcimg.cc/i/2024/10/22/67168e72d853e.jpg" style="zoom: 25%;" />
    
    - 如果只有 logo 分区，请按照下文 logo 分区教程操作
    
    - 如果只有 splash 分区，请按照下文 splash 分区教程操作

### 2.2	方法 2：系统包提取法

如果你有你的机器正在运行的系统的系统包，那么你可以使用该方法

1. 解压系统包

2. 观察系统包内是否有 logo 或 splash 分区

    - 如果只有 logo 分区，请按照下文 logo 分区教程操作
    
    - 如果只有 splash 分区，请按照下文 splash 分区教程操作

------

## 3	logo 分区教程

### 3.1	提取分区

1. 在脚本中输入

   ```
   logo
   n
   ```

    脚本会把 logo 分区的镜像文件（`logo.img`）保存到 `/sdcard/` 下

2. 将 `logo.img` 复制一份到电脑上

### 3.2	镜像文件的操作

##### 3.2.0	一些理论知识（可以不看）

1. 修改的原理

   `logo.img` 里面包含了几个 `.bmp` 文件，这些就是手机开机的时候要显示的图片，其中就包含我们需要的 logo。那要怎么修改呢？你或许会说直接解包，但是大部分时候解包工具是无法解包 Android 7 的 `logo.img` 的，我们需要一种通用的解决方式——**直接修改文件的 16 进制值**。

2. 实践

   首先，IMG 文件的 16 进制值里面会包含 bmp 图片的偏移地址，我们只需要找到这个偏移地址，然后把图片部分截取出来，就可以实现提取了。

   我们知道，BMP 图片开头两个字节是固定的 `42 4D`（也就是 `BM`），紧接着四个字节就是整个图片的大小（Little-Endian），在 UE 编辑器用 `dd` 命令可以很容易地把图片截出来。

   > 参见：[BMP 格式详解](https://www.cnblogs.com/wainiwann/p/7086844.html)

   但是每次都这样找会很麻烦，所以我准备了配置文件，这样就可以方便的进行替换了，详见下文。

##### 3.2.1	下载配置文件以及工具

0. 下载链接：https://www.123684.com/s/iBeVVv-lqhV

1. 解压你下载的工具包，你应该可以看到 `dist` 和 `配置文件` 两个文件夹

   ![](https://maxpcimg.cc/i/2024/10/22/6716af78e3a64.png)

2. 打开 `dist/` ，里面有 5 个 `bmp` 文件还有 1 个 `exe` 文件，那些 `bmp` 文件就是你以后要使用的开机画面

   ![](https://maxpcimg.cc/i/2024/10/22/6716af79a7efe.png)

3. 其中：
   - `1.bmp`：手机开机时显示的 logo，只会显示 1 秒不到的时间，接下来会显示 `4.bmp`
   - `2.bmp`：手机进入 FASTBOOT 模式时显示的 logo
   - `3.bmp`：手机进入缺电状态时显示的 logo
   - **`4.bmp`：手机开机时第一屏显示的图片，我们主要需要修改这个图片**
   - `5.bmp`：手机系统损坏时显示的图片

4. 编辑图片

    > 这里只展示 `4.bmp` 的修改

    - 首先你需要找一张你喜欢的图片，然后看看他的分辨率是多少，如果与你手机的分辨率不一致，就按照下面进行修改，如果一致就直接进行下一步

    - 使用画图打开图片，点击重新调整大小，设置为你手机的分辨率

    ![](https://maxpcimg.cc/i/2024/10/22/6716b7cf33f51.png)

    ![](https://maxpcimg.cc/i/2024/10/22/6716b7ce8205b.png)

    - 使用选择工具调整中间的 logo 的位置，大小和比例

    <img src="https://maxpcimg.cc/i/2024/10/22/6716b7ce53ccb.png" style="zoom: 80%;" />

    - 使用填充工具填充黑色到图片中空白的部分

    <img src="https://maxpcimg.cc/i/2024/10/22/6716b7cddc2f4.png" style="zoom:80%;" />

    - 另存为图片为 `4.bmp`

    ![](https://maxpcimg.cc/i/2024/10/22/6716b94a5dd7f.png)

    - 使用新的 `4.bmp` 替换工具里的 `4.bmp`

    ![](https://maxpcimg.cc/i/2024/10/22/6716b9b0f3a4f.png)

5. 生成新的镜像文件

    - 在 配置文件 文件夹里找到你的机型（如果没有，见下文生成教程）

    - 将配置文件拖动到 `genlogo.exe`

      ![](https://maxpcimg.cc/i/2024/10/22/6716bada8b5a5.png)

    - 等待片刻，脚本会在 `配置文件/` 文件夹里生成一个 `new_logo.img`

      ![](https://maxpcimg.cc/i/2024/10/22/6716bb6d4ac2f.png)

6. 刷入镜像

    - 将 `new_logo.img` 移动到手机上

    - 在手机上下载安装工具箱，授权 ROOT https://npm.elemecdn.com/staticdn@latest/lasystools/latools.apk

    - 点击工具箱左侧的分区管理

      <img src="https://maxpcimg.cc/i/2024/10/22/6716bc7d3504f.png" style="zoom: 25%;" />

    - 找到 logo 分区，点击它，然后点击刷入镜像

      <img src="https://maxpcimg.cc/i/2024/10/22/6716bc991d606.png" style="zoom:33%;" />

    - 选择 `new_logo.img` ，刷入重启即可

至此，修改完毕！

------


## 4	splash 分区教程

由于老板的手机是 logo 分区的，所以这部分内容以后更新。。
