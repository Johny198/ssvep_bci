from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations
import sys
import pyqtgraph as pg
import numpy as np


class Board:
    def __init__(self, board_id):
        # to check required parameters for specific board, check docs of brainflow
        parameters = BrainFlowInputParams()
        parameters.serial_port = 'COM3'  # to check port --> Device Manager --> Ports
        self.streaming_board = BoardShim(board_id, parameters)
        self.eeg_channels = self.streaming_board.get_eeg_channels(board_id)
        self.num_points = len(self.eeg_channels)*self.streaming_board.get_sampling_rate(board_id)
        self.sampling_rate = self.streaming_board.get_sampling_rate(board_id)


class App:
    def __init__(self, board_id, state, is_finished,mp_array):
        self.app = pg.QtGui.QApplication(sys.argv)
        self.board = Board(board_id)
        self.state = state
        self.is_finished = is_finished
        self.mp_array = mp_array

    def stream_data(self):
        self.board.streaming_board.prepare_session()
        self.board.streaming_board.start_stream(45000)

    def stop_streaming(self):
        self.board.streaming_board.stop_stream()
        self.board.streaming_board.release_session()

    def add_plots(self):
        win = pg.GraphicsLayoutWidget(title='Brain waves Plot',
                                      size=(800, 600), show=True)
        self.p = Plot(win=win, channels=self.board.eeg_channels)  # creates empty plots
        timer = pg.Qt.QtCore.QTimer()
        timer.timeout.connect(self.update_plots)
        timer.start(25)  # every 25ms executes update_plot function
        sys.exit(self.app.instance().exec_())


    def update_plots(self):  # updates data from each plot
        if self.is_finished.value == 1: #when stimuli are finished  exits the program
            sys.exit()
        if self.state.value != 0: #no need to display signal if there is no stimulus
            self.data = self.board.streaming_board.get_current_board_data(601)[1:5,:]
            self.data[0,600] = self.state.value #value of state is saved in last column
            for i in range(len(self.board.eeg_channels)):
                DataFilter.detrend(self.data[i,:600], DetrendOperations.CONSTANT.value)
                DataFilter.perform_bandstop(data=self.data[i,:600], sampling_rate=self.board.sampling_rate,  # bandstop filter 32-52
                                            center_freq=42, band_width=20, order=6,  #
                                            filter_type=FilterTypes.BUTTERWORTH.value, ripple=0)
                DataFilter.perform_bandpass(data=self.data[i,:600], sampling_rate=self.board.sampling_rate,  # bandpass filter 8-32
                                            center_freq=20, band_width=24, order=6,
                                            filter_type=FilterTypes.BUTTERWORTH.value, ripple=0)
                self.p.curves[i].setData(self.data[i,:600].tolist())
            if len(self.data[0]) == 601:
                flattened = self.data.flatten(order = 'C') #reshapes data into 1d
                for idx, num in enumerate(self.mp_array):
                    self.mp_array[idx] = flattened[idx] #share data between processes
class Plot:
    def __init__(self, channels, win):
        self.curves = []
        for i in range(len(channels)):  # adds empty plots to the main window
            p = win.addPlot(row=i, col=0, title='Channel {:d}'.format(i+1))
            p.hideAxis('bottom')
            p.hideAxis('left')
            curve = p.plot(pen=(255, 0, 0))
            self.curves.append(curve)


def run(state, is_finished, mp_array):
    a = App(state = state, board_id=1, is_finished = is_finished, mp_array = mp_array)  # 1 for Ganglion, 2 for Cyton
    a.stream_data()
    a.add_plots()
    a.stop_streaming()
