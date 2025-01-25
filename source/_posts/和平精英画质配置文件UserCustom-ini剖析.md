---
title: 和平精英画质配置文件UserCustom.ini剖析
date: 2025-01-20 13:09:50
id: post16
tags:
- Android搞机
- Shell
cover: https://maxpcimg.cc/i/2025/01/20/678deb163c6ae.jpg
banner_img: https://maxpcimg.cc/i/2025/01/20/678deb163c6ae.jpg
index_img: https://maxpcimg.cc/i/2025/01/20/678deb163c6ae.jpg
---

# 和平精英画质配置文件 UserCustom.ini 剖析

`UserCustom.ini`，俗称 `UC`，直译为「用户配置」，修改和平精英画质选项主要靠的就是修改这个文件。本篇文章，我将会带你了解这个文件的基本结构、加密方式，以及如何解密修改这个文件。

## 基本结构

> 以下内容均使用用户 0 即主应用作演示

如果你安装了和平精英，你可以在 `/storage/emulated/0/Android/data/com.tencent.tmgp.pubgmhd/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/Config/Android/UserCustom.ini` 找到这个配置文件，文件为 [INI 格式](www.gy328.com/ref/docs/ini.html)，遵守了 INI 格式的基本规范，但对部分内容做了加密。

打开这个文件，你会看到这样的结构：

```ini
[UserCustom DeviceProfile]
+CVars=0B57292C3B3E3D1C0F101A1C3F292A35160E444F
+CVars=0B57292C3B3E3D1C0F101A1C3F292A34101D444F
+CVars=0B57292C3B3E3D1C0F101A1C3F292A31101E11444F
+CVars=0B572C0A1C0B31101E112B1C0A16150C0D1016172A1C0D0D10171E4449
# 以上选项不一定相同，还有更多未列出...
[BackUp DeviceProfile]
+CVars=0B57292C3B3E3D1C0F101A1C3F292A35160E444F
+CVars=0B57292C3B3E3D1C0F101A1C3F292A34101D444F
+CVars=0B57292C3B3E3D1C0F101A1C3F292A31101E11444F
+CVars=0B572C0A1C0B31101E112B1C0A16150C0D1016172A1C0D0D10171E4449
# 以上选项不一定相同，还有更多未列出...
```

如果你没有使用工具修改过画质选项，那么这里的 `UserCustom DeviceProfile` 部分和 `BackUp DeviceProfile` 应当是相同的，下简称「配置部分」和「备份部分」。

---

## 加密解密方式

### 配置部分

我们先分析一下配置部分。

