import itertools
from itertools import combinations
import copy

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
    # print("checking started \n")
    for index, fd in enumerate(fds):
        # print("index ",fd)
        if set(fd['right']).issubset(non_prime_attributes):
            flag = 0
            for s in candidate_keys:
                # print("ck",s)
                if len(set(fd['left'])) < len(s) and (set(fd['left'])).issubset(s):
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

def decomposer(Lfds,Aclosure,relation_bcnf,k,X):
    i = 0
    while i < len(Lfds):
        if set(Lfds[i]["left"]).issubset(Aclosure) and set(Lfds[i]["right"]).issubset(Aclosure):
            i = i
            # print("enter 0")
        elif set(Lfds[i]["left"]).issubset(Aclosure) and set(Lfds[i]["right"]).issubset(Aclosure)==False:
            # print("enter 1")
            temp = set(Lfds[i]["left"]);
            temp = temp - X;
            tempclosure = find_closure(relation_bcnf[k]["attributes"], relation_bcnf[k]["fds"],temp);
            if X.issubset(tempclosure):
                Lfds[i]["left"] = temp
                Lfds[i]["right"] = X
            else:
                del Lfds[i]
                i = i-1
        elif set(Lfds[i]["left"]).issubset(Aclosure)==False and set(Lfds[i]["right"]).issubset(Aclosure):
            # print("enter 2")
            temp = set(Lfds[i]["left"])
            extra = temp - Aclosure
            temp = temp - extra -X
            if len(temp)==0:
                del Lfds[i]
                i = i-1
            else:
                temp = temp.union(X)
                Lfds[i]["left"] = temp
        else:
            temp = set(Lfds[i]["left"])
            extra = temp - Aclosure
            temp = temp - extra 
            temp = temp.union(X)
            Lfds[i]["left"] = temp
            temp = set(Lfds[i]["left"]);
            temp = temp - X;
            tempclosure = find_closure(relation_bcnf[k]["attributes"], relation_bcnf[k]["fds"],temp);
            if X.issubset(tempclosure):
                # print("enter 3 add")
                Lfds[i]["left"] = temp
                Lfds[i]["right"] = X
            else:
                # print("enter 3 del")
                del Lfds[i]
                i = i-1
        i = i+1
    return Lfds

def normalize_to_2nf(relation_1nf):

    relation_2nf = relation_1nf.copy()

    j = 0
    while j<(len(relation_2nf)):
        # print("normalizing ",j,relation_2nf[j])
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
            Bclosure = find_closure(relation_2nf[k]["attributes"], relation_2nf[k]["fds"], A)
            Aclosure = Bclosure.union(A)
            C = set(relation_2nf[k]["attributes"])-Aclosure
            C = C.union(A)
            X = A
            Y = Aclosure - X
            Z = C - X
            Lfds = []
            Rfds = []
            for fd in relation_2nf[k]["fds"]:
                d2 = copy.deepcopy(fd)
                d3 = copy.deepcopy(fd)
                Lfds.append(d2)
                Rfds.append(d3)
            # print cpy_list

            # print("up Rfds : ",Rfds)
            Lfds = decomposer(Lfds,Aclosure,relation_2nf,k,X);
            Rfds = decomposer(Rfds,C,relation_2nf,k,X);


            l_cand =  find_candidate_keys(Aclosure, Lfds)
            r_cand =  find_candidate_keys(C, Rfds)
            l_prime = find_prime_attributes(l_cand)
            r_prime = find_prime_attributes(r_cand)
            relation_2nf.append({"attributes": Aclosure, "fds": minimal_cover(list(Aclosure), Lfds),"candidate_keys":l_cand,"prime_attributes":l_prime,"non_prime_attributes":(Aclosure-l_prime)})
            relation_2nf.append({"attributes": C, "fds": minimal_cover(list(C), Rfds),"candidate_keys":r_cand,"prime_attributes":r_prime,"non_prime_attributes":(C-r_prime)})
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
            Bclosure = find_closure(relation_3nf[k]["attributes"], relation_3nf[k]["fds"], A)
            Aclosure = Bclosure.union(A)
            # print("closure", Aclosure)
            # R2 = A.union(B)
            # # R1 = find_closure(normalized_relations[k]["attributes"],normalized_relations[k]["fds"], A)

            # # Create the new relations R1 and R2
            # C = normalized_relations[k]["attributes"]-A-B
            C = set(relation_3nf[k]["attributes"])-Aclosure
            C = C.union(A)
            # R1 = A.union(C)
            # R2 = set(normalized_relations[k]["attributes"].copy())-find_closure(normalized_relations[k]["attributes"],normalized_relations[k]["fds"], B)
            X = A
            Y = Aclosure - X
            Z = C - X
            Lfds = []
            Rfds = []
            for fd in relation_3nf[k]["fds"]:
                d2 = copy.deepcopy(fd)
                d3 = copy.deepcopy(fd)
                Lfds.append(d2)
                Rfds.append(d3)
            # print cpy_list

            # print("up Rfds : ",Rfds)
            Lfds = decomposer(Lfds,Aclosure,relation_3nf,k,X);
            Rfds = decomposer(Rfds,C,relation_3nf,k,X);

            l_cand =  find_candidate_keys(Aclosure, Lfds)
            r_cand =  find_candidate_keys(C, Rfds)
            l_prime = find_prime_attributes(l_cand)
            r_prime = find_prime_attributes(r_cand)
            relation_3nf.append({"attributes": Aclosure, "fds": minimal_cover(list(Aclosure), Lfds),"candidate_keys":l_cand,"prime_attributes":l_prime,"non_prime_attributes":(Aclosure-l_prime)})
            relation_3nf.append({"attributes": C, "fds": minimal_cover(list(C), Rfds),"candidate_keys":r_cand,"prime_attributes":r_prime,"non_prime_attributes":(C-r_prime)})
            del relation_3nf[k]
            

    # print(normalized_relations,"\n")
    return relation_3nf

