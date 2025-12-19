"""
Demo 1: Keyboard-only input with manual genre switching.
Tests keyboard input and effect chains without genre classification.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from realtime_processor import RealtimeProcessor
import keyboard


def setup_genre_switcher(processor):
    """Set up hotkeys for switching genres in real-time."""
    
    def switch_to_rock(e):
        print("\n>>> Switching to Rock/Metal")
        processor.effect_chain.set_genre('Rock/Metal')
    
    def switch_to_jazz(e):
        print("\n>>> Switching to Jazz/Blues")
        processor.effect_chain.set_genre('Jazz/Blues')
    
    def switch_to_pop(e):
        print("\n>>> Switching to Pop")
        processor.effect_chain.set_genre('Pop')
    
    def switch_to_clean(e):
        print("\n>>> Switching to Clean (No Effects)")
        processor.effect_chain.set_genre('Clean')
    
    # Register hotkeys (use number keys)
    keyboard.on_press_key('1', switch_to_rock)
    keyboard.on_press_key('2', switch_to_jazz)
    keyboard.on_press_key('3', switch_to_pop)
    keyboard.on_press_key('4', switch_to_clean)
    
    print("\n" + "="*60)
    print("GENRE SWITCHING HOTKEYS ENABLED:")
    print("  Press 1 = Rock/Metal")
    print("  Press 2 = Jazz/Blues")
    print("  Press 3 = Pop")
    print("  Press 4 = Clean (No Effects)")
    print("="*60)


def main():
    """Main demo function."""
    
    print("\n" + "="*60)
    print("DEMO 1: Keyboard Input with Live Genre Switching")
    print("="*60)
    
    print("\nThis demo tests:")
    print("  - Keyboard tone generation")
    print("  - Effect chains for each genre")
    print("  - Real-time audio processing")
    print("  - Live genre switching with hotkeys")
    print("\nControls:")
    print("  Musical notes: A S D F G H J K (C D E F G A B C)")
    print("  Sharp notes: W E T Y U (C# D# F# G# A#)")
    print("\nGenre Switching:")
    print("  Press 1 = Rock/Metal")
    print("  Press 2 = Jazz/Blues")
    print("  Press 3 = Pop")
    print("  Press 4 = Clean (No Effects)")
    
    # Let user choose initial genre
    print("\n" + "-"*60)
    print("Select INITIAL genre:")
    print("  1. Rock/Metal - Distortion -> EQ -> Reverb")
    print("  2. Jazz/Blues - Chorus -> Compressor -> EQ -> Reverb")
    print("  3. Pop - Delay -> Bright EQ -> Light Reverb")
    print("  4. Clean (No Effects) - Bypass all effects")
    print("-"*60)
    
    genre_choice = input("\nInitial genre (1-4) [3]: ").strip()
    
    genre_map = {
        '1': 'Rock/Metal',
        '2': 'Jazz/Blues',
        '3': 'Pop',
        '4': 'Clean'
    }
    
    selected_genre = genre_map.get(genre_choice, 'Pop')
    
    print(f"\nStarting with: {selected_genre}")
    print("You can switch genres anytime by pressing 1, 2, 3, or 4")
    print("\nPress Ctrl+C to stop")
    print("="*60 + "\n")
    
    # Create processor with keyboard-only input, selected genre
    processor = RealtimeProcessor(
        sr=44100,
        block_size=128,  # Reduced from 256 for lower latency (~2.9ms)
        input_mode='keyboard',
        model_path=None,  # No genre classification
        reference_song_path=None
    )
    
    # Set the chosen genre
    processor.effect_chain.set_genre(selected_genre)
    
    # Set up genre switching hotkeys
    setup_genre_switcher(processor)
    
    # Start processing
    processor.start()


if __name__ == '__main__':
    main()
