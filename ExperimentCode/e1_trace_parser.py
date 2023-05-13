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

def data_creation():
    new_reno_data = []
    newReno = 'experiment_data/exp_1_Newreno_'
    for x in range(10):
        new_reno_data.append(average_time(newReno + str(x + 1) + ".tr"))
    reno_data = []
    Reno = 'experiment_data/exp_1_Reno_'
    for x in range(10):
        reno_data.append(average_time(Reno + str(x + 1) + ".tr"))
    tahoe_data = []
    Tahoe = 'experiment_data/exp_1_Tahoe_'
    for x in range(10):
        tahoe_data.append(average_time(Tahoe + str(x + 1) + ".tr"))

    vegas_data = []
    Vegas = 'experiment_data/exp_1_Vegas_'
    for x in range(10):
       vegas_data.append(average_time(Vegas + str(x + 1) + ".tr"))
    dataset = {"NewReno": new_reno_data, "Reno":reno_data, "Tahoe": tahoe_data, "Vegas" : vegas_data}
    return dataset

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
def main():
    #average time of packets, packets tranfered, packets dropped
    dataset = data_creation()
    print(dataset['Tahoe'])
    # print(dataset['Tahoe'])
    print(dataset.keys())
    graph_maker('drop_rate', dataset['Reno'], 'Reno')
    graph_maker('drop_rate', dataset['NewReno'], 'New Reno')
    graph_maker('drop_rate', dataset['Tahoe'], 'Tahoe')
    graph_maker('drop_rate', dataset['Vegas'],'Vegas')

    graph_maker('avg_time', dataset['Reno'], 'Reno')
    graph_maker('avg_time', dataset['NewReno'], 'New Reno')
    graph_maker('avg_time', dataset['Tahoe'], 'Tahoe')
    graph_maker('avg_time', dataset['Vegas'], 'Vegas')

    graph_maker('packets', dataset['Reno'], 'Reno')
    graph_maker('packets', dataset['NewReno'], 'New Reno')
    graph_maker('packets', dataset['Tahoe'], 'Tahoe')
    graph_maker('packets', dataset['Vegas'], 'Vegas')






if __name__ == "__main__":
    main()