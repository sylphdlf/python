import pyinotify

multi_event = pyinotify.IN_MODIFY
wm = pyinotify.WatchManager()


class MyEventHandler(pyinotify.ProcessEvent):
    def process_IN_MODIFY(self, event):
        print('MODIFY-', event.pathname)


handler = MyEventHandler()
notifier = pyinotify.Notifier(wm, handler)


def add_file_watch(path_):
    wm.add_watch(path_, multi_event)
    notifier.loop()



