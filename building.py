"""
Kelas Building dan fungsi terkait untuk mengelola gedung di latar belakang.
"""
import random
from config import width

# Struktur data untuk menyimpan gedung
buildings = {
    "back": [],  # Layer belakang (siluet)
    "main": [],  # Layer utama (dengan jendela)
    "front": []  # Layer depan (opsional)
}

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