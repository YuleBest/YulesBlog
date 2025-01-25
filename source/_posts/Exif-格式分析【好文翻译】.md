---
title: Exif 格式分析【好文翻译】
date: 2025-01-23 06:24:24
tags:
- 技术分析
- 好文翻译
- 好文转载
- 转载
categories:
- 转载
- 技术分析
id: z1
---

> 原标题：「Description of Exif file format」
>
> 原文发布日期：1999 年 5 月 28 日
>
> 原文链接：https://www.media.mit.edu/pia/Research/deepview/exif.html

# Exif 格式分析

目前，大多数新数码相机都使用 Exif 文件格式来存储图像。此规范由 JEIDA 制定，但其并没有公开技术文档，所以我参考互联网上已有的文档，对 Exif 做了一些简单的描述。

我相信这份文档基本上是基于 在 Exif 2.1 规范上，但实际上我没有看过官方规范，对于一些「未知」的项目，它可能需要被勘误。

这是免费文档，您可以将此文档的全部/部分用于任何目的（商业/非商业性）。

<p align="right">TsuruZoh Tachibanaya</p>

---

## 参考资料

- itojun 编写的 [Exif 文件格式](http://www.itojun.org/diary/199610.IWOOOS/exif.html)（日语文档）
- [Exif 文件 Mamoru](http://www.yk.rim.or.jp/~mamo/Computer/DS-7/exif.html) Ohno（日语文档）
- [TIFF6.0](http://partners.adobe.com/asn/developer/PDFS/TN/TIFF6.pdf) Adobe
- [TIFF/EP 编写的规范](http://www.pima.net/standards/iso/standards/documents/N4378.pdf) ISO TC42 WG18
- [exifdump](http://topo.math.u-psud.fr/~bousch/exifdump.py) 程序编写的规范，作者 Thierry Boush

---

## 什么是 Exif 文件格式？

基本上，Exif 文件 格式与 JPEG 文件格式相同。Exif 插入一些 image/digicam 信息数据和缩略图图像，然后根据 JPEG 转换为 JPEG 规范。因此，您可以通过 JPEG 兼容查看 Exif 格式的图像文件。

---

## JPEG 格式和标志

JPEG 文件都是以十六进制 `0xFFD8` 开始，以 `0xFFD9` 结束。在JPEG数据中有像 `0xFF**` 这样的数据，这些被称为「标志」，它表示 JPEG 信息数据段。`0xFFD8` 表示 SOI *（Start of image，图像开始）* ，`0xFFD9` 表示 EOI *（End of image，图像结束）* 。

这两个特殊的标志没有附加的数据，而其他的标志在标志后都带有附加的数据。基本的标志格式如下：

**0xFF + 标志数字（1 字节） + 数据大小（2 字节） + 数据（n 字节）**

数据大小  (2 字节) 是大端顺序表示（Motorola 方式），从高字节开始。请注意，「数据」包含了数据大小的描述，如果一个标志为：

```
FF C1 00 0C
```

则表示标志 `0xFFC1` 有 `0x000C`（十进制 `12`）个字节的数据，但是数据的大小 `12` 也包含了记录「数据大小」的字节，所以在 `0x000C` 后面只有 10 个字节的数据量。

在 JPEG 格式中，一些标志描绘数据后，跟着的就是 SOS *（Start of stream，数据流开始）* 标志。在 SOS 标志之后，就是 JPEG 图像流，直到 EOI 标志结束。

![](https://maxpcimg.cc/i/2025/01/23/679178b9e8a02.jpg)

---

## Exif 使用的标志

从 `0xFFE0` ~ `0xFFEF` 的标志是「APP 标志」，在解码 JPEG 图像的时候不是必需使用的。这些标志被用在用户应用中。例如：老款的奥林巴斯、佳能、卡西欧、爱克发的数码相机使用 JFIF *（JPEG档案交换格式）* 来存储相片的。JFIF 是使用 `APP0 (0xFFE0)` 标志来插入数码相机的配置数据和缩略图的。 

Exif也使用 APP 标志来插入数据，但是 Exif 使用 `APP1(0xFFE1)` 标志以避免和 JFIF 格式冲突。每个 Exif 文件格式都是从下面格式的内容开始的：

![](https://maxpcimg.cc/i/2025/01/23/67917a98c8022.png)

从 SOI（`0xFFD8`）标志开始，所以这是一个 JPEG 文件。后面随即跟着个一个 `APP1` 标志。所有的 `Exif` 数据都储存在 `APP1` 数据区中。在上表中的 `SSSS` 部分表示 `APP1` 数据 Exif 数据区域的大小。请注意，关于 `SSSS` 大小的描述包括 `SSSS` 本身。

APP1的数据从 `SSSS` 后开始。第一部分是特殊数据，使用ASCII字符「Exif」和两个字节的 `0x00` ，它定义了是否使用 Exif。

APP1标志数据之后，是其他JPEG标志。

---

## Exif 数据结构

Exif 数据的大致结构 （`APP1`） 如下所示。它采用了 Intel 的小端字节顺序方案，它包含 JPEG 格式缩略图。如上所述，Exif 数据是从 ASCII 字符「Exif」 和 2 字节的 `0x00`，Exif 数据紧随其后。Exif 使用 TIFF 规范来存储数据。更多 TIFF 格式的数据请参考 [TIFF 6.0 规范](https://www.itu.int/itudoc/itu-t/com16/tiff-fx/docs/tiff6.pdf)。

![](https://maxpcimg.cc/i/2025/01/23/67917e54ebe6b.png)

### TIFF 头的格式

TIFF 头指的是 TIFF 格式的前 8 个字节。前 2 个字节定义了 TIFF 数据采用何种字节顺序。如果是 `0x4949 (II)`，表示采用 Intel 的小端字节顺序；如果为 `0x4d4d (MM)`，表示采用 Motorola 的大端字节顺序。例如：值 305,419,896，用十六进制表示为 `0x12345678`，在 Motorola 的大端字节顺序中以 `0x12 0x34 0x56 0x78` 的顺序存储；如果采用 Intel 的小端字节顺序，则以 `0x78 0x56 0x34 0x12` 的顺序存储。

*现在来看，大多数数码相机采用 Intel 的方式。理光采用了 Motorola 的方式，索尼除了 D700 都采用 Intel 的的字节顺序，柯达 DC200/210/240 采用 Motorola 方式，但是 DC220/260 PowerPC 却采用了 Intel 的方式，因此我们在获取 Exif 数据时，必须每次都确认它的字节顺序。虽然 JPEG 数据只采用 Motorola 方式的字节顺序，但 Exif 却允许采用两种方式。我不明白为什么 Exif 不修改字节顺序为 Motorola 方式。*

然后的两个字节总是 2 个字节长度的 `0x002A`。如果数据采用Intel的字节顺序，这两个字节为 `0x2A 0x00`。如果采用 Motorola 的字节顺序，则为 `0x00 0x2A`。TIFF 头的最后 4 个字节是第一个 IFD  *（Image File Directory, described in next chapter，图像文件目录，描述下一个字符）* 的偏移量。在 TIFF 格式中，所有的偏移量都是从 TIFF 头的第 1 个字节（`II` 或者 `MM`）开始计算到所在位置的字节数目，这个偏移量也不例外。通常第一个 IFD 是紧跟在 TIFF 头后面的，所以它的偏移量为 `0x00000008`。

![](https://maxpcimg.cc/i/2025/01/23/67918135d788c.png)

### IFD：图像文件目录 (Image file directory)

接着 TIFF 头的是第一个 IFD。它包含了图像信息数据。在下表中，开始的两个字节 `EEEE` 表示这个 IFD 所包含的目录实体数量。然后紧跟着就是实体对象（每个实体 12 个字节）。在最后一个目录实体后面有一个 4 字节大小的数据（表中的是 `LLLLLLLL`），它表示下一个 IFD 的偏移量。如果这个偏移量的值是 `0x00000000`，就表示这个 IFD 是最后一个 IFD。

![](https://maxpcimg.cc/i/2025/01/23/679182856cc12.png)

上表中的 `TTTT`（2 字节）是标签号，代表各种数据。`ffff`（2 字节）是数据格式。`NNNNNNNN`（4 字节）是组成元素的数量。`DDDDDDDD`（4 字节） 包含数据本身或者数据的偏移量。

### 数据格式

数据格式（上表中的 `ffff`）如下表所定义的一样。rational 表示一个分数，它包含 2 个 signed / unsigned long integer 值，并且第 1 个为分子，第 2 个为分母。

![](https://maxpcimg.cc/i/2025/01/23/679184f357096.png)

你可以用组成元素的字节数的值乘以储存在 `NNNNNNNN` 区域中的组成元素的排序号（即元素数量）得到数据总长度。如果这个总长度小于 4 字节，那么 `DDDDDDDD` 中的是这个标签 *（Tag）* 的值。如果总长度大于等于 4 个字节，则 `DDDDDDDD` 中的是数据存储地址的偏移量。

### IFD 的数据结构

在Exif格式中，第一个 IFD 是 IFD0 *（主图像的IFD）* ，它链接着 IFD1 *（缩略图的 IFD）* 后 IFD 链终止。带式 IFD0 / IFD1 不包含像快门速度，焦距等任何数码相机的信息。IFD0 总是包含一个特殊的标签 `0x8769`，它代表着 Exif  SubIFD *（子 IFD）* 的偏移量。Exif SubIFD *（子IFD）* 也是 IFD 的格式，它包含了数码相机的信息。

Exif 格式的扩展方案 *（Exif2.1/DCF）* 中，Exif SubIFD 包含了特殊标签：Exif 互用偏移量 *（Exif Interoperability Offset）* （`0xA005`）。它指向互用的 IFD（Interoperability IFD）。在DCF *（数码相机格式）* 规范中，这个标签是必须的，且子 IFD0 和 IFD1 都可以使用互用的 IFD *Interoperability IFD）* 。通常，只有主图像带有这个标签。

一些数码相机使用 IFD 数据格式来表示制造商数据——制造商特殊的神秘数字区。要小心的编写程序，因为很难区分制造商数据是否使用了IFD格式。附录中有一些制造商数据的信息。

TIFF 数据的第一部分可以读取为：

```text
0000: 49 49 2A 00 08 00 00 00-02 00 1A 01 05 00 01 00
0010: 00 00 26 00 00 00 69 87-04 00 01 00 00 00 11 02
0020: 00 00 40 00 00 00 48 00-00 00 01 00 00 00
```

- 前 2 个字节是 `II`，字节对齐使用 Intel。
- 地址 `0x0004~0x0007` 为 `0x08000000`，IFD0 从地址 `0x0008` 开始
- 地址 `0x0008~0x0009` 为 `0x0200`，IFD0 的目录条目数为 2.
- 地址 `0x000a~0x000b` 为 `0x1A01`，则表示这是一个 XResolution（`0x011A`） 标签，它包含图像的水平分辨率。
- 地址 `0x000c~0x000d` 为 `0x0500`，该值的格式为 unsigned rational（`0x0005`） 的。
- 地址 `0x000e~0x0011` 为 `0x01000000`，元素数量为 1。无符号 Rational 的数据大小为 8 字节/组件，因此总数据长度为 8 字节。
- 总数据长度大于 4 字节，因此接下来的 4 字节包含一个偏移量的数据。
- 地址 `0x0012~0x0015` 为 `0x26000000`，XResolution 数据存储到地址 `0x0026`。
- 地址 `0x0026~0x0029` 为 `0x48000000`，分子为 72，地址 `0x002a~0x002d` 为 `0x0100000000`，分母为 1。所以 XResoultion 的价值 是 72/1。
- 地址 `0x0016~0x0017` 为 `0x6987`，下一个 Tag 为 Exif Offset（`0x8769`）。它的价值 是 Exif SubIFD 的偏移量
- 数据格式为 `0x0004`，无符号长整数。
- 此 Tag 有一个组件。unsigned long integer 的数据大小为 4 字节/组件，因此总数据大小为 4 字节。
- 总数据大小等于 4 字节，接下来的 4 字节包含 Exif SubIFD 的偏移值。
- 地址 `0x001e~0x0021` 为 `0x11020000`，Exif SubIFD 从地址 `0x0211` 开始。
- 这是最后一个目录条目，接下来的 4 个字节显示到下一个 IFD 的偏移量。
- 地址 `0x0022~0x0025` 为 `0x40000000`，下一个 IFD 从地址 `0x0040` 开始。

### 缩略图

Exif 格式包含 图像（理光 RDC-300Z 除外）。通常它位于 IFD1 旁边。有 3 种缩略图格式;JPEG 格式（JPEG 使用 YCbCr）、RGB TIFF 格式、YCbCr TIFF 格式。

#### JPEG 格式缩略图

如果 IFD1 中 Compression（`0x0103`） Tag 的值为 6，则缩略图格式为 JPEG。 大多数 Exif 图像使用 JPEG 格式作为缩略图。在这种情况下，您可以获得 IFD1 中 JpegIFOffset（`0x0201`） 包含的缩略图的偏移量，大小为 thumbnail 替换为 JpegIFByteCount（`0x0202`）标签。数据格式为普通 JPEG 格式，从 `0xFFD8` 开始，到 `0xFFD9` 结束。看起来 JPEG 格式和 160 * 120 像素的大小是 Exif 2.1 的推荐缩略图格式。

#### TIFF 格式缩略图

如果 IFD1 中 Compression（`0x0103`）Tag 的值为 1，则缩略图格式为 no compression（TIFF 格式）。缩略图数据的起点是 StripOffset（`0x0111`）Tag，缩略图的大小是 StripByteCounts（`0x0117`）Tag 的总和。

如果缩略图不使用压缩，并且 IFD1 中的 PhotometricInterpretation（0x0106）Tag 的值为 2，则缩略图使用 RGB 格式。在这种情况下，您只需复制数据即可查看缩略图或转换为计算机的 RGB 格式（如 BMP 格式，或复制到 VRAM 目录），柯达 DC-210/220/260 使用此格式。

如果该标签的值为 6，则 thumbnail 使用 YCbCr 格式。如果要查看缩略图，则必须将其转换为 RGB。理光 RDC4200/4300、Fuji DS-7/300 和 DX-5/7/9 使用此格式（较新的 RDC5000/MX-X00 系列使用 JPEG）。下一节是 Fuji DS 转换的简要说明 缩略图。有关更多详细信息，请参阅 [TIFF 6.0 规范](https://www.itu.int/itudoc/itu-t/com16/tiff-fx/docs/tiff6.pdf)。

在 DX-5/7/9 时，YCbCrSubsampling（`0x0212`） 的值为 `2,1`，PlanarConfiguration（`0x011c`） 的值为 `1`。所以此处的数据是一致的，如下：

```
Y（0,0），Y（1,0），Cb（0,0），Cr（0,0）， Y（2,0），Y（3,0），Cb（2,0），Cr（3.0），Y（4,0），Y（5,0），Cb（4,0），Cr（4,0）. . . .
```

这 括号中的数字是像素坐标。DX 系列 YCbCrCoefficients（`0x0211`） 的值为 `0.299/0.587/0.114`， ReferenceBlackWhite（`0x0214`） 的值为 `0,255,128,255,128,255`。因此，要从 Y/Cb/Cr 转换为 RGB 的运算为：

```
B(0,0)=(Cb-128)*(2-0.114*2)+Y(0,0)
R(0,0)=(Cr-128)*(2-0.299*2)+Y(0,0)
G(0,0)=(Y(0,0)-0.114*B(0,0)-0.299*R(0,0)))/0.587
```

---

## Exif/TIFF 中使用的标签号
Exif/TIFF 中使用的标签号如下所示。如果标签的元素数量有限制，则 CompoNo 列就是最大允许的元素个数，如果 CompoNo 列为空，代表没有限制。

您可以 [下载表格](https://d.feiliupan.com/t/40879326941417472/表格/表格157313.xlsx)

![](https://maxpcimg.cc/i/2025/01/23/67919425baf16.png)