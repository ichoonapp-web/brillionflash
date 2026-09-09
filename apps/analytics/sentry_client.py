import requests, os

class SentryAutomation:
    def __init__(self):
        self.base_url = "https://sentry.io/api/0"
        self.headers = {'Authorization': f'Bearer {os.getenv("SENTRY_TOKEN")}'}
        self.org = os.getenv("SENTRY_ORG")
    def get_unresolved_issues(self, project, limit=10):
        url = f"{self.base_url}/projects/{self.org}/{project}/issues/"
        params = {'query': 'is:unresolved', 'sort': 'date', 'limit': limit}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()
    def resolve_issue(self, issue_id):
        url = f"{self.base_url}/issues/{issue_id}/"
        payload = {'status': 'resolved'}
        response = requests.put(url, headers=self.headers, json=payload)
        return response.status_code == 200