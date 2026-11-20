# Frequency Analyzer - MHz Display

A real-time frequency analyzer that measures and displays audio frequencies in MHz, detects WiFi networks, and shows common radio bands. No special hardware receiver required!

## Features

### 🎙️ **Audio Frequency Analysis**
- Real-time FFT analysis from your microphone
- Displays peak frequency in kHz and MHz
- Visual spectrum graph showing frequency content up to 20kHz
- Live magnitude measurements

### 📡 **Radio Band Detection**
- AM Radio (0.5 - 1.6 MHz)
- FM Radio (88 - 108 MHz)
- CB Radio (26.965 - 27.405 MHz)
- WiFi 2.4GHz (2400 - 2500 MHz)
- WiFi 5GHz (4900 - 5900 MHz)
- LTE/Mobile Networks (700 - 2600 MHz)

### 📶 **WiFi Network Scanning**
- Detects all available WiFi networks near you
- Shows network name (SSID)
- Displays channel number and frequency
- Updates in real-time every ~5 seconds

### 📊 **Visual Displays**
- Live frequency spectrum graph
- Color-coded radio bands
- Signal strength indicators
- Frequency reference chart
- On-screen time and status

## Requirements

- Python 3.7+
- Pygame
- NumPy
- PyAudio

## Installation

### 1. Install Dependencies

```bash
python3 -m pip install -r frequency_requirements.txt
```

### 2. Windows-Specific Setup (for PyAudio)

If PyAudio installation fails, download the pre-built wheel:
```bash
# For Python 3.11 x64
python3 -m pip install pipwin
pipwin install pyaudio
```

Alternative: Use Conda
```bash
conda install pyaudio
```

## Usage

### Basic Usage
```bash
python3 frequency_analyzer.py
```

### Controls
| Key | Action |
|-----|--------|
| **ESC** | Exit application |
| **SPACE** | Force WiFi network scan |
| **Microphone Required** | For audio frequency analysis |

## Understanding the Display

### Spectrum Graph (Top)
- **X-axis**: Frequency from 0 to 20,000 Hz (0-20 kHz)
- **Y-axis**: Magnitude of frequency component
- **Green Line**: Real-time frequency peaks detected from microphone
- Used to detect audio frequencies and acoustic signals

### Radio Bands (Left Side)
Color-coded bands showing frequency ranges for different radio services:
- **Yellow**: AM Radio
- **Green**: FM Radio
- **Orange**: CB Radio
- **Cyan**: WiFi 2.4GHz
- **Blue**: WiFi 5GHz
- **Magenta**: LTE/Cellular

### Detected Signals (Right Side)
- **Peak Frequency**: Highest frequency detected from microphone
- **Magnitude**: Strength of the signal
- **WiFi Networks**: List of detected networks with channel/frequency info

### Reference Chart (Bottom)
Common frequencies for quick lookup and identification

## How It Works

### Audio Frequency Detection
1. Reads audio from your microphone
2. Performs Fast Fourier Transform (FFT) on audio samples
3. Identifies peak frequencies
4. Updates display in real-time

**What it can detect:**
- Voice/speech frequencies (85-255 Hz)
- Musical notes and instruments (25-20,000 Hz)
- Whistles, whistling tones
- Electronic beeps and alerts
- Any sound in the microphone's frequency range

### WiFi Detection
1. Uses Windows `netsh` command to scan available networks
2. Parses network information
3. Converts WiFi channel numbers to actual frequencies
4. Displays network names and signal info

**What it can detect:**
- All WiFi networks in range (2.4GHz & 5GHz)
- Channel numbers (1-14 for 2.4GHz, various for 5GHz)
- Network names (SSIDs)
- No receiver hardware needed - Windows has built-in WiFi scanning

### Radio Bands
Display shows theoretical ranges for various radio services:
- These are reference bands where certain radio services operate
- Actual reception requires a radio receiver tuned to those bands
- Display helps identify which "band" a detected frequency falls into

## Examples

