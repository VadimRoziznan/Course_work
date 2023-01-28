class WorkingWithFiles:

    def __init__(self, name_file='report_file.json'):
        self.name_file = name_file

    def file_write(self, file):
        with open(self.name_file, 'w') as f:
            f.write(f'{file}')
        return
