# 如何将 iOS 当前的锁屏壁纸导出来

## 背景

设置成 iPhone 桌面的图片，被删除之后，想要把图片回复出来。如果不越狱，没有很好的方式。

经过研究网上的资料和别人的经验，大体的思路如下:

1. 将 iPhone 备份一下
2. 使用工具找到备份中的文件，并恢复出来
3. 恢复出来的文件转化为图片文件

## Step 1 备份

1. 使用 iTunes 进行备份，可能需要先升级 iTunes 到对应的 iOS 对应的版本
2. 在设备上选择“备份”，最好是备份到本地

## Step 2 使用工具从备份中导出文件

1. 找一个工具，我使用的是 iPhone Backup Extractor Basic 版本，30+ 欧元，心疼啊！
2. 工具能够自动识别出本机上的备份

3. 选择导出模式，导出 home 目录，导出到本地

4. 找到锁屏桌面文件，不知道主程序界面在哪，因为我没有设置，所以可能没有，如果有的话，应该也是 cpbitmap 文件

5. 将 cpbitmap 文件转成图片文件，可以使用下面两个目录中的脚本

## 说明

这里插曲很多，好像是因为 iOS11 改变了 cpbitmap 的格式，导致网上的很多方法不能用了。
cpbitmap 几个特点:

1. 最后24个字节存了文件信息
2. 使用 RGBA 作为像素保存方式，但是和 png 的 R 和 B 是反的
3. 有个行对齐的概念，新版按照16像素对齐。例如，一行有 1943 个像素，那么，一行就有 `math.ceil(1943/16) * 16 = 1952` 个像素，每个像素4个字节，每一行的字节数就是 1952 * 4
4. 在转为 PNG 的时候，只需要读 1943 个像素就可以，本行剩余的可以直接略过，如果不略过就是错乱的, 在 [samples](samples) 目录也有转换错误的文件

## 参考资料

获取锁屏图片的大小：
<https://forums.macrumors.com/threads/iphone-6-plus-wallpaper-dimensions.1775299/page-2>
Github 上别人都示例，但是由于在线转换的网站被关了，所以也无法实现:
https://gist.github.com/sillygwailo/6631402

StackOverflow 上的示例代码：
python 和 js 都有，只有 js 的有用
<https://stackoverflow.com/questions/7998324/dot-cpbitmap-images-imgaename-cpbitmap/48158807#48158807?newreg=3f67b42138bc4f45ad965478aa9c08d9>

最后根据 Github 上下面的代码和上述链接才构成现在的代码
<https://gist.github.com/sfan5/8280735>
