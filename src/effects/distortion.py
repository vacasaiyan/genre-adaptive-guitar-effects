"""
Distortion/Overdrive effect using nonlinear clipping.
"""
import numpy as np


class Distortion:
    """Distortion/overdrive effect."""
    
    def __init__(self, gain=5.0, mix=1.0, type='tanh'):
        """
        Initialize distortion effect.
        
        Args:
            gain: Pre-gain amount (1.0-20.0)
            mix: Wet/dry mix (0.0=dry, 1.0=wet)
            type: Clipping type ('tanh', 'hard', 'soft')
        """
        self.gain = gain
        self.mix = mix
        self.type = type
        
    def process(self, audio):
        """
        Apply distortion to audio.
        
        Args:
            audio: Input audio (numpy array)
            
        Returns:
            Processed audio
        """
        # Classic tube-style overdrive
        # Pre-gain boost
        gained = audio * self.gain
        
        # Apply clipping based on type
        if self.type == 'tanh':
            # Smooth tube-like overdrive
            wet = np.tanh(gained)
        elif self.type == 'hard':
            # Tight hard clipping - clear and aggressive
            # Two-stage: soft then hard for character without harshness
            stage1 = np.tanh(gained * 0.6)  # First soft saturation
            wet = np.clip(stage1 * 2.2, -0.95, 0.95)  # Then clip at 0.95 to leave headroom
        elif self.type == 'soft':
            # Classic soft overdrive - warm and musical
            # Tube-style asymmetric soft clipping
            wet = np.tanh(gained * 1.2) * 0.9
            # Add slight even harmonics for warmth
            wet = wet + (np.tanh(gained * 0.3) ** 2) * 0.15
        elif self.type == 'asymmetric':
            # Maximum asymmetric saturation for chunky metal chug
            # More aggressive clipping with rich harmonics
            wet = np.where(gained >= 0,
                          np.tanh(gained * 1.8) * 1.1,     # Very hard positive (pick attack)
                          np.tanh(gained * 1.3) * 0.95)    # Medium negative (warmth)
        else:
            wet = gained
            
        # Mix wet and dry
        output = self.mix * wet + (1.0 - self.mix) * audio
        
        # Conservative output level
        output = output * 0.9
            
        return output.astype(np.float32)
    
    def set_params(self, gain=None, mix=None, type=None):
        """Update effect parameters."""
        if gain is not None:
            self.gain = gain
        if mix is not None:
            self.mix = mix
        if type is not None:
            self.type = type
