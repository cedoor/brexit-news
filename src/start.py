import src.daily_mirror as daily_mirror
import src.daily_star as daily_star
import src.indipendent as indipendent
import src.the_guardian as the_guardian
import src.the_sun as the_sun
import src.the_telegraph as the_telegraph


def run_all():
    the_guardian.start()
    the_sun.start()
    daily_star.start()
    the_telegraph.start()
    daily_mirror.start()
    indipendent.start()


newspaper = input("""
[0] Daily Mirror
[1] Daily Star
[2] Indipendent
[3] The Guardian
[4] The Sun
[5] The Telegraph

[9] All the above


Choose the newspaper to scrape: """)

print()

{
    "0": daily_mirror.start,
    "1": daily_star.start,
    "2": indipendent.start,
    "3": the_guardian.start,
    "4": the_sun.start,
    "5": the_telegraph.start,
    "9": run_all
}[newspaper]()
