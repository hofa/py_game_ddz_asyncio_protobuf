# protoc 协议生成
protoc -I=. --python_out=./proto sb.proto

protoc -I=. --python_out=./protocols game.proto
protoc -I=. --python_out=./client/protocols game.proto

# 启动服务器
python3 server.py

# 启动客户端
python3 client/start.py

# 测试式客户端启动
python3 startTest.py

# py3依赖安装
pip3 install -e requirement.txt

tag 0.0.2
