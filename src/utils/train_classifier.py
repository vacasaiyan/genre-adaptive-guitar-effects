"""
Batch training and evaluation script.
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from genre_classifier.train import train_model


def main():
    """
    Run training with different configurations.
    """
    print("="*70)
    print("GENRE CLASSIFIER TRAINING")
    print("="*70)
    
    # Configuration
    csv_path = os.path.join(os.path.dirname(__file__), '..', '..', 
                           'Data', 'features_3_sec_extracted.csv')
    model_save_path = os.path.join(os.path.dirname(__file__), '..', '..', 
                                   'models', 'genre_classifier.pth')
    
    print(f"\nTraining configuration:")
    print(f"  Data: {csv_path}")
    print(f"  Model output: {model_save_path}")
    print(f"  Epochs: 50")
    print(f"  Batch size: 64")
    print(f"  Learning rate: 0.001")
    print()
    
    if not os.path.exists(csv_path):
        print(f"ERROR: Features file not found: {csv_path}")
        print("Please ensure GTZAN dataset features are available.")
        return
    
    response = input("Start training? (y/n): ").strip().lower()
    if response != 'y':
        print("Training cancelled.")
        return
    
    # Train model
    print("\nStarting training...\n")
    train_model(
        csv_path=csv_path,
        model_save_path=model_save_path,
        epochs=50,
        batch_size=64,
        lr=0.001
    )
    
    print("\n" + "="*70)
    print("Training complete!")
    print("="*70)
    print(f"\nModel saved to: {model_save_path}")
    print("\nYou can now run the full system demo:")
    print("  cd demos")
    print("  python demo_3_full_system.py")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()
