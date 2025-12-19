"""
Real-time audio feature extraction for genre classification.
Extracts MFCCs and other features from buffered audio windows.
"""
import numpy as np
import librosa


class FeatureExtractor:
    """Extract audio features from real-time audio buffers."""
    
    def __init__(self, sr=44100, n_mfcc=20, hop_length=512):
        """
        Initialize feature extractor.
        
        Args:
            sr: Sampling rate
            n_mfcc: Number of MFCC coefficients
            hop_length: Hop length for feature extraction
        """
        self.sr = sr
        self.n_mfcc = n_mfcc
        self.hop_length = hop_length
        
    def extract_features(self, audio_buffer):
        """
        Extract features from audio buffer.
        Matches GTZAN dataset features (58 total).
        
        Args:
            audio_buffer: numpy array of audio samples
            
        Returns:
            Feature vector (numpy array) with 58 features
        """
        # Ensure audio is 1D
        if len(audio_buffer.shape) > 1:
            audio_buffer = np.mean(audio_buffer, axis=1)
        
        # CRITICAL: Trim/pad to exactly 66149 samples to match GTZAN training data
        # This is necessary because the length feature in training data is constant
        GTZAN_SEGMENT_LENGTH = 66149
        if len(audio_buffer) > GTZAN_SEGMENT_LENGTH:
            audio_buffer = audio_buffer[:GTZAN_SEGMENT_LENGTH]
        elif len(audio_buffer) < GTZAN_SEGMENT_LENGTH:
            audio_buffer = np.pad(audio_buffer, (0, GTZAN_SEGMENT_LENGTH - len(audio_buffer)))
        
        features = []
        
        # 1. Length (number of samples, not seconds - matches GTZAN CSV format)
        features.append(len(audio_buffer))
        
        # 2. Chroma STFT (mean and variance)
        chroma_stft = librosa.feature.chroma_stft(y=audio_buffer, sr=self.sr, hop_length=self.hop_length)
        features.append(np.mean(chroma_stft))
        features.append(np.var(chroma_stft))
        
        # 3. RMS (mean and variance)
        rms = librosa.feature.rms(y=audio_buffer, hop_length=self.hop_length)
        features.append(np.mean(rms))
        features.append(np.var(rms))
        
        # 4. Spectral centroid (mean and variance)
        spectral_centroid = librosa.feature.spectral_centroid(y=audio_buffer, sr=self.sr, hop_length=self.hop_length)
        features.append(np.mean(spectral_centroid))
        features.append(np.var(spectral_centroid))
        
        # 5. Spectral bandwidth (mean and variance)
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=audio_buffer, sr=self.sr, hop_length=self.hop_length)
        features.append(np.mean(spectral_bandwidth))
        features.append(np.var(spectral_bandwidth))
        
        # 6. Spectral rolloff (mean and variance)
        spectral_rolloff = librosa.feature.spectral_rolloff(y=audio_buffer, sr=self.sr, hop_length=self.hop_length)
        features.append(np.mean(spectral_rolloff))
        features.append(np.var(spectral_rolloff))
        
        # 7. Zero crossing rate (mean and variance)
        zcr = librosa.feature.zero_crossing_rate(y=audio_buffer, hop_length=self.hop_length)
        features.append(np.mean(zcr))
        features.append(np.var(zcr))
        
        # 8. Harmony and perceptr (mean and variance)
        try:
            y_harm, y_perc = librosa.effects.hpss(audio_buffer)
            features.append(np.mean(y_harm))
            features.append(np.var(y_harm))
            features.append(np.mean(y_perc))
            features.append(np.var(y_perc))
        except:
            # If HPSS fails, use zeros
            features.extend([0.0, 0.0, 0.0, 0.0])
        
        # 9. Tempo
        try:
            tempo, _ = librosa.beat.beat_track(y=audio_buffer, sr=self.sr)
            features.append(float(tempo))
        except:
            features.append(120.0)  # Default tempo
        
        # 10. MFCCs (20 coefficients, mean and variance)
        mfccs = librosa.feature.mfcc(y=audio_buffer, sr=self.sr, n_mfcc=self.n_mfcc, hop_length=self.hop_length)
        for i in range(self.n_mfcc):
            features.append(float(np.mean(mfccs[i])))
        for i in range(self.n_mfcc):
            features.append(float(np.var(mfccs[i])))
        
        return np.array(features, dtype=np.float32)
    
    def get_feature_dim(self):
        """Return the dimensionality of feature vector."""
        # 1 (length) + 2 (chroma) + 2 (rms) + 2 (centroid) + 2 (bandwidth) + 
        # 2 (rolloff) + 2 (zcr) + 4 (harmony/perceptr) + 1 (tempo) + 40 (mfcc mean+var)
        return 58
