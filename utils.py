__author__ = 'ahadu_tsegaye'


def convert_seconds_to_sexagesimals(duration_sec):
    h, m_tmp = divmod(float(duration_sec) / 3600, 1)
    m = convert_to_quarters(m_tmp * 60)
    return '{},{}'.format(int(h), int(m))


def convert_to_quarters(minutes):
    m = -1
    if minutes < 15:
        m = 0
    elif minutes < 30:
        m = 25
    elif minutes < 45:
        m = 50
    elif minutes < 60:
        m = 75
    return m


def get_value_if_key_exists(akey, amap):
    value = None
    if akey in amap:
        value = amap[akey]
    return value


def read_file_as_list(filename):
    with open(filename) as data_file:
        data_list = data_file.readlines()
    return [x.strip() for x in data_list]
