# TODO: depending on the complexity of dumping payloads, may need a formatter class
#       with dump as an instance.

def dump(result, type = 'sct'):
    if type == 'sct':
        return {'type': 'sct', 'payload': result}
    else:
        raise Exception("No matching type, %s, for dumping payload")
