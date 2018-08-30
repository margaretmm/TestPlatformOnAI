
----使用场景举例:
  比如产品GUI界面是否黑屏, 场景很多,窗口很多而且位置也很多, 如果出现1个或多个黑屏窗口或者黑屏出现在多个窗口中的任意一个位置, 都需要能识别出来自动保存统计结果; 还有类似黑屏,但不是黑屏的场景, 比如背景也是黑色,但中间有些其他的形状物体,不能被误识别成黑屏等等;最终达到减少人工检查界面的工作消耗; 提升检测效率,做到无人值守检测;而CNN比传统的图像识别软件适应性强, 因为不需要切图之类的和布局强绑定的操作;


----整体结构图:
https://github.com/margaretmm/TestPlatformOnAI/issues/4


---模块&功能描述---


1离线学习模块	使用Tensorflow python版本,基于Inception4 网络做迁移学习;
             离线训练阶段需要准备很多正常,和各种黑屏场景的图片训练我们新的模型



2.在线图像识别测试平台	
   2.1.	Web服务器使用Tomcat+sprintBoot(比较通用,代码没有提供)
   2.2.	算法调度模块主要是用于选择哪种识别算法(目前只支持一种模型)
   2.3.	图像识别子模块: 使用Java版本的TensorFlow 解析训练好的模型, 用于识别SUT端传输过来的图片, 是否有黑屏异常出现, 识别效果通过准确率来判断是否是合理


3.SUT端Agent:
    Python实现,主要提供定时截屏, 压缩存储, 异步发送到测试平台端


4. 传输模块:
    使用rabbitMq 作为Agent和测试平台之间的通信中间件


  
  
----识别效果示意:
https://github.com/margaretmm/TestPlatformOnAI/issues/6
识别效率还比较高, 基本上每张图片不用一秒给出判断结果
  
  ()Server平台端代码只提供了图像识别功能部分代码)


