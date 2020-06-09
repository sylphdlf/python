import sys
sys.path.append("/data/project/cloud/python/FileScan/Utils/")

import os
import json
import RabbitmqProducer as Producer
import RedisUtils
import pyinotify


redis_ = RedisUtils.get_conn()


# 获取文件增加的内容
def get_log_content(path_):
    org_size = redis_.get('size|' + path_)
    new_size = os.path.getsize(path_)
    content_ = ''
    if org_size is None:
        # redis_.set('size|' + path, 0)
        return
    # 文件内容有新增
    elif new_size > int(org_size):
        f = open(path_, 'r')
        # 定位到上次的位置
        f.seek(int(org_size), 0)
        # 读取所有新增的内容
        content_ = f.read(new_size - int(org_size))
        f.close()
    # 文件清空，切换日期
    elif new_size < int(org_size):
        f = open(path_, 'r')
        if new_size == 0:
            f.seek(0, 0)
        else:
            content_ = f.read()
            f.seek(new_size, 0)
        f.close()
    # 重新设定文件位置
    redis_.set('size|' + path, new_size)
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


multi_event = pyinotify.IN_MODIFY
wm = pyinotify.WatchManager()


class MyEventHandler(pyinotify.ProcessEvent):

    def process_IN_MODIFY(self, event):
        print('MODIFY-', event.pathname)
        content = get_log_content(event.pathname)
        print(content == 'None')
        print(content == null)
        if len(str(content).strip()) > 0 and content != 'None':
            send_msg(json.dumps({'key': str(event.pathname).rsplit(os.sep, 1)[1], 'value': content}))


notifier = pyinotify.Notifier(wm, MyEventHandler())

file_paths = get_value("log_file_monitor")
if file_paths is not None:
    for inner_path in file_paths:
        wm.add_watch(inner_path, multi_event)

notifier.loop()

# if __name__ == '__main__':
#     file_paths = get_value("log_file_monitor")
#     if file_paths is not None:
#         for path in file_paths:
#             print(path)
#             add_file_watch(path)
