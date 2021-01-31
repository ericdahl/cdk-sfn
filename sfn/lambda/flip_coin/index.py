import random


def handler(event, context):
    return {
        "result": random.choice(["heads", "tails"])
    }


if __name__ == "__main__":
    print(handler(None, None))
