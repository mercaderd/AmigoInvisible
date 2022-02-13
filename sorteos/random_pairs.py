import random

class element:
    
    def __init__(self, id, ex_id):
        self.id = id
        self.ex_id = ex_id
        self.partner = None
    
    def __str__(self) -> str:
        return self.id + ' -> ' + self.partner



def try_random_pairs(element_list):
    aux = element_list.copy()
    for e in element_list:
        r =random.choice(aux)
        while ((e==r) or (e.ex_id == r.id)):
            if len(aux) < 2:
                return None
            r =random.choice(aux)
        aux.remove(r)
        e.partner = r.id
    return element_list


def random_pairs(user_list):
    result = None
    while (not result):
        result = try_random_pairs(user_list)
    return result

