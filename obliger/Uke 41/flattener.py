a = ["this", ["is", ["a", "list"]]]

def flattening(liste: list):
    new_list = []
    for i in liste:
        if type(i) == list:
            i = flattening(i)
            new_list += i
        else:
            new_list.append(i)
    return new_list

a = flattening(a)
print(a)