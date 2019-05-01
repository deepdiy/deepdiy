# DeepDIY: Deep Learning, Do It Yourself

### Welcome to contact me: pubrcv@163.com

### Introduction

This is an open source project to help people who are trying to use Deep Neural Network model for image processing but  troubled by programming or computation resources. With DeepDIY, you can:

- Run mainstream deep learning models without coding, user-friendly GUI provided
- Train your own network on your own data in cloud (Free, One-click, fast, No programming)
- A database of shared model zoo and weight available
![quicker_ae952ca6-4438-4db8-aedf-04cbcf1c9d75.png](https://i.loli.net/2019/04/09/5cabe077a59c3.png)

### Installation

1. Clone this repository

2. Install dependencies

   `pip3 install -r requirements.txt`

3. Run setup from the repository root directory

   `python3 setup.py install`

A Window executable package made by Pyinstaller is available

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
