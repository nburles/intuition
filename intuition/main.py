import tendo.singleton, multiprocessing, os
import protocol, my_owl, owl_upload, file_backup
from owl_types import ControlTypes
from signal_handler import signal_handler

me = tendo.singleton.SingleInstance()

def main():
    os.makedirs('values_to_upload', exist_ok = True)
    with signal_handler():
        write_proc = multiprocessing.Process(target = owl_upload.upload)
        write_proc.start()
        read_proc = multiprocessing.Process(target = file_backup.read_msgs)

    protocol.OwlIntuitionProtocol.datagram_received = my_owl.datagram_received
    protocol.OwlBaseMessage.enqueue = my_owl.enqueue
    protocol.OwlSolar.to_dict = my_owl.solar_dict
    protocol.OwlElectricity.to_dict = my_owl.electricity_dict
    protocol.OwlWeather.to_dict = my_owl.weather_dict
    try:
        my_owl.q.put(ControlTypes.START)
        with signal_handler():
            read_proc.start()
        protocol.start_listening()
    except:
        pass

    file_backup.q.put(ControlTypes.END)
    read_proc.join()
    my_owl.q.put(ControlTypes.END)
    write_proc.join()

if __name__ == "__main__":
    main()

