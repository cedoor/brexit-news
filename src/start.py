import src.the_guardian as the_guardian


def start(newspaper):
    print()

    return {
        "0": the_guardian.start
    }[newspaper]()


print("""
[0] The Guardian

Choose the newspaper to scrape: """, end="")

start(input())