def normalize_to_bcnf(relation_3nf):
    relation_bcnf = relation_3nf.copy()
    j = 0 
    p = 0
    while j<(len(relation_bcnf)):
        # print("random \n",relation_bcnf,"\n")
        isbcnf,pd_index = is_in_BCNF(relation_bcnf[j]["prime_attributes"], relation_bcnf[j]["non_prime_attributes"], relation_bcnf[j]["candidate_keys"], relation_bcnf[j]["fds"])
        if(isbcnf):
            j=j+1
            continue
        else:
            vindex = pd_index[0]
            # print(isbcnf,pd_index)
            # Identify the A, B, and C sets
            k = j
            A = set(relation_bcnf[j]["fds"][vindex]['left'])
            B = set(relation_bcnf[j]["fds"][vindex]['right'])
            Bclosure = find_closure(relation_bcnf[k]["attributes"], relation_bcnf[k]["fds"], A)
            Aclosure = Bclosure.union(A)
            # Aclosure = B.union(A)

            C = set(relation_bcnf[j]["attributes"])-Aclosure
            C = C.union(A)
            
            X = A
            Y = Aclosure - X
            Z = C - X
            
            # R1 = A.union(C)
            # R2 = set(normalized_relations[k]["attributes"].copy())-find_closure(normalized_relations[k]["attributes"],normalized_relations[k]["fds"], B)

            Lfds = []
            Rfds = []
            for fd in relation_bcnf[k]["fds"]:
                d2 = copy.deepcopy(fd)
                d3 = copy.deepcopy(fd)
                Lfds.append(d2)
                Rfds.append(d3)

            Lfds = decomposer(Lfds,Aclosure,relation_bcnf,k,X);
            Rfds = decomposer(Rfds,C,relation_bcnf,k,X);
            

            print("Lfds :",Lfds)
            print("Rfds : ",Rfds)
            l_cand =  find_candidate_keys(Aclosure, Lfds)
            r_cand =  find_candidate_keys(C, Rfds)
            l_prime = find_prime_attributes(l_cand)
            r_prime = find_prime_attributes(r_cand)
            relation_bcnf.append({"attributes": Aclosure, "fds": minimal_cover(list(Aclosure), Lfds),"candidate_keys":l_cand,"prime_attributes":l_prime,"non_prime_attributes":(Aclosure-l_prime)})
            relation_bcnf.append({"attributes": C, "fds": minimal_cover(list(C), Rfds),"candidate_keys":r_cand,"prime_attributes":r_prime,"non_prime_attributes":(C-r_prime)})
            del relation_bcnf[k]
            
            

    # print(normalized_relations,"\n")
    return relation_bcnf

def printedges(fds):
    for i in range(0, len(fds)):
        input = ''.join(str(num) for num in fds[i]["left"])
        output = ''.join(str(num) for num in fds[i]["right"])
        print(input+"->"+output, end="  ")
    print("")

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

    # print(lj_mat)
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

