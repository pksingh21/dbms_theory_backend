import itertools
from itertools import combinations


def find_closure(attributes, fds, X):
    closure = set(X)
    old_closure = set()
    while closure != old_closure:
        old_closure = set(closure)
        for fd in fds:
            if set(fd['left']).issubset(closure):
                closure |= set(fd['right'])
    return closure

def find_candidate_keys(attributes, fds):
    candidate_keys = []
    for i in range(1, len(attributes)+1):
        for subset in itertools.combinations(attributes, i):
            flag = 0
            for j in range(0, len(candidate_keys)):
                if (candidate_keys[j].issubset(set(subset))):
                    flag = 1
                    break
            if flag == 1:
                continue
            closure = find_closure(attributes, fds, subset)
            if closure == set(attributes):
                candidate_keys.append(set(subset))
    return candidate_keys

def find_prime_attributes(candidate_keys):
    prime_attributes = set()
    for key in candidate_keys:
        prime_attributes.update(set(key))
    return prime_attributes

def is_in_2NF(prime_attributes, non_prime_attributes, candidate_keys, fds):
    problem_dependencies = []
    for index, fd in enumerate(fds):
        if set(fd['right']).issubset(non_prime_attributes):
            flag = 0
            for s in candidate_keys:
                if len(set(fd['left'])) != len(s) and set(fd['left']).issubset(s):
                    flag = 1
                    break  # Stop checking if a match is found
            if (flag):
                problem_dependencies.append(index)

    if len(problem_dependencies) == 0:
        return [True, problem_dependencies]
    else:
        return [False, problem_dependencies]

def is_in_3NF(prime_attributes, non_prime_attributes, candidate_keys, fds):

    temp_violated_list = []
    # Check if every functional dependency is in 3NF
    for index, fd in enumerate(fds):
        left = fd['left']
        right = fd['right']
        # Check if every attribute in Y is a prime attribute of R
        # print("This",right,prime_attributes)
        if set(right).issubset(prime_attributes):
            continue
        # Check if X is a superkey for R
        # print(left,candidate_keys)
        flag = 0
        for i in range(0, len(candidate_keys)):
            if candidate_keys[i].issubset(set(left)):
                flag = 1
        if flag == 1:
            continue
        # print("yay")
        temp_violated_list.append(index)
    if len(temp_violated_list) == 0:
        return [True, temp_violated_list]
    else:
        return [False, temp_violated_list]

def is_in_BCNF(prime_attributes, non_prime_attributes, candidate_keys, fds):
    temp_violated_list = []
        # Check if every functional dependency is in 3NF
    for index, fd in enumerate(fds):
        left = fd['left']
        right = fd['right']

        flag = 0
        for i in range(0, len(candidate_keys)):
            if candidate_keys[i].issubset(set(left)):
                flag = 1
        if flag == 1:
            continue
        # print("yay")
        temp_violated_list.append(index)

    if len(temp_violated_list) == 0:
        return [True, temp_violated_list]
    else:
        return [False, temp_violated_list]

