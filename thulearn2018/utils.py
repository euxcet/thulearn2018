def size_format(size_b):
    if(size_b < 1024):
        return "%.2f"%(size_b) + 'B'
    elif(size_b < 1024 * 1024):
        return "%.2f"%(size_b / 1024) + 'KB'
    elif(size_b < 1024 * 1024 * 1024):
        return "%.2f"%(size_b / 1024 / 1024) + 'MB'
    elif(size_b > 1024 * 1024 * 1024 * 1024):
        return "%.2f"%(size_b / 1024 / 1024 / 1024) + 'GB'
