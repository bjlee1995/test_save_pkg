from NIPA_DB import nipa_mariadb
import time, traceback, logging, os

def sort_packet_data(packet_data):
    data_list = []
    data_count = 0
    data_dic = {}
    for data in packet_data:
        sensor = data['SENSOR_ID']
        packet_num = data['PACKET_NUM']
        if not sensor in data_dic:
            data_dic[sensor] = data_count
            data_list.append([])
            data_count += 1
        data_list[data_dic[sensor]].append(packet_num)
    return data_dic, data_list

def loss_rate_cal(sensor_packet):
    first, last = sensor_packet[0], sensor_packet[-1]
    list_legnth = len(sensor_packet)
    data_length = last - first + 1
    if data_length < 0:
        data_length += 256
    receive_rate = 100 - round(list_legnth / data_length * 100, 2)
    return list_legnth, data_length, receive_rate

def insert_form(data_column_one, data_column_two):
    result = []
    for sensor, sensor_packet in zip(data_column_one, data_column_two):
        receive_rate = loss_rate_cal(sensor_packet)
        temp_list = [sensor, receive_rate[2], receive_rate[0], receive_rate[1]]
        result.append(temp_list)
    return result

def main():
    while True:
        try:
            maria_db_packet = nipa_mariadb()
            ttime = 300
            packet_data = maria_db_packet.select_sec(column='SENSOR_ID, PACKET_NUM',
                                                     table='T_SENSOR_PACKETNUM', sec=ttime)
            if packet_data == ():
                continue

            available_sensor_dic, packet_list = sort_packet_data(packet_data)
            available_sensor_list = available_sensor_dic.keys()
            msg = insert_form(available_sensor_list, packet_list)
            maria_db_packet.sensor_error_insert(msg)
            time.sleep(ttime)
        except:
            logging.error(traceback.print_exc())
            time.sleep(ttime)

if __name__ == '__main__':
    pwd = os.getcwd()
    path = '/root/nipa/gen/log/error.log'
    logging.basicConfig(filename=path,
                        level=logging.DEBUG, format='%(asctime)s %(message)s')
    logging.info('WOREKR DATA SCRIPT is executed')
    main()
