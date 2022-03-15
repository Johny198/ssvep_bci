from multiprocessing import Process, Value, Array


def get_bci_data(state,is_finished,mp_array):
    from ssvep.modules.signal import display
    display.run(state, is_finished,mp_array) 

def display_stimuli(state,is_finished):
    from ssvep.modules.stimuli import stimulus
    stimulus.draw(state,is_finished)

def extract(mp_array,is_finished):
    from ssvep.modules.signal import extraction
    extraction.cca(mp_array,is_finished)

if __name__ == '__main__':
    state = Value('i',0)
    last_state = Value('i',0)
    is_finished = Value('i',0)
    mp_array = Array('d', 2404)

    proc1 = Process(target = get_bci_data, args = (state,is_finished,mp_array))
    proc2 = Process(target = display_stimuli, args = (state, is_finished))
    proc3 = Process(target = extract, args = (mp_array, is_finished))
    proc2.start()
    proc1.start()
    proc3.start()
    proc2.join()
    proc1.join()
    proc3.join()
