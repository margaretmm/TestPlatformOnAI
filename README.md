
整体结构图:
https://github.com/margaretmm/TestPlatformOnAI/issues/4


主要实现功能:
1. Python离线训练: 基于inception4 网络迁移学习训练成新的模型
2. 在线解析模型识别新图片: 核心代码是Tensorflow_prediction.java(没有提供Java服务端所有代码)
3. agent模块是部署在客户端的截图传输代码


使用场景举例:
  比如产品GUI界面是否黑屏, 场景很多,窗口很多, 如果出现黑屏,或者黑屏出现在多个窗口中的任意一个位置, 我们都需要能识别出来自动保存统计结果, 减少人工检查界面的
  识别效果示意: https://github.com/margaretmm/TestPlatformOnAI/issues/6
  
  


