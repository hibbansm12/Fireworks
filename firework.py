"""
Kelas Firework untuk mengelola kembang api.
"""
import random
import math
from particle import Particle

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