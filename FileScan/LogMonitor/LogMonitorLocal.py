import sys
import os
import json
import FileScan.Utils.RabbitmqProducer as Producer
import FileScan.Utils.RedisUtils as RedisUtils


redis_ = RedisUtils.get_conn()

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


# 发送MQ消息
def send_msg(content_):
    Producer.send_msg("mq_to_nodejs", content_)


if __name__ == '__main__':
    file_path = "/Users/lfd/Documents/workspace.nosync/log/webApi_err.log"
    content_= get_log_content(file_path)
    if content_ is not None and len(str(content_).strip()) > 0:
        send_msg(json.dumps({'key': str(file_path).rsplit(os.sep, 1)[1], 'value': content_}))