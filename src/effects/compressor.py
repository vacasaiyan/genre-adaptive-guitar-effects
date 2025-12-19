"""
Compressor effect using envelope follower and gain reduction.
"""
import numpy as np


class Compressor:
    """Dynamic range compressor."""
    
    def __init__(self, sr=44100, threshold=-20.0, ratio=4.0, 
                 attack=0.005, release=0.1, makeup_gain=1.0):
        """
        Initialize compressor.
        
        Args:
            sr: Sampling rate
            threshold: Threshold in dB
            ratio: Compression ratio
            attack: Attack time in seconds
            release: Release time in seconds
            makeup_gain: Output makeup gain
        """
        self.sr = sr
        self.threshold = threshold
        self.ratio = ratio
        self.makeup_gain = makeup_gain
        
        # Attack/release coefficients
        self.attack_coeff = np.exp(-1.0 / (attack * sr))
        self.release_coeff = np.exp(-1.0 / (release * sr))
        
        # Envelope follower state
        self.envelope = 0.0
        
    def process(self, audio):
        """
        Apply compression to audio.
        
        Args:
            audio: Input audio (numpy array)
            
        Returns:
            Compressed audio
        """
        output = np.zeros_like(audio)
        
        for i in range(len(audio)):
            # Envelope follower
            input_level = np.abs(audio[i])
            
            if input_level > self.envelope:
                # Attack
                self.envelope = self.attack_coeff * self.envelope + \
                               (1.0 - self.attack_coeff) * input_level
            else:
                # Release
                self.envelope = self.release_coeff * self.envelope + \
                               (1.0 - self.release_coeff) * input_level
            
            # Convert to dB
            envelope_db = 20 * np.log10(self.envelope + 1e-10)
            
            # Calculate gain reduction
            if envelope_db > self.threshold:
                # Above threshold: compress
                gain_db = self.threshold + (envelope_db - self.threshold) / self.ratio
                gain_reduction = gain_db - envelope_db
            else:
                # Below threshold: unity gain
                gain_reduction = 0.0
            
            # Convert back to linear
            gain = 10 ** (gain_reduction / 20.0)
            
            # Apply gain and makeup gain
            output[i] = audio[i] * gain * self.makeup_gain
        
        return output.astype(np.float32)
    
    def set_params(self, threshold=None, ratio=None, makeup_gain=None):
        """Update compressor parameters."""
        if threshold is not None:
            self.threshold = threshold
        if ratio is not None:
            self.ratio = ratio
        if makeup_gain is not None:
            self.makeup_gain = makeup_gain
    
    def reset(self):
        """Reset envelope state."""
        self.envelope = 0.0
