
整体结构图:
https://github.com/margaretmm/TestPlatformOnAI/issues/4


模块&功能描述
1离线学习模块	使用Tensorflow python版本,基于Inception4 网络做迁移学习;
             离线训练阶段需要准备很多正常,和各种黑屏场景的图片训练我们新的模型
             
             
2.在线图像识别测试平台	
   2.1.	Web服务器使用Tomcat+sprintBoot
   2.2.	算法调度模块主要是用于选择哪种识别算法(目前只支持一种模型)
   2.3.	图像识别子模块: 使用Java版本的TensorFlow 解析训练好的模型, 用于识别SUT端传输过来的图片, 是否有黑屏异常出现, 识别效果通过准确率来判断是否是合理
   
   
3.SUT端Agent:
    Python实现,主要提供定时截屏, 压缩存储, 异步发送到测试平台端
    
    
4. 传输模块:
    使用rabbitMq 作为Agent和测试平台之间的通信中间件



使用场景举例:
  比如产品GUI界面是否黑屏, 场景很多,窗口很多, 如果出现黑屏,或者黑屏出现在多个窗口中的任意一个位置, 我们都需要能识别出来自动保存统计结果, 减少人工检查界面的
  
  
  识别效果示意: https://github.com/margaretmm/TestPlatformOnAI/issues/6
  
  


