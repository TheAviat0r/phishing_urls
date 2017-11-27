from bcolors import bcolors
from algo import BAD_SAMPLE_CONSTANT

def get_response(answer, algo_type):
    response = bcolors.BOLD + str.ljust(answer[0].url, 40) + (' - [%s]' % algo_type)

    assert answer[1] == -9999 or answer[1] == 0 or answer[1] == 1

    if answer[1] == 0:
        response += " --->" + bcolors.BOLD + bcolors.OKGREEN + " Not phishing" + bcolors.ENDC
    if answer[1] == 1:
        response += " --->" + bcolors.BOLD + bcolors.FAIL + " Phishing" + bcolors.ENDC 
    if answer[1] == BAD_SAMPLE_CONSTANT:
        response += " --->" + bcolors.BOLD + bcolors.WARNING + " Bad sample" + bcolors.ENDC

    return response
