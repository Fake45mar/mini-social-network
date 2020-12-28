def get_dict_request(request):
    body_request = request.body.decode('utf-8').split('&')
    title_body_dict = {}
    for el in body_request:
        title, value = el.split('=')
        title_body_dict[title.replace('+', ' ').replace('%40', '@')] = value.replace('+', ' ').replace('%40', '@')
    return title_body_dict
