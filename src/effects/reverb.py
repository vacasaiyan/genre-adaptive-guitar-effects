"""
Simple reverb effect using multiple comb and allpass filters.
"""
import numpy as np


class Reverb:
    """Schroeder reverb using comb and allpass filters."""
    
    def __init__(self, sr=44100, room_size=0.5, damping=0.5, mix=0.3):
        """
        Initialize reverb effect.
        
        Args:
            sr: Sampling rate
            room_size: Room size (0.0-1.0)
            damping: High frequency damping (0.0-1.0)
            mix: Wet/dry mix
        """
        self.sr = sr
        self.room_size = room_size
        self.damping = damping
        self.mix = mix
        
        # Comb filter delays (in samples) - tuned for ~44.1kHz
        comb_delays = [int(sr * t / 44100) for t in [1557, 1617, 1491, 1422, 1277, 1356, 1188, 1116]]
        
        # Allpass filter delays
        allpass_delays = [int(sr * t / 44100) for t in [225, 556, 441, 341]]
        
        # Initialize comb filters
        self.comb_buffers = [np.zeros(d) for d in comb_delays]
        self.comb_positions = [0] * len(comb_delays)
        self.comb_feedback = [0.0] * len(comb_delays)
        
        # Initialize allpass filters
        self.allpass_buffers = [np.zeros(d) for d in allpass_delays]
        self.allpass_positions = [0] * len(allpass_delays)
        
        self.update_parameters()
        
    def update_parameters(self):
        """Update filter coefficients based on room size and damping."""
        # Comb filter feedback based on room size
        base_feedback = 0.84 + self.room_size * 0.1
        for i in range(len(self.comb_buffers)):
            self.comb_feedback[i] = base_feedback
            
    def process(self, audio):
        """
        Apply reverb to audio.
        
        Args:
            audio: Input audio (numpy array)
            
        Returns:
            Reverbed audio
        """
        output = np.zeros_like(audio)
        
        for i in range(len(audio)):
            # Sum all comb filter outputs
            comb_sum = 0.0
            
            for j, (buffer, pos) in enumerate(zip(self.comb_buffers, self.comb_positions)):
                # Read from buffer
                delayed = buffer[pos]
                
                # Apply damping (simple lowpass)
                filtered = delayed * (1.0 - self.damping) + \
                          self.comb_feedback[j] * delayed * self.damping
                
                # Write to buffer
                buffer[pos] = audio[i] + filtered * self.comb_feedback[j]
                
                # Update position
                self.comb_positions[j] = (pos + 1) % len(buffer)
                
                comb_sum += delayed
            
            # Normalize comb output
            comb_out = comb_sum / len(self.comb_buffers)
            
            # Pass through allpass filters
            allpass_out = comb_out
            
            for j, (buffer, pos) in enumerate(zip(self.allpass_buffers, self.allpass_positions)):
                delayed = buffer[pos]
                buffer[pos] = allpass_out + delayed * 0.5
                allpass_out = delayed - allpass_out * 0.5
                self.allpass_positions[j] = (pos + 1) % len(buffer)
            
            # Mix dry and wet
            output[i] = (1.0 - self.mix) * audio[i] + self.mix * allpass_out
        
        return output.astype(np.float32)
    
    def set_params(self, room_size=None, damping=None, mix=None):
        """Update reverb parameters."""
        if room_size is not None:
            self.room_size = room_size
            self.update_parameters()
        if damping is not None:
            self.damping = damping
        if mix is not None:
            self.mix = mix
    
    def reset(self):
        """Reset all buffers."""
        for buffer in self.comb_buffers:
            buffer.fill(0.0)
        for buffer in self.allpass_buffers:
            buffer.fill(0.0)
        self.comb_positions = [0] * len(self.comb_buffers)
        self.allpass_positions = [0] * len(self.allpass_buffers)
