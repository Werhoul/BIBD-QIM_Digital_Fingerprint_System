# BIBD-QIM_Digital_Fingerprint_System

## 简介
该项目系本科课程《信息隐藏技术》的课程设计，是对数字指纹编码算法、对图像的数字水印嵌入与提取算法、对该数字指纹系统进行攻击测试等要求的粗糙实现。

## 使用说明
本项目使用MySQL数据库存储用于生成数字指纹的`user_id` 、`work_id` 以及由此生成的数字指纹，所以在您运行本项目之前，您需要：
1. 使用您的开发工具连接您计算机上的MySQL数据库并运行`init_db.sql` ，届时程序会在您本地运行本项目需要的数据库与数据表，并插入一些测试信息
2. 请您更改配置文件`config.ini` 中数据库的对应信息

由于本人偷懒，该项目使用起来可能会有些麻烦，我在`main.py` 中实现了为一位用户分发图像和批量为若干个用户分发图像的功能，你可以通过命令行和特定参数来使用它。而合谋攻击与叛逆者追踪（私以为写的很烂）的功能，想要使用可能还需要去看`colluded_attack.py` 和`db_oprations.py` 的`if __name__ == "__main__":` 部分，我暂时还没有将该部分的逻辑也放到`main.py` 中方便直接通过命令行使用。

## 基于
本项目基于以下开源项目开发：

- [Quantization Index Modulation](https://github.com/pl561/QuantizationIndexModulation) - 该项目使用 MIT 许可证。
- [BIBDCalc](https://github.com/gflegar/BIBDCalc) - 该项目使用 GPL-2.0 许可证。

## 致谢
感谢开发出[Quantization Index Modulation](https://github.com/pl561/QuantizationIndexModulation) 与[BIBDCalc](https://github.com/gflegar/BIBDCalc) 的两位老师，他们的项目加快了我学习对应算法的速度，让我收获颇丰。
感谢互联网创造的丰富有趣的表情图，它们为我带来了快乐并且成为我测试我的拙作的素材。当然，如果您是其中一些表情图的作者并且不喜欢我使用它的方式，请您[联系我](werhoul@163.com)删除。