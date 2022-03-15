from sklearn.cross_decomposition import CCA
from scipy import signal
import numpy as np



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
            self.sig_array = np.vstack([signal.square(2*np.pi*freq*t+phase*np.pi+np.pi),signal.square(2*np.pi*freq*t+phase*np.pi),signal.square(2*np.pi*freq*2*t+phase*np.pi+np.pi),signal.square(2*np.pi*freq*2*t+phase*np.pi)])
        else:
            self.type = 'sawtooth'
            self.sig_array = np.vstack([signal.sawtooth(2*np.pi*freq*t-phase*np.pi),signal.sawtooth(2*np.pi*freq*t-phase*np.pi+np.pi),signal.sawtooth(2*np.pi*freq*2*t-phase*np.pi),signal.sawtooth(2*np.pi*freq*2*t-phase*np.pi+np.pi)])



def cca(mp_array, is_finished):

    ref1 = Reference_Group(freq = 12, phase = 0.7, length = 3, waveform = 'sin')
    ref2 = Reference_Group(freq = 15, phase = 1.05, length = 3, waveform = 'square' )
    ref3 = Reference_Group(freq = 10, phase = 0.35, length = 3, waveform = 'saw' )
    refs = np.array([ref1,ref2,ref3])

    while is_finished.value != 1:
        if mp_array[0] != 0:
            shared_array = np.array(mp_array[:]).reshape(4,601) #reshape shared array to 2d, last column is state value
            corr_array = np.zeros((len(refs),1))
            if shared_array[0,600] != 0:
                for i, ref in enumerate(refs):
                    cca = CCA(n_components = 1)
                    u,v = cca.fit_transform(shared_array[:,:600].T, ref.sig_array.T)
                    corr = np.corrcoef(u.T,v.T)[0,1]
                    corr_array[i]  = corr
                    #print('Correlation coefficient for {} signal is {} \n observed state was {}'.format(ref.type,corr, int(shared_array[0,600])))
                idx = np.where(corr_array == np.max(corr_array))[0][0]
                print('Highest correlation coefficient: {} \n type of signal: {} \n state: {}'.format(np.max(corr_array), refs[idx].type, int(shared_array[0,600])))
