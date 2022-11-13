import requests

'''Список HTTP методов'''


class Http_methods:
    headers = {'Content-Type': 'application/json'}
    cookie = ''

    @staticmethod
    def session():
        result = requests.session()
        return result
    @staticmethod
    def get(url, body =None, headers=None):
        json_body={}
        if body is not None:
            json_body.update(body)
        if headers is not None:
            Http_methods.headers.update(headers)
        result = requests.get(url, json=json_body, headers=Http_methods.headers, cookies=Http_methods.cookie)
        return result

    @staticmethod
    def post(url, body,headers=None):
        if headers is not None:
            Http_methods.headers.update(headers)
        result = requests.post(url, headers=Http_methods.headers, cookies=Http_methods.cookie, json=body)
        return result

    @staticmethod
    def put(url, body, headers=None):
        if headers is not None:
            Http_methods.headers.update(headers)
        result = requests.put(url, headers=Http_methods.headers, cookies=Http_methods.cookie, json=body)
        return result

    @staticmethod
    def delete(url, body, headers=None):
        if headers is not None:
            Http_methods.headers.update(headers)
        result = requests.delete(url, headers=Http_methods.headers, cookies=Http_methods.cookie, json=body)
        return result
