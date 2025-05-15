"""
SIMULASI KEMBANG API
---------------------------------
Program ini mensimulasikan tampilan kembang api di latar belakang kota malam
menggunakan PyOpenGL dan Pygame.

Fitur:
- Simulasi kembang api dengan efek partikel
- Latar belakang kota dengan gedung-gedung
- Efek visual seperti bintang dan bulan
- Interaksi pengguna untuk meluncurkan kembang api

Anggota Kelompok:
- Anzar Rahman Permana  (227006082)
- Diaz Rifqi Munggaran  (227006087)
- Fajar Nurdiansyah     (227006077)
- Hibban Sani Muttaqin  (227006073)
- Muhammad Yusril Fauzi (227006067)

Grafika Komputer, 2025
"""

# ================== IMPORTS ==================
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
import time
import sys

# ================== KONFIGURASI ==================
# Konfigurasi layar
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60

# Konfigurasi partikel
PARTICLE_COUNT = 150
GRAVITY = [0.0, -9.8]
EXPANSION_BOOST = 1.2
DRAG_FACTOR = 0.2

# Konfigurasi kembang api
FIREWORK_LAUNCH_SPEED = 15.0
FIREWORK_LIFETIME = 2.0
FIREWORK_SIZE = 0.15

# ================== VARIABEL GLOBAL ==================
width, height = WINDOW_WIDTH, WINDOW_HEIGHT
random.seed(42)  # Seed tetap untuk konsistensi
stars = [(random.randint(0, width), random.randint(height // 2, height)) for _ in range(PARTICLE_COUNT)]

# Struktur data untuk menyimpan gedung
buildings = {
    "back": [],  # Layer belakang (siluet)
    "main": [],  # Layer utama (dengan jendela)
    "front": []  # Layer depan (opsional)
}

# ================== KELAS PARTIKEL ==================
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

# ================== KELAS KEMBANG API ==================
class Firework:
    """
    Kelas untuk mengelola kembang api.
    Menangani peluncuran, ledakan, dan perilaku kembang api.
    """
    def __init__(self, launch_pos):
        # Properti dasar
        self.particles = []
        self.launch_pos = launch_pos
        self.exploded = False
        self.explosion_time = 0.0
        
        # Efek visual
        self.trail_particles = []
        
        # Tema warna
        self.color_theme = random.choice([
            "red",       # Merah-oranye-kuning
            "blue",      # Biru-cyan-hijau
            "purple",    # Ungu-pink-magenta
            "gold",      # Emas-kuning-oranye
            "green",     # Hijau-lime-cyan
            "rainbow",   # Warna-warni
            "silver",    # Putih-abu-abu-biru muda
            "pink"       # Pink-magenta-ungu muda
        ])
        
        self.launch()

    def get_launch_color(self):
        # Dapatkan warna peluncuran berdasarkan tema
        if self.color_theme == "red":
            return [1.0, 0.3, 0.0, 1.0]  # Oranye kemerahan
        elif self.color_theme == "blue":
            return [0.2, 0.4, 1.0, 1.0]  # Biru
        elif self.color_theme == "purple":
            return [0.7, 0.2, 1.0, 1.0]  # Ungu
        elif self.color_theme == "gold":
            return [1.0, 0.8, 0.0, 1.0]  # Emas
        elif self.color_theme == "green":
            return [0.1, 0.8, 0.2, 1.0]  # Hijau
        elif self.color_theme == "rainbow":
            return [1.0, 1.0, 1.0, 1.0]  # Putih untuk rainbow
        elif self.color_theme == "silver":
            return [0.8, 0.8, 1.0, 1.0]  # Biru muda untuk silver
        elif self.color_theme == "pink":
            return [1.0, 0.5, 0.8, 1.0]  # Pink
        else:
            return [1.0, 1.0, 0.0, 1.0]  # Default kuning

    def get_color_variation(self, theme):
        if theme == "red":
            return [
                random.uniform(0.8, 1.0),    # R
                random.uniform(0.0, 0.5),    # G
                random.uniform(0.0, 0.2),    # B
                1.0
            ]
        elif theme == "blue":
            return [
                random.uniform(0.0, 0.2),    # R
                random.uniform(0.3, 0.8),    # G
                random.uniform(0.8, 1.0),    # B
                1.0
            ]
        elif theme == "purple":
            return [
                random.uniform(0.5, 0.9),    # R
                random.uniform(0.0, 0.4),    # G
                random.uniform(0.8, 1.0),    # B
                1.0
            ]
        elif theme == "gold":
            return [
                random.uniform(0.8, 1.0),    # R
                random.uniform(0.7, 1.0),    # G
                random.uniform(0.0, 0.3),    # B
                1.0
            ]
        elif theme == "green":
            return [
                random.uniform(0.0, 0.3),    # R
                random.uniform(0.7, 1.0),    # G
                random.uniform(0.0, 0.5),    # B
                1.0
            ]
        elif theme == "rainbow":
            # Pilih warna acak
            hue = random.random()
            # Konversi HSV ke RGB (sederhana)
            h = hue * 6.0
            i = int(h)
            f = h - i
            if i % 2 == 0:
                f = 1 - f
            n = 0.5
            if i == 0:
                return [1.0, f, n, 1.0]
            elif i == 1:
                return [f, 1.0, n, 1.0]
            elif i == 2:
                return [n, 1.0, f, 1.0]
            elif i == 3:
                return [n, f, 1.0, 1.0]
            elif i == 4:
                return [f, n, 1.0, 1.0]
            else:
                return [1.0, n, f, 1.0]
        elif theme == "silver":
            v = random.uniform(0.7, 1.0)
            return [v, v, random.uniform(v-0.1, v+0.1), 1.0]
        elif theme == "pink":
            return [
                random.uniform(0.9, 1.0),    # R
                random.uniform(0.4, 0.8),    # G
                random.uniform(0.7, 1.0),    # B
                1.0
            ]

    def launch(self):
        # Partikel utama (peluncuran)
        main_color = self.get_launch_color()  # Warna sesuai tema
        self.particles.append(Particle(
            position=self.launch_pos,
            color=main_color,
            velocity=[0, 15.0],  # Lebih tinggi dari fireworks_v1.py (aslinya 5.0)
            lifetime=2.0,
            size=0.15,  # Ukuran lebih kecil dari sebelumnya (0.3)
            is_launch_particle=True
        ))

    def explode(self):
        # Membuat partikel ledakan dengan pola melengkung
        explosion_pos = list(self.particles[0].position)  # Posisi ledakan
        
        # Membuat beberapa garis melengkung
        num_curves = random.randint(12, 18)  # Lebih banyak garis melengkung (aslinya 10-15)
        
        for curve_idx in range(num_curves):
            # Arah dasar untuk kurva ini
            base_angle = 2 * math.pi * curve_idx / num_curves
            # Jumlah titik dalam kurva
            num_points = random.randint(10, 15)  # Lebih banyak partikel (aslinya 8-12)
            
            # Warna untuk kurva ini
            curve_color = self.get_color_variation(self.color_theme)
            
            # Buat partikel sepanjang kurva
            for i in range(num_points):
                # Variasi sudut untuk membuat kurva
                angle_variation = math.sin(i / num_points * math.pi) * 0.5
                angle = base_angle + angle_variation
                
                # Kecepatan lebih tinggi di tengah kurva
                speed_factor = 1.0 + math.sin(i / num_points * math.pi) * 0.4  # Kurangi faktor kecepatan lagi (aslinya 0.6)
                speed = random.uniform(1.5, 3.5) * speed_factor  # Kurangi kecepatan dasar lagi (aslinya 2.0-4.5)
                
                velocity = [
                    math.cos(angle) * speed,
                    math.sin(angle) * speed
                ]
                
                # Ukuran partikel lebih besar di ujung kurva
                is_end = (i == 0 or i == num_points - 1)
                size = random.uniform(0.25, 0.4) if is_end else random.uniform(0.1, 0.2)  # Kurangi ukuran (aslinya 0.4-0.6 untuk ujung)
                
                particle = Particle(
                    position=explosion_pos,
                    color=curve_color,
                    velocity=velocity,
                    lifetime=random.uniform(1.5, 2.5),  # Hidup lebih lama (aslinya 1.2-2.0)
                    size=size
                )
                
                # Tandai partikel ujung
                if is_end:
                    particle.is_curve_end = True
                
                self.particles.append(particle)
        
        self.exploded = True
        self.explosion_time = 0.0  # Reset waktu ledakan

    def update(self, dt):
        # Update partikel
        if self.exploded:
            self.explosion_time += dt
        
        gravity = [0.0, -9.8]  # Sama seperti fireworks_v1.py
        expansion_boost = 1.2  # Kurangi faktor boost pada fase ekspansi (aslinya 1.5)
        drag_factor = 0.2  # Tambahkan faktor hambatan untuk memperlambat partikel
        
        for p in self.particles:
            # Periksa apakah partikel mencapai puncak (kecepatan vertikal berubah dari positif ke negatif)
            if not p.is_launch_particle and not p.has_peaked and p.velocity[1] < 0:
                p.has_peaked = True
                p.peak_time = p.age
            
            # Update fisika
            if not p.is_launch_particle and p.expansion_phase and p.age < p.expansion_time:
                # Fase ekspansi: melambatkan gravitasi dan menambah boost pada kecepatan
                p.velocity[0] *= (1.0 + 0.1 * dt * expansion_boost)  # Kurangi boost lagi (aslinya 0.15)
                p.velocity[1] *= (1.0 + 0.1 * dt * expansion_boost)  # Kurangi boost lagi (aslinya 0.15)
                # Gravitasi lebih rendah selama ekspansi
                p.velocity[0] += gravity[0] * dt * 0.3
                p.velocity[1] += gravity[1] * dt * 0.3
            else:
                # Fase normal: gravitasi penuh
                p.expansion_phase = False
                
                # Tambahkan hambatan (drag) untuk memperlambat partikel
                if not p.is_launch_particle:
                    speed = math.sqrt(p.velocity[0]**2 + p.velocity[1]**2)
                    if speed > 0.5:  # Hanya berikan hambatan jika kecepatan cukup tinggi
                        drag = drag_factor * speed * dt
                        p.velocity[0] *= (1.0 - drag)
                        p.velocity[1] *= (1.0 - drag)
                
                p.velocity[0] += gravity[0] * dt
                p.velocity[1] += gravity[1] * dt
            
            p.position[0] += p.velocity[0] * dt
            p.position[1] += p.velocity[1] * dt
            
            # Tambahkan partikel ke ekor setiap beberapa frame
            p.trail_counter += dt
            if p.trail_counter > 0.02:  # Tambahkan ekor lebih sering (aslinya 0.03)
                p.trail_counter = 0
                # Buat salinan posisi dan warna yang memudar untuk ekor
                trail_color = p.color.copy()
                trail_color[3] *= 0.85  # Lebih terang (aslinya 0.7)
                
                # Lebih banyak partikel ekor untuk partikel ujung
                trail_count = 1
                if p.is_curve_end:
                    trail_count = 2  # Partikel ujung lebih banyak ekor
                
                for _ in range(trail_count):
                    p.trail.append({
                        'pos': p.position.copy(),
                        'color': trail_color.copy(),
                        'age': 0,
                        'max_age': 0.7,  # Ekor bertahan lebih lama (aslinya 0.5)
                        'size': p.size * random.uniform(0.6, 0.9)  # Ukuran bervariasi
                    })
            
            # Update usia ekor dan hapus yang sudah tua
            for trail in p.trail[:]:
                trail['age'] += dt
                if trail['age'] > trail['max_age']:
                    p.trail.remove(trail)
                else:
                    # Memudar ekor seiring waktu dengan kurva lebih lambat
                    alpha_ratio = 1.0 - (trail['age'] / trail['max_age']) ** 1.5  # Kurva kemulusan
                    trail['color'][3] = p.color[3] * alpha_ratio * 0.7  # Lebih terang (aslinya 0.5)
            
            # Update usia dan transparansi
            p.age += dt
            age_ratio = p.age / p.lifetime
            
            # Partikel ledakan mempertahankan transparansi lebih lama
            if not p.is_launch_particle:
                fade_start = 0.6  # Mulai memudar pada 60% lifetime (bertahan lebih lama)
                
                # Jika partikel sudah melewati puncak, tambahkan pemudar tambahan
                if p.has_peaked:
                    # Hitung waktu sejak mencapai puncak
                    time_since_peak = p.age - p.peak_time
                    
                    # Waktu hingga partikel menghilang sepenuhnya sejak mencapai puncak
                    # Semakin negatif kecepatan vertikal, semakin cepat memudar
                    fall_fade_factor = min(1.0, abs(p.velocity[1]) / 5.0) * p.fall_fade_speed
                    
                    # Gunakan faktor pemudar sebagai pengali untuk alpha
                    fade_multiplier = max(0.0, 1.0 - time_since_peak * fall_fade_factor)
                    
                    # Semakin rendah posisi Y, semakin transparan
                    height_factor = max(0.0, min(1.0, (p.position[1] + 8) / 10.0))
                    
                    # Gabungkan semua faktor pemudar
                    if age_ratio < fade_start:
                        p.color[3] = 1.0 * fade_multiplier * height_factor
                    else:
                        fade_ratio = (age_ratio - fade_start) / (1.0 - fade_start)
                        p.color[3] = (1.0 - fade_ratio) * fade_multiplier * height_factor
                else:
                    if age_ratio < fade_start:
                        p.color[3] = 1.0
                    else:
                        fade_ratio = (age_ratio - fade_start) / (1.0 - fade_start)
                        p.color[3] = 1.0 - fade_ratio
            else:
                p.color[3] = 1.0 - age_ratio  # Fade out normal untuk partikel peluncuran
            
            # Update ukuran
            if p.is_launch_particle:
                # Partikel peluncuran membesar mendekati puncak
                vel_ratio = abs(p.velocity[1]) / 15.0  # 15.0 adalah kecepatan awal
                size_factor = 1.0 + 2.0 * (1.0 - vel_ratio)  # Maksimum 3x ukuran awal
                p.size = p.initial_size * size_factor
            else:
                # Partikel ledakan mengecil seiring waktu kecuali partikel ujung kurva
                if p.is_curve_end:
                    # Partikel ujung tetap lebih besar
                    pulse = math.sin(p.age * 8)  # Berkedip lebih cepat (aslinya 5)
                    p.size = p.initial_size * (0.7 + 0.2 * pulse)  # Kurangi ukuran (aslinya 0.9 + 0.3)
                elif p.expansion_phase and p.age < p.expansion_time:
                    # Pada fase ekspansi, ukuran meningkat
                    expansion_ratio = p.age / p.expansion_time
                    p.size = p.initial_size * (1.0 + expansion_ratio * 0.5)  # Kurangi peningkatan ukuran (aslinya 0.8)
                else:
                    # Setelah fase ekspansi, perlahan mengecil
                    p.size = p.initial_size * (1.0 - age_ratio * 0.5)  # Mengecil lebih lambat (minimum 50%)
                
                # Update rotasi hanya untuk partikel ledakan
                p.rotation += p.rotation_speed * dt

        # Hapus partikel yang sudah mati
        self.particles = [p for p in self.particles if p.age < p.lifetime]

        # Trigger ledakan saat partikel utama mencapai puncak
        if not self.exploded and len(self.particles) > 0 and self.particles[0].velocity[1] < 0:
            self.explode()
            self.particles.pop(0)  # Hapus partikel utama

# ================== KELAS GEDUNG ==================
class Building:
    """
    Kelas untuk mengelola gedung di latar belakang.
    Menangani properti dan tampilan gedung.
    """
    def __init__(self, x, width_b, height_b, shape, with_window):
        # Properti dasar
        self.x = x
        self.width = width_b
        self.height = height_b
        self.shape = shape
        self.with_window = with_window
        self.windows = []
        
        # Generate jendela jika diperlukan
        if with_window:
            old_state = random.getstate()
            random_seed = hash((x, width_b, height_b)) % 10000
            random.seed(random_seed)
            self.generate_windows()
            random.setstate(old_state)
    
    def generate_windows(self):
        col_count = int(self.width // 15)
        row_count = int(self.height // 15)  # Lebih banyak jendela secara vertikal
        for i in range(col_count):
            for j in range(row_count):
                if random.random() > 0.5:  # Lebih banyak jendela (probabilitas tinggi)
                    continue
                wx = self.x + 5 + i * 12
                wy = 5 + j * 15  # Jarak antar jendela lebih pendek
                if wy + 10 < self.height:
                    self.windows.append((wx, wy))

# ================== FUNGSI RENDER ==================
def draw_gradient_sky():
    """Menggambar latar langit dengan gradien."""
    glBegin(GL_QUADS)
    glColor3f(0.0, 0.0, 0.1)
    glVertex2f(0, 0)
    glVertex2f(width, 0)
    glColor3f(0.0, 0.1, 0.2)
    glVertex2f(width, height)
    glVertex2f(0, height)
    glEnd()

def draw_stars():
    glColor3f(1.0, 1.0, 1.0)
    glPointSize(2.0)
    glBegin(GL_POINTS)
    for star in stars:
        glVertex2f(*star)
    glEnd()

def draw_circle(x, y, radius, segments=100):
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)
    for i in range(segments + 1):
        angle = 2 * math.pi * i / segments
        glVertex2f(x + radius * math.cos(angle), y + radius * math.sin(angle))
    glEnd()

def draw_glowing_moon():
    center_x, center_y = width // 2, int(height * 0.65)
    radius = 120
    for i in range(1, 6):
        glow_radius = radius + i * 15
        alpha = 0.05
        glColor4f(1.0, 1.0, 0.6, alpha)
        draw_circle(center_x, center_y, glow_radius)
    glColor3f(1.0, 1.0, 0.6)
    draw_circle(center_x, center_y, radius)

def draw_building(building):
    x = building.x
    width_b = building.width
    height_b = building.height
    shape = building.shape
    
    # Tentukan warna berdasarkan jenis gedung
    if not building.with_window:  # Gedung belakang
        glColor3f(0.0, 0.0, 0.0)  # Hitam pekat
    else:  # Gedung depan dengan jendela
        glColor3f(0.05, 0.05, 0.15)  # Biru tua cenderung hitam
    
    glBegin(GL_POLYGON)

    if shape == "flat":
        glVertex2f(x, 0)
        glVertex2f(x + width_b, 0)
        glVertex2f(x + width_b, height_b)
        glVertex2f(x, height_b)
    
    elif shape == "step":
        glVertex2f(x, 0)
        glVertex2f(x + width_b, 0)
        glVertex2f(x + width_b, height_b - 20)
        glVertex2f(x + width_b * 0.7, height_b - 20)
        glVertex2f(x + width_b * 0.7, height_b)
        glVertex2f(x + width_b * 0.3, height_b)
        glVertex2f(x + width_b * 0.3, height_b - 20)
        glVertex2f(x, height_b - 20)

    elif shape == "tower":
        tower_w = width_b * 0.3
        tower_x = x + (width_b - tower_w) / 2
        glVertex2f(x, 0)
        glVertex2f(x + width_b, 0)
        glVertex2f(x + width_b, height_b - 30)
        glVertex2f(tower_x + tower_w, height_b - 30)
        glVertex2f(tower_x + tower_w, height_b)
        glVertex2f(tower_x, height_b)
        glVertex2f(tower_x, height_b - 30)
        glVertex2f(x, height_b - 30)

    elif shape == "eiffel":
        # Ujung seperti menara Eiffel
        glVertex2f(x, 0)
        glVertex2f(x + width_b, 0)
        glVertex2f(x + width_b, height_b - 40)
        glVertex2f(x + width_b / 2 + 5, height_b - 40)
        glVertex2f(x + width_b / 2, height_b + 20)  # lebih tinggi & ramping
        glVertex2f(x + width_b / 2 - 5, height_b - 40)
        glVertex2f(x, height_b - 40)

    elif shape == "chimney":
        # Cerobong asap
        chimney_w = width_b * 0.2
        chimney_x = x + (width_b - chimney_w) / 2
        chimney_h = 25
        glVertex2f(x, 0)
        glVertex2f(x + width_b, 0)
        glVertex2f(x + width_b, height_b)
        glVertex2f(x, height_b)
        glEnd()
        glBegin(GL_POLYGON)
        glVertex2f(chimney_x, height_b)
        glVertex2f(chimney_x + chimney_w, height_b)
        glVertex2f(chimney_x + chimney_w, height_b + chimney_h)
        glVertex2f(chimney_x, height_b + chimney_h)

    glEnd()

    # Gambar jendela hanya jika gedung memiliki jendela (gedung depan)
    if building.with_window:
        draw_saved_windows(building)

def draw_saved_windows(building):
    glColor3f(1.0, 1.0, 0.7)  # Warna jendela sedikit lebih cerah
    for wx, wy in building.windows:
        glBegin(GL_QUADS)
        glVertex2f(wx, wy)
        glVertex2f(wx + 6, wy)
        glVertex2f(wx + 6, wy + 10)
        glVertex2f(wx, wy + 10)
        glEnd()

def generate_building_layer(min_height, max_height, density=1.0, with_window=True, y_offset=0):
    # Set seed agar konsisten
    old_state = random.getstate()
    random.seed(42 + hash(min_height + max_height) % 100)
    
    layer = []
    x = 0
    while x < width:
        w = random.randint(50, 90)
        h = random.randint(min_height, max_height)
        shape = random.choice(["flat", "step", "tower", "eiffel", "chimney"])
        building = Building(x, w, h + y_offset, shape, with_window)
        layer.append(building)
        x += int(w * density) + random.randint(3, 12)
    
    # Kembalikan state random
    random.setstate(old_state)
    return layer

def generate_city():
    # Layer belakang - gedung tinggi, siluet saja
    buildings["back"] = generate_building_layer(min_height=250, max_height=350, density=0.8, with_window=False, y_offset=30)
    # Layer depan - gedung utama dengan jendela
    buildings["main"] = generate_building_layer(min_height=200, max_height=280, density=1.0, with_window=True)
    # Hapus layer pengisi (front)
    buildings["front"] = []

def draw_city_background():
    # Gambar semua gedung dari data yang sudah dibuat
    for building in buildings["back"]:
        draw_building(building)
    for building in buildings["main"]:
        draw_building(building)
    # Hapus pemanggilan untuk menggambar layer front
    # for building in buildings["front"]:
    #     draw_building(building)

# ================== FUNGSI RENDER PARTIKEL ==================
def draw_particle(position, color, size=0.2, rotation=0.0, shape="circle", trail=None, is_curve_end=False):
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
    
    # Konversi koordinat dari kembang api ke koordinat layar
    screen_pos = [
        (position[0] * 100) + width/2,  # Skala dan geser ke tengah
        position[1] * 100 + 100         # Skala dan geser ke atas sedikit
    ]
    
    # Gambar ekor terlebih dahulu (sebelum partikel utama)
    if trail:
        # Gunakan garis untuk ekor, bukan titik
        glLineWidth(2.0)  # Lebar garis ekor
        
        if len(trail) > 1:
            glBegin(GL_LINE_STRIP)
            for trail_segment in trail:
                trail_screen_pos = [
                    (trail_segment['pos'][0] * 100) + width/2,
                    (trail_segment['pos'][1] * 100) + 100
                ]
                glColor4f(*trail_segment['color'])
                glVertex2f(trail_screen_pos[0], trail_screen_pos[1])
            glEnd()
        
        # Gambar partikel trail individual untuk efek yang lebih baik
        for trail_segment in trail:
            trail_screen_pos = [
                (trail_segment['pos'][0] * 100) + width/2,
                (trail_segment['pos'][1] * 100) + 100
            ]
            # Ukuran bergantung pada partikel trail
            trail_size = size * 20 * (1.0 - trail_segment['age'] / trail_segment['max_age'])  # Kurangi ukuran trail (aslinya 25)
            
            if 'size' in trail_segment:
                trail_size = trail_segment['size'] * 20  # Kurangi ukuran trail (aslinya 25)
                
            glPointSize(trail_size)
            glBegin(GL_POINTS)
            glColor4f(*trail_segment['color'])
            glVertex2f(trail_screen_pos[0], trail_screen_pos[1])
            glEnd()
    
    # Perbesar ukuran partikel agar lebih terlihat
    actual_size = size * 35  # Kurangi ukuran (aslinya 50)
    
    glPushMatrix()
    glTranslatef(screen_pos[0], screen_pos[1], 0)
    glRotatef(rotation, 0, 0, 1)  # Rotasi di sumbu Z
    
    # Jika ini adalah partikel ujung kurva, gambar dengan warna yang lebih cerah
    display_color = color.copy()
    if is_curve_end:
        for i in range(3):  # Terangkan RGB, jangan ubah alpha
            display_color[i] = min(1.0, color[i] * 1.3)  # Kurangi kecerahan (aslinya 1.5)
    
    # Gambar glow untuk partikel yang lebih besar
    if is_curve_end or size > 0.3:
        glow_size = actual_size * 1.3  # Kurangi ukuran glow (aslinya 1.5)
        glow_color = display_color.copy()
        glow_color[3] *= 0.3  # Transparansi untuk glow
        
        if shape == "circle":
            segments = 16
            glBegin(GL_TRIANGLE_FAN)
            glColor4f(*glow_color)
            glVertex2f(0, 0)  # Titik tengah
            for i in range(segments + 1):
                angle = 2 * math.pi * i / segments
                x = math.cos(angle) * glow_size / 2
                y = math.sin(angle) * glow_size / 2
                glVertex2f(x, y)
            glEnd()
        else:  # square
            half_size = glow_size / 2
            glBegin(GL_QUADS)
            glColor4f(*glow_color)
            glVertex2f(-half_size, -half_size)
            glVertex2f(half_size, -half_size)
            glVertex2f(half_size, half_size)
            glVertex2f(-half_size, half_size)
            glEnd()
    
    # Gambar partikel berdasarkan bentuknya
    if shape == "circle":
        segments = 16  # Jumlah segmen lingkaran
        glBegin(GL_TRIANGLE_FAN)
        glColor4f(*display_color)
        glVertex2f(0, 0)  # Titik tengah
        for i in range(segments + 1):
            angle = 2 * math.pi * i / segments
            x = math.cos(angle) * actual_size / 2
            y = math.sin(angle) * actual_size / 2
            glVertex2f(x, y)
        glEnd()
    else:  # square
        half_size = actual_size / 2
        glBegin(GL_QUADS)
        glColor4f(*display_color)
        glVertex2f(-half_size, -half_size)
        glVertex2f(half_size, -half_size)
        glVertex2f(half_size, half_size)
        glVertex2f(-half_size, half_size)
        glEnd()
    
    glPopMatrix()
    
    # Reset blend mode ke normal setelah menggambar partikel
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# ================== FUNGSI UTILITAS ==================
def init_gl():
    """Inisialisasi OpenGL dan pengaturan dasar."""
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# ================== MAIN PROGRAM ==================
def main():
    """
    Fungsi utama program.
    Menangani inisialisasi, game loop, dan cleanup.
    """
    # Inisialisasi
    pygame.init()
    display = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Kota Malam dengan Kembang Api - PyOpenGL")
    glutInit()
    
    init_gl()
    generate_city()
    
    # Setup variabel game
    fireworks = []
    last_time = time.time()
    clock = pygame.time.Clock()
    
    # Game loop
    running = True
    while running:
        # Update waktu
        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Luncurkan kembang api
                    old_state = random.getstate()
                    random.seed(int(time.time() * 1000) % 10000)
                    launch_pos = [random.uniform(-5, 5), -8.0]
                    fireworks.append(Firework(launch_pos))
                    random.setstate(old_state)
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        # Update
        for fw in fireworks:
            fw.update(dt)
        fireworks = [fw for fw in fireworks if len(fw.particles) > 0]
        
        # Render
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Gambar latar belakang
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        draw_gradient_sky()
        draw_stars()
        draw_glowing_moon()
        draw_city_background()
        
        # Gambar kembang api
        for fw in fireworks:
            for p in fw.particles:
                draw_particle(p.position, p.color, p.size, p.rotation, p.shape, p.trail, p.is_curve_end)
        
        # Finalisasi render
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        pygame.display.flip()
        clock.tick(FPS)
    
    # Cleanup
    pygame.quit()

if __name__ == "__main__":
    main()
