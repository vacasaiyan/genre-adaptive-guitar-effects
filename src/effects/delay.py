"""
Delay effect using circular buffer.
"""
import numpy as np


class Delay:
    """Delay/echo effect."""
    
    def __init__(self, sr=44100, delay_time=0.3, feedback=0.4, mix=0.3):
        """
        Initialize delay effect.
        
        Args:
            sr: Sampling rate
            delay_time: Delay time in seconds
            feedback: Feedback amount (0.0-0.95)
            mix: Wet/dry mix
        """
        self.sr = sr
        self.delay_time = delay_time
        self.feedback = feedback
        self.mix = mix
        
        # Delay buffer (max 2 seconds)
        self.max_delay_samples = int(2.0 * sr)
        self.buffer = np.zeros(self.max_delay_samples)
        self.write_pos = 0
        
        self.update_delay_samples()
        
    def update_delay_samples(self):
        """Update delay samples based on delay time."""
        self.delay_samples = int(self.delay_time * self.sr)
        self.delay_samples = np.clip(self.delay_samples, 1, self.max_delay_samples - 1)
        
    def process(self, audio):
        """
        Apply delay to audio.
        
        Args:
            audio: Input audio (numpy array)
            
        Returns:
            Delayed audio
        """
        output = np.zeros_like(audio)
        
        for i in range(len(audio)):
            # Read delayed sample
            read_pos = (self.write_pos - self.delay_samples) % self.max_delay_samples
            delayed = self.buffer[read_pos]
            
            # Write input + feedback to buffer
            self.buffer[self.write_pos] = audio[i] + delayed * self.feedback
            
            # Mix dry and wet
            output[i] = (1.0 - self.mix) * audio[i] + self.mix * delayed
            
            # Update write position
            self.write_pos = (self.write_pos + 1) % self.max_delay_samples
        
        return output.astype(np.float32)
    
    def set_params(self, delay_time=None, feedback=None, mix=None):
        """Update delay parameters."""
        if delay_time is not None:
            self.delay_time = delay_time
            self.update_delay_samples()
        if feedback is not None:
            self.feedback = np.clip(feedback, 0.0, 0.95)
        if mix is not None:
            self.mix = mix
    
    def reset(self):
        """Reset delay buffer."""
        self.buffer.fill(0.0)
        self.write_pos = 0
