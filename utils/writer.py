file_to_write_in = open('output.rebec', 'w')


class writer_class(object):
    @staticmethod
    def write(text, tabs=0):
        for i in range(tabs):
            file_to_write_in.write('\t')
        file_to_write_in.write('{}\n'.format(text))

    @staticmethod
    def close():
        file_to_write_in.close()


writer = writer_class()
