class rebec_program_conf:
    def __init__(self, rebec_count, max_msgservers_count, max_msgservers_seq, property_length, non_causality_count, causality_count, backwards_count,maximum_method_calls):
        self.rebec_count = rebec_count
        self.max_msgservers_count = max_msgservers_count
        self.max_msgservers_seq = max_msgservers_seq
        self.connections = {}
        self.property_length = property_length
        self.non_causality_count = non_causality_count
        self.causality_count = causality_count
        self.backwards_count = backwards_count
        self.maximum_method_calls = maximum_method_calls

    def set_connections(self, connections):
        self.connections = connections

    def __repr__(self):
        return repr({
            'rebec_count': self.rebec_count,
            'max_msgservers_count': self.max_msgservers_count,
            'max_msgservers_seq': self.max_msgservers_seq,
            'property_length': self.property_length,
            'non_causality_count': self.non_causality_count,
            'causality_count': self.causality_count,
        })
