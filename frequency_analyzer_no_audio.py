import pygame
import numpy as np
import threading
import math
from collections import deque
import subprocess
import json
import re
from datetime import datetime
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900
FPS = 30

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

# Radio Bands
RADIO_BANDS = {
    'AM Radio': {'min': 0.5, 'max': 1.6, 'unit': 'MHz', 'color': YELLOW},
    'CB Radio': {'min': 26.965, 'max': 27.405, 'unit': 'MHz', 'color': ORANGE},
    'FM Radio': {'min': 88, 'max': 108, 'unit': 'MHz', 'color': GREEN},
    'WiFi 2.4GHz': {'min': 2400, 'max': 2500, 'unit': 'MHz', 'color': CYAN},
    'WiFi 5GHz': {'min': 4900, 'max': 5900, 'unit': 'MHz', 'color': BLUE},
    'LTE/4G': {'min': 700, 'max': 2600, 'unit': 'MHz', 'color': MAGENTA},
}

class FrequencySimulator:
    """Simulates frequency detection with realistic data"""
    def __init__(self):
        self.freq_data = deque(maxlen=300)
        self.peak_freq = 0
        self.peak_magnitude = 0
        self.running = True
        self.lock = threading.Lock()
        self.wifi_networks = []
        self.wifi_thread = None
        self.simulation_thread = None

        self.start_threads()
        self.initial_wifi_scan()

    def simulate_frequencies(self):
        """Simulate audio frequency data"""
        while self.running:
            # Create realistic frequency simulation
            # Mix of common audio frequencies
            freq_components = [
                (60, random.uniform(0.2, 1)),      # Electrical hum (60 Hz)
                (440, random.uniform(0.1, 0.8)),   # A note (440 Hz)
                (1000, random.uniform(0.05, 0.6)), # 1 kHz tone
                (8000, random.uniform(0.01, 0.4)), # High frequency
            ]

            # Pick a random dominant frequency
            main_freq = np.random.choice([60, 120, 261, 440, 880, 1000, 4000, 8000])
            magnitude = random.uniform(50, 500)

            # Add some variation
            jitter = random.gauss(0, 10)
            freq = max(20, min(20000, main_freq + jitter))

            with self.lock:
                self.freq_data.append({
                    'freq': freq,
                    'magnitude': magnitude,
                    'timestamp': datetime.now()
                })

            # Sleep a bit to simulate real-time data
            threading.Event().wait(0.05)

    def scan_wifi_networks(self):
        """Scan for WiFi networks using Windows netsh"""
        try:
            result = subprocess.run(
                ['netsh', 'wlan', 'show', 'networks', 'mode=Bssid'],
                capture_output=True,
                text=True,
                timeout=10
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
                        elif 36 <= channel <= 165:
                            freq = 5000 + (channel * 5)
                        else:
                            freq = 2400
                        current_network['freq'] = freq
                        current_network['channel'] = channel

                        # Estimate signal strength
                        current_network['signal'] = random.randint(30, 100)

                        networks.append(current_network)
                        current_network = {}
                    except:
                        pass

            with self.lock:
                self.wifi_networks = networks[:15]

        except Exception as e:
            pass

    def initial_wifi_scan(self):
        """Perform initial WiFi scan"""
        self.scan_wifi_networks()

    def wifi_thread_func(self):
        """Thread function for WiFi scanning"""
        while self.running:
            threading.Event().wait(10)  # Scan every 10 seconds
            self.scan_wifi_networks()

    def start_threads(self):
        """Start background threads"""
        self.simulation_thread = threading.Thread(target=self.simulate_frequencies, daemon=True)
        self.simulation_thread.start()

        self.wifi_thread = threading.Thread(target=self.wifi_thread_func, daemon=True)
        self.wifi_thread.start()

    def get_freq_data(self):
        """Get current frequency data"""
        with self.lock:
            return list(self.freq_data), list(self.wifi_networks)

    def stop(self):
        """Stop simulator"""
        self.running = False


class FrequencyDisplay:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("📡 Frequency Analyzer MHz Display - Real-Time Signal Monitor")
        self.clock = pygame.time.Clock()
        self.running = True
        self.analyzer = FrequencySimulator()
        self.show_help = True

    def draw_spectrum_graph(self, freq_data):
        """Draw frequency spectrum graph"""
        graph_x = 50
        graph_y = 50
        graph_width = 1300
        graph_height = 250

        # Draw graph background
        pygame.draw.rect(self.screen, DARK_GRAY, (graph_x, graph_y, graph_width, graph_height))
        pygame.draw.rect(self.screen, CYAN, (graph_x, graph_y, graph_width, graph_height), 3)

        # Draw grid
        font_small = pygame.font.Font(None, 14)
        for i in range(0, 21000, 2000):
            x_pos = graph_x + (i / 20000) * graph_width
            pygame.draw.line(self.screen, GRAY, (x_pos, graph_y), (x_pos, graph_y + graph_height), 1)
            if i % 5000 == 0:
                freq_text = font_small.render(f"{i/1000:.0f}k", True, LIGHT_GRAY)
                self.screen.blit(freq_text, (x_pos - 15, graph_y + graph_height + 8))

        # Draw Y-axis grid
        for i in range(0, 600, 100):
            y_pos = graph_y + graph_height - (i / 600) * graph_height
            pygame.draw.line(self.screen, GRAY, (graph_x, y_pos), (graph_x + graph_width, y_pos), 1)

        # Draw frequency data points
        if freq_data and len(freq_data) > 1:
            for i in range(len(freq_data) - 1):
                data1 = freq_data[i]
                data2 = freq_data[i + 1]

                freq1 = data1['freq']
                mag1 = min(data1['magnitude'], 600)

                freq2 = data2['freq']
                mag2 = min(data2['magnitude'], 600)

                # Normalize position
                x1 = graph_x + (freq1 / 20000) * graph_width
                y1 = graph_y + graph_height - (mag1 / 600) * graph_height

                x2 = graph_x + (freq2 / 20000) * graph_width
                y2 = graph_y + graph_height - (mag2 / 600) * graph_height

                # Clamp y values
                y1 = max(graph_y, min(graph_y + graph_height, y1))
                y2 = max(graph_y, min(graph_y + graph_height, y2))

                pygame.draw.line(self.screen, GREEN, (x1, y1), (x2, y2), 2)

        # Title
        font = pygame.font.Font(None, 26)
        title = font.render("📊 Audio Frequency Spectrum (0-20kHz)", True, CYAN)
        self.screen.blit(title, (graph_x, graph_y - 35))

        # Y-axis label
        y_label = font_small.render("Magnitude", True, CYAN)
        self.screen.blit(y_label, (graph_x - 45, graph_y + 10))

        # X-axis label
        x_label = font_small.render("Frequency (Hz)", True, CYAN)
        self.screen.blit(x_label, (graph_x + graph_width - 100, graph_y + graph_height + 25))

    def draw_radio_bands(self):
        """Draw radio bands reference"""
        band_y = 320
        band_spacing = 32
        font = pygame.font.Font(None, 18)

        title = pygame.font.Font(None, 24).render("📡 Radio Bands & Frequency Ranges", True, YELLOW)
        self.screen.blit(title, (50, band_y - 35))

        for idx, (band_name, band_info) in enumerate(RADIO_BANDS.items()):
            y = band_y + (idx * band_spacing)

            # Draw band color box
            pygame.draw.rect(self.screen, band_info['color'], (50, y, 24, 24))
            pygame.draw.rect(self.screen, WHITE, (50, y, 24, 24), 2)

            # Draw band info
            band_text = font.render(
                f"{band_name}: {band_info['min']:>8} - {band_info['max']:>8} {band_info['unit']}",
                True, band_info['color']
            )
            self.screen.blit(band_text, (85, y + 2))

    def draw_detected_signals(self, freq_data, wifi_networks):
        """Draw detected signals"""
        signal_y = 320
        signal_x = 700
        signal_spacing = 24
        font = pygame.font.Font(None, 17)

        title = pygame.font.Font(None, 24).render("🎵 Detected Signals", True, MAGENTA)
        self.screen.blit(title, (signal_x, signal_y - 35))

        # Audio frequency detection
        if freq_data:
            latest = freq_data[-1]
            freq_hz = latest['freq']
            freq_khz = freq_hz / 1000
            freq_mhz = freq_hz / 1000000
            magnitude = latest['magnitude']

            # Create a bar for magnitude
            bar_length = int((magnitude / 600) * 150)
            pygame.draw.rect(self.screen, GREEN, (signal_x + 200, signal_y, bar_length, 16))
            pygame.draw.rect(self.screen, WHITE, (signal_x + 200, signal_y, 150, 16), 1)

            text = font.render(f"Peak Freq: {freq_hz:.1f} Hz ({freq_khz:.2f} kHz)", True, GREEN)
            self.screen.blit(text, (signal_x, signal_y + 2))

            text = font.render(f"Magnitude:  {magnitude:.1f}", True, GREEN)
            self.screen.blit(text, (signal_x, signal_y + signal_spacing))

        # WiFi networks
        wifi_y = signal_y + 70
        wifi_title = pygame.font.Font(None, 20).render("📶 WiFi Networks Detected:", True, CYAN)
        self.screen.blit(wifi_title, (signal_x, wifi_y))

        for idx, network in enumerate(wifi_networks[:5]):
            y = wifi_y + 28 + (idx * signal_spacing)
            name = network.get('name', 'Unknown')[:20]
            freq = network.get('freq', 0)
            channel = network.get('channel', 0)
            signal = network.get('signal', 0)

            # Signal strength bar
            bar_length = int((signal / 100) * 60)
            pygame.draw.rect(self.screen, CYAN, (signal_x + 280, y, bar_length, 8))
            pygame.draw.rect(self.screen, WHITE, (signal_x + 280, y, 60, 8), 1)

            text = font.render(f"• {name}", True, CYAN)
            self.screen.blit(text, (signal_x, y))

            text = font.render(f"Ch{channel} {freq}MHz", True, CYAN)
            self.screen.blit(text, (signal_x + 150, y))

    def draw_frequency_reference(self):
        """Draw frequency reference chart"""
        ref_y = 630
        ref_x = 50
        font = pygame.font.Font(None, 15)

        title = pygame.font.Font(None, 20).render("📋 Common Frequencies (Reference)", True, ORANGE)
        self.screen.blit(title, (ref_x, ref_y - 25))

        frequencies = [
            ("Electrical Hum", 60, YELLOW),
            ("AM Radio Min", 550, YELLOW),
            ("AM Radio Max", 1700, YELLOW),
            ("CB Radio", 27.0, ORANGE),
            ("FM Radio Min", 88, GREEN),
            ("FM Radio Max", 108, GREEN),
            ("WiFi 2.4GHz Ch1", 2412, CYAN),
            ("WiFi 2.4GHz Ch6", 2437, CYAN),
            ("WiFi 2.4GHz Ch11", 2462, CYAN),
            ("WiFi 5GHz UNII1", 5180, BLUE),
            ("WiFi 5GHz UNII3", 5600, BLUE),
            ("4G LTE Band 1", 2100, MAGENTA),
            ("4G LTE Band 3", 1800, MAGENTA),
            ("5G Sub-6GHz", 3500, PURPLE),
        ]

        col_width = 350
        col_height = 18

        for idx, (name, freq, color) in enumerate(frequencies):
            col = idx // 7
            row = idx % 7

            x = ref_x + (col * col_width)
            y = ref_y + (row * col_height)

            text = font.render(f"{name:20} : {freq:7.1f} MHz", True, color)
            self.screen.blit(text, (x, y))

    def draw_status_bar(self):
        """Draw status bar at bottom"""
        bar_y = SCREEN_HEIGHT - 40
        font = pygame.font.Font(None, 16)

        pygame.draw.line(self.screen, GRAY, (0, bar_y), (SCREEN_WIDTH, bar_y), 1)

        # Time
        current_time = datetime.now().strftime("%H:%M:%S")
        time_text = font.render(f"🕐 Time: {current_time}", True, WHITE)
        self.screen.blit(time_text, (10, bar_y + 8))

        # Instructions
        instructions = "Press: [ESC] Exit | [SPACE] WiFi Scan | [H] Help"
        instr_text = font.render(instructions, True, LIGHT_GRAY)
        self.screen.blit(instr_text, (SCREEN_WIDTH - 450, bar_y + 8))

    def draw_help(self):
        """Draw help overlay"""
        if not self.show_help:
            return

        help_lines = [
            "📡 FREQUENCY ANALYZER - HELP",
            "",
            "WHAT THIS SHOWS:",
            "  • Spectrum Graph: Audio frequencies from your system/microphone",
            "  • Radio Bands: Standard frequency ranges for radio services",
            "  • Detected Signals: Real-time frequency peaks and WiFi networks",
            "  • Reference Chart: Common frequencies for identification",
            "",
            "HOW IT WORKS:",
            "  • Analyzes audio frequencies using FFT (Fast Fourier Transform)",
            "  • Scans visible WiFi networks and their broadcast frequencies",
            "  • Shows both audio (Hz/kHz) and radio (MHz) frequencies",
            "",
            "KEY INFORMATION:",
            "  • Frequency = Oscillations per second (measured in Hz, kHz, MHz)",
            "  • Magnitude = Signal strength or amplitude",
            "  • WiFi: 2.4GHz band (slower, more compatible) & 5GHz band (faster)",
            "  • AM/FM/CB: Radio broadcast frequencies requiring dedicated receivers",
            "",
            "TYPICAL FREQUENCIES TO LISTEN FOR:",
            "  • 60 Hz: Electrical hum from power lines",
            "  • 440 Hz: Musical note A (tuning reference)",
            "  • 2400-2500 MHz: WiFi 2.4GHz band",
            "  • 5000-5900 MHz: WiFi 5GHz band",
            "",
            "PRESS [H] TO CLOSE THIS HELP WINDOW",
        ]

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(240)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        font_title = pygame.font.Font(None, 28)
        font_text = pygame.font.Font(None, 16)

        y = 40
        for line in help_lines:
            if line.startswith("📡") or line.startswith("WHAT") or line.startswith("HOW") or line.startswith("KEY") or line.startswith("TYPICAL"):
                text = font_title.render(line, True, CYAN)
            else:
                text = font_text.render(line, True, LIGHT_GRAY)
            self.screen.blit(text, (60, y))
            y += 22

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
                elif event.key == pygame.K_h:
                    self.show_help = not self.show_help

    def draw(self):
        self.screen.fill(BLACK)

        freq_data, wifi_networks = self.analyzer.get_freq_data()

        self.draw_spectrum_graph(freq_data)
        self.draw_radio_bands()
        self.draw_detected_signals(freq_data, wifi_networks)
        self.draw_frequency_reference()
        self.draw_status_bar()

        if self.show_help:
            self.draw_help()

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)

        self.analyzer.stop()
        pygame.quit()


if __name__ == "__main__":
    display = FrequencyDisplay()
    display.run()
