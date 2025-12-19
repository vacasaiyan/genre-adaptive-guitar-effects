"""
Chorus effect using delayed modulated copies.
"""
import numpy as np


class Chorus:
    """Chorus effect."""
    
    def __init__(self, sr=44100, rate=1.5, depth=0.003, mix=0.5):
        """
        Initialize chorus effect.
        
        Args:
            sr: Sampling rate
            rate: LFO rate in Hz
            depth: Modulation depth in seconds
            mix: Wet/dry mix
        """
        self.sr = sr
        self.rate = rate
        self.depth = depth
        self.mix = mix
        
        # Delay buffer (max 50ms)
        self.max_delay_samples = int(0.05 * sr)
        self.buffer = np.zeros(self.max_delay_samples)
        self.write_pos = 0
        
        # LFO phase
        self.lfo_phase = 0.0
        
    def process(self, audio):
        """
        Apply chorus to audio.
        
        Args:
            audio: Input audio (numpy array)
            
        Returns:
            Processed audio
        """
        output = np.zeros_like(audio)
        
        for i in range(len(audio)):
            # Write input to buffer
            self.buffer[self.write_pos] = audio[i]
            
            # Generate LFO (sine wave)
            lfo = np.sin(2 * np.pi * self.lfo_phase)
            self.lfo_phase += self.rate / self.sr
            if self.lfo_phase >= 1.0:
                self.lfo_phase -= 1.0
            
            # Calculate delay in samples
            delay_samples = int(self.depth * self.sr * (1.0 + lfo) / 2.0)
            delay_samples = np.clip(delay_samples, 0, self.max_delay_samples - 1)
            
            # Read from buffer with delay
            read_pos = (self.write_pos - delay_samples) % self.max_delay_samples
            delayed = self.buffer[read_pos]
            
            # Mix dry and wet
            output[i] = self.mix * delayed + (1.0 - self.mix) * audio[i]
            
            # Update write position
            self.write_pos = (self.write_pos + 1) % self.max_delay_samples
        
        return output.astype(np.float32)
    
    def set_params(self, rate=None, depth=None, mix=None):
        """Update effect parameters."""
        if rate is not None:
            self.rate = rate
        if depth is not None:
            self.depth = depth
        if mix is not None:
            self.mix = mix
    
    def reset(self):
        """Reset buffer and LFO phase."""
        self.buffer.fill(0.0)
        self.write_pos = 0
        self.lfo_phase = 0.0
