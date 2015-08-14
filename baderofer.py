"""
.. baderofer.py
"""

class Elections(object):
    def __init__(self, threshold, seats):
        self.threshold = threshold
        self.seats = seats

        self.parties = {}
        self.agreements = set()

    def register_party(self, name, head):
        self.parties[name] = (head,)

    def register_agreement(self, party1, party2):
        for ag in self.agreements:
            if party1 in ag or party2 in ag:
                raise ValueError("Party already in agreement.")
        self.agreements.add(frozenset([party1, party2]))

    def elect(self, elections):
        total_votes = sum(elections.itervalues())
        v_threshold = self.threshold * total_votes
        passed = set(p for p, v in elections.viewitems() if v >= v_threshold)
        general_indicator = sum(elections[p] for p in passed)
        seats = dict((p, self.seats * elections[p] / general_indicator)
                     for p in passed)
        agreements = set(ag for ag in self.agreements if ag <= passed)
        if agreements:
            ag_union = frozenset.union(*(ag for ag in agreements))
        else:
            ag_union = frozenset()
        lists = set(agreements) |\
            set(frozenset([p]) for p in passed if not p in ag_union)
        list_votes = lambda l: sum(elections[p] for p in l)
        list_seats = lambda l: sum(seats[p] for p in l)
        list_indicator = lambda l: list_votes(l) // (list_seats(l) + 1)
        party_indicator = lambda p: elections[p] // (seats[p] + 1)
        while sum(seats.viewvalues()) < self.seats:
            bonus_list = max(lists, key=list_indicator)
            if len(bonus_list) == 1:
                seats[list(bonus_list)[0]] += 1
                continue

            party1, party2 = bonus_list
            if party_indicator(party1) > party_indicator(party2):
                seats[party1] += 1
            else:
                seats[party2] += 1

        return seats


if __name__ == '__main__':
    e = Elections(0.0375, 120)
    e.register_party('A', 'a')
    e.register_party('B', 'b')
    e.register_party('C', 'c')
    e.register_party('D', 'd')
    e.register_party('E', 'e')
    e.register_agreement('A', 'B')
    results = e.elect({'A': 17500, 'B': 16500, 'C': 17500, 'D': 16500,
                       'E': 8000, 'F': 100})
    for p, s in sorted(results.viewitems(), key=lambda t: -t[1]):
        print p, s

