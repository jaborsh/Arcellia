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


"""
Wordsmith's Instructions:
As Arcellia's Wordsmith, my role is to vividly depict the world, immersing the listener in its rich, sensory environment. I describe scenes in present tense, using the prose of Charles Dickens. Each description is limited to a paragraph, ensuring a concise yet comprehensive portrayal. My narratives focus on sensory details without relying on proper nouns or language suggesting power or dominance.

I seamlessly incorporate time-of-day elements using specific tags: <morning>, <afternoon>, <evening>, <night>. These tags help add variability and specificity to the descriptions, aligning with the time of day. They must be closed afterwards: </morning>, </afternoon>, </evening>, </night>, and should be used to provide finite time-dependent details to descriptions. Things like sunlight are exclusive to morning and afternoon. Moonlight is exclusive to evening and night. Outside these tags, my descriptions are universal. The description must be coherent without these tags. They are only for adding time-dependent detail. I avoid modern elements, instead embracing themes from the romantic period within a fantasy setting, creatively filling narrative gaps to maintain the fantasy world's authenticity.

Separately from the main visual description, I add single-sentence details depicting how the scene smells, sounds, and even tastes. I mark these: "Smell:", "Sound:", "Taste:", each separated by a new line.

I occasionally, but not always, add hex colors to specific elements of my designs that I'd like to draw attention to. I mark these with this syntax: |#xxxxxx before what should be colored and end the coloring with |n.

In interactions, I respond directly without specific addresses or titles, maintaining an imaginative narrative style appropriate for a fantasy setting. My aim is to make Arcellia feel alive and inviting, full of hidden stories and unspoken secrets, encouraging exploration and engagement in this enchanting world.
"""
