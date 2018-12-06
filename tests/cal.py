


leader = {
    "CTO": 10,
    "Leader": 5,
    "PHP": 5,
    "android": 4,
    "ios": 3,
    "h5": 3,
    "test": 3,
    "product": 3,
    "PM": 3,
    "行政": 2,
    "运维": 3,
    "DBA": 3,
    "UI": 2,
    "IM": 1,
}

group = {
    "PHP": 9,
    "Android": 7,
    "IOS": 5,
    "Test": 5,
    "H5": 5,
    "product": 4,
    "行政": 3,
    "运维": 4,
    "DBA": 3,
    "UI": 3,
    "IM": 2,
}

count = 0
for s in leader:
    count = leader[s] + count

print("leader:", count)

count = 0
for s in group:
    count = group[s] + count

print("group:", count)