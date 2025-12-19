"""
Demo 3: Full system with genre classification from reference song.
Tests complete integration: input, genre classification, and adaptive effects.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from realtime_processor import RealtimeProcessor
import keyboard


def setup_genre_switcher(processor):
    """Set up hotkeys for manual genre override during playback."""
    
    def switch_to_rock(e):
        print("\n>>> Manual Override: Switching to Rock/Country")
        processor.effect_chain.set_genre('Rock/Country')
    
    def switch_to_jazz(e):
        print("\n>>> Manual Override: Switching to Jazz/Blues")
        processor.effect_chain.set_genre('Jazz/Blues')
    
    def switch_to_pop(e):
        print("\n>>> Manual Override: Switching to Pop")
        processor.effect_chain.set_genre('Pop')
    
    def switch_to_clean(e):
        print("\n>>> Manual Override: Switching to Clean (No Effects)")
        processor.effect_chain.set_genre('Clean')
    
    def switch_to_metal(e):
        print("\n>>> Manual Override: Switching to Metal (8-Stage Aggressive)")
        processor.effect_chain.set_genre('Metal')
    
    # Register hotkeys
    keyboard.on_press_key('1', switch_to_rock)
    keyboard.on_press_key('2', switch_to_jazz)
    keyboard.on_press_key('3', switch_to_pop)
    keyboard.on_press_key('4', switch_to_clean)
    keyboard.on_press_key('5', switch_to_metal)
    
    print("\n" + "="*60)
    print("MANUAL GENRE OVERRIDE (optional):")
    print("  Press 1 = Rock/Country")
    print("  Press 2 = Jazz/Blues")
    print("  Press 3 = Pop")
    print("  Press 4 = Clean (No Effects)")
    print("  Press 5 = Metal (8-Stage Aggressive)")
    print("="*60)


def main():
    """Run full system demo with genre classification."""
    print("\n" + "="*60)
    print("DEMO 3: Full System with Genre-Adaptive Effects")
    print("="*60)
    print("\nThis demo tests:")
    print("  - Real-time genre classification from reference song")
    print("  - Automatic effect chain switching based on genre")
    print("  - Live guitar/keyboard processing with adaptive effects")
    print("  - Low-latency audio (64-sample buffers, WASAPI)")
    print("\nSupported audio formats:")
    print("  - WAV, MP3, FLAC, OGG, M4A (librosa supports all)")
    print("\nSetup:")
    print("  1. Place a test song (NOT in training dataset) in any folder")
    print("  2. Specify full path to song file")
    print("  3. Connect guitar to Audient iD44 if using guitar mode")
    
    # Get reference song path
    print("\n" + "-"*60)
    print("Example songs to test:")
    print("  - A blues/jazz song -> should classify as Jazz/Blues")
    print("  - A metal song -> should classify as Metal (8-stage aggressive)")
    print("  - A rock/country song -> should classify as Rock/Country")
    print("  - A pop song -> should classify as Pop")
    print("\nSupported formats: WAV, MP3, FLAC, OGG, M4A")
    print("-"*60)
    
    song_path = input("\nEnter FULL path to reference song: ").strip()
    
    # Remove quotes if user copied path with quotes
    song_path = song_path.strip('"').strip("'")
    
    if not os.path.exists(song_path):
        print(f"\nError: Song file not found: {song_path}")
        print("Please provide a valid path to an audio file.")
        print("Example: C:\\Music\\test_song.mp3")
        return
    
    input_mode = input("\nInput mode (keyboard/guitar/both) [guitar]: ").strip() or 'guitar'
    
    model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'genre_classifier.pth')
    
    if not os.path.exists(model_path):
        print(f"\n⚠ Warning: Pretrained model not found at {model_path}")
        print("Please train the model first using:")
        print("  python src/genre_classifier/train.py")
        print("\nContinuing without genre classification (effects will not adapt)...")
        model_path = None
    
    print("\n" + "="*60)
    print("Starting full system...")
    print(f"Reference song: {os.path.basename(song_path)}")
    print("Genre will be classified from the reference song every 1 second")
    print("Effect chain will adapt automatically based on detected genre")
    print("\nYou can also manually override with hotkeys 1-4")
    if input_mode == 'keyboard':
        print("\nPlay notes on keyboard: A S D F G H J K (white keys)")
        print("Sharp notes: W E T Y U (black keys)")
    elif input_mode == 'guitar':
        print("\nPlay guitar through Audient iD44 (WASAPI low-latency mode)")
    else:
        print("\nUse both keyboard and guitar!")
    print("\nPress Ctrl+C to stop")
    print("="*60 + "\n")
    
    # Create processor with full configuration and low-latency settings
    processor = RealtimeProcessor(
        sr=44100,
        block_size=64,  # Ultra-low latency
        input_mode=input_mode,
        model_path=model_path,
        reference_song_path=song_path,
        output_device=84 if input_mode in ['guitar', 'both'] else None  # WASAPI output
    )
    
    # Set WASAPI input for guitar
    if input_mode in ['guitar', 'both']:
        processor.guitar_input.set_device(86)  # WASAPI Analogue 1/2 Input
    
    # Set up genre switching hotkeys
    setup_genre_switcher(processor)
    
    # Start processing
    processor.start()


if __name__ == '__main__':
    main()
