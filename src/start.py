import src.guardian as guardian


def start(newspaper):
    print()

    return {
        "0": guardian.start
    }[newspaper]()


print("""
[0] Guardian

Choose the newspaper to scrape: """, end="")

start(input())
