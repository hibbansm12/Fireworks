"""
Kelas Particle untuk mengelola partikel kembang api.
"""
import random
import math

class Particle:
    """
    Kelas untuk mengelola partikel kembang api.
    Menangani properti dan perilaku partikel individual.
    """
    def __init__(self, position, color, velocity, lifetime, size=0.2, is_launch_particle=False):
        # Properti dasar
        self.position = list(position)      # [x, y]
        self.color = list(color)            # [R, G, B, A]
        self.velocity = list(velocity)      # [vx, vy]
        self.lifetime = lifetime            # Waktu hidup (detik)
        self.age = 0.0                      # Usia partikel
        
        # Properti visual
        self.initial_size = size            # Ukuran awal
        self.size = size                    # Ukuran saat ini
        self.shape = random.choice(["circle", "square"])  # Bentuk partikel
        self.rotation = 0.0                 # Rotasi (derajat)
        self.rotation_speed = random.uniform(-180, 180)  # Kecepatan rotasi
        
        # Properti perilaku
        self.is_launch_particle = is_launch_particle  # Partikel peluncuran
        self.is_curve_end = False           # Partikel ujung kurva
        self.expansion_phase = True         # Fase ekspansi
        self.expansion_time = random.uniform(0.2, 0.5)  # Durasi ekspansi
        self.has_peaked = False             # Status puncak
        self.peak_time = 0                  # Waktu puncak
        
        # Efek visual
        self.trail = []                     # Ekor partikel
        self.trail_counter = 0              # Counter ekor
        self.fall_fade_speed = random.uniform(0.5, 1.5)  # Kecepatan memudar 