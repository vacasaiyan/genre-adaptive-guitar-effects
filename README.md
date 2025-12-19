# Genre-Adaptive Guitar Multi-Effects System

![System Architecture](src/utils/presentation_figures/slide1_system_overview.png)

## Abstract

In this project, I am going to introduce a new real-time guitar multieffects pedals system that automatically alters a digital signal processing chain solely based on a genre classification system with deep learning. In this system we will be using 58 different audio features that all come from a song of choice or the guitar input signal itself, the respective songs will be classified by genre by using a neural network system that achieved a 89.23 percent accuracy when tested with the GTZAN dataset. The guitar signal processing effect chain will be dynamically changed, based on the genre of any song of choice. In total we will be using 5 different signal effect chains presets (metal, rock/country, jazz, blues, pop, clean) which were created with various DSP code modules such as the following: noise gate, parametric equalizer, distortion, delay, chorus and compression. This system has the objective of creating bridges between AI music analysis and audio engineering, which will allow musicians to get high quality guitar tone without manually adjusting any DSP parameters. The real-time efficiency of this system was tested with processing latencies that were good enough for any type of live performance.

## Introduction

Multi-effects guitar pedals are necessary tools in the world of music production, enabling musicians to experiment with different types of tones for any type of the different musical styles. But, manually adjusting the settings of these effects implies that the user should have expertise in the area of audio engineering and it can also be extremely time consuming, especially during practicing, live and recording sessions. It is known that different musical genres match with different types of guitar tones, for example: Metal requires heavy distortion, jazz goes well with warm tones, rock traditionally will always use an overdrive tone, and lastly classical music usually is played by a clean signal.

Recent research and advances in the area of deep learning have allowed us to efficiently and accurately determine the genre of a song by constructing a music genre classification system that uses audio features as inputs, but few systems have created a bridge between these genre classification systems and real audio engineering. This final project will introduce a smart guitar multi-effects system that will:

- Genre classify songs with 89.23% accuracy
- Automatically adjust the settings of five different genre-based effect chains
- Create high quality DSP code modules
- Have low processing latencies

As for the system architecture, we will use: feautre extracitons, deep learning based classification, and adaptive DSP that will have high audio quality while also having smart automation capabilities

## System Architecture

You can see the complete archictecture of this system below. The signal chain path follows this order:

1. **Input Stage**: Guitar signal acquisition at 44.1 kHz sampling rate and song input for classification
2. **Feature Extraction**: 58 audio features form the song and guitar input signal are computed in real-time
3. **Genre Classification**: Neural network classifier gets the musical genre
4. **Preset Selection**: Respective genre will be mapped to one of the five multi-effects presets
5. **Effect Chain**: Configurable DSP modules for audio processing
6. **Output Stage**: Output signal wil be delivered to the amplifier

## Feature Extraction

This system will extracts 58 audio features from the input song and guitar signal:

- **MFCC (40 features)**: 20 mel-frequency cepstral coefficients with their respective means and variances
- **Spectral Features (6)**: Centroid and rolloff with their respective mean and variances
- **Temporal Features (2)**: Zero-crossing rate characteristic
- **Harmonic Features (2)**: Chroma STFT
- **Bandwidth (2)**: Spectral bandwidth
- **Tempo (2)**: Beat data
- **RMS Energy (6)**: Energy characteristics

The librosa library will be used for feature extraction for more efficient implementations that will also be suitable for any type of real-time processing.

![All 58 Features](src/utils/signal_chain_viz/all_features_58.png)

## Genre Classification Model

We will use the GTZAN dataset to train a multi;ayered perceptron (MLP) for classificcation. This model's architecture flow consists of:

- Input layer: 58 features
- Hidden layers: 2 layers with 128 neurons each
- Activation: ReLU with 30% dropout
- Output layer: 10 genre classes
- Framework: PyTorch

Neural networks are a great choice for implementing this classifier since they have fast interference and processing time accpetable enough for real-time use cases, as well as high accuracy when compared to classical machine learning methods.

The genre classfier will map 10 GTZAN datasets to 5 multi-effects presets:

- Metal → Metal preset
- Rock + Country → Rock/Country preset
- Jazz + Blues → Jazz/Blues preset
- Pop + Disco + Reggae + Hip-Hop → Pop preset
- Classical → Clean preset

![Confusion Matrix](src/utils/validation_results/confusion_matrix.png)

Fig: Confusion matrix showing classification accuracy across 10 genres. Overall accuracy: 89.23%.

## Genre-based Multi-Effects Presets

5 different signal effects chain were implemented based of traditional audio engineering techniques:

**Metal Preset (6 stages):** Noise gate (-45 dB) → Pre-EQ (HPF + mid boost) → Heavy distortion (50x gain, asymmetric) → Post-EQ (V-shaped) → Delay (330 ms) → Compressor (2:1)

**Rock/Country (3 stages):** Moderate distortion (11.5x gain) → Mid-focused EQ (+8 dB at 800 Hz) → Subtle reverb