def normalize_to_2nf(relation_1nf):

    relation_2nf = relation_1nf.copy()

    j = 0
    while j<(len(relation_2nf)):
        is2nf,pd_index = is_in_2NF(relation_2nf[j]["prime_attributes"], relation_2nf[j]["non_prime_attributes"], relation_2nf[j]["candidate_keys"], relation_2nf[j]["fds"])
        if(is2nf):
            j=j+1
            continue
        else:
            vindex = pd_index[0]
            # Identify the A, B, and C sets
            k = j
            A = set(relation_2nf[j]["fds"][vindex]['left'])
            B = set(relation_2nf[j]["fds"][vindex]['right'])
            Bclosure = find_closure(relation_2nf[k]["attributes"], relation_2nf[k]["fds"], B)
            Aclosure = Bclosure.union(A)
            print("closure", Aclosure)
            # R2 = A.union(B)
            # # R1 = find_closure(normalized_relations[k]["attributes"],normalized_relations[k]["fds"], A)

            # # Create the new relations R1 and R2
            # C = normalized_relations[k]["attributes"]-A-B
            C = set(relation_2nf[k]["attributes"])-Aclosure
            C = C.union(A)
            # R1 = A.union(C)
            # R2 = set(normalized_relations[k]["attributes"].copy())-find_closure(normalized_relations[k]["attributes"],normalized_relations[k]["fds"], B)

            Lfds = relation_2nf[k]["fds"].copy()
            i = 0
            while i < len(Lfds):
                if set(Lfds[i]["left"]).issubset(Aclosure) and set(Lfds[i]["right"]).issubset(Aclosure):
                    i = i
                else:
                    del Lfds[i]
                    i = i-1
                i = i+1

            # Add the new relations to the list of normalized relations
            Rfds = relation_2nf[k]["fds"].copy()
            if fds[vindex] in Rfds:
                Rfds.remove(relation_2nf[j]["fds"][vindex])
            i = 0
            while i < len(Rfds):
                if set(Rfds[i]["left"]).issubset(C) and set(Rfds[i]["right"]).issubset(C):
                    i = i
                # elif Rfds[i] not in Lfds:
                #     C=C.union(Rfds[i]["left"])
                #     C=C.union(Rfds[i]["right"])
                else:
                    del Rfds[i]
                    i = i-1
                i = i+1


            l_cand =  find_candidate_keys(Aclosure, Lfds)
            r_cand =  find_candidate_keys(C, Rfds)
            l_prime = find_prime_attributes(l_cand)
            r_prime = find_prime_attributes(r_cand)
            relation_2nf.append({"attributes": Aclosure, "fds": Lfds,"candidate_keys":l_cand,"prime_attributes":l_prime,"non_prime_attributes":(Aclosure-l_prime)})
            relation_2nf.append({"attributes": C, "fds": Rfds,"candidate_keys":r_cand,"prime_attributes":r_prime,"non_prime_attributes":(C-r_prime)})
            del relation_2nf[k]
            

    # print(normalized_relations,"\n")
    return relation_2nf

def normalize_to_3nf(relation_2nf):

    relation_3nf = relation_2nf.copy()

    j = 0
    while j<(len(relation_3nf)):
        is3nf,pd_index = is_in_3NF(relation_3nf[j]["prime_attributes"], relation_3nf[j]["non_prime_attributes"], relation_3nf[j]["candidate_keys"], relation_3nf[j]["fds"])
        if(is3nf):
            j=j+1
            continue
        else:
            vindex = pd_index[0]
            # Identify the A, B, and C sets
            k = j
            A = set(relation_3nf[j]["fds"][vindex]['left'])
            B = set(relation_3nf[j]["fds"][vindex]['right'])
            Bclosure = find_closure(relation_3nf[k]["attributes"], relation_3nf[k]["fds"], B)
            Aclosure = Bclosure.union(A)
            print("closure", Aclosure)
            # R2 = A.union(B)
            # # R1 = find_closure(normalized_relations[k]["attributes"],normalized_relations[k]["fds"], A)

            # # Create the new relations R1 and R2
            # C = normalized_relations[k]["attributes"]-A-B
            C = set(relation_3nf[k]["attributes"])-Aclosure
            C = C.union(A)
            # R1 = A.union(C)
            # R2 = set(normalized_relations[k]["attributes"].copy())-find_closure(normalized_relations[k]["attributes"],normalized_relations[k]["fds"], B)

            Lfds = relation_3nf[k]["fds"].copy()
            i = 0
            while i < len(Lfds):
                if set(Lfds[i]["left"]).issubset(Aclosure) and set(Lfds[i]["right"]).issubset(Aclosure):
                    i = i
                else:
                    del Lfds[i]
                    i = i-1
                i = i+1

            # Add the new relations to the list of normalized relations
            Rfds = relation_3nf[k]["fds"].copy()
            if fds[vindex] in Rfds:
                Rfds.remove(relation_3nf[j]["fds"][vindex])
            i = 0
            while i < len(Rfds):
                if set(Rfds[i]["left"]).issubset(C) and set(Rfds[i]["right"]).issubset(C):
                    i = i
                # elif Rfds[i] not in Lfds:
                #     C=C.union(Rfds[i]["left"])
                #     C=C.union(Rfds[i]["right"])
                else:
                    del Rfds[i]
                    i = i-1
                i = i+1


            l_cand =  find_candidate_keys(Aclosure, Lfds)
            r_cand =  find_candidate_keys(C, Rfds)
            l_prime = find_prime_attributes(l_cand)
            r_prime = find_prime_attributes(r_cand)
            relation_3nf.append({"attributes": Aclosure, "fds": Lfds,"candidate_keys":l_cand,"prime_attributes":l_prime,"non_prime_attributes":(Aclosure-l_prime)})
            relation_3nf.append({"attributes": C, "fds": Rfds,"candidate_keys":r_cand,"prime_attributes":r_prime,"non_prime_attributes":(C-r_prime)})
            del relation_3nf[k]
            

    # print(normalized_relations,"\n")
    return relation_3nf

