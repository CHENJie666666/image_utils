# image_utils
Some useful utils for common image processing

## 1. 图像超分

### opencv超分

- 安装包

```shell
pip uninstall opencv-python
pip install opencv-contrib-python
```

- 下载模型文件（[opencv_contrib/modules/dnn_superres at master · opencv/opencv_contrib (github.com)](https://github.com/opencv/opencv_contrib/tree/master/modules/dnn_superres)），并存放至代码所在同级目录的super_resolution_cv2_models文件夹中
- 调用`super_resolution_cv2.py`文件

第一个参数为图片文件所在路径

第二个参数为模型类型，可选项为'espcn', 'edsr', 'fsrcnn', 'lapsrn'（默认为'espcn'）

第三个参数为放大倍数，前三个模型可放大2/3/4倍，最后一个模型可以放大2/4/8倍（默认为4）

```shell
python super_resolution_cv2.py './test.png' 'espcn' 4
```



## 2. 图像基本处理

### 2.1 背景透明处理

#### pillow

- 调用`background_transparent.py`文件

```shell
python background_transparent.py 'test.jpg'
```

- 指定背景色（十六进制或RGB值）

```shell
python background_transparent.py 'test.jpg' -hex '123456'
python background_transparent.py 'test.jpg' -rgb 230 230 230
```


