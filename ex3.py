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
        plt.xlabel('Queue Count')
        plt.ylabel('num of Packets')
        plt.show()

    elif data_type == "drop_rate":
        y_axis = [x[2] * 100 for x in data]
        x_axis = [x + 1 for x in range(len(y_axis))]
        plt.plot(x_axis, y_axis)
        plt.title('Drop Rate of ' + name)
        plt.xlabel('Queue Count')
        plt.ylabel('percentage of drop')
        plt.show()

    elif data_type == "avg_time":
        y_axis = [x[0] for x in data]
        x_axis = [x + 1 for x in range(len(y_axis))]
        plt.plot(x_axis, y_axis)
        plt.title('Avg Time of ' + name)
        plt.xlabel('Queue Count')
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
    loc1 = 'experiment_3_data/exp_3_Reno_DropTail_'
    loc2 = 'experiment_3_data/exp_3_Reno_RED_'
    loc3 ='experiment_3_data/exp_3_Sack1_DropTail_'
    loc4 ='experiment_3_data/exp_3_Sack1_RED_'
    data_creation(dataset, 'Reno_DropTail', loc1)
    data_creation(dataset, 'Reno_RED', loc2)
    data_creation(dataset, 'Sack_DropTail', loc3)
    data_creation(dataset, 'Sack_RED', loc4)

    print(dataset.keys())
    graph_maker('drop_rate', dataset['Reno_DropTail'], 'Reno DropTail')
    graph_maker('drop_rate', dataset['Reno_RED'], 'Reno RED')
    graph_maker('drop_rate', dataset['Sack_DropTail'], 'Sack DropTail')
    graph_maker('drop_rate', dataset['Sack_RED'],'Sack RED')

    graph_maker('avg_time', dataset['Reno_DropTail'], 'Reno DropTail')
    graph_maker('avg_time', dataset['Reno_RED'], 'Reno RED')
    graph_maker('avg_time', dataset['Sack_DropTail'], 'Sack DropTail')
    graph_maker('avg_time', dataset['Sack_RED'], 'Sack RED')

    graph_maker('packets', dataset['Reno_DropTail'], 'Reno DropTail')
    graph_maker('packets', dataset['Reno_RED'], 'Reno RED')
    graph_maker('packets', dataset['Sack_DropTail'], 'Sack DropTail')
    graph_maker('packets', dataset['Sack_RED'], 'Sack RED')


if __name__ == "__main__":
    main()