**Jazz/Blues (4 stages):** Chorus (1.2 Hz modulation) → Compression (3:1, -18 dB) → Warm EQ (low-mid boost) → Room reverb

**Pop (3 stages):** Delay (250 ms, 30% feedback) → Bright EQ (+7 dB at 2-5 kHz) → Reverb

**Clean:** Bypass mode (zero processing) for classical music

## Digital Signal Processing Modules

The 5 distinct signal effects chain were create bu using seven core DSP modules as their building blocks:

**Noise Gate:** Eliminates background noise while preserving transients for high gain signal chains.

**Parametric equalizer (EQ):** Second-order IIR biquad filters implementated in a way that will allows use to modify its gain, frequency, and bandwidth (Q factor)

**Distortion:** hyperbolic tangent based asymmetric clipping with the objective of emphasizing harmonics.

**Compressor:** Dynamic range reduction for compression of the signal amplitude with ratio R, threshold T, and gain M.

**Chorus:** Delay based chorus effects which creates several pitch variations for better spatial width.

**Delay:** Consisits of a circular buffer with feedback for better echo effects.

**Reverb:** Uses parallel comb and a series of various allpass filters to create a natural room ambience effect.

## Results

### Classification Performance

Our classifier managed to achieve greate results, particulalry for classical (98% F1), metal (94% F1), and jazz (91% F1) genres. This made up believed that these genres have distinct and recognizable timbral and temporal characteristics that are easily captures by our classifer. We can see the biggest inaccuracies when categorizing rock and country songd, which both have lots of similar characteristics, which explains why I combine them into a single Rock/Country preset.

| Genre | Precision | Recall | F1-Score |
|-------|-----------|--------|----------|
| Blues | 0.83 | 0.85 | 0.84 |
| Classical | 0.99 | 0.97 | 0.98 |
| Country | 0.88 | 0.80 | 0.84 |
| Disco | 0.79 | 0.85 | 0.82 |
| Hip-Hop | 0.87 | 0.90 | 0.88 |
| Jazz | 0.94 | 0.89 | 0.91 |
| Metal | 0.95 | 0.93 | 0.94 |
| Pop | 0.85 | 0.85 | 0.85 |
| Reggae | 0.86 | 0.90 | 0.88 |
| Rock | 0.83 | 0.88 | 0.85 |
| **Average** | **0.88** | **0.89** | **0.88** |
| **Accuracy** | | **89.23%** | |

### Feature Space Analysis

![t-SNE Visualization](src/utils/validation_results/tsne_visualization.png)

Metal, classical, and hip-hop gernes have separated clusters, while blues, jazz, and rock are not so distinct, implying an overlap in their musical characterisitcs. Cluster visualization proves the effectiveness of the feature extraction methods and classifier performance.

### Signal Processing Quality

![Metal Waveforms](src/utils/signal_chain_viz/Metal_waveforms.png)

This metal singal processing chain:
- Emphasizes harmonics while at the same time not having excessive background noise.
- A controlled dynamic range
- V shape EQ, suitable for metal genre
- low latency

### Real-Time Porcessing Performance

System metrics on a lenovo thinkpad laptop (intel 6400u, 8 GB RAM):

- Feature extraction: 5-8 ms per frame
- Inference less than 1 ms
- Digital signal processing: 2-3 ms per frame
- Final Latency: 8-12 ms

## DEMO

Two demo modes were implemented for testing this system:

1. **Real-time Guitar Input**: Demonstrate the different effects chains for the guitar input
2. **Full System Demo**: Complete genre classification plus guitar DSP system

## Installation

```bash
pip install -r requirements.txt
```

### Required Packages
- numpy
- scipy
- librosa
- scikit-learn
- sounddevice
- matplotlib
- PyTorch

## Usage

### Demo 1: Real-time Guitar Input
```bash
python demos/demo_2_guitar_input.py
```

### Demo 2: Full System
```bash
python demos/demo_3_full_system.py
```

## Conclusions

This system introduces a new real-time guitar multi-effects systems that merges deep learning based genre classification with an adaptive digital singl processing system. The main contribution of this project are:

- Use of 58 distinct audio features for genre clasification (89.23% accuracy)
- Five high quality guitar multi-effects chains that are optimized for their respective inteded genre
- An 8-stage metal distortion chain
- Low latency and therefore a suitable Real-time performance for live sessions/recordings
- Open-source

This systems show the various applications of AI music analysis for audio engineering, and it also demonstrate that smart autiomation can imporove musical creativity. I will continue to study and explore:

- Other AI models for higher accuracy
- Increments the amount of audio features
- User feedback on presets tones
- Incorporation with digital audio workstations
- Different instruments other guitars.

## Author

Ivan Andre Castillo Barahona  
Department of Electrical Engineering  
National Tsinghua University  
Hsinchu city, Taiwan  
ivan.andrecb2@gmail.com

## License

MIT License
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
