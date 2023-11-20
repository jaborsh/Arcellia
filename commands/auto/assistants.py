import time

from openai import OpenAI
from server.conf.secret_settings import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

string_subs = {
    "–": "-",
    "—": "-",
}


def create_thread():
    return client.beta.threads.create().id


class Assistant:
    def __init__(self):
        self.id = None
        self.thread = create_thread()

    def ask(self, query):
        client.beta.threads.messages.create(
            thread_id=self.thread,
            role="user",
            content=query,
        )
        run = client.beta.threads.runs.create(
            thread_id=self.thread,
            assistant_id=self.id,
        )
        run = self.wait_on_run(run, self.thread)
        messages = client.beta.threads.messages.list(thread_id=self.thread, limit=1)
        text = messages.data[0].content[0].text.value
        print(text)
        for i, j in string_subs.items():
            text = text.replace(i, j)
        return text

    def wait_on_run(self, run, thread):
        while run.status == "queued" or run.status == "in_progress":
            run = client.beta.threads.runs.retrieve(
                thread_id=thread,
                run_id=run.id,
            )
            time.sleep(0.5)
        return run


class Designer(Assistant):
    def __init__(self):
        super().__init__()
        self.id = "asst_QV9gKtfRNuTYhi8sCWHw9sob"