这部分第一行会有一个[节](https:# zh.wikipedia.org/wiki/INI%E6%96%87%E4%BB%B6)：`[UserCustom DeviceProfile]` 来做标志，随后是固定的 `+CVars=...` 格式，这里的 `...` 实际上是经过 16 进制转换后再进行简单[替换加密](https:# baike.baidu.com/item/%E6%9B%BF%E6%8D%A2%E5%BC%8F%E5%AF%86%E7%A0%81/10197380)的产物。密文的每两个字符可以对应为明文的一个字符。

经过分析，我们得到了这个映射表：

```shell
["明文"]="密文"
["A"]="38" ["a"]="18" ["B"]="3B" ["b"]="1B" ["C"]="3A" ["c"]="1A" ["D"]="3D" ["d"]="1D"
["E"]="3C" ["e"]="1C" ["F"]="3F" ["f"]="1F" ["G"]="3E" ["g"]="1E" ["H"]="31" ["h"]="11"
["I"]="30" ["i"]="10" ["J"]="33" ["j"]="13" ["K"]="32" ["k"]="12" ["L"]="35" ["l"]="15"
["M"]="34" ["m"]="14" ["N"]="37" ["n"]="17" ["O"]="36" ["o"]="16" ["P"]="29" ["p"]="09"
["Q"]="28" ["q"]="08" ["R"]="2B" ["r"]="0B" ["S"]="2A" ["s"]="0A" ["T"]="2D" ["t"]="0D"
["U"]="2C" ["u"]="0C" ["V"]="2F" ["v"]="0F" ["W"]="2E" ["w"]="0E" ["X"]="21" ["x"]="01"
["Y"]="20" ["y"]="00" ["Z"]="23" ["z"]="03" ["."]="57" ["0"]="49" ["1"]="48" ["2"]="4B"
["3"]="4A" ["4"]="4D" ["5"]="4C" ["6"]="4F" ["7"]="4E" ["8"]="41" ["9"]="40" ["="]="44"
```

有了这个表，我们就可以干很多事情了。首先我们随机选取一行进行分析验证：

```ini
+CVars= 0B 57 29 2C 3B 3E 3D 1C 0F 10 1A 1C 3F 29 2A 31 10 1E 11 44 4F  #密文
+CVars= r  .  P  U  B  G  D  e  v  i  c  e  F  P  S  H  i  g  h  =  6   #明文
```

我们得到了结果 `CVars=r.PUBGDeviceFPSHigh=6`，这就是和平精英画质配置文件的其中一项。但是这么多内容如果全靠人去转换，肯定是不可行的，所以，一系列「画质助手」就应运而生了，他们可以利用手机的算力来进行解密。我没有这个技术力，所以只能写一个简单的 Shell Bash 解密脚本：

```bash
input_file="/storage/emulated/0/Android/data/com.tencent.tmgp.pubgmhd/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/Config/Android/UserCustom.ini"
output_file="UC_解密.ini"

declare -A encryptMap=(
        ["A"]="38" ["a"]="18" ["B"]="3B" ["b"]="1B" ["C"]="3A" ["c"]="1A" ["D"]="3D" ["d"]="1D"
        ["E"]="3C" ["e"]="1C" ["F"]="3F" ["f"]="1F" ["G"]="3E" ["g"]="1E" ["H"]="31" ["h"]="11"
        ["I"]="30" ["i"]="10" ["J"]="33" ["j"]="13" ["K"]="32" ["k"]="12" ["L"]="35" ["l"]="15"
        ["M"]="34" ["m"]="14" ["N"]="37" ["n"]="17" ["O"]="36" ["o"]="16" ["P"]="29" ["p"]="09"
        ["Q"]="28" ["q"]="08" ["R"]="2B" ["r"]="0B" ["S"]="2A" ["s"]="0A" ["T"]="2D" ["t"]="0D"
        ["U"]="2C" ["u"]="0C" ["V"]="2F" ["v"]="0F" ["W"]="2E" ["w"]="0E" ["X"]="21" ["x"]="01"
        ["Y"]="20" ["y"]="00" ["Z"]="23" ["z"]="03" ["."]="57" ["0"]="49" ["1"]="48" ["2"]="4B"
        ["3"]="4A" ["4"]="4D" ["5"]="4C" ["6"]="4F" ["7"]="4E" ["8"]="41" ["9"]="40" ["="]="44"
) # 解密映射表定义

rm -f $output_file"
cp $input_file /data/local/tmp/tmp.ini
local input_file="/data/local/tmp/tmp.ini"
sed -i '/.BackUp.*/,$d' $input_file

while IFS= read -r line; do
	if [[ $line == +CVars=* ]]; then
		prefix="+CVars="
        encrypted_part="${line#$prefix}"
        decrypted_part=""           
        for ((i=0; i<${#encrypted_part}; i+=2)); do
            code="${encrypted_part:i:2}"
            decrypted_part+="${decryptMap[$code]}"
        done           
        echo "$prefix$decrypted_part" >> "$output_file"
    else
        echo "$line" >> "$output_file"
    fi
done < "$input_file"
rm -f /data/local/tmp/tmp.ini
echo -e "${gr}- 解密完成，已保存到 $output_file${res}"
```

运行这个脚本，你会在脚本所在目录看到一个被解密的 `UserCustom.ini`，里面只包含配置部分，至于为什么要截掉备份部分后面会说。

解密后的文件大致如下，每个人可能会有所不同，我对部分项做了注释：

```ini
[UserCustom DeviceProfile]
# 节标志
+CVars=r.PUBGDeviceFPSLow=6
# 在流畅品质中可选的最高帧率，数值：20/25/30/40/60/6，6为全部启用，下同
+CVars=r.PUBGDeviceFPSMid=6
# 在均衡品质中可选的最高帧率，数值：20/25/30/40/60/6
+CVars=r.PUBGDeviceFPSHigh=6
# 在高清品质中可选的最高帧率，数值：20/25/30/40/60/6
+CVars=r.UserQualitySetting=1
# 画面质量设置，0-流畅，1-均衡，2-高清，3-超高清
+CVars=r.UserShadowSwitch=0
# 游戏阴影开关，0-关闭，1-开启
+CVars=r.ShadowQuality=0
# 阴影质量，范围：0～3，写0阴影无法显示
+CVars=r.MobileContentScaleFactor=1.500000
# 内容比例乘数，即游戏分辨率，分辨率越高，画面越清晰，对性能要求越高。调节范围：0.75～3
+CVars=r.UserVulkanSetting=0
# Vulkan图形优化设置，0=关闭，1=开启
+CVars=r.UserQualitySettingTA=1
# 画面质量设置，0-流畅，1-均衡，2-高清，3-超高清
+CVars=r.MobileHDR=0.0
# 高清画质 0.0=高清，1.0=HDR高清
+CVars=r.Mobile.SceneColorFormat=0.0
# 覆盖用于移动渲染器的场景颜色的内存布局（RGBA；不支持的重写格式默认使用默认值0 :(默认）根据项目设置和设备支持自动选择适当的格式；1：PF_FloatRGBA 32Bit ；2：PF_FloatR11G11B10 64Bit
+CVars=r.UserHDRSetting=2
# 画面风格设置，1-经典，2-鲜艳，3-写实，4-柔和，6-电影
+CVars=r.ACESStyle=2
# ACES风格，未知效果，范围0～9
+CVars=r.UserMSAASetting=0
# 抗锯齿设置，0-关闭，1-开启，需要先开启抗锯齿支持
+CVars=r.DefaultFeature.AntiAliasing=0.0
# 设置当前抗锯齿方法，0-关闭，1-FXAA，2-TAA，3-MSAA。FXAA效率最高，但效果最差,只做了最后的图像边缘锐化，TAA的缺点是比较容易模糊，有重影，MSAA的优点是物体边缘和贴图分开处理，边缘会比较清晰。缺点是开销会比TAA稍大
+CVars=r.MobileMSAA=1.0
# 游戏使用的抗锯齿倍数，数值：1/2/4
+CVars=r.MSAACount=4.0
# 抗锯齿总数，范围：0-4
+CVars=r.MaterialQualityLevel=0
# 画面质量等级，0-低，流畅画质，无法显示阴影。 1-高，高清画质，地板有反光。 2-中，均衡画质，无反光
+CVars=r.Shadow.MaxCSMResolution=4
# 渲染阴影深度的最大平方尺寸，可理解为阴影分辨率，数值越大，消耗性能越大，范围：4-2048
+CVars=r.Shadow.CSM.MaxMobileCascades=0
# 用于渲染阴影的动态光源数量，范围：0～2，写0阴影无法显示
+CVars=r.Shadow.DistanceScale=0
# 阴影渲染范围，游戏默认0.6，调节范围：0～2，写0阴影无法显示
+CVars=r.StaticMeshLODDistanceScale=1.3
# 用于计算静态网格的离散LOD的距离的比例因子，房子石头之类的东西显示距离，范围：0.8～1.3
+CVars=foliage.LODDistanceScale=0.6
# 树叶细节显示距离比例，范围：0.6～1
+CVars=r.DetailMode=0
# 细节模式，0-低，1-中，2-高
+CVars=r.Streaming.PoolSize=200
# 纹理池大小，数值越大纹理越清晰，范围：1～300，低于1定义不生效
+CVars=r.EmitterSpawnRateScale=0.5
# 发射器频率比例，未知效果，范围：0.5～1
+CVars=r.ParticleLODBias=2
# 粒子系统的LOD偏差，范围：0～2
+CVars=r.DepthOfFieldQuality=0
# 调整深景质量，未知效果，只能0
+CVars=r.RefractionQuality=0
# 定义允许调整质量或性能的失真/折射质量。未知效果，只能0
+CVars=foliage.MinLOD=0
# 树叶最小多细节层次，未知效果，只能写0
+CVars=r.MaxAnisotropy=4
# 各向异性过滤，数值越大远处材质渲染更清晰，消耗性能越大，范围：0～8
```

### 备份部分

这部分是用来校验的，节标志为 `[BackUp DeviceProfile]`，在修改 `UserCustom.ini` 的情况下打开游戏，游戏会对 `UserCustom.ini` 文件进行一次读取，并把 `[UserCustom DeviceProfile]` 节的代码和 `[BackUp DeviceProfile]` 节的代码作对比校验，若校验不通过，则会使用 `[BackUp DeviceProfile]` 中的代码对 `[UserCustom DeviceProfile]` 作重置。

所以，修改文件后如果不想被「自动恢复」，就需要让两部分的代码保持一致才行，当然，你也可以通过修改文件权限的方式不让软件修改，但这一般需要 Root。

---

## 如何修改

如果你清晰了解了以上内容，那么「修改和平精英画质配置文件」的方法相信你已经有思路了，简单来说，就是：**解密 - 修改 - 重新加密** - 锁定文件（可选）。加密就是解密的逆向操作。

使用我新上线的 Bash 工具即可完成全过程，你可以选择自定义修改，还是使用我给你做好的预设。快去试试吧！
