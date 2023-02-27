


from itertools import combinations


def closure(attributes, fds, X):
    closure1 = set(X)
    if(len(closure1)==0):
        return closure1
    old_closure = set()
    while closure1 != old_closure:
        old_closure = set(closure1)
        for fd in fds:
            # print(fd)
            if set(fd['left']).issubset(closure1): 
                closure1 |= set(fd['right'])
    return closure1

def minimal_cover(attrs, fds):
    """Find the minimal cover of the given relation."""
    # Step 1: remove extraneous attributes from the right-hand side of each FD.
    fds1 = []
    for fd in fds:
        for B in fd['right']:
            A = fd['left']
            fds1.append({"left":A,"right":[B]})
    print("fds1",fds1,end="\n\n")

    # Step 2: remove redundant functional dependencies.
    fds2 = fds1.copy()
    not_fd2 = []
    for fd in fds1:
        # if not any(set(fd['left']).issubset(fd2['left']) and set(fd['right']) == set(fd2['right']) for fd2 in fds2):
        #     fds2.append(fd)
        tempfd = fds2.copy()
        tempfd.remove({"left":fd["left"],"right":fd["right"]})
        # print(tempfd)
        if set(fd["right"]).issubset(closure(attrs,tempfd,fd["left"])):
            fds2 = tempfd
            not_fd2.append({"left":fd["left"],"right":fd["right"]})
    print("fd2",fds2)
    print("fd2",not_fd2,end="\n\n")
    # Step 3: remove redundant attributes from the left-hand side of each FD.
    fds3 = []
    for fd in fds2:
            for X in combinations(fd['left'], len(fd['left']) - 1):
                print(X)
                if closure(attrs, fds2, X) == closure(attrs, fds2, fd['left']):
                    fd = {'left': list(X), 'right': fd['right']}
            fds3.append(fd)
    print("fd3",fds3)
    fds4 = []
    travel = set()
    for index,fd in enumerate(fds3):
        if index not in travel:
            right = set(fd["right"])
            travel.add(index)
            for indexi,fdx in enumerate(fds3):
                if indexi not in travel and set(fd["left"])==set(fdx["left"]):
                    right = set(fd["right"]).union(set(fdx["right"]))
                    travel.add(indexi)
            fds4.append({"left":fd["left"],"right":list(right)})


    return fds4

# Example usage:A->C, AC->D, E->H, E->AD
# attributes = ['A', 'B', 'C', 'D', 'E','H']
# fds = [
#     {'left': ['A'], 'right': ['C']},
#     {'left': ['A','C','B'], 'right': ['D']},
#     {'left': ['E'], 'right': ['H']},
#     {'left': ['E'], 'right': ['A','D']}
# ]
attributes = ['v','w','x','y','z']
fds = [
    {'left': ['v'], 'right': ['w']},
    {'left': ['v','w'], 'right': ['x']},
    {'left': ['y'], 'right': ['v','x','y']}
]
minimal_fds = minimal_cover(attributes, fds)
print(minimal_fds) # [