---
title: Root教程，但无需刷机包和第三方REC（DSU侧载）
date: 2024-07-27 23:12:19
tags:
- Android搞机
- 刷机
- 技术帖
categories:
- Android刷机
id: post3
cover: https://maxpcimg.cc/i/2024/09/29/66f8cb5c3f890.jpg
banner_img: https://maxpcimg.cc/i/2024/09/29/66f8cb5c3f890.jpg
index_img: https://maxpcimg.cc/i/2024/09/29/66f8cb5c3f890.jpg
---

这是一篇适用于 **无法获取刷机包** 且 **没有第三方REC适配** 的机型的ROOT教程，前提有二：

- 解锁了Bootloader

- Android版本＞9

下面教程开始~



------

# 备份与检查支持情况

### 备份

1. 虽然本教程的操作不需要清除数据，但还是请备份好你的所有重要资料，避免意外情况发生。

### 下载

2. 打开https://www.123pan.com/s/iBeVVv-WZ3V.html 下载安装DSU Sideload和Treble Check；

3. 打开Treble Check，检查你的CPU体系架构与Project Treble支持情况。

   <img src="https://img.picgo.net/2024/07/27/dc70a92ab1db72ab8a1313cf52744511f14510d93ac98d5.jpg" alt="dc70a92ab1db72ab8a1313cf5274451" style="zoom: 33%;" />

   <img src="https://img.picgo.net/2024/07/27/a4965c67c3f79af31b0b4c887726878a046ce43d6a17016.jpg" alt="a4965c67c3f79af31b0b4c887726878" style="zoom: 50%;" />

4. 下载**适合你的**[GSI](https://developer.android.google.cn/topic/generic-system-image?hl=zh-cn)，比较推荐https://sourceforge.net/projects/andyyan-gsi/files ，怎么选择适合你的呢？我们看看文件的命名：
   - *a64* or *arm64*：指的就是你的CPU架构；
   - *v* or *g*：即 *Vanilla* 或 *Google*，*v* 表示没有自带谷歌框架，*g* 表示预置了谷歌框架，这个怎么选取决于你的个人爱好；
   - *S* or *N*：即 *SuperSU* 或 *No SuperSU*，**我们需要超级用户权限，所以选 *S* 的**；
   - *vndklite* or *-*：*vndklite* 适用于VNDKLite设备或非VNDKLite设备上的可读写系统。**如果设备支持Project Treble，选择带 *vndklite* 的，如果不支持Project Treble，应选择不带的**。

   <img src="https://img.picgo.net/2024/07/28/cee3b5cfa2752b07a61125b57fcc17fb8ff0309142aa984.jpg" alt="cee3b5cfa2752b07a61125b57fcc17f" style="zoom: 50%;" />

------

确认您的设备支持DSU侧载，并下载对应镜像文件后后，您可进行下一步。

# 安装并进入系统

### 安装

1. 打开DSU Sideload，点击*设定 - 新建文件夹 - 随便命名 - 允许 - 继续* ；

   ![070758e77e2664f3b0b5d8d3f3c0ad2](https://img.picgo.net/2024/07/28/070758e77e2664f3b0b5d8d3f3c0ad2ee054a610aa13972.jpg)

2. 在软件中设定好镜像路径、空间大小（最低5GB）后点击安装，等待进度条跑完，如下图：

   ![a29978e6f0228ba5c33a5244471395e](https://img.picgo.net/2024/07/27/a29978e6f0228ba5c33a5244471395ecb10bfa955063c9b.jpg)

3. 将手机打开USB调试，连接电脑；
4. 在电脑上打开[adb终端](https://mrzzoxo.lanzoue.com/b02plghuh)，手机上授权调试；
5. 终端中执行下面的命令：

    ```shell
    adb shell sh "/storage/emulated/0/Android/data/vegabobo.dsusideloader/files/install"
    ```
    等待终端中返回信息 `DSU installation activity has been started!` 就安装成功了：
    
    ![38a1d04d33579d06185507487e97413](https://img.picgo.net/2024/07/28/38a1d04d33579d06185507487e97413bf0af4f7ec389e91.jpg)

    没有电脑的话，你也可以使用Termex、Shizuku等进行安装，可进入DSU Sideload点 *查看指令* 获取指令。
    
### 进入系统

6. 等待几秒钟，点击通知中的 *重启* 进入到侧载的系统；

   > 如果卡Fastboot，说明你配置有误或者你的手机不支持DSU，直接长按电源键重启后舍弃即可。

   <img src="https://img.picgo.net/2024/07/28/1e6d8938c1e5a59456f1974a42f1570e717b5b3c3a14109.jpg" alt="1e6d8938c1e5a59456f1974a42f1570" style="zoom:25%;" />

7. 重启完成后，如果进入原系统，就重试；

   如果成功进入侧载系统，就使用数据线连接电脑，电脑打开adb终端；

8. 在adb终端**有序地**执行：

   ```shell
   adb shell
   su
   cd /dev/block/bootdevice/by-name
   ls -l
   ```
   此时，我们应注意列表中 *boot* 或 *init_boot* 镜像的地址，下以 <u>原地址</u> 代称（请忽视图中标号）；

   > 如何选择boot.img或init_boot.img？
   >
   > 内核版本为...androidx-...（x≥13）的机器，修补/刷入/备份的镜像分区应为init_boot，其他的为boot，另外，若您使用APatch，则应该使用boot.

   <img src="https://img.picgo.net/2024/07/28/e752a652645251a82a6805a0025317317f897f3a023eb9c.jpg" alt="e752a652645251a82a6805a00253173" style="zoom: 67%;" />

9. 在电脑上任意位置新建一个文件夹，在adb终端有序执行下面的指令，将镜像拷贝到电脑上：

   ```shell
   dd if=原地址 of=/sdcard/镜像名称.img
   adb pull /sdcard/镜像名称.img D:\aaaa
   ```

   <img src="https://img.picgo.net/2024/07/28/7ce508bf9cc6b0cc604370a5b6db4c8f73e14cfe22c5266.jpg" alt="7ce508bf9cc6b0cc604370a5b6db4c8" style="zoom: 80%;" />

10. 重启返回原系统。

------

目前，我们已经成功获取到了手机的 boot/init_boot 镜像，可以使用[我的教程](https://www.coolapk.com/feed/57221213?shareKey=ODgyYzI3Y2VmZWExNjY4YTg3ZmM~&shareUid=18214705&shareFrom=com.coolapk.market_14.2.3)中的第二步开始进行修补，获取Root权限啦~本篇教程到此结束！

<p align=right>写于2024年7月8日·酷安</p>
