from locust import HttpUser, task, between

# Using Locust to load test the server
class User(HttpUser):
    wait_time = between(1, 4)

    @task
    def test_all(self):
        self.client.get("/api/all")

    @task(2)
    def test_first(self):
        self.client.get("/api/first")
