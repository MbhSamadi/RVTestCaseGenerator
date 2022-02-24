class name_gen_class():
    def __init__(self):
        self.rebeca_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                             'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.rebeca_counter = 0
        self.rebeca_names_map = dict()

        self.rebeca_msgserver_counter = dict()

    def get_rebeca_name(self, rebeca_number):
        if rebeca_number in self.rebeca_names:
            return rebeca_number
        if rebeca_number in self.rebeca_names_map:
            return self.rebeca_names_map[rebeca_number]

        rebec_name = self.rebeca_names[rebeca_number]
        self.rebeca_names_map[rebeca_number] = rebec_name
        return rebec_name

    def get_rebeca_msgserver(self, rebeca_number):
        rebeca_name = self.get_rebeca_name(rebeca_number)

        msgserver_number = self.rebeca_msgserver_counter[
            rebeca_number] if rebeca_number in self.rebeca_msgserver_counter else 0

        msgserver_name = '{}{}'.format(rebeca_name.lower(), msgserver_number)
        self.rebeca_msgserver_counter[rebeca_number] = msgserver_number + 1

        return msgserver_name

    # def get_rebec_name_from_instance(instance_name):
    #     return instance_name[:instance_name.find('i')]

    def get_rebeca_name_of_msgserver(self, msgserver):
        return msgserver[0].upper()

    def get_known_rebeca_name_of_rebeca(self, rebeca):
        return 'kr_{}'.format(rebeca)

    def get_instance_name(self, rebec, instance_count):
        return '{}i{}'.format(rebec, instance_count)

    # def get_rebeca_msgserver_by_msgserver_number(self, rebeca_number, msgserver_number):


name_gen = name_gen_class()
