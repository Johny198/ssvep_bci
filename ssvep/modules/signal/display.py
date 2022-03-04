from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations
import sys
import pyqtgraph as pg
from sklearn.cross_decomposition import CCA
from scipy import signal
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
    def __init__(self, board_id, state, is_finished, refs):
        self.app = pg.QtGui.QApplication(sys.argv)
        self.board = Board(board_id)
        self.state = state
        self.is_finished = is_finished
        self.refs = refs

    def stream_data(self):
        self.board.streaming_board.prepare_session()
        self.board.streaming_board.start_stream(601)

    def stop_streaming(self):
        self.board.streaming_board.stop_stream()
        self.board.streaming_board.release_session()

    def filter(self):
        self.is_filtered = not self.is_filtered

    def add_plots(self):
        win = pg.GraphicsLayoutWidget(title='Brain waves Plot',
                                      size=(800, 600), show=True)
        self.p = Plot(win=win, channels=self.board.eeg_channels)  # creates empty plots
        self.is_filtered = False
        timer = pg.Qt.QtCore.QTimer()
        timer.timeout.connect(self.update_plots)
        timer.start(25)  # every 25ms executes update_plot function
        button = pg.Qt.QtWidgets.QPushButton("Filter", win)
        button.setGeometry(720, 5, 40, 30)
        button.clicked.connect(self.filter)
        button.show()
        sys.exit(self.app.instance().exec_())

    def update_plots(self):  # updates data from each plot
        if self.is_finished.value == 1: #when stimuli are finished  exits the program
            sys.exit()
        if self.state.value != 0: #no need to display signal if there is no stimulus
            self.data = self.board.streaming_board.get_current_board_data(self.board.num_points)[1:5,:]
            if self.is_filtered is True:
                for i, channel in enumerate(self.board.eeg_channels):
                    DataFilter.detrend(self.data[i], DetrendOperations.CONSTANT.value)
                    DataFilter.perform_bandstop(data=self.data[i], sampling_rate=self.board.sampling_rate,  # bandstop filter 49-51
                                                center_freq=50, band_width=16, order=4,
                                                filter_type=FilterTypes.BUTTERWORTH.value, ripple=0)
                    DataFilter.perform_bandpass(data=self.data[i], sampling_rate=self.board.sampling_rate,  # bandpass filter 1-49
                                                center_freq=24.5, band_width=48, order=4,
                                                filter_type=FilterTypes.BUTTERWORTH.value, ripple=0)
                    self.p.curves[i].setData(self.data[i].tolist())
                if len(self.data[0]) == 600:  #CCA 
                    for ref in self.refs:
                        cca = CCA(n_components = 1)
                        u,v = cca.fit_transform(self.data.T, ref.sig_array.T)
                        corr = np.corrcoef(u.T,v.T)[0,1]
                        print('Correlation coefficient for {} signal is {} \n observed state was {}'.format(ref.type,corr, self.state.value)) #1- sawtooth stimulus 2-sinusoidal 3-square
                        DataFilter.write_file(self.data,'test.csv', 'w')

            else:
                for i, channel in enumerate(self.board.eeg_channels):  # if is_filtered == False displays signal without filtering)
                    self.p.curves[i].setData(self.data[i].tolist())


class Plot:
    def __init__(self, channels, win):
        self.curves = []
        for i, channel in enumerate(channels):  # adds empty plots to the main window
            p = win.addPlot(row=i, col=0, title='Channel {:d}'.format(channel))
            p.hideAxis('bottom')
            p.hideAxis('left')
            curve = p.plot(pen=(255, 0, 0))
            self.curves.append(curve)
            
class Reference_Group():
    def __init__(self,waveform,freq,phase, length):
        self.freq = freq
        self.phase = phase
        self.waveform = waveform
        self.length = length
        t = np.arange(0,self.length,1/200)
        if self.waveform == 'sin':
            self.type = 'sinusoidal'
            self.sig_array = np.vstack([np.sin(2*np.pi*freq*t+phase*np.pi),np.cos(2*np.pi*freq*t+phase*np.pi),np.sin(2*np.pi*freq*2*t+phase*np.pi),np.cos(2*np.pi*freq*2*t+phase*np.pi)])
        elif self.waveform == 'square':
            self.type = 'square'
            self.sig_array = np.vstack([signal.square(2*np.pi*freq*t+phase*np.pi),signal.square(2*np.pi*freq*2*t+phase*np.pi)])
        else:
            self.type = 'sawtooth'
            self.sig_array = np.vstack([signal.sawtooth(2*np.pi*freq*t-phase*np.pi),signal.sawtooth(2*np.pi*freq*2*t-phase*np.pi)])

def run(state, is_finished):
    ref1 = Reference_Group(freq = 12, phase = 0.7, length = 3, waveform = 'sin')
    ref2 = Reference_Group(freq = 15, phase = 1.05, length = 3, waveform = 'square' )
    ref3 = Reference_Group(freq = 10, phase = 0.35, length = 3, waveform = 'saw' )
    refs = np.array([ref1,ref2,ref3])
    a = App(state = state, board_id=1, refs = refs, is_finished = is_finished)  # 1 for Ganglion, 2 for Cyton
    a.stream_data()
    a.add_plots()
    a.stop_streaming()