def normalize_to_bcnf(relation_3nf):
    relation_bcnf = relation_3nf.copy()
    j = 0 
    p = 0
    while j<(len(relation_bcnf)):
        # print("random ",relation_bcnf[j],"random ")
        isbcnf,pd_index = is_in_BCNF(relation_bcnf[j]["prime_attributes"], relation_bcnf[j]["non_prime_attributes"], relation_bcnf[j]["candidate_keys"], relation_bcnf[j]["fds"])
        # print(isbcnf,pd_index)
        if(isbcnf):
            j=j+1
            continue
        else:
            vindex = pd_index[0]
            # Identify the A, B, and C sets
            k = j
            A = set(relation_bcnf[j]["fds"][vindex]['left'])
            B = set(relation_bcnf[j]["fds"][vindex]['right'])
            Aclosure = B.union(A)

            C = set(relation_bcnf[j]["attributes"])-Aclosure
            C = C.union(A)
            
            Lfds = relation_bcnf[k]["fds"].copy()
            i = 0
            while i < len(Lfds):
                if set(Lfds[i]["left"]).issubset(Aclosure) and set(Lfds[i]["right"]).issubset(Aclosure):
                    i = i
                else:
                    del Lfds[i]
                    i = i-1
                i = i+1

            # Add the new relations to the list of normalized relations
            Rfds = relation_bcnf[k]["fds"].copy()
            if fds[vindex] in Rfds:
                Rfds.remove(relation_bcnf[j]["fds"][vindex])
            i = 0
            while i < len(Rfds):
                if set(Rfds[i]["left"]).issubset(C) and set(Rfds[i]["right"]).issubset(C):
                    i = i
                else:
                    del Rfds[i]
                    i = i-1
                i = i+1

            l_cand =  find_candidate_keys(Aclosure, Lfds)
            r_cand =  find_candidate_keys(C, Rfds)
            l_prime = find_prime_attributes(l_cand)
            r_prime = find_prime_attributes(r_cand)
            relation_bcnf.append({"attributes": Aclosure, "fds": Lfds,"candidate_keys":l_cand,"prime_attributes":l_prime,"non_prime_attributes":(Aclosure-l_prime)})
            relation_bcnf.append({"attributes": C, "fds": Rfds,"candidate_keys":r_cand,"prime_attributes":r_prime,"non_prime_attributes":(C-r_prime)})
            del relation_bcnf[k]
            
            

    # print(normalized_relations,"\n")
    return relation_bcnf

def printedges(fds):
    for i in range(0, len(fds)):
        input = ''.join(str(num) for num in fds[i]["left"])
        output = ''.join(str(num) for num in fds[i]["right"])
        print(input+"->"+output, end="  ")
    print("")

# def verify_FDs(original_relation, original_fds, decomposed_relations):
#     # Check if the FDs are preserved in each 3NF relation
#     for relation in decomposed_relations:
#         for X, A in original_fds.items():
#             if set(X) <= set(relation["left"]):
#                 closure = compute_closure(X, relation, original_fds)
#                 if set(A) != closure.intersection(set(A)):
#                     return False
#     return True

