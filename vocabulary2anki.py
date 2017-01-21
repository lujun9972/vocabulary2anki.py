import dictionary.baiCiZhanDictionary

def output_dict(d,keys,sep='|'):
    vals = map(lambda key:d.get(key),keys)
    return sep.join(vals)
