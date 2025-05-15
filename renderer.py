"""
Fungsi-fungsi rendering untuk menggambar elemen visual.
"""
import random
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from config import width, height, PARTICLE_COUNT
from building import buildings

# Inisialisasi bintang
stars = [(random.randint(0, width), random.randint(height // 2, height)) for _ in range(PARTICLE_COUNT)]

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

def draw_city_background():
    # Gambar semua gedung dari data yang sudah dibuat
    for building in buildings["back"]:
        draw_building(building)
    for building in buildings["main"]:
        draw_building(building)

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