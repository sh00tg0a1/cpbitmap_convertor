# 如何将 iOS 当前的锁屏壁纸导出来

[[English](README.en.md)]

## 背景

如果把某张照片设为 iPhone 壁纸后又删除了原图，想要再次取得这张图片会比较麻烦，不越狱几乎没有好办法。

经过研究网上的资料和别人的经验，大体的思路如下:

1. 将 iPhone 备份一下
2. 使用工具找到备份中的文件，并恢复出来
3. 恢复出来的文件转化为图片文件

## Step 1 备份

1. 使用 iTunes 为设备创建备份，如有必要先升级到与当前 iOS 版本兼容的 iTunes。
2. 备份时选择 "本电脑"，将备份保存到本地。

## Step 2 使用工具从备份中导出文件

1. 准备一款备份提取工具，我用的是 iPhone Backup Extractor（Basic 版，约 30 欧元）。
2. 工具会自动识别本机上的备份。
3. 选择导出模式，将 home 目录解压到本地。
4. 找到锁屏壁纸文件；如果也设置了主屏幕壁纸，同样会存在对应的 cpbitmap 文件。
5. 通过本仓库的脚本将 cpbitmap 文件转换为图片。

## Step 3 使用 Python 或 JS 代码进行图片导出

1. 选择 Python 或 Node.js 版本的脚本。
2. 安装依赖：
    1. Python: `pip install -r python/requirements.txt`
    2. JS: `npm install`
3. 运行脚本：
    1. Python: `python python/convert_cpbitmap.py {source} {destination}`
    2. JS: `node js/index.js {source} {destination}`

## 说明

需要注意的是，cpbitmap 格式在 iOS 11 之后发生了变化，网上很多旧方法已经无法使用。
cpbitmap 几个特点:

1. 最后24个字节存了文件信息
2. 使用 RGBA 作为像素保存方式，但是和 png 的 R 和 B 是反的
3. 有个行对齐的概念，新版按照16像素对齐。例如，一行有 1943 个像素，那么，一行就有 `math.ceil(1943/16) * 16 = 1952` 个像素，每个像素4个字节，每一行的字节数就是 1952 * 4
4. 在转为 PNG 的时候，只需要读 1943 个像素就可以，本行剩余的可以直接略过，如果不略过就是错乱的, 在 [samples](samples) 目录也有转换错误的文件

## 参考资料

获取锁屏图片的大小:

<https://forums.macrumors.com/threads/iphone-6-plus-wallpaper-dimensions.1775299/page-2>

Github 上有人分享了示例，但在线转换的网站已关闭，无法直接使用：
https://gist.github.com/sillygwailo/6631402

StackOverflow 上也有人给出示例代码，既有 Python 版本也有 JavaScript 版本，不过只有后者能正确运行。
<https://stackoverflow.com/questions/7998324/dot-cpbitmap-images-imgaename-cpbitmap/48158807#48158807?newreg=3f67b42138bc4f45ad965478aa9c08d9>

最终根据 Github 上的示例代码以及以上链接整理出了当前的脚本

<https://gist.github.com/sfan5/8280735>
