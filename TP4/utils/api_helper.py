import requests


class RequestsApi:
    """Wrapper class to enrich python requests library."""
    def __init__(self, base_url, **kwargs):
        """Initialises an instance of this wrapper api class."""
        self.base_url = base_url
        self.session = requests.Session()
        for arg in kwargs:
            if isinstance(kwargs[arg], dict):
                kwargs[arg] = self.__deep_merge(getattr(self.session, arg), kwargs[arg])
            setattr(self.session, arg, kwargs[arg])

    def request(self, method, url, **kwargs):
        """Trigger generic HTTP method calls."""
        return self.session.request(method, self.base_url+url, **kwargs)

    def head(self, url, **kwargs):
        """Trigger HTTP head requests."""
        return self.session.head(self.base_url+url, **kwargs)

    def get(self, url, **kwargs):
        """Trigger HTTP get requests."""
        return self.session.get(self.base_url+url, **kwargs)

    def post(self, url, **kwargs):
        """Trigger HTTP post requests."""
        return self.session.post(self.base_url+url, **kwargs)

    def put(self, url, **kwargs):
        """Trigger HTTP put requests."""
        return self.session.put(self.base_url+url, **kwargs)

    def patch(self, url, **kwargs):
        """Trigger HTTP patch requests."""
        return self.session.patch(self.base_url+url, **kwargs)

    def delete(self, url, **kwargs):
        """Trigger HTTP delete requests."""
        return self.session.delete(self.base_url+url, **kwargs)

    @staticmethod
    def __deep_merge(source, destination):
        for key, value in source.items():
            if isinstance(value, dict):
                node = destination.setdefault(key, {})
                RequestsApi.__deep_merge(value, node)
            else:
                destination[key] = value
        return destination
