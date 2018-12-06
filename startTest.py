from multiprocessing import Process
import os
import sys
path = os.path.dirname(os.path.realpath(__file__))
def f(num):
    usernames = ["test0001", "test0003", "test0004"]
    os.system("python3 {0}/client/start.py {1}".format(path, usernames[num]))

if __name__ == '__main__':

    # print(sys.argv)
    for num in range(3):
        Process(target=f, args=(num, )).start()