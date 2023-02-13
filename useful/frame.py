def get_gradus(toponym):
    a = str(float(toponym["boundedBy"]["Envelope"]['upperCorner'].split()[1]) -
            float(toponym["boundedBy"]["Envelope"]['lowerCorner'].split()[1]))
    b = str(float(toponym["boundedBy"]["Envelope"]['upperCorner'].split()[0]) -
            float(toponym["boundedBy"]["Envelope"]['lowerCorner'].split()[0]))
    return [a, b]
