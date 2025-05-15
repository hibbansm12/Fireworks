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

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import time
import sys

from config import width, height, FPS
from building import generate_city
from renderer import (
    init_gl, draw_gradient_sky, draw_stars,
    draw_glowing_moon, draw_city_background,
    draw_particle
)
from firework import Firework

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