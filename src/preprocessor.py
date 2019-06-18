import librosa

class Preprocessor:
	def __init__(self, raw_x, raw_y):
		self.raw_x, self.raw_y = raw_x, raw_y
		self.preprocess()

	def preprocess(self):
		pass

	def preprocess_wf(self, fn):
		# Load the audio as a waveform 'y'
		# Store the sampling rate as 'sr'
		y, sr = librosa.load(fn)
		# Set the hop length; at 22050 Hz, 512 samples ~= 23ms
		hop_length = 512

		# Separate harmonics and percussives into two waveforms
		y_harmonic, y_percussive = librosa.effects.hpss(y)

		# Beat track on the percussive signal
		tempo, beat_frames = librosa.beat.beat_track(y=y_percussive,
													 sr=sr)

		# Compute MFCC features from the raw signal
		mfcc = librosa.feature.mfcc(y=y, sr=sr, hop_length=hop_length,
									n_mfcc=13)

		# And the first-order differences (delta features)
		mfcc_delta = librosa.feature.delta(mfcc)

		# Stack and synchronize between beat events
		# This time, we'll use the mean value (default) instead of median
		beat_mfcc_delta = librosa.util.sync(np.vstack([mfcc, mfcc_delta]),
											beat_frames)

		# Compute chroma features from the harmonic signal
		chromagram = librosa.feature.chroma_cqt(y=y_harmonic,
												sr=sr)
