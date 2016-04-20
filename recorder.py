import matplotlib
matplotlib.use('TkAgg') # THIS MAKES IT FAST!
import numpy
import scipy
import struct
import pyaudio
import threading
import pylab
import struct

class SwhRecorder:
    """Simple, cross-platform class to record from the microphone."""

    def __init__(self):
        """minimal garb is executed when class is loaded."""
        self.RATE=48100
        self.BUFFERSIZE=2**12 #1024 is a good buffer size
        self.secToRecord=.1
        self.threadsDieNow=False
        self.newAudio=False
        # note:freq(hZ)    
        self.THRESHOLD = 40000
        self.notes = {
                        1:{'C':32.703,
                        'C#/Db':34.648,
                        'D':36.708,
                        'D#/Eb':38.891,	
                        'E':41.203,
                        'F#/Gb':46.249,
                        'G':48.999,
                        'G#/Ab':51.913,
                        'A':55,
                        'A#/Bb':58.27,
                        'B':61.735},
                        
                        2:{'C':65.406,	
                        'C#/Db':69.296,
                        'D':73.416,
                        'D#/Eb':77.782,
                        'E':82.407,
                        'F':87.307,
                        'F#/Gb':92.499,
                        'G':97.999,
                        'G#/Ab':103.826,
                        'A':110,
                        'A#/Bb':116.541,
                        'B':123.471},
                        
                        3:{'C':130.813,
                        'C#/Db':138.591,
                        'D':146.832,
                        'D#/Eb':155.563,
                        'E':164.814,
                        'F':174.614,
                        'F#/Gb':184.997,
                        'G':195.998,
                        'G#/Ab':207.652,
                        'A':220,
                        'A#/Bb':233.082,
                        'B':246.942},
                        
                        4:{'C':261.626,
                        'C#/Db':277.183,
                        'D':293.665,
                        'D#/Eb':311.127,
                        'E':329.628,
                        'F':349.228,
                        'F#/Gb':369.994,
                        'G':391.995,
                        'G#/Ab':415.305,
                        'A':440,
                        'A#/Bb':466.164,
                        'B':493.883},
                        
                        5:{'C':523.251,
                        'C#/Db':554.365,
                        'D':587.33,
                        'D#/Eb':622.254,
                        'E':659.255,
                        'F':698.456,
                        'F#/Gb':739.989,
                        'G':783.991,
                        'G#/Ab':830.609,
                        'A':880,
                        'A#/Bb':932.328,
                        'B':987.767},
                        
                        6:{'C':1046.502,
                        'C#/Db':1108.731,
                        'D':1174.659,
                        'D#/Eb':1244.508,
                        'E':1318.51,
                        'F':1396.913,
                        'F#/Gb':1479.978,
                        'G':1567.982,
                        'G#/Ab':1661.219,
                        'A':1760,
                        'A#/Bb':1864.655,
                        'B':1975.533},
                        
                        7:{'C':2093.005,
                        'C#/Db':2217.461,
                        'D':2349.318,
                        'D#/Eb':2489.016,
                        'E':2637.021,
                        'F':2793.826,
                        'F#/Gb':2959.955,
                        'G':3135.964,
                        'G#/Ab':3322.438,
                        'A':3520,
                        'A#/Bb':3729.31,
                        'B':3951.066},
                        
                        8:{'C':4186.009,
                        'C#/Db':4434.922,
                        'D':4698.636,
                        'D#/Eb':4978.032,
                        'E':5274.042,
                        'F':5587.652,
                        'F#/Gb':5919.91,
                        'G':6271.928,
                        'G#/Ab':6644.876,
                        'A':7040,
                        'A#/Bb':7458.62,
                        'B':7902.132},
                        
                        9:{'C':8372.018,
                        'C#/Db':8869.844,
                        'D':9397.272,
                        'D#/Eb':9956.064,
                        'E':10548.084,
                        'F':11175.304,
                        'F#/Gb':11839.82,
                        'G':12543.856,
                        'G#/Ab':13289.752,
                        'A':14080,
                        'A#/Bb':14917.24,
                        'B':15804.26}
                    }
                    
        self.ranges = [
        (0,	16.8375),
        (16.8375,	17.839),
        (17.839,	18.8995),
        (18.8995,	20.023),
        (20.023,	21.214),
        (21.214,	22.4755),
        (22.4755,	23.8115),
        (23.8115,	25.2275),
        (25.2275,	26.728),
        (26.728,	28.3175),
        (28.3175,	30.0015),
        (30.0015,	31.7855),
        (31.7855,	33.6755),
        (33.6755,	35.678),
        (35.678,	37.7995),
        (37.7995,	40.047),
        (40.047,	42.4285),
        (42.4285,	44.9515),
        (44.9515,	47.624),
        (47.624,	50.456),
        (50.456,	53.4565),
        (53.4565,	56.635),
        (56.635,	60.0025),
        (60.0025,	63.5705),
        (63.5705,	67.351),
        (67.351,	71.356),
        (71.356,	75.599),
        (75.599,	80.0945),
        (80.0945,	84.857),
        (84.857,	89.903),
        (89.903,	95.249),
        (95.249,	100.9125),
        (100.9125,	106.913),
        (106.913,	113.2705),
        (113.2705,	120.006),
        (120.006,	127.142),
        (127.142,	134.702),
        (134.702,	142.7115),
        (142.7115,	151.1975),
        (151.1975,	160.1885),
        (160.1885,	169.714),
        (169.714,	179.8055),
        (179.8055,	190.4975),
        (190.4975,	201.825),
        (201.825,	213.826),
        (213.826,	226.541),
        (226.541,	240.012),
        (240.012,	254.284),
        (254.284,	269.4045),
        (269.4045,	285.424),
        (285.424,	302.396),
        (302.396,	320.3775),
        (320.3775,	339.428),
        (339.428,	359.611),
        (359.611,	380.9945),
        (380.9945,	403.65),
        (403.65,	427.6525),
        (427.6525,	453.082),
        (453.082,	480.0235),
        (480.0235,	508.567),
        (508.567,	538.808),
        (538.808,	570.8475),
        (570.8475,	604.792),
        (604.792,	640.7545),
        (640.7545,	678.8555),
        (678.8555,	719.2225),
        (719.2225,	761.99),
        (761.99,	807.3),
        (807.3,	855.3045),
        (855.3045,	906.164),
        (906.164,	960.0475),
        (960.0475,	1017.1345),
        (1017.1345,	1077.6165),
        (1077.6165,	1141.695),
        (1141.695,	1209.5835),
        (1209.5835,	1281.509),
        (1281.509,	1357.7115),
        (1357.7115,	1438.4455),
        (1438.4455,	1523.98),
        (1523.98,	1614.6005),
        (1614.6005,	1710.6095),
        (1710.6095,	1812.3275),
        (1812.3275,	1920.094),
        (1920.094,	2034.269),
        (2034.269,	2155.233),
        (2155.233,	2283.3895),
        (2283.3895,	2419.167),
        (2419.167,	2563.0185),
        (2563.0185,	2715.4235),
        (2715.4235,	2876.8905),
        (2876.8905,	3047.9595),
        (3047.9595,	3229.201),
        (3229.201,	3421.219),
        (3421.219,	3624.655),
        (3624.655,	3840.188),
        (3840.188,	4068.5375),
        (4068.5375,	4310.4655),
        (4310.4655,	4566.779),
        (4566.779,	4838.334),
        (4838.334,	5126.037),
        (5126.037,	5430.847),
        (5430.847,	5753.781),
        (5753.781,	6095.919),
        (6095.919,	6458.402),
        (6458.402,	6842.438),
        (6842.438,	7249.31),
        (7249.31,	7680.376),
        (7680.376,	8137.075),
        (8137.075,	8620.931),
        (8620.931,	9133.558),
        (9133.558,	9676.668),
        (9676.668,	10252.074),
        (10252.074,	10861.694),
        (10861.694,	11507.562),
        (11507.562,	12191.838),
        (12191.838,	12916.804),
        (12916.804,	13684.876),
        (13684.876,	14498.62),
        (14498.62,	15360.752),
        (15360.752,	20000)
        ]
        
        self.chords = [
        'C',
        'C# / Db',
        'D',
        'D# / Eb',
        'E',
        'F',
        'F# / Gb',
        'G',
        'G# / Ab',
        'A',
        'A# / Bb',
        'B',
        'C',
        'C# / Db',
        'D',
        'D# / Eb',
        'E',
        'F',
        'F# / Gb',
        'G',
        'G# / Ab',
        'A',
        'A# / Bb',
        'B',
        'C',
        'C# / Db',
        'D',
        'D# / Eb',
        'E',
        'F',
        'F# / Gb',
        'G',
        'G# / Ab',
        'A',
        'A# / Bb',
        'B',
        'C',
        'C# / Db',
        'D',
        'D# / Eb',
        'E',
        'F',
        'F# / Gb',
        'G',
        'G# / Ab',
        'A',
        'A# / Bb',
        'B',
        'C',
        'C# / Db',
        'D',
        'D# / Eb',
        'E',
        'F',
        'F# / Gb',
        'G',
        'G# / Ab',
        'A',
        'A# / Bb',
        'B',
        'C',
        'C# / Db',
        'D',
        'D# / Eb',
        'E',
        'F',
        'F# / Gb',
        'G',
        'G# / Ab',
        'A',
        'A# / Bb',
        'B',
        'C',
        'C# / Db',
        'D',
        'D# / Eb',
        'E',
        'F',
        'F# / Gb',
        'G',
        'G# / Ab',
        'A',
        'A# / Bb',
        'B',
        'C',
        'C# / Db',
        'D',
        'D# / Eb',
        'E',
        'F',
        'F# / Gb',
        'G',
        'G# / Ab',
        'A',
        'A# / Bb',
        'B',
        'C',
        'C# / Db',
        'D',
        'D# / Eb',
        'E',
        'F',
        'F# / Gb',
        'G',
        'G# / Ab',
        'A',
        'A# / Bb',
        'B',
        'C',
        'C# / Db',
        'D',
        'D# / Eb',
        'E',
        'F',
        'F# / Gb',
        'G',
        'G# / Ab',
        'A',
        'A# / Bb',
        'B'
        ]
        
        self.circle = {
        'C':['C', 'Dm', 'Em', 'F', 'G', 'Am'],
        'C# / Db':['C#', 'D#m', 'E#m', 'F#', 'G#', 'A#m'],
        'D':['D', 'Em', 'F#m', 'G', 'A', 'Bm'],
        'D# / Eb':['Eb', 'Fm', 'Gm', 'Ab', 'Bb', 'Cm'],
        'E':['E', 'F#m', 'G#m', 'A', 'B', 'C#m'],
        'F':['F', 'Gm', 'Am', 'Bb', 'C', 'Dm'],
        'F# / Gb':['F#', 'G#m', 'A#m', 'B', 'C#', 'D#m'],
        'G':['G', 'Am', 'Bm', 'C', 'D', 'Em'],
        'G# / Ab':['Ab', 'Bbm', 'Cm', 'Db', 'Eb', 'Fm'],
        'A':['A', 'Bm', 'C#m', 'D', 'E', 'F#m'],
        'A# / Bb':['Bb', 'Cm', 'Dm', 'Eb', 'F', 'Gm'],
        'B':['B', 'C#m', 'D#m', 'E', 'F#', 'G#m']
        }
        
        self.last_played = ''

