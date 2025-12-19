"""
Genre classification model - simple MLP for real-time inference.
"""
import torch
import torch.nn as nn
import numpy as np
import joblib
import os
from collections import deque


class GenreClassifierMLP(nn.Module):
    """Simple MLP for genre classification."""
    
    def __init__(self, input_dim=58, hidden_dim=128, num_classes=10):
        """
        Initialize MLP classifier.
        
        Args:
            input_dim: Input feature dimension (58 features from GTZAN CSV)
            hidden_dim: Hidden layer dimension
            num_classes: Number of genre classes (10 GTZAN genres)
        """
        super(GenreClassifierMLP, self).__init__()
        
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, num_classes)
        )
        
    def forward(self, x):
        return self.network(x)


class GenreClassifier:
    """Genre classifier with temporal smoothing."""
    
    # 10 GTZAN genres (index matches model output)
    GTZAN_GENRES = [
        'blues', 'classical', 'country', 'disco', 'hiphop',
        'jazz', 'metal', 'pop', 'reggae', 'rock'
    ]
    
    # Map GTZAN genres to effect presets
    GENRE_TO_PRESET = {
        'rock': 'Rock/Country',
        'country': 'Rock/Country',
        'metal': 'Metal',
        'jazz': 'Jazz/Blues',
        'blues': 'Jazz/Blues',
        'pop': 'Pop',
        'disco': 'Pop',
        'reggae': 'Pop',
        'hiphop': 'Pop',
        'classical': 'Clean'
    }
    
    def __init__(self, model_path=None, smoothing_window=3):
        """
        Initialize genre classifier.
        
        Args:
            model_path: Path to pretrained model weights
            smoothing_window: Number of predictions to smooth over
        """
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = GenreClassifierMLP(input_dim=58, hidden_dim=128, num_classes=10)
        
        # Load scaler
        self.scaler = None
        if model_path:
            # Load model weights
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            
            # Load scaler (should be in same directory as model)
            scaler_path = model_path.replace('.pth', '_scaler.pkl')
            if os.path.exists(scaler_path):
                self.scaler = joblib.load(scaler_path)
                print(f"✓ Loaded scaler from {scaler_path}")
            else:
                print(f"⚠️  Warning: Scaler not found at {scaler_path}")
                print("   Predictions may be inaccurate without feature normalization!")
        
        self.model.to(self.device)
        self.model.eval()
        
        # Smoothing buffer
        self.smoothing_window = smoothing_window
        self.prediction_buffer = deque(maxlen=smoothing_window)
        
    def predict(self, features):
        """
        Predict genre from features and map to effect preset.
        
        Args:
            features: Feature vector (numpy array)
            
        Returns:
            Effect preset name (e.g., 'Rock/Metal', 'Jazz/Blues', 'Pop', 'Clean')
        """
        # Normalize features using scaler (CRITICAL for accurate predictions)
        if self.scaler is not None:
            features = self.scaler.transform(features.reshape(1, -1))[0]
        
        with torch.no_grad():
            features_tensor = torch.FloatTensor(features).unsqueeze(0).to(self.device)
            output = self.model(features_tensor)
            prediction = torch.argmax(output, dim=1).item()
        
        # Add to smoothing buffer
        self.prediction_buffer.append(prediction)
        
        # Majority vote
        if len(self.prediction_buffer) >= self.smoothing_window:
            smoothed_prediction = np.bincount(list(self.prediction_buffer)).argmax()
        else:
            smoothed_prediction = prediction
        
        # Map from model output index to GTZAN genre name
        gtzan_genre = self.GTZAN_GENRES[smoothed_prediction]
        
        # Map GTZAN genre to effect preset
        effect_preset = self.GENRE_TO_PRESET[gtzan_genre]
        
        return effect_preset
    
    def reset_smoothing(self):
        """Reset the smoothing buffer."""
        self.prediction_buffer.clear()
