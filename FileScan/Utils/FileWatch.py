import pyinotify


multi_event = pyinotify.IN_MODIFY
wm = pyinotify.WatchManager()


class MyEventHandler(pyinotify.ProcessEvent):

    def process_IN_MODIFY(self, event):
        print('MODIFY-', event.pathname)


notifier = pyinotify.Notifier(wm, MyEventHandler())


# def add_file_watch(path_):
wm.add_watch("/data/sh/log/registry.log", multi_event)


notifier.loop()

# if __name__ == '__main__':
#     add_file_watch("/data/sh/log/registry.log")


