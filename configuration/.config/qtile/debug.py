import os
import io
import datetime

class Debugger:
    def __init__(self, output_directory_path=os.path.expanduser(os.path.join('~', '.local', 'share', 'qtile')), n=3):
        log_history = list()
        for file_name in os.listdir(output_directory_path):
            if file_name.endswith('_qtile-theme.log'):
                log_history.append(file_name)

        for file_name in log_history[:-n]:
            os.remove(os.path.join(output_directory_path, file_name))
        output_file_path = os.path.expanduser(os.path.join(output_directory_path, f'{datetime.datetime.now().isoformat()}_qtile-theme.log'))
        self.output_handle = io.open(output_file_path, 'w', encoding='utf-8')

    def log(self, data):
        self.output_handle.write(f'{datetime.datetime.now().isoformat()}\t{data}\n')
        self.output_handle.flush()

    def __del__(self):
        self.output_handle.close()


if __name__ == '__main__':
    debugger = Debugger()
    debugger.log('test')
    debugger.log('test2')