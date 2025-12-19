"""
Effect chain manager - applies effects sequentially based on genre.
"""
from .distortion import Distortion
from .chorus import Chorus
from .compressor import Compressor
from .eq import EQ
from .delay import Delay
from .reverb import Reverb
from .noise_gate import NoiseGate

class EffectChain:
    """Manages and applies genre-specific effect chains."""
    
    GENRE_CHAINS = {
        'Rock/Country': {
            'effects': ['distortion', 'eq', 'reverb'],
            'params': {
                'distortion': {'gain': 11.5, 'mix': 1.0, 'type': 'tanh'},
                'eq': {'preset': 'metal'},
                'reverb': {'room_size': 0.1, 'damping': 0.2, 'mix': 0.10}
            },
            'output_gain': 0.1  # Overdrive is more controlled
        },
        'Jazz/Blues': {
            'effects': ['chorus', 'compressor', 'eq', 'reverb'],
            'params': {
                'chorus': {'rate': 1.2, 'depth': 0.003, 'mix': 0.4},
                'compressor': {'threshold': -18.0, 'ratio': 3.0, 'makeup_gain': 1.2},
                'eq': {'preset': 'warm'},
                'reverb': {'room_size': 0.4, 'damping': 0.4, 'mix': 0.25}
            },
            'output_gain': 1.05  # Moderate reduction - compressor adds makeup gain
        },
        'Pop': {
            'effects': ['delay', 'eq', 'reverb'],
            'params': {
                'delay': {'delay_time': 0.25, 'feedback': 0.3, 'mix': 0.25},
                'eq': {'preset': 'bright'},
                'reverb': {'room_size': 0.3, 'damping': 0.4, 'mix': 0.25}
            },
            'output_gain': 1.1  # Slight reduction - fairly neutral
        },
        'Clean': {
            'effects': [],  # No effects - bypass
            'params': {},
            'output_gain': 1.1  # No change - baseline reference
        },
        'Metal': {
            # 8-Stage Professional Metal Lead & Rhythm Tone
            # Signal chain: Noise Gate -> Pre-EQ -> Distortion -> Post-EQ -> Delay -> Compressor
            'effects': ['noise_gate', 'eq_pre', 'distortion', 'eq_post', 'delay', 'compressor'],
            'params': {
                 # Stage 0: Noise gate (cuts hum and noise before distortion)
                'noise_gate': {'threshold': -45.0, 'attack': 0.001, 'release': 0.08},

                # Stage 1: Pre-distortion tightening (HPF simulation + mid focus)
                'eq_pre': {'preset': 'metal_pre'},
                
                # Stage 2-3: Multi-stage clipping with MAXIMUM gain for loud harmonics
                'distortion': {'gain': 50.0, 'mix': 1.0, 'type': 'asymmetric'},
                
                # Stage 4-6: Post-distortion shaping (fizz control + V-shape + solo voicing)
                'eq_post': {'preset': 'metal_post'},
                
                # Stage 7: Filtered delay (always active for solo)
                'delay': {'delay_time': 0.33, 'feedback': 0.4, 'mix': 0.3},
                
                # Stage 8: Sustain compressor
                'compressor': {'threshold': -15.0, 'ratio': 2.0, 'makeup_gain': 1.3}
            },
            'output_gain': 0.1  # Prevent interface clipping while keeping internal tone
        }
    }
    
    def __init__(self, sr=44100, initial_genre='Pop'):
        """
        Initialize effect chain.
        
        Args:
            sr: Sampling rate
            initial_genre: Initial genre for effect chain
        """
        self.sr = sr
        self.current_genre = initial_genre
        self.active_effects = []  # Initialize active_effects list
        self.output_gain = 1.0  # Initialize output gain
        
        # Initialize all effect types
        # For Metal Solo, we need separate EQ instances for pre/post distortion
        self.effects_pool = {
            'distortion': Distortion(),
            'chorus': Chorus(sr=sr),
            'compressor': Compressor(sr=sr),
            'eq': EQ(sr=sr),
            'eq_pre': EQ(sr=sr),   # Pre-distortion tightening
            'eq_post': EQ(sr=sr),  # Post-distortion shaping
            'delay': Delay(sr=sr),
            'reverb': Reverb(sr=sr),
            'noise_gate': NoiseGate(sr=sr)
        }
        
        # Set initial chain
        self.set_genre(initial_genre)
        
    def set_genre(self, genre):
        """
        Switch to a different genre effect chain.
        
        Args:
            genre: Genre name ('Rock/Metal', 'Jazz/Blues', 'Pop')
        """
        if genre not in self.GENRE_CHAINS:
            print(f"Warning: Unknown genre '{genre}', using Pop")
            genre = 'Pop'
        
        if genre == self.current_genre:
            return  # No change needed
            
        self.current_genre = genre
        chain_config = self.GENRE_CHAINS[genre]
        
        # Update active effects
        self.active_effects = chain_config['effects']
        
        # Store output gain for this genre
        self.output_gain = chain_config.get('output_gain', 1.0)
        
        # Configure effect parameters
        for effect_name, params in chain_config['params'].items():
            effect = self.effects_pool[effect_name]
            
            # Set parameters based on effect type
            if hasattr(effect, 'set_params'):
                effect.set_params(**params)
            elif hasattr(effect, 'set_preset'):
                effect.set_preset(params['preset'])
            
            # Reset effect state
            if hasattr(effect, 'reset'):
                effect.reset()
        
        if self.active_effects:
            print(f"Switched to {genre} effect chain: {' -> '.join(self.active_effects)}")
        else:
            print(f"Switched to {genre} (clean/bypass - no effects)")
        
    def process(self, audio):
        """
        Apply the current effect chain to audio.
        
        Args:
            audio: Input audio (numpy array)
            
        Returns:
            Processed audio
        """
        output = audio.copy()
        
        # Apply effects in sequence
        for effect_name in self.active_effects:
            effect = self.effects_pool[effect_name]
            output = effect.process(output)
        
        # Apply output gain compensation to normalize volume across genres
        output = output * self.output_gain
        
        return output
    
    def get_current_genre(self):
        """Return the current genre."""
        return self.current_genre
    
    def reset_all(self):
        """Reset all effects."""
        for effect in self.effects_pool.values():
            if hasattr(effect, 'reset'):
                effect.reset()
