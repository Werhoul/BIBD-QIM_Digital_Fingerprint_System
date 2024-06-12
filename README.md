# BIBD-QIM_Digital_Fingerprint_System  
  
## 简介  
该项目系本科课程《信息隐藏技术》的课程设计，是对数字指纹编码算法、对图像的数字水印嵌入与提取算法、对该数字指纹系统进行攻击测试等要求的粗糙实现。  

## 运行前配置
本项目使用MySQL数据库存储用于生成数字指纹的`user_id` 、`work_id` 以及由此生成的数字指纹，所以在您运行本项目之前，您需要：  
1. 使用您的开发工具连接您计算机上的MySQL数据库并运行`init_db.sql` ，届时程序会在您本地创建运行本项目需要的数据库与数据表，并插入一些测试信息  
2. 更改配置文件`config.ini` 中数据库的对应信息  
  
## 使用说明   
  
### 1. 图像分发 (`distri` 选项)  
在这个例子中，我们需要传入 `--option distri` 来指定执行图像分发，随后传入 `<user_id>` 和 `<work_id>` 作为参数。命令行的使用格式如下：  
  
```bash  
python main.py --option distri 0157435433 3B85FFDE6
```  
这条命令将会处理用户 ID 为 `0157435433` 和作品 ID 为 `3B85FFDE6` 的图像分发。  
  
### 2. 合谋攻击 (`cldatk` 选项)  
在这个例子中，我们需要传入 `--option cldatk` 来指定执行合谋攻击，随后传入若干个图像文件名和攻击类型。命令行的使用格式如下：  
  
```bash  
python main.py --option cldatk image1.png image2.png image3.png majority
```  
这条命令将使用提供的三个图像文件（`image1.png`, `image2.png`, `image3.png`）进行 "majority" 攻击类型的合谋攻击，并将结果保存为 `majority_attack_result.png`。  

## 不足
### 图像格式适配存在问题
本项目在编写时主要考虑了`.jpg`这一文件格式，而没有考虑对其他文件格式进行适配。

虽然`original_images`文件夹中存在一些`.png`格式的图像，但使用这些图像作为实验材料可能会存在问题。这个问题可能会在后续的版本中修复。

### 无法实现理想的叛逆者追踪效果
对合谋攻击生成的图像提取数字指纹，得到的结果为全1的01串。

这样的结果无法和数据库中存储的数字指纹进行对比得出有意义的结论。出现这个结果的原因可能是QIM嵌入和提取算法的部分或者合谋攻击的部分未能达到理想效果导致的。

## 基于  
本项目基于以下开源项目开发：  
  
- [Quantization Index Modulation](https://github.com/pl561/QuantizationIndexModulation) - 该项目使用 MIT 许可证。  
- [BIBDCalc](https://github.com/gflegar/BIBDCalc) - 该项目使用 GPL-2.0 许可证。  
  
## 致谢  
感谢开发出[Quantization Index Modulation](https://github.com/pl561/QuantizationIndexModulation) 与[BIBDCalc](https://github.com/gflegar/BIBDCalc) 的两位老师，他们的项目加快了我学习对应算法的速度，让我收获颇丰。  
感谢互联网创造的丰富有趣的表情图，它们为我带来了快乐并且成为我测试我的拙作的素材。当然，如果您是其中一些表情图的作者并且不喜欢我使用它的方式，请您[联系我](werhoul@163.com)删除。