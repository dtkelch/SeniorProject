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
        self.notes = {
                    'C':    16.351,	
                    'C# / Db':	17.324,	
                    'D':	18.354,	
                    'D# / Eb':	19.445,	
                    'E':	20.601,	
                    'F':	21.827,	
                    'F# / Gb':	23.124,	
                    'G':	24.499,	
                    'G# / Ab':	25.956,	
                    'A':	27.5,	
                    'A# / Bb':	29.135,	
                    'B':	30.868,	
                    'C':	32.703,	
                    'C# / Db':	34.648,	
                    'D':	36.708,	
                    'D# / Eb':	38.891,	
                    'E':	41.203,	
                    'F# / Gb':	46.249,	
                    'G':	48.999,	
                    'G# / Ab':	51.913,	
                    'A':	55,	
                    'A# / Bb':	58.27,	
                    'B':	61.735,	
                    'C':	65.406,	
                    'C# / Db':	69.296,	
                    'D':	73.416,	
                    'D# / Eb':	77.782,	
                    'E':	82.407,	
                    'F':	87.307,	
                    'F# / Gb':	92.499,	
                    'G':	97.999,	
                    'G# / Ab':	103.826,	
                    'A':	110,	
                    'A# / Bb':	116.541,	
                    'B':	123.471,	
                    'C':	130.813,	
                    'C# / Db':	138.591,	
                    'D':	146.832,	
                    'D# / Eb':	155.563,	
                    'E':	164.814,	
                    'F':	174.614,	
                    'F# / Gb':	184.997,	
                    'G':	195.998,	
                    'G# / Ab':	207.652,	
                    'A':	220,	
                    'A# / Bb':	233.082,	
                    'B':	246.942,	
                    'C':	261.626,	
                    'C# / Db':	277.183,	
                    'D':	293.665,	
                    'D# / Eb':	311.127,	
                    'E':	329.628,	
                    'F':	349.228,	
                    'F# / Gb':	369.994,	
                    'G':	391.995,	
                    'G# / Ab':	415.305,	
                    'A':	440,	
                    'A# / Bb':	466.164,	
                    'B':	493.883,	
                    'C':	523.251,	
                    'C# / Db':	554.365,	
                    'D':	587.33,	
                    'D# / Eb':	622.254,	
                    'E':	659.255,	
                    'F':	698.456,	
                    'F# / Gb':	739.989,	
                    'G':	783.991,	
                    'G# / Ab':	830.609,	
                    'A':	880,	
                    'A# / Bb':	932.328,	
                    'B':	987.767,	
                    'C':	1046.502,	
                    'C# / Db':	1108.731,	
                    'D':	1174.659,	
                    'D# / Eb':	1244.508,	
                    'E':	1318.51,	
                    'F':	1396.913,	
                    'F# / Gb':	1479.978,	
                    'G':	1567.982,	
                    'G# / Ab':	1661.219,	
                    'A':	1760,	
                    'A# / Bb':	1864.655,	
                    'B':	1975.533,	
                    'C':	2093.005,	
                    'C# / Db':	2217.461,	
                    'D':	2349.318,	
                    'D# / Eb':	2489.016,	
                    'E':	2637.021,	
                    'F':	2793.826,	
                    'F# / Gb':	2959.955,	
                    'G':	3135.964,	
                    'G# / Ab':	3322.438,	
                    'A':	3520,	
                    'A# / Bb':	3729.31,	
                    'B':	3951.066,	
                    'C':	4186.009,	
                    'C# / Db':	4434.922,	
                    'D':	4698.636,	
                    'D# / Eb':	4978.032,	
                    'E':	5274.042,	
                    'F':	5587.652,	
                    'F# / Gb':	5919.91,	
                    'G':	6271.928,	
                    'G# / Ab':	6644.876,	
                    'A':	7040,	
                    'A# / Bb':	7458.62,	
                    'B':	7902.132,	
                    'C':	8372.018,	
                    'C# / Db':	8869.844,	
                    'D':	9397.272,	
                    'D# / Eb':	9956.064,	
                    'E':	10548.084,	
                    'F':	11175.304,	
                    'F# / Gb':	11839.82,	
                    'G':	12543.856,	
                    'G# / Ab':	13289.752,	
                    'A':	14080,	
                    'A# / Bb':	14917.24,	
                    'B':	15804.264
                    }

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

    def downsample(self,data,mult):
        """Given 1D data, return the binned average."""
        overhang=len(data)%mult
        if overhang: data=data[:-overhang]
        data=numpy.reshape(data,(len(data)/mult,mult))
        data=numpy.average(data,1)
        return data    

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
        freq = xs[numpy.argmax(ys)]
        print("xs max: ", freq)

    ### VISUALIZATION ###

    def plotAudio(self):
        """open a matplotlib popup window showing audio data."""
        pylab.plot(self.audio.flatten())
        pylab.show()