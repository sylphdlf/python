import sys
import os
import json
import pyinotify
import time
sys.path.append("/data/project/cloud/python/FileScan/Utils/")

import RabbitmqProducer as Producer
import RedisUtils


redis_ = RedisUtils.get_conn()
notifier = None


# 获取文件增加的内容
def get_log_content(path_):
    org_size = redis_.get('size|' + path_)
    new_size = os.path.getsize(path_)
    content_ = ''
    if org_size is None:
        redis_.set('size|' + path_, 0)
        print("org_size is None")
        return
    # 文件内容有新增
    elif new_size > int(org_size):
        f = open(path_, 'r')
        # 定位到上次的位置
        f.seek(int(org_size), 0)
        # 读取所有新增的内容
        content_ = f.read(new_size - int(org_size))
        print("new_size > int(org_size)")
        f.close()
    # 文件清空，切换日期
    elif new_size < int(org_size):
        f = open(path_, 'r')
        if new_size == 0:
            f.seek(0, 0)
            print("new_size < int(org_size) new_size == 0")
        else:
            print("new_size < int(org_size) else")
            content_ = f.read()
            f.seek(new_size, 0)
        f.close()
    # 重新设定文件位置
    redis_.set('size|' + path_, new_size)
    return content_
    # f = open(path, 'r')


# 从redis中得到value
def get_value(key):
    if redis_.get(key) is not None:
        return json.loads(redis_.get(key))
    else:
        print(key + " is Null")


# 发送MQ消息
def send_msg(content_):
    Producer.send_msg("mq_to_nodejs", content_)


class MyEventHandler(pyinotify.ProcessEvent):
    def process_IN_MODIFY(self, event):#文件修改
        print('MODIFY-', event.pathname)
        content = get_log_content(event.pathname)
        if content is not None and len(str(content).strip()) > 0:
            send_msg(json.dumps({'key': str(event.pathname).rsplit(os.sep, 1)[1], 'value': content}))

    def process_IN_MOVE_SELF(self, event):#日志打包，移动
        global notifier
        print(print('MOVED_SELF-', event.pathname))
        notifier.stop()


def start_watch():
    while True:
        print("sleep 5")
        time.sleep(5)
        global notifier
        notifier = None
        multi_event = pyinotify.IN_MODIFY | pyinotify.IN_MOVE_SELF
        wm = pyinotify.WatchManager()
        notifier = pyinotify.Notifier(wm, MyEventHandler())
        file_paths = get_value("log_file_monitor")
        try:
            if file_paths is not None:
                for inner_path in file_paths:
                    wm.add_watch(inner_path, multi_event)
            notifier.loop()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    start_watch()