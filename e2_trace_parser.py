import matplotlib.pyplot as plt

def average_time(file_name):
    packet_count = 0
    letterCheck = None
    time = []
    startTime = 0
    drop = 0
    with open(file_name, 'r') as file:
        for index, line in enumerate(file):
            values = line.split(' ')

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
        droprate = drop/packet_count
    else:
        droprate = 0.00
    return (average_time, packet_count, droprate)




def graph_maker(data_type, data, name):
    if data_type == "packets":
        y_axis = [x[1] for x in data]
        x_axis = [x + 1 for x in range(len(y_axis))]
        plt.plot(x_axis, y_axis)
        plt.title(name + ' Packets')
        plt.xlabel('CBR Rate')
        plt.ylabel('num of Packets')
        plt.show()

    elif data_type == "drop_rate":
        y_axis = [x[2] * 100 for x in data]
        x_axis = [x + 1 for x in range(len(y_axis))]
        plt.plot(x_axis, y_axis)
        plt.title('Drop Rate of ' + name)
        plt.xlabel('CBR Rate')
        plt.ylabel('percentage of drop')
        plt.show()

    elif data_type == "avg_time":
        y_axis = [x[0] for x in data]
        x_axis = [x + 1 for x in range(len(y_axis))]
        plt.plot(x_axis, y_axis)
        plt.title('Avg Time of ' + name)
        plt.xlabel('CBR Rate')
        plt.ylabel('packet transfer average')
        plt.show()

def data_creation(dataset, name, location):
    data = []
    for x in range(10):
        data.append(average_time(location + str(x + 1) + ".tr"))
    dataset[name] = data

def main():
    #average time of packets, packets tranfered, packets dropped
    dataset = dict()
    loc1 = 'experiment_2_data/exp_2_Reno_Reno_'
    loc2 = 'experiment_2_data/exp_2_Reno_Newreno_'
    loc3 ='experiment_2_data/exp_2_Vegas_Newreno_'
    loc4 ='experiment_2_data/exp_2_Vegas_Vegas_'
    data_creation(dataset, 'Reno_Reno', loc1)
    data_creation(dataset, 'Reno_Newreno', loc2)
    data_creation(dataset, 'Vegas_Newreno', loc3)
    data_creation(dataset, 'Vegas_Vegas', loc4)

    print(dataset.keys())
    graph_maker('drop_rate', dataset['Reno_Reno'], 'Reno Reno')
    graph_maker('drop_rate', dataset['Reno_Newreno'], 'Reno Newreno')
    graph_maker('drop_rate', dataset['Vegas_Newreno'], 'Vegas Newreno')
    graph_maker('drop_rate', dataset['Vegas_Vegas'],'Vegas Vegas')

    graph_maker('avg_time', dataset['Reno_Reno'], 'Reno Reno')
    graph_maker('avg_time', dataset['Reno_Newreno'], 'Reno Newreno')
    graph_maker('avg_time', dataset['Vegas_Newreno'], 'Vegas Newreno')
    graph_maker('avg_time', dataset['Vegas_Vegas'], 'Vegas Vegas')

    graph_maker('packets', dataset['Reno_Reno'], 'Reno Reno')
    graph_maker('packets', dataset['Reno_Newreno'], 'Reno Newreno')
    graph_maker('packets', dataset['Vegas_Newreno'], 'Vegas Newreno')
    graph_maker('packets', dataset['Vegas_Vegas'], 'Vegas Vegas')


if __name__ == "__main__":
    main()