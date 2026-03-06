from locust import HttpUser, task


class LogUser(HttpUser):

    @task
    def send_log(self):
        self.client.post(
            "/logs/",
            json={
                "service": "auth",
                "level": "INFO",
                "message": "login success"
            },
        )