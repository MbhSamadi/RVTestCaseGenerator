from utils.writer import writer
from utils.name_gen import name_gen


class send_message_decleration():
    def __init__(self, source_rebeca, rebeca_instance, msgserver_name):
        self.source_rebeca = source_rebeca
        self.rebeca_instance = rebeca_instance
        self.msgserver_name = msgserver_name

    def write(self):
        rebeca = self.rebeca_instance
        if str(self.source_rebeca) == name_gen.get_rebeca_name_of_msgserver(self.msgserver_name):
            rebeca = 'self'
        writer.write('{}.{}();'.format(rebeca, self.msgserver_name), 2)
