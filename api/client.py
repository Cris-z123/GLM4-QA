import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from config.settings import API_BASE_URL, API_KEY


class APIClient:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        self.session = self._create_session()

    def _create_session(self):
        """
        创建带重试机制的 Session
        """
        session = requests.Session()
        retries = Retry(
            total=3,  # 最大重试次数
            backoff_factor=1,  # 重试间隔
            status_forcelist=[500, 502, 503, 504]  # 需要重试的状态码
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    def get_data(self, endpoint, params=None):
        """
        GET请求
        :param endpoint: API端点
        :param params: 请求数据
        :return: 响应数据
        """
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def post_data(self, endpoint, data):
        """
        POST请求
        :param endpoint: API端点
        :param data: 请求数据
        :return: 响应数据
        """
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
