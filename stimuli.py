from psychopy import visual, event
import numpy as np
from scipy import signal


class Square():
    def __init__(self, size, color, pos, win):
        self.sq_stim = visual.Rect(win=win, size=(size, size), pos=pos,
                                   colorSpace='rgb', units='cm',
                                   lineColor=color, fillColor=color)

    def op_change(self, freq, phase, wave, frame):  # opacity modulation by waveform
            if wave == 'sin':
                self.sq_stim.opacity = 0.5 * (1 + np.sin(2 * np.pi *
                                              freq * (frame/60) + np.pi*phase))
            elif wave == 'square':
                self.sq_stim.opacity = 0.5 * (1 + signal.square(2 * np.pi *
                                              freq * (frame/60) + np.pi * phase))
            elif wave == 'sawtooth':
                self.sq_stim.opacity = 0.5 * (1 - signal.sawtooth(2 * np.pi *
                                              freq * (frame / 60) - np.pi * phase))
            self.sq_stim.draw()

    def change_col(self, color):  # visual cue
        self.sq_stim.color = color
        self.sq_stim.draw()


class Exp_Window():
    def __init__(self):  # creates window and lists of stimuli
        self.win = visual.Window(size=[1536, 864], units='pix',
                                 colorSpace='rgb', color=(-1, -1, -1),
                                 monitor='testMonitor', fullscr=True)
        self.text_list = []
        self.square_list = []
        self.stimuli_list = []

    def add_square(self, size, color, pos):  # adds square stimulus
        sq_stim = Square(size=size, color=color, pos=pos, win=self.win)
        self.square_list.append(sq_stim)

    def add_text(self, text, height, pos):  # adds text
        text_stim = visual.TextStim(win=self.win, text=text, height=height,
                                    pos=pos, colorSpace='rgb',
                                    color=(1, 1, 1), units='pix')
        self.text_list.append(text_stim)

    '''def add_grid(self, grid_size, color, size):  # creates grid of squares in case more stimuli were needed
        pos_y = 0
        multi = 1.5
        self.grid_size = grid_size
        for i in range(self.grid_size[0]):
            pos_x_1 = size/2 + size/4
            for j in range(int(self.grid_size[1]/2)):
                    sq_stim1 = Square(size=size, color=color,
                                      pos=(pos_x_1, pos_y), win=self.win)
                    sq_stim2 = Square(size=size, color=color,
                                      pos=(-pos_x_1, pos_y), win=self.win)
                    pos_x_1 += 1.5*size
                    self.stimuli_list.extend([sq_stim1, sq_stim2])
            if i == 0:
                pos_y = multi*size
            elif multi > 0:
                multi *= -1
            else:
                multi = multi*(-1) + 1.5
            pos_y = multi * size

    def draw_grid(self):  # draw grid of squares
        for i in range(len(self.stimuli_list)):
            self.stimuli_list[i].sq_stim.draw()

    def flash_grid(self, freq, phase_inc, waves, time):  # makes grid flicker
        combs = [(x, y) for x in waves for y in freq]  # combinations of frequency and waveform
        phase = phase_inc  # phase increment with succesive stimuli
        counter = 0
        for i in range(time):
            for j in range(self.grid_size[0]*self.grid_size[1]):  # for each stimulus changes opacity
                self.stimuli_list[j].op_change(combs[counter][1], phase_inc,
                                               combs[counter][0], i)
                counter += 1
                if counter == len(combs):
                    counter = 0
                phase_inc += phase
                if phase_inc > 2:
                    phase_inc = phase_inc - 2
            self.win.flip()'''


# DEFINE STIMULI
win0 = Exp_Window()  # create instance of Exp_Window

win0.add_square(size=5, color=(0, 1, 0), pos=(-10, 0))
win0.add_square(size=5, color=(0, 1, 0), pos=(0, 0))
win0.add_square(size=5, color=(0, 1, 0), pos=(10, 0))

win0.add_text(text='Badanie składa się z trzech prób. Twoim zadaniem jest skupienie uwagi na migającym kwadracie, wskazanym wcześniej przez wizualną wskazówkę. Aby zobaczyć wskazówkę, naciśnij dowolny klawisz', height=20, pos=(0, 0))
win0.add_text(text='Skup wzrok na żółtym kwadracie i naciśnij dowolny klawisz aby rozpocząć badanie', height=20, pos=(0, -200))
win0.add_text(text='To koniec badania. Dziękujemy za udział.', height=20, pos=(0, 0))

time = 180

# DRAWING

win0.text_list[0].draw()
win0.win.flip()
event.waitKeys()
temp = [0, 1, 2]
for i in range(len(win0.square_list)):
    rnd = np.random.choice(temp)
    temp.remove(rnd)
    win0.square_list[rnd].change_col(color=(1, 1, 0))
    for j in win0.square_list:
        j.sq_stim.draw()
    win0.text_list[1].draw()
    win0.win.flip()
    event.waitKeys()
    win0.square_list[rnd].change_col(color=(0, 1, 0))
    win0.win.flip()
    for j in range(time):
        win0.square_list[0].op_change(freq=10, wave='sawtooth', phase=0.35,
                                      frame=j)
        win0.square_list[1].op_change(freq=12, wave='sin', phase=0.7,
                                      frame=j)
        win0.square_list[2].op_change(freq=15, wave='square', phase=1.05,
                                      frame=j)
        win0.win.flip()
win0.text_list[2].draw()
win0.win.flip()
event.waitKeys()
