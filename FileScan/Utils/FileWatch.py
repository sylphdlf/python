import pyinotify


multi_event = pyinotify.IN_MODIFY
wm = pyinotify.WatchManager()


class MyEventHandler(pyinotify.ProcessEvent):

    def process_IN_MODIFY(event):
        print('MODIFY-', event.pathname)
        content = get_log_content(path)
        if len(str(content).strip()) != 0:
            send_msg(json.dumps({'key': str(path).rsplit(os.sep, 1)[1], 'value': content}))


notifier = pyinotify.Notifier(wm, MyEventHandler())


def add_file_watch(path_):
    wm.add_watch(path_, multi_event)


notifier.loop()


