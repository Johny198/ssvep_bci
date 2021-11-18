from psychopy import visual, event, info
import sys

win0 = visual.Window([1536,864], screen = 0, monitor = 'testMonitor', fullscr = True, color = [-1,-1,-1], units = 'pix')
fps = 60
face_l = visual.ImageStim(win = win0, image='face_l.png', units='pix', size=(150,396), colorSpace='rgb255', pos = (-90,0), color = (255,255,100))
face_r = visual.ImageStim(win = win0, image='face_r.png', units='pix', size=(151,396), colorSpace='rgb255', pos = (90,0), color = (255, 120, 255))
vase = visual.ImageStim(win = win0, image='vase.png', units='pix', size=(290,396), colorSpace='rgb255', pos = (0,0), color = (255,255,255))

arrowVert = [(-0.4,0.05),(-0.4,-0.05),(-.2,-0.05),(-.2,-0.1),(0,0),(-.2,0.1),(-.2,0.05)]
arrow = visual.ShapeStim(win=win0, vertices=arrowVert, fillColor='yellow', size=250, lineColor='yellow', pos = (0,200), ori = 90, autoDraw = True)

for frameN in range(fps):
    if (frameN % 4) == 0:
        face_l.color = (255,255,100)
        face_r.color = (255,255,100)
        face_l.draw()
        face_r.draw()
    else:
        face_l.color = (255, 120, 255)
        face_r.color = (255, 120, 255)
        face_l.draw()
        face_r.draw()
    if (frameN % 2) == 0: 
        vase.draw()
    win0.flip()
