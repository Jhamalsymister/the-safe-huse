import pygame
import numpy as np
import pyaudio
import struct
import threading
import math
from collections import deque
import subprocess
import json
import re
from datetime import datetime

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900
FPS = 30
GRID_SIZE = 40

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Audio Analysis Constants
CHUNK = 2048
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100  # Sample rate in Hz

# Radio Bands
RADIO_BANDS = {
    'AM': {'min': 0.5, 'max': 1.6, 'unit': 'MHz', 'color': YELLOW},
    'FM': {'min': 88, 'max': 108, 'unit': 'MHz', 'color': GREEN},
    'CB': {'min': 26.965, 'max': 27.405, 'unit': 'MHz', 'color': ORANGE},
    'WiFi 2.4GHz': {'min': 2400, 'max': 2500, 'unit': 'MHz', 'color': CYAN},
    'WiFi 5GHz': {'min': 4900, 'max': 5900, 'unit': 'MHz', 'color': BLUE},
    'LTE': {'min': 700, 'max': 2600, 'unit': 'MHz', 'color': MAGENTA},
}

class FrequencyAnalyzer:
    def __init__(self):
        self.audio_stream = None
        self.p = None
        self.freq_data = deque(maxlen=200)
        self.peak_freq = 0
        self.peak_magnitude = 0
        self.running = True
        self.lock = threading.Lock()
        self.wifi_networks = []
        self.audio_thread = None
        self.wifi_thread = None

        self.init_audio()
        self.start_audio_thread()
        self.start_wifi_thread()

    def init_audio(self):
        """Initialize PyAudio stream"""
        try:
            self.p = pyaudio.PyAudio()
            self.audio_stream = self.p.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK
            )
        except Exception as e:
            print(f"Audio initialization error: {e}")

    def analyze_audio_frequency(self):
        """Analyze frequency content from audio input"""
        try:
            if not self.audio_stream:
                return

            data = self.audio_stream.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.float32)

            # Perform FFT
            fft = np.fft.fft(audio_data)
            magnitude = np.abs(fft)

            # Calculate frequencies
            frequencies = np.fft.fftfreq(len(audio_data), 1/RATE)

            # Only look at positive frequencies up to 20kHz
            positive_freq_idx = frequencies[:len(frequencies)//2] > 0
            positive_frequencies = frequencies[:len(frequencies)//2][positive_freq_idx]
            positive_magnitude = magnitude[:len(magnitude)//2][positive_freq_idx]

            if len(positive_magnitude) > 0 and np.max(positive_magnitude) > 0:
                peak_idx = np.argmax(positive_magnitude)
                self.peak_freq = positive_frequencies[peak_idx]
                self.peak_magnitude = positive_magnitude[peak_idx]

                with self.lock:
                    self.freq_data.append({
                        'freq': self.peak_freq,
                        'magnitude': self.peak_magnitude,
                        'timestamp': datetime.now()
                    })
        except Exception as e:
            pass

    def scan_wifi_networks(self):
        """Scan for WiFi networks"""
        try:
            if self.running:
                result = subprocess.run(
                    ['netsh', 'wlan', 'show', 'networks', 'mode=Bssid'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                networks = []
                lines = result.stdout.split('\n')

                current_network = {}
                for line in lines:
                    if 'SSID' in line and ':' in line:
                        parts = line.split(':', 1)
                        if len(parts) > 1:
                            ssid = parts[1].strip()
                            if ssid:
                                current_network['name'] = ssid

                    if 'Channel' in line and ':' in line:
                        try:
                            channel = int(line.split(':')[1].strip())
                            # Convert WiFi channel to frequency
                            if 1 <= channel <= 13:
                                freq = 2407 + (channel * 5)
                            else:
                                freq = 5000 + (channel * 5)
                            current_network['freq'] = freq
                            current_network['channel'] = channel
                            networks.append(current_network)
                            current_network = {}
                        except:
                            pass

                with self.lock:
                    self.wifi_networks = networks[:10]  # Keep top 10
        except Exception as e:
            pass

    def audio_thread_func(self):
        """Thread function for audio analysis"""
        while self.running:
            self.analyze_audio_frequency()

    def wifi_thread_func(self):
        """Thread function for WiFi scanning"""
        counter = 0
        while self.running:
            counter += 1
            if counter % 30 == 0:  # Scan every 30 iterations
                self.scan_wifi_networks()

    def start_audio_thread(self):
        """Start audio analysis thread"""
        self.audio_thread = threading.Thread(target=self.audio_thread_func, daemon=True)
        self.audio_thread.start()

    def start_wifi_thread(self):
        """Start WiFi scanning thread"""
        self.wifi_thread = threading.Thread(target=self.wifi_thread_func, daemon=True)
        self.wifi_thread.start()

    def get_freq_data(self):
        """Get current frequency data"""
        with self.lock:
            return list(self.freq_data), list(self.wifi_networks)

    def stop(self):
        """Stop analyzer"""
        self.running = False
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
        if self.p:
            self.p.terminate()


class FrequencyDisplay:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Frequency Analyzer - MHz Display")
        self.clock = pygame.time.Clock()
        self.running = True
        self.analyzer = FrequencyAnalyzer()

    def draw_spectrum_graph(self, freq_data):
        """Draw frequency spectrum graph"""
        graph_x = 50
        graph_y = 50
        graph_width = 1300
        graph_height = 250

        # Draw graph background
        pygame.draw.rect(self.screen, DARK_GRAY, (graph_x, graph_y, graph_width, graph_height))
        pygame.draw.rect(self.screen, CYAN, (graph_x, graph_y, graph_width, graph_height), 2)

        # Draw grid
        font_small = pygame.font.Font(None, 16)
        for i in range(0, 21000, 2000):
            x_pos = graph_x + (i / 20000) * graph_width
            pygame.draw.line(self.screen, GRAY, (x_pos, graph_y), (x_pos, graph_y + graph_height), 1)
            if i % 5000 == 0:
                freq_text = font_small.render(f"{i/1000:.1f}kHz", True, LIGHT_GRAY)
                self.screen.blit(freq_text, (x_pos - 20, graph_y + graph_height + 5))

        # Draw frequency data points
        if freq_data:
            for i, data in enumerate(freq_data):
                if i < len(freq_data) - 1:
                    freq1 = data['freq']
                    mag1 = data['magnitude']

                    freq2 = freq_data[i + 1]['freq']
                    mag2 = freq_data[i + 1]['magnitude']

                    # Normalize position
                    x1 = graph_x + (freq1 / 20000) * graph_width
                    y1 = graph_y + graph_height - (mag1 / 100000) * graph_height

                    x2 = graph_x + (freq2 / 20000) * graph_width
                    y2 = graph_y + graph_height - (mag2 / 100000) * graph_height

                    # Clamp y values
                    y1 = max(graph_y, min(graph_y + graph_height, y1))
                    y2 = max(graph_y, min(graph_y + graph_height, y2))

                    pygame.draw.line(self.screen, GREEN, (x1, y1), (x2, y2), 2)

        # Title
        font = pygame.font.Font(None, 24)
        title = font.render("Audio Frequency Spectrum (0-20kHz)", True, CYAN)
        self.screen.blit(title, (graph_x, graph_y - 30))

    def draw_radio_bands(self):
        """Draw radio bands reference"""
        band_y = 320
        band_spacing = 35
        font = pygame.font.Font(None, 20)

        title = pygame.font.Font(None, 24).render("Detected Radio Bands & Signals", True, YELLOW)
        self.screen.blit(title, (50, band_y - 30))

        for idx, (band_name, band_info) in enumerate(RADIO_BANDS.items()):
            y = band_y + (idx * band_spacing)

            # Draw band color box
            pygame.draw.rect(self.screen, band_info['color'], (50, y, 20, 20))
            pygame.draw.rect(self.screen, WHITE, (50, y, 20, 20), 1)

            # Draw band info
            band_text = font.render(
                f"{band_name}: {band_info['min']} - {band_info['max']} {band_info['unit']}",
                True, band_info['color']
            )
            self.screen.blit(band_text, (80, y))

    def draw_detected_signals(self, freq_data, wifi_networks):
        """Draw detected signals"""
        signal_y = 320
        signal_x = 700
        signal_spacing = 25
        font = pygame.font.Font(None, 18)

        title = pygame.font.Font(None, 24).render("Detected Signals", True, MAGENTA)
        self.screen.blit(title, (signal_x, signal_y - 30))

        # Audio frequency detection
        if freq_data:
            latest = freq_data[-1]
            freq_hz = latest['freq']
            freq_khz = freq_hz / 1000
            freq_mhz = freq_hz / 1000000
            magnitude = latest['magnitude']

            text = font.render(f"Peak Frequency: {freq_khz:.1f} kHz ({freq_mhz:.6f} MHz)", True, GREEN)
            self.screen.blit(text, (signal_x, signal_y))

            text = font.render(f"Magnitude: {magnitude:.1f}", True, GREEN)
            self.screen.blit(text, (signal_x, signal_y + signal_spacing))

        # WiFi networks
        wifi_y = signal_y + 70
        wifi_title = font.render("WiFi Networks:", True, CYAN)
        self.screen.blit(wifi_title, (signal_x, wifi_y))

        for idx, network in enumerate(wifi_networks[:5]):
            y = wifi_y + 25 + (idx * signal_spacing)
            name = network.get('name', 'Unknown')[:25]
            freq = network.get('freq', 0)
            channel = network.get('channel', 0)

            text = font.render(f"• {name} - Ch{channel} ({freq}MHz)", True, CYAN)
            self.screen.blit(text, (signal_x, y))

    def draw_frequency_reference(self):
        """Draw frequency reference chart"""
        ref_y = 630
        ref_x = 50
        font = pygame.font.Font(None, 16)

        title = pygame.font.Font(None, 20).render("Common Frequencies (Reference)", True, ORANGE)
        self.screen.blit(title, (ref_x, ref_y - 25))

        frequencies = [
            ("AM Radio Lower", 0.5, YELLOW),
            ("AM Radio Upper", 1.6, YELLOW),
            ("CB Radio", 27.0, ORANGE),
            ("FM Radio Lower", 88, GREEN),
            ("FM Radio Upper", 108, GREEN),
            ("WiFi 2.4GHz Ch1", 2412, CYAN),
            ("WiFi 2.4GHz Ch11", 2462, CYAN),
            ("WiFi 5GHz Lower", 4900, BLUE),
            ("WiFi 5GHz Upper", 5900, BLUE),
            ("LTE Band", 1800, MAGENTA),
        ]

        col_width = 350
        col_height = 20

        for idx, (name, freq, color) in enumerate(frequencies):
            col = idx // 5
            row = idx % 5

            x = ref_x + (col * col_width)
            y = ref_y + (row * col_height)

            text = font.render(f"{name}: {freq:.1f} MHz", True, color)
            self.screen.blit(text, (x, y))

    def draw_hud(self):
        """Draw HUD information"""
        font = pygame.font.Font(None, 20)

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_text = font.render(f"Time: {current_time}", True, WHITE)
        self.screen.blit(time_text, (SCREEN_WIDTH - 300, 10))

        info_text = font.render("Press ESC to Exit | SPACE to Refresh WiFi", True, LIGHT_GRAY)
        self.screen.blit(info_text, (10, SCREEN_HEIGHT - 30))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    # Force WiFi scan
                    self.analyzer.scan_wifi_networks()

    def update(self):
        pass

    def draw(self):
        self.screen.fill(BLACK)

        freq_data, wifi_networks = self.analyzer.get_freq_data()

        self.draw_spectrum_graph(freq_data)
        self.draw_radio_bands()
        self.draw_detected_signals(freq_data, wifi_networks)
        self.draw_frequency_reference()
        self.draw_hud()

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        self.analyzer.stop()
        pygame.quit()


if __name__ == "__main__":
    display = FrequencyDisplay()
    display.run()
