from locust import HttpUser, task

class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        self.client.get("/hello-world-orjson")
        #self.client.get("/hello-world-orjson")