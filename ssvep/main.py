from multiprocessing import Process, Value

def get_bci_data(state, is_finished):
    from ssvep.modules.signal import display
    display.run(state, is_finished)

def display_stimuli(state, is_finished):
    from ssvep.modules.stimuli import stimulus
    stimulus.draw(state, is_finished)




if __name__ == '__main__':
    state = Value('i',0)
    is_finished = Value('i',0)
    proc1 = Process(target = get_bci_data, args = (state,is_finished))
    proc2 = Process(target = display_stimuli, args = (state,is_finished))
    proc2.start()
    proc1.start()
    proc2.join()
    proc1.join()
