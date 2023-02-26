import itertools

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
            flag =0
            for j in range(0,len(candidate_keys)):
                if(candidate_keys[j].issubset(set(subset))):
                    flag = 1
                    break
            if flag==1:
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

def is_in_2NF(prime_attributes,non_prime_attributes,candidate_keys,fds):
    problem_dependencies = []
    for index, fd in enumerate(fds):
        if set(fd['right']).issubset(non_prime_attributes):
            flag = 0
            for s in candidate_keys:
                if len(set(fd['left']))!=len(s) and set(fd['left']).issubset(s) :
                    flag = 1
                    break  # Stop checking if a match is found
            if(flag):
                problem_dependencies.append(index)
    
    if len(problem_dependencies)==0:
        return [True,problem_dependencies]
    else:
        return [False,problem_dependencies]


def check_3nf(attributes, fds,candidate_keys,prime_attributes):
    
    temp_violated_list = []
    print(fds)
    # Check if every functional dependency is in 3NF
    for index,fd in enumerate(fds):
        left = fd['left']
        right = fd['right']
        # Check if every attribute in Y is a prime attribute of R
        print("This",right,prime_attributes)
        if set(right).issubset(prime_attributes):
            continue
        # Check if X is a superkey for R
        # print(left,candidate_keys)
        flag = 0
        for i in range(0,len(candidate_keys)):
            if candidate_keys[i].issubset(set(left)) :
                flag = 1
        if flag == 1:
            continue
        # print("yay")
        temp_violated_list.append(index)
        
    return temp_violated_list


def normalize_to_2nf(attributes, fds,violated_index):

    normalized_relations = [{"attributes":set(attributes),"fds":fds}]
    for vindex in violated_index:
        print(fds[vindex])
        # Identify the A, B, and C sets
        k = len(normalized_relations)-1
        A = set(fds[vindex]['left'])
        B = set(fds[vindex]['right'])
        R2 = A.union(B)
        # R1 = find_closure(normalized_relations[k]["attributes"],normalized_relations[k]["fds"], A)
        
        # Create the new relations R1 and R2
        C = normalized_relations[k]["attributes"]-A-B
        R1 = A.union(C)
        # R2 = set(normalized_relations[k]["attributes"].copy())-find_closure(normalized_relations[k]["attributes"],normalized_relations[k]["fds"], B)

        tempfds = normalized_relations[k]["fds"].copy()
        tempfds.remove(fds[vindex])
        i = 0
        while i<len(tempfds):
            if set(tempfds[i]["left"]).issubset(R1) and set(tempfds[i]["right"]).issubset(R1):
                i = i
            else:
                del tempfds[i]
                i=i-1
            i=i+1

        # Add the new relations to the list of normalized relations
        normalized_relations.append({"attributes":R2,"fds":[fds[vindex]]})
        normalized_relations.append({"attributes":R1,"fds":tempfds})
        del normalized_relations[k]

    # print(normalized_relations,"\n")
    return normalized_relations
 
def printedges(fds):
    for i in range(0,len(fds)):
        input = ''.join(str(num) for num in fds[i]["left"])
        output = ''.join(str(num) for num in fds[i]["right"])
        print(input+"->"+output,end="  ")
    print("")
# A->C, B->DE, D->C
# Example usage:
# attributes = ['A', 'B', 'C', 'D', 'E']
# fds = [
#     {'left': ['A'], 'right': ['C']},
#     {'left': ['B'], 'right': ['D','E']},
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
output = ''.join(str(num) for num in attributes)
print("R(",output,") ",end="")
printedges(fds)
candidate_keys = find_candidate_keys(attributes, fds)
print(candidate_keys)

prime_attributes = find_prime_attributes(candidate_keys)
print("Prime Attributes",prime_attributes)

non_prime_attributes = set(attributes) - prime_attributes
# print("Non Prime Attributes",non_prime_attributes)

is_2nf,violated_index_2NF = is_in_2NF(prime_attributes,non_prime_attributes,candidate_keys,fds)
# print(is_2nf,violated_index)

in_2nf = normalize_to_2nf(attributes,fds,violated_index_2NF)
for i in range(0,len(in_2nf)):
    output = ''.join(in_2nf[i]["attributes"])
    print("R"+str(i+1)+"("+output+")",end=" ")
    printedges(in_2nf[i]["fds"])
    in_2nf[i]["candidate_keys"]=find_candidate_keys(in_2nf[i]["attributes"], in_2nf[i]["fds"])
    in_2nf[i]["prime_attributes"]=find_prime_attributes(in_2nf[i]["candidate_keys"])


print(in_2nf)
violated_index_3nf = []
final_3nf = []
for i in range(0,len(in_2nf)):
    violated_index_3nf.append(check_3nf(in_2nf[i]["attributes"], in_2nf[i]["fds"], in_2nf[i]["candidate_keys"],in_2nf[i]["prime_attributes"]))
    print(violated_index_3nf)
    final_3nf.append(normalize_to_2nf(in_2nf[i]["attributes"], in_2nf[i]["fds"],violated_index_3nf[i]))
    
     
print(final_3nf)

