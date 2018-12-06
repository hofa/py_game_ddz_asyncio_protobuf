# protoc 协议生成
protoc -I=. --python_out=./proto sb.proto

protoc -I=. --python_out=./protocols game.proto
protoc -I=. --python_out=./client/protocols game.proto