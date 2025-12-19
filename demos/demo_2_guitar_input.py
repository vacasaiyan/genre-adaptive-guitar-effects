"""
Demo 2: Test guitar input from Audient i44.
Tests guitar input capture, preprocessing, and effects.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from realtime_processor import RealtimeProcessor
from input_modules.guitar_input import GuitarInput
import keyboard


def list_audio_devices():
    """List available audio input devices."""
    guitar_input = GuitarInput()
    guitar_input.list_devices()


def setup_genre_switcher(processor):
    """Set up hotkeys for switching genres in real-time."""
    
    def switch_to_rock(e):
        print("\n>>> Switching to Rock/Country")
        processor.effect_chain.set_genre('Rock/Country')
    
    def switch_to_jazz(e):
        print("\n>>> Switching to Jazz/Blues")
        processor.effect_chain.set_genre('Jazz/Blues')
    
    def switch_to_pop(e):
        print("\n>>> Switching to Pop")
        processor.effect_chain.set_genre('Pop')
    
    def switch_to_clean(e):
        print("\n>>> Switching to Clean (No Effects)")
        processor.effect_chain.set_genre('Clean')
    
    def switch_to_metal(e):
        print("\n>>> Switching to Metal (8-Stage Aggressive Metal)")
        processor.effect_chain.set_genre('Metal')
    
    # Register hotkeys (use number keys)
    keyboard.on_press_key('1', switch_to_rock)
    keyboard.on_press_key('2', switch_to_jazz)
    keyboard.on_press_key('3', switch_to_pop)
    keyboard.on_press_key('4', switch_to_clean)
    keyboard.on_press_key('5', switch_to_metal)
    
    print("\n" + "="*60)
    print("GENRE SWITCHING HOTKEYS ENABLED:")
    print("  Press 1 = Rock/Country")
    print("  Press 2 = Jazz/Blues")
    print("  Press 3 = Pop")
    print("  Press 4 = Clean (No Effects)")
    print("  Press 5 = Metal (8-Stage Aggressive Metal)")
    print("="*60)


def main():
    """Run guitar input demo."""
    print("\n" + "="*60)
    print("DEMO 2: Guitar Input with Live Genre Switching")
    print("="*60)
    print("\nThis demo tests:")
    print("  - Guitar input capture from Audient i44")
    print("  - High-pass filtering and normalization")
    print("  - Real-time effect processing")
    print("  - Live genre switching with hotkeys")
    print("\nSetup:")
    print("  1. Connect guitar to Audient i44 Hi-Z input")
    print("  2. Ensure Audient i44 is selected as default input device")
    print("  3. Adjust input gain on the interface")
    print("\nAvailable audio devices:")
    print("-" * 60)
    list_audio_devices()
    print("-" * 60)
    
    # Let user choose initial genre
    print("\n" + "-"*60)
    print("Select INITIAL genre:")
    print("  1. Rock/Country - Distortion -> EQ -> Reverb")
    print("  2. Jazz/Blues - Chorus -> Compressor -> EQ -> Reverb")
    print("  3. Pop - Delay -> Bright EQ -> Light Reverb")
    print("  4. Clean (No Effects) - Bypass all effects")
    print("  5. Metal - 8-Stage Aggressive Metal Lead & Rhythm")
    print("-"*60)
    
    genre_choice = input("\nInitial genre (1-5) [1]: ").strip()
    
    genre_map = {
        '1': 'Rock/Country',
        '2': 'Jazz/Blues',
        '3': 'Pop',
        '4': 'Clean',
        '5': 'Metal'
    }
    
    selected_genre = genre_map.get(genre_choice, 'Rock/Country')
    
    input("\nPress Enter to start (ensure guitar is connected)...")
    
    print(f"\nStarting with: {selected_genre}")
    print("You can switch genres anytime by pressing 1, 2, 3, 4, or 5")
    print("Play your guitar to hear the processed sound")
    print("Press Ctrl+C to stop")
    print("="*60 + "\n")
    
    # Create processor with guitar input, Rock/Metal genre
    processor = RealtimeProcessor(
        sr=44100,
        block_size=32,  # Ultra-low latency (~1.45ms per buffer)
        input_mode='guitar',
        model_path=None,
        reference_song_path=None,
        output_device=84  # WASAPI Analogue 1/2 Output
    )
    
    # Set specific WASAPI input device for lower latency
    # Device 86: Analogue 1/2 Input (WASAPI)
    processor.guitar_input.set_device(86)
    
    # Set the chosen genre
    processor.effect_chain.set_genre(selected_genre)
    
    # Set up genre switching hotkeys
    setup_genre_switcher(processor)
    
    # Start processing
    processor.start()


if __name__ == '__main__':
    main()
