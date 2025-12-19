"""
Simple noise gate for cutting out low-level signals.
"""
import numpy as np


class NoiseGate:
    """Noise gate that mutes signals below threshold."""
    
    def __init__(self, sr=44100, threshold=-40.0, attack=0.001, release=0.05):
        """
        Initialize noise gate.
        
        Args:
            sr: Sampling rate
            threshold: Gate threshold in dB
            attack: Attack time in seconds (how fast gate opens)
            release: Release time in seconds (how fast gate closes)
        """
        self.sr = sr
        self.threshold = threshold
        
        # Attack/release coefficients
        self.attack_coeff = np.exp(-1.0 / (attack * sr))
        self.release_coeff = np.exp(-1.0 / (release * sr))
        
        # Envelope follower state
        self.envelope = 0.0
        self.gate_gain = 0.0
        
    def process(self, audio):
        """
        Apply noise gate to audio.
        
        Args:
            audio: Input audio (numpy array)
            
        Returns:
            Gated audio
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
            
            # Calculate gate state
            if envelope_db > self.threshold:
                # Above threshold: gate open (gain = 1.0)
                target_gain = 1.0
            else:
                # Below threshold: gate closed (gain = 0.0)
                target_gain = 0.0
            
            # Smooth gate transitions
            if target_gain > self.gate_gain:
                # Opening gate (fast attack)
                self.gate_gain = self.attack_coeff * self.gate_gain + \
                                (1.0 - self.attack_coeff) * target_gain
            else:
                # Closing gate (slow release)
                self.gate_gain = self.release_coeff * self.gate_gain + \
                                (1.0 - self.release_coeff) * target_gain
            
            # Apply gate
            output[i] = audio[i] * self.gate_gain
        
        return output.astype(np.float32)
    
    def set_params(self, threshold=None, attack=None, release=None):
        """Update gate parameters."""
        if threshold is not None:
            self.threshold = threshold
        if attack is not None:
            self.attack_coeff = np.exp(-1.0 / (attack * self.sr))
        if release is not None:
            self.release_coeff = np.exp(-1.0 / (release * self.sr))
    
    def reset(self):
        """Reset gate state."""
        self.envelope = 0.0
        self.gate_gain = 0.0
