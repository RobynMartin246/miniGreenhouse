import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as DateFormatter
import argparse
import random

# python3 graph_csv.py control front_window front_office front_office_humidifier

def multirow_figure(control_data, files):
    fig, axes = plt.subplots(2, 1, sharex=True)
    fig.suptitle('Temp and Humidity Comparison', fontsize=16)

    files_data = {}
    
    for file in files:
        if not file:
            break
        data = np.genfromtxt(file + '.csv', delimiter=',', encoding=None, names="Time, Temp, Humidity", skip_header=1, dtype=None)
        files_data[file] = {
            'name': file,
            'temp': data["Temp"],
            'hum': data["Humidity"],
            'color': "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
        }
    c_time = control_data["Time"]
    c_temp = control_data["Temp"]
    c_hum = control_data["Humidity"]

    compare_temp = axes[0]
    compare_humidity = axes[1]

    x_range = np.arange(len(c_time), step=200)
    x_label = [x.split()[1] for x in c_time[x_range]]

    compare_temp.set_title('Temp')
    compare_temp.plot(c_time, c_temp, color='red', label='Control')
    compare_temp.set_xticks(x_range)
    
    compare_temp.grid(True, which='major', axis='y', ls='--', lw=.5, c='k', alpha=.3)

    max_length = len(c_time)
    for file, data in files_data.items():
        compare_temp.plot(c_time, data['temp'][:max_length], color=data['color'], label=file)
    
    fig.legend(bbox_to_anchor=(1, .95), ncol=3)

    compare_humidity.plot(c_time, c_hum, color='red', label='Control')
    for file, data in files_data.items():
        compare_humidity.plot(c_time, data['hum'][:max_length], color=data['color'], label=file)
    compare_humidity.set_title('Humidity')
    compare_humidity.grid(True, which='major', axis='y', ls='--', lw=.5, c='k', alpha=.3)
    compare_humidity.set_xticks(x_range)
    compare_humidity.set_xticklabels(x_label, rotation=45, ha='right')
    
    fig.tight_layout(pad=2)
    
    plt.show()

def single_row_figure(control_data, file_name):
    c_time = control_data["Time"]
    c_temp = control_data["Temp"]
    c_hum = control_data["Humidity"]

    fig = plt.figure()
    ax_1 = fig.add_subplot()
    ax_1.set_title(file_name + " Temp and Humidity") 
    ax_1.plot(c_time, c_temp, color='red', label='Temp')
    ax_1.plot(c_time, c_hum, color='steelblue', label='Humidity')
    plt.legend()
    x_range = np.arange(len(c_time), step=200)
    x_label = [x.split()[1] for x in c_time[x_range]]
    ax_1.set_xticks(x_range)
    ax_1.set_xticklabels(x_label, rotation=45, ha='right')
    # Provide tick lines across the plot 
    ax_1.grid(True, which='major', axis='y', ls='--', lw=.5, c='k', alpha=.3)
    
    fig.tight_layout(pad=2)
    plt.show()
    return

def main(control_file, *args): 
    control_data = np.genfromtxt(control_file + '.csv', delimiter=',', encoding=None, names="Time, Temp, Humidity", skip_header=1, dtype=None)
    if args[0]:
        files = args[0]
        multirow_figure(control_data, files)
    else:
        single_row_figure(control_data, control_file)
   
    # fig.savefig('temp.png')

# python3 graph_csv.py temp.txt
parser = argparse.ArgumentParser(description='Graph given CSVs')
parser.add_argument('control', metavar='Control Group FileName', type=str, nargs=1,
                    help='pass at least one filepath. The first file will be treated as the control group')
parser.add_argument('files', metavar='Additional FileNames', type=str, nargs='*',
                    help='csv files')

args = parser.parse_args()
main(args.control[0], args.files)