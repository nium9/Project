{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pydub\n",
    "import speech_recognition as sr\n",
    "import matplotlib.pyplot as plt\n",
    "from scipy.io import wavfile as wav\n",
    "from scipy.fftpack import fft\n",
    "import numpy as np\n",
    "rate, data = wav.read('Data/Data_for_stage_3/hello_internet_wav_edition.wav')\n",
    "fft_out = fft(data)\n",
    "%matplotlib inline\n",
    "plt.plot(data, np.abs(fft_out))\n",
    "plt.show()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