### Detecting Frequencies
1. **Hum Detection**: Run the app and listen to electrical hum (60 Hz in USA, 50 Hz in EU)
2. **Whistle Detection**: Whistle into your microphone and see the frequency peak
3. **WiFi Networks**: See all WiFi around you and their exact frequencies
4. **Music**: Play music and watch the spectrum graph show instrument frequencies

### Practical Uses
- Identify audio frequencies from various sources
- Monitor WiFi network channels and frequencies
- Detect interference or noise frequencies
- Acoustic analysis and debugging
- Educational purposes to understand frequency spectrum

## Limitations

- **Audio Analysis**: Limited to microphone input (up to 20kHz usually)
- **Radio Reception**: Can detect WiFi (built-in Windows support), but radio band reception requires actual radio hardware
- **Accuracy**: Depends on microphone quality and calibration
- **Real-time WiFi**: Scans every few seconds (not continuous stream)

## Technical Details

### FFT Parameters
- Chunk Size: 2048 samples
- Sample Rate: 44.1 kHz
- Channels: Mono
- Format: 32-bit Float

### Frequency Resolution
- Resolution = Sample Rate / Chunk Size
- = 44,100 Hz / 2048 = ~21.5 Hz per bin
- Can detect frequencies ±10 Hz range

## Troubleshooting

### No Audio Data Detected
- Check microphone is connected and working
- Test microphone in Windows Sound Settings
- Grant microphone permission to the application
- Try speaking into microphone to generate frequencies

### WiFi Networks Not Detected
- Ensure WiFi is turned on
- Run with administrator privileges
- Check Windows Firewall allows network access
- Wait a few seconds, networks update every 5+ seconds

### PyAudio Installation Issues
- See Windows-Specific Setup section above
- Try: `py -m pip install pipwin` then `pipwin install pyaudio`
- Alternative: Use Conda instead of pip

### High CPU Usage
- Reduce FPS by adjusting clock.tick value
- Close other applications using microphone
- WiFi scanning can cause spikes

## System Requirements

- Windows, Mac, or Linux
- Microphone input device
- WiFi adapter (for WiFi detection)
- 64-bit Python recommended
- ~50-100 MB RAM usage

## Educational Value

This tool helps understand:
- **Digital Signal Processing**: FFT and frequency analysis
- **Radio Spectrum**: How different services use frequency ranges
- **Networking**: WiFi frequencies and channel allocation
- **Acoustics**: Audio frequency characteristics
- **Real-time Processing**: Event-driven display updates

## Advanced: Working with Real Radio Hardware

To receive actual radio broadcasts (requires additional hardware):

1. **RTL-SDR Dongle** (~$25)
   - Software Defined Radio receiver
   - 24 MHz to 1766 MHz coverage
   - Use with libraries like `pyrtlsdr` or `gr-osmosdr`

2. **Recommended Libraries**
   - `pyrtlsdr` - RTL-SDR Python interface
   - `GnuRadio` - Advanced signal processing
   - `CubicSDR` - GUI for SDR receivers

3. **Extended Analyzer (Future)**
   - Integrate RTL-SDR support
   - Real-time FM/AM demodulation
   - Spectrum analyzer for radio bands

## License

Open source - use freely for educational and personal purposes.

## Future Enhancements

- [ ] Recording frequency data to file
- [ ] Frequency alarm/notification system
- [ ] Real-time spectrum waterfall view
- [ ] RTL-SDR hardware support
- [ ] AM/FM radio demodulation
- [ ] Frequency database and identification
- [ ] Multi-threaded WiFi scanning
- [ ] Export data to CSV

## Tips & Tricks

1. **Best Results**: Use in a quiet environment for clearer audio analysis
2. **WiFi Optimization**: Run WiFi scan (SPACE) to get fresh network list
3. **Frequency ID**: Use reference chart to identify detected frequencies
4. **Monitoring**: Leave running to track WiFi changes over time
5. **Testing**: Generate test tones with online tone generators

Enjoy exploring the wireless spectrum around you!
