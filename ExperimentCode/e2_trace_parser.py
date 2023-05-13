import matplotlib.pyplot as plt

def data_retrieval(file_name):
    data = []
    with open(file_name, 'r') as file:
        for line in file:
            values = line.split(' ')
            if values[7] != '3':
                data.append((values[0], values[1], values[7]))
    return data

def data_parse(data):
    packet_count = 0
    letterCheck = None
    time = []
    startTime = 0
    drop = 0

    for index, values in enumerate(data):
        if (letterCheck == None and values[0] == "+") or letterCheck == 'r':
            letterCheck = '+'
            startTime = float(values[1])
            continue
        elif values[0] == 'r':
            packet_count += 1
            time.append(float(values[1]) - startTime)
            letterCheck = 'r'
        if values[0] == 'd':
            drop += 1

    average_time = sum(time) / len(time)
    if drop > 0:
        droprate = drop / packet_count
    else:
        droprate = 0.00
    return (average_time, packet_count, droprate)

def spliter(data):
    data1 = [x for x in data if x[2] == '1']
    data2 = [x for x in data if x[2] == '2']
    return (data_parse(data1), data_parse(data2))

def graph_maker(data, label1, label2):
    packet1 = [x[0][1] for x in data]
    packet2 = [x[1][1] for x in data]
    plt.title('Total Packets')
    plt.plot([x for x in range(1,10)],packet1, label=f"{label1} 1")
    plt.plot([x for x in range(1,10)],packet2, label=f"{label2} 2")
    plt.ylabel("Packets")
    plt.xlabel("CBR Rate")
    plt.legend()
    plt.show()

    avg1 = [x[0][0] for x in data]
    avg2 = [x[1][0] for x in data]
    plt.title('Average Time')
    plt.plot([x for x in range(1, 10)], avg1, label=f"{label1} 1")
    plt.plot([x for x in range(1, 10)],avg2, label=f"{label2} 2")
    plt.ylabel("Time in seconds")
    plt.xlabel("CBR Rate")
    plt.legend()
    plt.show()

    drop1 = [x[0][2] * 100 for x in data]
    drop2 = [x[1][2] * 100 for x in data]
    plt.title('Drop Rate')
    plt.plot([x for x in range(1, 10)], drop1, label=f"{label1} 1")
    plt.plot([x for x in range(1, 10)], drop2, label=f"{label2} 2")
    plt.ylabel("Percentage")
    plt.xlabel("CBR Rate")
    plt.legend()
    plt.show()

def data_organize(loc, label1, label2):
    whole_set = []
    for num in range(9):
        data = data_retrieval(loc + str(num + 1) + ".tr")
        result = spliter(data)
        whole_set.append(result)
    for result in whole_set:
        print(result)
    graph_maker(whole_set, label1, label2)

def main():
    data_organize("./data/exp_2_Reno_Newreno_", "Reno", "NewReno")
    data_organize("./data/exp_2_Reno_Reno_", "Reno","Reno")
    data_organize("./data/exp_2_Vegas_Newreno_", "Vegas","NewReno")
    data_organize("./data/exp_2_Vegas_Vegas_","Vegas","Vegas")


if __name__ == "__main__":
    main()