# **seetaFace6 (Docker版本)**

## 1. 简介

项目基于`SeetaFace6` 封装的python接口,使用简便,性能与原始c++模块基本一致,
模块上`SeetaFace6` 相较于`SeetaFace2` 上训练样本更多，准确率更高，提供的功能和识别模型也更多
接口封装上，放弃了使用 `pybind11` 封装python 接口，接口函数完全纯 c 接口，使用 ctypes 调用，解除不同版本python使用上的限制
`10分钟搞定`是夸张说法，但本次项目基本涵盖了普通商用人脸识别所需的大部分功能，并且使用简单。

## 2.下载模型（已下载则忽略）
百度网盘：https://pan.baidu.com/share/init?surl=LlXe2-YsUxQMe-MLzhQ2Aw 提取码：ngne  
将下载的所有 *.csta 模型文件 放入 `seetaFace6Python/seetaface/model` 目录下

## 3. 运行示例
本版本使用docker发布，需要安装docker后运行
```
docker build . -t seetaface6
```
## 运行
```
docker run --rm -p 8080:8080 seetaface6
```
## 测试
### 人脸检测
```
curl --location --request POST 'http://127.0.0.1:8080/detect' \
--form 'image1=@"/Users/yuebo/Downloads/11.jpg"' \
```
响应结果
```json
{
    "faces": [
        {
            "pos": [
                456,
                242,
                349,
                480
            ],
            "age": 31,
            "gender": 1,
            "mask": [
                0,
                0,
                0,
                0,
                0
            ]
        }
    ]
}
```
* pos: 人脸在图片中的位置
* age: 年龄
* gender: 性别, 0：男  1：女
* mask:  `[左眼，右眼，鼻子，左边嘴角，右边嘴角]` 的数组，0：没被遮挡  1：被遮挡
### 人脸比对
```
curl --location --request POST 'http://127.0.0.1:8080/recon' \
--form 'image1=@"/Users/yuebo/Downloads/11.jpg"' \
--form 'image2=@"/Users/yuebo/Downloads/22.jpg"'
```
响应
```json
[
    {
        "result": 0.7792949676513672
    }
]
```
如果精度大于0.6，则可以认为是匹配。
