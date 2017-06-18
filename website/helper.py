


def VideoPreview(filename):
    return u"<div style=\" width:640px; margin-right: 10px;\">" \
           u"<iframe width=\"100%%\" height=\"450\" src=\"https://www.youtube.com/embed/{}\" " \
           u"allowfullscreen></iframe>" \
           u"<br />".format(filename)