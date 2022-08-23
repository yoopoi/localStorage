def dictSliceKey(data,key):
    _dict = {}
    for key in data:
        if key != "extra":
            _dict[key] = data[key]
    return _dict