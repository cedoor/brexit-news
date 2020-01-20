import src.the_guardian as the_guardian
import src.the_sun as the_sun


def start(newspaper):
    print()

    return {
        "0": the_guardian.start,
        "1": the_sun.start
    }[newspaper]()


print("""
[0] The Guardian
[1] The Sun

Choose the newspaper to scrape: """, end="")

start(input())
