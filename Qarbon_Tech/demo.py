l1 = [{"V":"S001"},{"V":"S002"},{"VI":"S001"},{"VI":"S005"},{"VII":"S005"},{"V":"S009"},{"VIII":"S007"}]
unique_values = set()
for i in l1:
    for j in i:
        unique_values.add(i[j])
result = {"Unique Values" : unique_values}
print(result)

