def invert(dict):
    inverted_list={}
    for key in dict:
        if dict[key] in inverted_list:
            inverted_list[dict[key]].append(key)
        else:
            inverted_list[dict[key]] = [key]
    for key in dict:
        inverted_list[dict[key]].sort()
    return inverted_list

if __name__ == "__main__":
    dict={1:"abc",3:"a",72:"abc",9:"bop",4:"adw",5:"adw",6:"a",7:"abc",8:"a",10:"bop",2:"bop"}
    print (invert(dict))
