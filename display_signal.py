from brainflow.board_shim import BoardShim, BrainFlowInputParams
import sys
import pyqtgraph as pg

class Plot:
    def __init__(self, board, id):
        self.board_id = id
        self.board = board
        self.channels = self.board.get_eeg_channels(self.board_id)
        self.num_points = len(self.channels)*self.board.get_sampling_rate(self.board_id)
        self.app = pg.QtGui.QApplication(sys.argv)
        self.win = pg.GraphicsLayoutWidget(title='Brain waves Plot',
                                           size=(1000, 800), show=True)
        self.curves = []
        for i,channel in enumerate(self.channels):
            p = self.win.addPlot(row=i, col=0, title='Channel {:d}'.format(channel))
            p.hideAxis('bottom')
            p.hideAxis('left')
            curve = p.plot( pen=(255, 0, 0))
            self.curves.append(curve)
        timer = pg.Qt.QtCore.QTimer()
        timer.timeout.connect(self.update_plot)
        timer.start()
        sys.exit(self.app.instance().exec_())   
    def update_plot(self):
        data = self.board.get_current_board_data(self.num_points)
        for i,channel in enumerate(self.channels):
            self.curves[i].setData(data[channel].tolist())
        self.app.processEvents()


def main():
    # to check required parameters for specific board, check docs of brainflow
    parameters = BrainFlowInputParams()
    parameters.serial_port = 'COM3'  # to check port --> Device Manager --> Ports
    board_id = 1  # 1 for Ganglion, 2 for Cyton
    streaming_board = BoardShim(board_id, parameters)
    streaming_board.prepare_session()
    streaming_board.start_stream(50000)
    p = Plot(streaming_board, board_id)
    streaming_board.stop_stream()
    streaming_board.release_session()

if __name__ == "__main__":
    main()