def LJ_tester(p_relation,c_relation):
    plist = list(p_relation[0]["attributes"])
    n = len(plist)
    m = len(c_relation)
    lj_mat = []
    for i in range(0,m):
        temp = []
        for j in range(0,n):
            temp.extend([0])
        lj_mat.append(temp)

    print(lj_mat)
    for i in range(0,m):
        for k in set(c_relation[i]["attributes"]):
            lj_mat[i][plist.index(k)] = 1
    ans = False
    # print(lj_mat)
    for i in range(0,m):
        j=0
        while j<len(p_relation[0]["fds"]):
            left = p_relation[0]["fds"][j]["left"]
            all_1 = all(lj_mat[i][plist.index(val)] == 1 for val in left)
            # print(all_1)
            if(all_1):
                right = p_relation[0]["fds"][j]["right"]
                all_1l = all(lj_mat[i][plist.index(val)] == 1 for val in right)
                if(all_1l):
                    j = j+1
                    continue
                for val in right:
                    lj_mat[i][plist.index(val)]=1
                j=0
            else:
                j=j+1
        all_cut = all(val==1 for val in lj_mat[i])
        if(all_cut): 
            ans = True   
    # print(lj_mat)
    return [ans,lj_mat]


# A->C, B->DE, D->C
# Example usage:
# attributes = ['A', 'B', 'C', 'D', 'E']
# fds = [
#     {'left': ['A'], 'right': ['C']},
#     {'left': ['B'], 'right': ['D', 'E']},
#     {'left': ['D'], 'right': ['C']}
# ]
# attributes = ['A', 'B', 'C']
# fds = [
#     {'left': ['A'], 'right': ['B']},
#     {'left': ['B'], 'right': ['C']}
# ]
attributes = ['A', 'B', 'C','D','E','F']
fds = [
    {'left': ['A','B'], 'right': ['C']},
    {'left': ['C'], 'right': ['D']},
    {'left': ['C'], 'right': ['E']},
    {'left': ['E'], 'right': ['F']},
    {'left': ['F'], 'right': ['A']}
]
# attributes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
# fds = [
#     {'left': ['A'], 'right': ['D', 'B']},
#     {'left': ['B'], 'right': ['C']},
#     {'left': ['E'], 'right': ['F', 'G']},
#     {'left': ['A', 'E'], 'right': ['H']}
# ]
output = ''.join(str(num) for num in attributes)
print("R(", output, ") ", end="")
printedges(fds)
candidate_keys = find_candidate_keys(attributes, fds)
print(candidate_keys)

prime_attributes = find_prime_attributes(candidate_keys)
print("Prime Attributes", prime_attributes)

non_prime_attributes = set(attributes) - prime_attributes
# print("Non Prime Attributes",non_prime_attributes)

relation_1nf = [{"attributes":attributes,"fds":fds,"candidate_keys":candidate_keys,"prime_attributes":prime_attributes,"non_prime_attributes":non_prime_attributes}]

relation_2nf = normalize_to_2nf(relation_1nf)
print("\nconverted to 2NF\n\n Relations :=> ",relation_2nf,"\n")
for i in range(0, len(relation_2nf)):
    output = ''.join(relation_2nf[i]["attributes"])
    print("R"+str(i+1)+"("+output+")", end=" ")
    printedges(relation_2nf[i]["fds"])


relation_3nf = normalize_to_3nf(relation_2nf)
print("\nconverted to 3NF\n\n Relations :=> ",relation_3nf,"\n")
for i in range(0, len(relation_3nf)):
    output = ''.join(relation_3nf[i]["attributes"])
    print("R"+str(i+1)+"("+output+")", end=" ")
    printedges(relation_3nf[i]["fds"])



# violated_index_bcnf = []
relation_bcnf= normalize_to_bcnf(relation_3nf)
print("\nconverted to BCNF\n\n Relations :=> ",relation_3nf,"\n")
for i in range(0, len(relation_bcnf)):
    output = ''.join(relation_bcnf[i]["attributes"])
    print("R"+str(i+1)+"("+output+")", end=" ")
    printedges(relation_bcnf[i]["fds"])


# print(LJ_tester(relation_1nf,relation_bcnf))

 


