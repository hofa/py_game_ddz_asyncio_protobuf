import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from proto import sb_pb2

def main():
    loginReq = sb_pb2.LoginRequest()
    loginReq.username = "liuweilong"
    loginReq.password = "123456"
    out = loginReq.SerializeToString()  
    print(out)  

    decode = sb_pb2.LoginRequest()  
    decode.ParseFromString(out) 
    print(decode)

    print(os.path.abspath(".."))

if __name__ == '__main__':
    main()