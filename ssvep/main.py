from multiprocessing import Process, Value

def get_bci_data(state):
    from ssvep.modules.signal import display
    display.run(state)

def display_stimuli(state):
    from ssvep.modules.stimuli import stimulus
    stimulus.draw(state)




if __name__ == '__main__':
    state = Value('i',0)
    proc1 = Process(target = get_bci_data, args = (state,))
    proc2 = Process(target = display_stimuli, args = (state,))
    proc2.start()
    proc1.start()
    proc2.join()
    proc1.join()