#        for freq in self.notes.values():
#            
#        self.frequencies = self.notes.values().values()
#        self.ranges = []
#        lower_bound = 0
#        upper_bound = (self.frequencies[0]+self.frequencies[1])/2
#        self.ranges.append([lower_bound, upper_bound])
#        
#        for i in range(1, len(self.frequencies)-1):
#            lower_bound = upper_bound
#            upper_bound = (self.frequencies[i]+self.frequencies[i+1])/2       
#            self.ranges.append([lower_bound, upper_bound])
#            
#        lower_bound = upper_bound
#        upper_bound = self.frequencies[-1]*2
#        self.ranges.append([lower_bound, upper_bound])

        print 'chords: ', len(self.chords), 'ranges', len(self.ranges)




    def setup(self):
        """initialize sound card."""
        #TODO - windows detection vs. alsa or something for linux
        #TODO - try/except for sound card selection/initiation

        self.buffersToRecord=int(self.RATE*self.secToRecord/self.BUFFERSIZE)
        if self.buffersToRecord==0: self.buffersToRecord=1
        self.samplesToRecord=int(self.BUFFERSIZE*self.buffersToRecord)
        self.chunksToRecord=int(self.samplesToRecord/self.BUFFERSIZE)
        self.secPerPoint=1.0/self.RATE

        self.p = pyaudio.PyAudio()
        self.inStream = self.p.open(format=pyaudio.paInt16,channels=1,
            rate=self.RATE,input=True,frames_per_buffer=self.BUFFERSIZE)
        self.xsBuffer=numpy.arange(self.BUFFERSIZE)*self.secPerPoint
        self.xs=numpy.arange(self.chunksToRecord*self.BUFFERSIZE)*self.secPerPoint
        self.audio=numpy.empty((self.chunksToRecord*self.BUFFERSIZE),dtype=numpy.int16)               

    def close(self):
        """cleanly back out and release sound card."""
        self.p.close(self.inStream)

    ### RECORDING AUDIO ###  

    def getAudio(self):
        """get a single buffer size worth of audio."""
        audioString=self.inStream.read(self.BUFFERSIZE)
        return numpy.fromstring(audioString,dtype=numpy.int16)

    def record(self,forever=True):
        """record secToRecord seconds of audio."""
        while True:
            if self.threadsDieNow: break
            for i in range(self.chunksToRecord):
                self.audio[i*self.BUFFERSIZE:(i+1)*self.BUFFERSIZE]=self.getAudio()
            self.newAudio=True 
            if forever==False: break

    def continuousStart(self):
        """CALL THIS to start running forever."""
        self.t = threading.Thread(target=self.record)
        self.t.start()

    def continuousEnd(self):
        """shut down continuous recording."""
        self.threadsDieNow=True

    ### MATH ###

    def fft(self,data=None,trimBy=10,logScale=False,divBy=100):
        if data==None: 
            data=self.audio.flatten()
        left,right=numpy.split(numpy.abs(numpy.fft.fft(data)),2)
        ys=numpy.add(left,right[::-1])
        if logScale:
            ys=numpy.multiply(20,numpy.log10(ys))
        xs=numpy.arange(self.BUFFERSIZE/2,dtype=float)
        if trimBy:
            i=int((self.BUFFERSIZE/2)/trimBy)
            ys=ys[:i]
            xs=xs[:i]*self.RATE/self.BUFFERSIZE
        if divBy:
            ys=ys/float(divBy)
        return xs,ys
        
    def getNote(self, xs, ys):
        play_next = []
        # this filters out the noise, only continues if there        
        if max(ys) > self.THRESHOLD:
            
            # gets the most frequent frequency
            high_freq = numpy.argmax(ys)
            
            # the frequency of the most frequent frequency
            played_freq = xs[high_freq]
            
            # finds which chord correspends to the frequency
            loc = [i for i, rng in enumerate(self.ranges) if played_freq > rng[0] and played_freq <= rng[1]]
            chord = self.chords[loc[0]]
            play_next = self.circle[chord]
            
            # only prints if different from last chord
            if play_next != self.last_played:
                self.last_played = play_next
                return [chord, play_next]
