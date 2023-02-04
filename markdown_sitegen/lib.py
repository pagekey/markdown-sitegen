

def get_root_path(relpath):
    res = ''
    # Get the number of slashes
    num_dirs = len(list(filter(lambda x: len(x) > 0, relpath.split('/'))))
    for i in range(num_dirs):
        res += '../'
    return res
