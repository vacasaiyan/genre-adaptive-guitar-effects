# Genre-Adaptive Guitar Effects System

![System Architecture](docs/images/system_overview.png)

## Overview

A real-time intelligent guitar effects processor that automatically adapts digital signal processing (DSP) parameters based on musical genre classification using machine learning. The system achieves **89.23% classification accuracy** on the GTZAN dataset and provides five professionally-designed effect presets.

## Key Features

- **Real-time Genre Classification**: 58 audio features + Random Forest classifier
- **5 Adaptive Effect Presets**: Metal, Rock/Country, Jazz/Blues, Pop, Clean
- **Professional DSP Modules**: Noise gate, parametric EQ, distortion, delay, compression
- **8-Stage Metal Preset**: Professional-grade extreme distortion chain
- **Low Latency**: < 12 ms total processing time, suitable for live performance
- **Manual Override**: Full artistic control with AI-assisted suggestions

## System Architecture

```
Guitar Input → Feature Extraction (58 features) → AI Classifier (89.23% acc)
                                                         ↓
    Processed Output ← Effect Chain ← Preset Selection
```

## Installation

### Prerequisites
```bash
Python 3.8+
pip install -r requirements.txt
```

### Required Packages
- numpy
- scipy
- librosa
- scikit-learn
- sounddevice
- matplotlib

## Quick Start

### Demo 1: Audio File Processing
Process pre-recorded audio files:
```bash
python demos/demo_1_audio_file.py
```

### Demo 2: Live Guitar Input
Real-time guitar processing with auto genre detection:
```bash
python demos/demo_2_guitar_input.py
```

### Demo 3: Full System Visualization
Complete pipeline with real-time visualizations:
```bash
python demos/demo_3_full_system.py
```

## Project Structure

```
├── src/
│   ├── effects/          # DSP effect modules
│   │   ├── distortion.py
│   │   ├── eq.py
│   │   ├── delay.py
│   │   ├── compressor.py
│   │   ├── noise_gate.py
│   │   └── effect_chain.py
│   ├── ai/              # AI classification
│   │   └── model.py
│   └── utils/           # Feature extraction & visualization
│       └── feature_extractor.py
├── demos/               # Demo applications
│   ├── demo_1_audio_file.py
│   ├── demo_2_guitar_input.py
│   └── demo_3_full_system.py
├── models/              # Pre-trained models
│   └── genre_classifier.pkl
└── Data/                # GTZAN dataset (not included)
```

## Genre-to-Preset Mapping

| Genre(s) | Preset | Key Characteristics |
|----------|--------|---------------------|
| Metal | Metal | 50x distortion, V-EQ, noise gate |
| Rock + Country | Rock/Country | 10x distortion, 400ms delay |
| Jazz + Blues | Jazz/Blues | 2x distortion, warm compression |
| Pop + Disco + Reggae + Hip-Hop | Pop | Clean + subtle compression |
| Classical | Clean | Bypass (no processing) |

## Technical Details

### Feature Extraction (58 features)
- **MFCC**: 20 means + 20 variances (40 features)
- **Spectral**: Centroid, Rolloff, Bandwidth (6 features)
- **Temporal**: Zero-crossing rate, Tempo (4 features)
- **Harmonic**: Chroma STFT (2 features)
- **Energy**: RMS statistics (6 features)

### AI Model
- **Algorithm**: Random Forest (200 estimators)
- **Accuracy**: 89.23% on GTZAN test set
- **Inference Time**: < 1 ms

### DSP Performance
- **Sampling Rate**: 44.1 kHz
- **Buffer Size**: 1024 samples
- **Total Latency**: 8-12 ms
- **Processing**: Real-time on standard laptop

## Metal Preset Signal Chain

```
Input → Noise Gate → Pre-EQ → Heavy Distortion (50x) → 
Post-EQ → Filtered Delay → Compressor → Output
```

**Specifications:**
- Noise Gate: -40 dB threshold, 10ms attack
- Pre-EQ: +3 dB midrange boost (800 Hz)
- Distortion: Asymmetric clipping (3:1 ratio)
- Post-EQ: V-shaped curve (-6 dB mids)
- Delay: 330 ms with HPF at 400 Hz
- Compressor: 4:1 ratio for sustain

## Usage Examples

### Process an Audio File
```python
from demos.demo_1_audio_file import main
main()  # Select audio file and preset
```

### Real-Time Guitar Processing
```python
from demos.demo_2_guitar_input import main
main()  # Connect guitar interface, select preset
```

### Full System with Visualization
```python
from demos.demo_3_full_system import main
main()  # See live classification and effect visualization
```

## Results

### Classification Performance
- Overall Accuracy: **89.23%**
- Best Performance: Classical (98%), Metal (94%), Jazz (91%)
- Real-time Feature Extraction: 5-8 ms per frame

### Audio Quality
- Professional-grade distortion modeling
- Minimal artifacts and noise
- Dynamic range preservation
- Frequency-appropriate EQ curves

## Citation

If you use this system in your research, please cite:

```bibtex
@inproceedings{genre_adaptive_effects2025,
  title={Real-Time Genre-Adaptive Guitar Effects System Using Deep Learning},
  author={Your Name},
  booktitle={Proceedings of IEEE Conference},
  year={2025}
}
```

## Conference Paper

Full technical details available in the conference paper:
- [IEEE Paper PDF](conference_paper/Genre_Adaptive_Guitar_Effects_IEEE.pdf)
- Includes methodology, results, and performance analysis

## License

MIT License - See LICENSE file for details

## Acknowledgments

- GTZAN Dataset creators (George Tzanetakis)
- librosa audio processing library
- scikit-learn machine learning library
- Open-source audio engineering community

## Contributing

Contributions welcome! Please submit pull requests or open issues for:
- Additional effect presets
- Improved DSP algorithms
- Extended genre support
- Performance optimizations

## Contact

For questions or collaboration:
- GitHub Issues: [Report bugs or request features]
- Email: your.email@university.edu

---

**Note**: This project was developed for DSP research and educational purposes. GTZAN dataset required for model training (not included in repository).