def minimal_to_3nf(attributes, minimal_fds):
    fds4 = []
    travel = set()
    for index,fd in enumerate(minimal_fds):
        if index not in travel:
            right = set(fd["right"])
            travel.add(index)
            for indexi,fdx in enumerate(minimal_fds):
                if indexi not in travel and set(fd["left"])==set(fdx["left"]):
                    # print(indexi,fdx)
                    right = right.union(set(fdx["right"]))
                    travel.add(indexi)
            fds4.append({"left":fd["left"],"right":list(right)})

    attributes = set(attributes)
    # candidate_keys = [];
    relation = [];
    for fd in fds4:
        A = set(fd["left"])
        B = set(fd["right"])
        # candidate_keys.append(A)
        attributes = attributes - A-B;
        relation.append({"attributes":A.union(B),"fds":[fd],"candidate_keys":A,"prime_attributes":find_prime_attributes(A),"non_prime_attributes":B})
    if len(attributes)>0:
        ck = set();
        for fd in relation:
            ck = ck.union(fd["prime_attributes"]);
        print(ck,attributes)
        relation.append({"attributes":ck.union(attributes),"fds":[],"candidate_keys":ck.union(attributes),"prime_attributes":{},"non_prime_attributes":{}})
    return relation


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
    # print("fds1",fds1,end="\n\n")

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
    # print("fd2",fds2)
    # print("fd2",not_fd2,end="\n\n")
    # Step 3: remove redundant attributes from the left-hand side of each FD.

    fds3 = []
    for fd in fds2:
            for i in range(1,len(fd['left'])):
                check =0
                for X in combinations(fd['left'], i):
                    # print("got : ",X)
                    if closure(attrs, fds2, X) == closure(attrs, fds2, fd['left']):
                        check = 1;
                        fd = {'left': list(X), 'right': fd['right']}
                        break
                if check==0:
                    break
            fds3.append(fd)
    # print("fd3",fds3)


    return fds3

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
# attributes = ['A', 'B', 'C','D']
# fds = [
#     {'left': ['A','B'], 'right': ['B','C']},
# ]
# attributes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
# fds = [
#     {'left': ['A'], 'right': ['D', 'B']},
#     {'left': ['B'], 'right': ['C']},
#     {'left': ['E'], 'right': ['F', 'G']},
#     {'left': ['A', 'E'], 'right': ['H']}
# ]
# best example
attributes = ['a','b','c','d','e','f']
fds = [
    {'left': ['a'], 'right': ['c']},
    {'left': ['d'], 'right': ['c']},
    {'left': ['d','c'], 'right': ['e']},
    {'left': ['d'], 'right': ['f']}
]
# bcnf test
# attributes = ['a','b','c']
# fds = [
#     {'left': ['a','b'], 'right': ['c']},
#     {'left': ['c'], 'right': ['b']}
# ]
# attributes = ['a','b','c','d','e','f']
# fds = [
#     {'left': ['c','b'], 'right': ['f']},
#     {'left': ['a','d','b','c'], 'right': ['f']}
# ]
# attributes = ['a','b','c','d','e','f']
# fds = [
#     {'left': ['a'], 'right': ['b','c']},
#     {'left': ['d','c'], 'right': ['e']},
#     {'left': ['b'], 'right': ['d']},
#     {'left': ['e'], 'right': ['a']}
# ]

print("All the attributes and the Fds are given to change them change the input in code directly")


output = ''.join(str(num) for num in attributes)
print("R(", output, ") ", end="")
printedges(fds)
candidate_keys = find_candidate_keys(attributes, fds)
print("\nCandidate Keys",candidate_keys)

prime_attributes = find_prime_attributes(candidate_keys)
print("Prime Attributes", prime_attributes)

non_prime_attributes = set(attributes) - prime_attributes
# print("Non Prime Attributes",non_prime_attributes)

relation_1nf = [{"attributes":attributes,"fds":minimal_cover(attributes, fds),"candidate_keys":candidate_keys,"prime_attributes":prime_attributes,"non_prime_attributes":non_prime_attributes}]

print("R1",relation_1nf);

relation_2nf = normalize_to_2nf(relation_1nf)
# print("\nconverted to 2NF\n\n Relations :=> ",relation_2nf,"\n")
print("\nconverted to 2NF\n\n Relations :=> ")
for i in range(0, len(relation_2nf)):
    output = ''.join(relation_2nf[i]["attributes"])
    print("R"+str(i+1)+"("+output+")", end=" ")
    printedges(relation_2nf[i]["fds"])


relation_3nf = normalize_to_3nf(relation_2nf)
# print("\nconverted to 3NF\n\n Relations :=> ",relation_3nf,"\n")
print("\nconverted to 3NF\n\n Relations :=> ")
for i in range(0, len(relation_3nf)):
    output = ''.join(relation_3nf[i]["attributes"])
    print("R"+str(i+1)+"("+output+")", end=" ")
    printedges(relation_3nf[i]["fds"])



violated_index_bcnf = []
relation_bcnf= normalize_to_bcnf(relation_1nf)
# print("\nconverted to BCNF\n\n Relations :=> ",relation_bcnf,"\n")
print("\nconverted to BCNF\n\n Relations :=> \n")
for i in range(0, len(relation_bcnf)):
    output = ''.join(relation_bcnf[i]["attributes"])
    print("R"+str(i+1)+"("+output+")", end=" ")
    printedges(relation_bcnf[i]["fds"])


print("\nLJ_testing",LJ_tester(relation_1nf,relation_bcnf))

 

# print("closure",find_closure(attributes, fds, [""]))

minimal_fds = minimal_cover(attributes, fds)
print("\nMinimal Cover \n",minimal_fds) # [

minimal_3NF = minimal_to_3nf(attributes,minimal_fds);
print("\nconverted to MINIMAL 3NF\n\n Relations :=> \n")
for i in range(0, len(minimal_3NF)):
    output = ''.join(minimal_3NF[i]["attributes"])
    print("R"+str(i+1)+"("+output+")", end=" ")
    printedges(minimal_3NF[i]["fds"])