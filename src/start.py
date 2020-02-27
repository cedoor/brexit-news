import sys
import time

import src.daily_mirror as daily_mirror
import src.daily_star as daily_star
import src.indipendent as indipendent
import src.the_guardian as the_guardian
import src.the_sun as the_sun
import src.the_telegraph as the_telegraph


max_attempts = 3


def run_all():
    daily_mirror.start()
    daily_star.start()
    indipendent.start()
    the_guardian.start()
    the_sun.start()
    the_telegraph.start()


def get_error_info(error):
    for info in error:
        print("\t%s" % info)


def error_handler(newspaper):
    for attempt in range(max_attempts + 1):
        try:
            {
                "0": daily_mirror.start,
                "1": daily_star.start,
                "2": indipendent.start,
                "3": the_guardian.start,
                "4": the_sun.start,
                "5": the_telegraph.start,
                "9": run_all
            }[newspaper]()
            break

        except: # catch *all* exceptions
            error = sys.exc_info()

            if attempt >= max_attempts:
                error = sys.exc_info()
                print("\n\nToo many attempts. Closing program")
                print("Last error:")
                get_error_info(error)
                break
            
            print("\n\nAn error occurred:")
            get_error_info(error)
            print()

            seconds = 10 * (attempt + 1)
            while seconds >= 0:
                sys.stdout.write("\rRestarting function in %s sec\033[K" % (seconds))
                time.sleep(1)
                seconds -= 1
            
            print("\n\n")


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
error_handler(newspaper)
