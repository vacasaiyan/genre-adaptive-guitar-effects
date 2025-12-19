"""
Parametric EQ using second-order IIR filters.
"""
import numpy as np
from scipy import signal


class EQ:
    """Parametric equalizer with multiple bands."""
    
    def __init__(self, sr=44100, preset='flat'):
        """
        Initialize EQ.
        
        Args:
            sr: Sampling rate
            preset: EQ preset ('flat', 'bright', 'warm', 'metal')
        """
        self.sr = sr
        self.bands = []
        self.states = []
        
        self.set_preset(preset)
        
    def set_preset(self, preset):
        """
        Set EQ from preset.
        
        Args:
            preset: Preset name
        """
        self.bands = []
        
        if preset == 'bright':
            # Boost high-mids and highs for pop
            self.bands = [
                {'freq': 2000, 'gain': 7.0, 'Q': 1.0},
                {'freq': 5000, 'gain': 6.0, 'Q': 1.0}
            ]
        elif preset == 'warm':
            # Boost low-mids for jazz/blues
            self.bands = [
                {'freq': 200, 'gain': 4.0, 'Q': 1.0},
                {'freq': 800, 'gain': 5.0, 'Q': 1.0}
            ]
        elif preset == 'metal':
            # Classic Rock Overdrive - STRONG mid boost, warm, crunchy
            # Emphasis on mids for cutting through and singing sustain
            self.bands = [
                {'freq': 100, 'gain': 1.0, 'Q': 1.0},    # Bass warmth
                {'freq': 400, 'gain': 3.0, 'Q': 0.9},    # Low-mid body
                {'freq': 800, 'gain': 8.0, 'Q': 0.8},    # STRONG MID BOOST - tube screamer hump
                {'freq': 1500, 'gain': 5.0, 'Q': 0.9},   # Upper-mid presence
                {'freq': 3000, 'gain': 3.0, 'Q': 1.0},   # High-mid clarity
                {'freq': 6000, 'gain': 1.0, 'Q': 1.2},   # Treble definition
            ]
        elif preset == 'metal_pre':
            # STAGE 1: Pre-distortion tightening
            # HPF simulation (cut lows) + aggressive mid focus + attack emphasis
            self.bands = [
                {'freq': 135, 'gain': -15.0, 'Q': 0.7},   # HPF simulation - ULTRA tight low end
                {'freq': 1000, 'gain': 13.0, 'Q': 1.0},   # Mid focus - MORE distortion in mids
                {'freq': 2500, 'gain': 6.0, 'Q': 1.2},    # High-mid attack emphasis before clipping
            ]
        elif preset == 'metal_post':
            # STAGES 4-6: Post-distortion shaping
            # Fizz control + V-shaped metal EQ + solo voicing
            self.bands = [
                {'freq': 7000, 'gain': -10.0, 'Q': 0.7},   # Fizz control (less cut = more harmonics)
                {'freq': 90, 'gain': 18.0, 'Q': 1.2},      # Sub-bass punch (chug foundation)
                {'freq': 150, 'gain': 35.0, 'Q': 0.8},     # Bass boost (MASSIVE chug weight)
                {'freq': 500, 'gain': -14.0, 'Q': 1.0},    # Deeper mid scoop (more chug definition)
                {'freq': 3000, 'gain': 15.0, 'Q': 1.1},    # Upper-mid harmonics
                {'freq': 5000, 'gain': 24.0, 'Q': 0.9},    # Treble boost (EXTREME pick attack)
                {'freq': 1500, 'gain': 13.5, 'Q': 0.8},    # Solo mid lift (cut through)
            ]
        else:
            # Flat
            self.bands = []
        
        # Initialize filter states
        self.states = [np.zeros(2) for _ in self.bands]
        
    def _design_peaking_filter(self, freq, gain, Q):
        """
        Design a peaking filter.
        
        Args:
            freq: Center frequency in Hz
            gain: Gain in dB
            Q: Quality factor
            
        Returns:
            b, a coefficients
        """
        A = 10 ** (gain / 40.0)
        w0 = 2 * np.pi * freq / self.sr
        alpha = np.sin(w0) / (2 * Q)
        
        b0 = 1 + alpha * A
        b1 = -2 * np.cos(w0)
        b2 = 1 - alpha * A
        a0 = 1 + alpha / A
        a1 = -2 * np.cos(w0)
        a2 = 1 - alpha / A
        
        # Normalize
        b = np.array([b0, b1, b2]) / a0
        a = np.array([a0, a1, a2]) / a0
        
        return b, a
        
    def process(self, audio):
        """
        Apply EQ to audio.
        
        Args:
            audio: Input audio (numpy array)
            
        Returns:
            Equalized audio
        """
        output = audio.copy()
        
        # Apply each band
        for i, band in enumerate(self.bands):
            b, a = self._design_peaking_filter(band['freq'], band['gain'], band['Q'])
            output, self.states[i] = signal.lfilter(b, a, output, zi=self.states[i])
        
        return output.astype(np.float32)
    
    def reset(self):
        """Reset filter states."""
        self.states = [np.zeros(2) for _ in self.bands]
