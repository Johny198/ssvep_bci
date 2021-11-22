from psychopy import visual, event


class Experiment_Window:
    def __init__(self, size, screen_nr, color):
        self.win = visual.Window(size = size, screen = screen_nr, monitor = 'testMonitor', fullscr = True, color = color)
        self.im_list = []
        self.text_list = []
    def add_im_stim(self, path, pos, color):
        self.im_stim = visual.ImageStim(win = self.win, image = path, units = 'pix', pos = pos, colorSpace = 'rgb', color = color)
        self.im_list.append(self.im_stim)
    def add_text_stim(self,pos,color, text):
        self.text_stim = visual.TextStim(win=self.win, text = text, pos = pos, color = color, units = 'pix')
        self.text_list.append(self.text_stim)
    def add_shape_stim(self, pos, color, vert, size, ori):
        self.shape_stim = visual.ShapeStim(win = self.win, units = 'pix', size = size, pos = pos, fillColor = color, lineColor = color, vertices = vert, ori = ori)

# parameters
fps = 60
win0 = Experiment_Window(size = [1536,864], screen_nr = 0, color = 'black') # screen_nr = 1 displays window on external screen
win0.add_im_stim(path = 'face_l.png',pos = (-90,0), color = (1,0,1) )
win0.add_im_stim(path = 'face_r.png', pos = (90,0), color = (1,0,1))
win0.add_im_stim(path = 'vase.png', pos = (0,0), color = (1,1,1))
vert = [(-0.4,0.05),(-0.4,-0.05),(-.2,-0.05),(-.2,-0.1),(0,0),(-.2,0.1),(-.2,0.05)]
win0.add_shape_stim(pos = (-180,0), color = 'yellow', size = 250, vert = vert, ori = 0)
win0.add_text_stim(pos = (0, 0), color = 'white', text = 'Na ekranie zobaczysz migający obraz złożony z kilku niezależnych rysunków. Twoim zadaniem jest skupienie uwagi na rysunku wskazanym przez żółtą strzałkę. Żeby przejść dalej naciśnij dowolny klawisz. ')
win0.add_text_stim(pos = (0, 0), color = 'white', text = 'To koniec. Dziękujemy za udział w badaniu.')


# drawing
win0.text_list[0].draw()
win0.win.flip()
event.waitKeys()
win0.shape_stim.autoDraw = True
for frameN in range(60):
    if frameN >= 20 and frameN < 40:
        win0.shape_stim.pos = (0,210)
        win0.shape_stim.ori = 90
    elif frameN >= 40:
        win0.shape_stim.pos = (180,0)
        win0.shape_stim.ori = 180
    if (frameN % 4) == 0: # 30hz
        win0.im_list[0].draw()
        win0.im_list[1].draw()
    if (frameN % 2) == 0: # 20 hz
        win0.im_list[2].draw()
    win0.win.flip()
win0.shape_stim.autoDraw = False
win0.win.flip()
win0.text_list[1].draw()
win0.win.flip()
event.waitKeys()

