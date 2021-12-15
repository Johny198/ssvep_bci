from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes
import sys
import pyqtgraph as pg


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
    def __init__(self, board_id):
        self.app = pg.QtGui.QApplication(sys.argv)
        self.board = Board(board_id)
    def stream_data(self):
        self.board.streaming_board.prepare_session()
        self.board.streaming_board.start_stream(45000)
    def stop_streaming(self):
        self.board.streaming_board.stop_stream()
        self.board.streaming_board.release_session()
    def filter(self):
        self.is_filtered = not self.is_filtered
    def add_plots(self):
        win = pg.GraphicsLayoutWidget(title='Brain waves Plot',
                                           size=(800, 600), show=True)
        self.p = Plot(win = win, channels = self.board.eeg_channels ) # creates empty plots
        self.is_filtered = False
        timer = pg.Qt.QtCore.QTimer()
        timer.timeout.connect(self.update_plots)
        timer.start(25) # every 25ms executes update_plot function
        sys.exit(self.app.instance().exec_())


    def update_plots(self): # updates data from each plot
        data = self.board.streaming_board.get_current_board_data(self.board.num_points)
        if self.is_filtered == True:
            for i,channel in enumerate(self.board.eeg_channels):
                DataFilter.perform_bandstop( data=data[channel], sampling_rate=self.board.sampling_rate, #bandstop filter 49-51
                                            center_freq = 50, band_width = 2, order = 4,
                                            filter_type = FilterTypes.BUTTERWORTH.value, ripple = 0)
                DataFilter.perform_bandpass(data = data[channel], sampling_rate=self.board.sampling_rate, # bandpass filter 1-49
                                            center_freq = 25, band_width = 48, order = 4,
                                            filter_type = FilterTypes.BUTTERWORTH.value, ripple = 0 )
                self.p.curves[i].setData(data[channel].tolist())
        else:
            for i,channel in enumerate(self.board.eeg_channels): # if is_filtered == False displays signal without filtering
                self.p.curves[i].setData(data[channel].tolist())

class Plot:
    def __init__(self,channels, win):
        self.curves = []
        for i,channel in enumerate(channels): #adds empty plots to the main window
            p = win.addPlot(row=i, col=0, title='Channel {:d}'.format(channel))
            p.hideAxis('bottom')
            p.hideAxis('left')
            curve = p.plot( pen=(255, 0, 0))
            self.curves.append(curve)

def main():
    a = App(board_id = 1) # 1 for Ganglion, 2 for Cyton
    a.stream_data()
    a.add_plots()
    a.stop_streaming()

if __name__ == "__main__":
    main()
