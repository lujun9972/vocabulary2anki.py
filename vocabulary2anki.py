from functools import reduce
def output_dict(d,keys,sep='|'):
    vals = map(lambda key:d.get(key),keys)
    return sep.join(vals)
