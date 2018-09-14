import stomp
import time

gQueue_name = '/queue/SampleQueue'
gTopic_name = '/topic/SampleTopic'
gListener_name = 'SampleListener'
gPost = 61613
gIP="10.66.170.16"


class SampleListener(object):
    def on_message(self, headers, message):
        print('headers: %s' % headers)
        print('message: %s' % message)

class ActiveMq(object):
    def __init__(self,queue_name,ip,port =61613,topic_name=None):
        self.queue_name = queue_name
        self.topic_name = topic_name
        self.ip=ip
        self.port = 61613
        self.mq=[(self.ip, self.port)]

    # 推送到队列queue
    def send_to_queue(self,msg):
        conn = stomp.Connection10(self.mq)
        conn.start()
        conn.connect()
        conn.send(self.queue_name, msg)
        conn.disconnect()


    # 推送到主题
    def send_to_topic(self,msg):
        conn = stomp.Connection10(self.mq)
        conn.start()
        conn.connect()
        conn.send(self.topic_name, msg)
        conn.disconnect()


    ##从队列接收消息
    def receive_from_queue(self):
        conn = stomp.Connection10(self.mq)
        conn.set_listener(gListener_name, SampleListener())
        conn.start()
        conn.connect()
        conn.subscribe(self.queue_name)
        time.sleep(1)  # secs
        conn.disconnect()


    ##从主题接收消息
    def receive_from_topic(self):
        conn = stomp.Connection10(self.mq)
        conn.set_listener(gListener_name, SampleListener())
        conn.start()
        conn.connect()
        conn.subscribe(self.topic_name)
        while 1:
            self.send_to_topic('topic')
            time.sleep(3)  # secs
        conn.disconnect()


if __name__ == '__main__':
    mq=ActiveMq(gQueue_name,gIP)
    mq.send_to_queue('len 123')
    # mq.receive_from_queue()
