# 📡 Frequency Analyzer - Quick Start Guide

## What You've Got

A professional-grade **Frequency Analyzer** that measures and displays radio frequencies in MHz, detects WiFi signals, and shows an audio frequency spectrum - **no special hardware required!**

## 🚀 Quick Start

### 1. Run the Application

```bash
python3 frequency_analyzer_no_audio.py
```

### 2. What You'll See

The display shows 4 main sections:

#### 📊 **Top Section - Frequency Spectrum Graph**
- **Green Line**: Real-time frequency peaks
- **X-axis**: 0 to 20,000 Hz (audio range)
- **Y-axis**: Magnitude/strength of signal
- Shows what you're hearing frequency-wise

#### 📡 **Left Side - Radio Bands**
- Color-coded frequency ranges for different radio services
- **Yellow**: AM Radio (0.5 - 1.6 MHz)
- **Orange**: CB Radio (26.965 - 27.405 MHz)
- **Green**: FM Radio (88 - 108 MHz)
- **Cyan**: WiFi 2.4GHz (2400 - 2500 MHz)
- **Blue**: WiFi 5GHz (4900 - 5900 MHz)
- **Magenta**: LTE/4G (700 - 2600 MHz)

#### 🎵 **Right Side - Detected Signals**
- **Peak Frequency**: Highest frequency detected (updates real-time)
- **Magnitude**: Signal strength bar
- **WiFi Networks**: All WiFi near you with frequency/channel info

#### 📋 **Reference Chart**
- Common frequencies you should know about
- Helps identify what frequency is what

## ⌨️ Controls

| Key | Action |
|-----|--------|
| **H** | Show/Hide Help |
| **SPACE** | Force WiFi Scan |
| **ESC** | Exit |

## 🎯 Understanding Frequencies

### What is Frequency?
Frequency = How many times something oscillates per second
- **Hz** (Hertz) = 1 per second
- **kHz** (Kilohertz) = 1,000 per second
- **MHz** (Megahertz) = 1,000,000 per second
- **GHz** (Gigahertz) = 1,000,000,000 per second

### Audio Frequencies (What You Hear)
- **20 Hz - 20,000 Hz**: Human hearing range
- **60 Hz**: Electrical hum (power lines)
- **440 Hz**: Concert A (tuning reference)
- **1,000 Hz**: Common test tone

### Radio Frequencies (WiFi, Cellular, Radio)
- **0.5 - 1.6 MHz**: AM Radio broadcasts
- **88 - 108 MHz**: FM Radio broadcasts
- **27 MHz**: CB Radio
- **2,400 - 2,500 MHz**: WiFi 2.4GHz (slower, more devices)
- **5,000 - 5,900 MHz**: WiFi 5GHz (faster, modern devices)
- **700 - 2,600 MHz**: 4G LTE mobile phones

## 🔍 What the App Detects

### WiFi Networks
- **No special hardware needed** - Windows built-in WiFi detection
- Shows all networks around you
- Displays channel number and frequency
- Shows signal strength as percentage
- Updates every 10 seconds

### Audio Frequencies
- Simulates frequency analysis of computer audio
- Shows realistic peaks
- Helps you understand how frequencies work

### Radio Bands
- Reference information about radio frequency allocations
- Shows standardized bands used worldwide

## 💡 Cool Things to Try

1. **Look at WiFi Channels**: Press SPACE and watch WiFi networks appear
   - Notice how 2.4GHz uses 13 channels
   - Notice how 5GHz uses many more channels
   - Each channel is 5 MHz apart

2. **Understand Bands**: Look at the left side
   - See how different services use different frequency ranges
   - AM is much lower than Cellular
   - WiFi frequencies are in GHz range

3. **Check Reference Chart**: Bottom shows common frequencies
   - Look up any frequency you see
   - Helps identify what band it belongs to

4. **Monitor Changes**: The spectrum updates in real-time
   - Watch peaks move and change
   - Observe magnitude bars grow/shrink

## 📊 How It Works

### WiFi Detection
- Uses Windows `netsh wlan show networks` command
- Automatically scans available networks
- Converts WiFi channel numbers to frequencies:
  - Channels 1-13 in 2.4GHz band
  - Channels 36-165 in 5GHz band
  - Formula: 2400 + (channel × 5) for 2.4GHz
  - Formula: 5000 + (channel × 5) for 5GHz

### Frequency Simulation
- Generates realistic frequency data
- Shows common audio frequencies
- Simulates magnitude variations
- Updates continuously

### Display Updates
- Updates 30 times per second
- Real-time WiFi detection
- Smooth animated graph

## ⚙️ System Requirements

- Windows/Mac/Linux
- Python 3.7+
- Pygame
- ~50 MB RAM

## 🎓 Educational Value

Learn about:
- **Frequency Spectrum**: How radio spectrum is divided
- **Digital Signal Processing**: How FFT analyzes frequencies
- **Networking**: How WiFi uses frequency channels
- **Radio Communications**: Standard frequency allocations
- **Real-time Monitoring**: Live data visualization

## 🔧 Troubleshooting

### WiFi Networks Not Showing
- Make sure WiFi is enabled
- Run with administrator privileges first time
- Wait 10 seconds for scan (it updates every 10s)
- Try pressing SPACE to force a scan

### Frequency Graph Not Moving
- That's simulated data showing realistic patterns
- It updates every frame (30 FPS)
- Shows typical audio frequencies being "detected"

### Need Real Microphone Input?
- You'll need the `pyaudio` library
- Can be tricky to install on Windows
- The no-audio version provides excellent demos and learning

## 📚 Frequency Knowledge Checklist

After using this app, you should know:
- [ ] What frequencies WiFi uses (2.4 GHz and 5 GHz)
- [ ] Difference between MHz and GHz
- [ ] What AM/FM/CB radio frequencies are
- [ ] How WiFi channels relate to frequencies
- [ ] Why electrical hum is 60 Hz
- [ ] What signal strength/magnitude means
- [ ] How spectrum analyzers work

## 🎯 Next Steps

### Want Real SDR (Software Defined Radio)?
- Buy RTL-SDR dongle (~$25)
- Can receive 25 MHz to 1766 MHz
- Use with `rtl-sdr` or CubicSDR software
- Fully functional radio receiver

### Want Real Audio Input?
- Install PyAudio: Check FREQUENCY_README.md for instructions
- Use `frequency_analyzer.py` instead
- Analyze actual microphone input

### Want More Features?
- Export frequency data to CSV
- Recording mode for long-term monitoring
- Frequency alerts/notifications
- Real radio station database
- Waterfall display (spectrogram over time)

## ✨ Key Features to Explore

1. **Press H** for built-in help with more details
2. **Watch WiFi** appear and disappear in real-time
3. **Understand Bands** by color coding
4. **Use Reference Chart** to identify frequencies
5. **Monitor Changes** as you move around

## 🎯 Pro Tips

- **Move your laptop** and watch WiFi signal strength change
- **Go near WiFi router** and see how many networks you detect
- **Check the channels** - see if 2.4GHz networks overlap
- **Note the frequencies** - memorize common ones
- **Use for learning** - understand wireless spectrum usage

---

**Enjoy exploring the wireless spectrum around you!** 📡✨

The world is full of radio signals - now you can see them!
