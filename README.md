# DeepDIY: Deep Learning, Do It Yourself


<img src="https://i.imgur.com/y9XKKNz.png"/>



[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)  [![GitHub license](https://img.shields.io/github/license/deepdiy/deepdiy.svg)](https://github.com/deepdiy/deepdiy/blob/master/LICENSE)  [![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/deepdiy/deepdiy/graphs/commit-activity)  [![GitHub release](https://img.shields.io/github/release/deepdiy/deepdiy.svg)](https://github.com/deepdiy/deepdiy/releases)  [![GitHub stars](https://img.shields.io/github/stars/deepdiy/deepdiy.svg?style=social)](https://GitHub.com/deepdiy/deepdiy/stargazers/)  [![GitHub downloads](https://img.shields.io/github/downloads/deepdiy/deepdiy/total.svg)](https://github.com/deepdiy/deepdiy/releases)

### Welcome to contact me: pubrcv@163.com

### Introduction

This is an open source project to help people who are trying to use Deep Neural Network model for image processing but  troubled by programming or computation resources. With DeepDIY, you can:

- Run mainstream deep learning models without coding, user-friendly GUI provided
- Train your own network on your own data in cloud (Free, One-click, fast, No programming)
- A database of shared model zoo and weight available

# Quick Start

## 1. Load image file or folder

![load local image files](https://i.imgur.com/yb6n4E6.gif)

## 2. Run a deep learning model

![run_model](https://i.imgur.com/TIM8psK.gif)

## 3. Train a model on own data

### 3.1 Edit the basic configuration of networks (eg. Number of classes)

   ![train_config](https://i.imgur.com/WUMJJFF.gif)

### 3.2 Labeling images using VIA or other annotation tools

   ![train_config](https://i.imgur.com/fi64CJL.gif)

### 3.3 Pack data

   ​	DeepDIY will split your training data (image + anotation file) into train set and validation set. And then pack all of data (train set, validation set and config file) into a zip file name "dataset.zip"

   ![train-pack](https://i.imgur.com/8CuEIq7.gif)

### 3.4 Train on colab


   ![train-run](https://i.imgur.com/Lx8W1RP.gif)

   ![train-colab](https://i.imgur.com/C7x2ucW.gif)

   ![train-evaluate](https://imgur.com/mgEMw1g.gif)


   # Installation

------

   ## Executable Version:

   1. Download **win64 portable version**: https://github.com/deepdiy/deepdiy/releases

   2. **Unzip** and go to

      ```
      ./path_of_downloaded_package/deepdiy/DeepDIY.exe
      ```

   3. **Double click** DeepDIY.exe , Done!

   ## Source Code Version:

   ### Method 1:

   1. Clone this repository

   2. Run setup from the repository root directory

      ```python
      python3 setup.py install
      ```

   ### Method 2:

   1. Clone this repository

   2. Install dependencies

      ```python
      pip install -r requirements.txt
      ```

   3. Install kivy.garden.matplotlib

      ```
      garden install --kivy matplotlib
      ```



   ## Notice:

   For OS X users, you may need to install kivy and kivy-garden manually. The 'garden' command is available only after kivy-garden is installed successfully. Please refer to following page:

   https://kivy.org/doc/stable/installation/installation-osx.html

### Model Zoo in DeepDIY

Most of mainstream deep learning network will be included in DeepDIY, including but not limited to:

- Classification: VGG, ResNet, Inception, MobilNet
- Object Detection: YOLO, SSD
- Segmentation: Mask-RCNN, UNet

DeepDIY encourage users to share new models and weights trained on their own data.

### Training with Google Colab

You can train network on your own data without GPU, the training task in performed on Google Colab[https://colab.research.google.com/]. Free, fast, private and safe. Only one click, leave and drink a cup of coffee, done!

### User-Friendly & Developer-Friendly

- Easy to use GUI, no need programming even when training most complicated networks by your self.
- Plugin-Archetecture, easy to understand and very simple to develop new plugins if you want to add new functions

### Kivy based GUI

Kivy[https://kivy.org/] is a coss-platform Python framework for GUI development. Very easy to understand and use.

### Developing Plugins

The core of DeepDIY software is a resource tree, which is stored in a Python dictionary. For any plugin, DeepDIY will sync resource tree dict with plugin as a property(called 'data') of plugin class. There are two type of plugins: Processing and Display.

##### Processing plugins

Plugin can acquire data from tree, after running your functions, just insert result data as a child of selected node. Result can be displayed by Display plugins.

##### Display plugins

When user click a node in resouce tree, certain display plugin will be activated. Plugin can acquire selected data from the tree, and return a Kivy widget, the widget will be embedded in the window.

### Requirements

Python 3.7.1, Kivy 1.10.1, TensorFlow 1.13, Keras 2.2.4, OpenCV 4.0.0.21, Numpy 1.15.4, Scipy 1.1.0, Matplotlib 3.0.2

### Licence

MIT is licensed under MIT license.
