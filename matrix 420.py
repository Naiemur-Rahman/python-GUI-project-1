import sys
import pygame
import random
import webbrowser
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout
from PyQt6.QtGui import QPainter, QImage

# MAIN WINDOW 

class MainApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Naiem's Delulu")
        self.setStyleSheet("background-color: black;")
        self.setGeometry(100, 100, 800, 600)

        # Stacked Widget (to switch between pages)
        self.stack = QStackedWidget()
        
        # Pages
        self.main_menu = MainMenu(self)
        self.matrix_rain_page = MatrixRainPage(self)

        self.stack.addWidget(self.main_menu)
        self.stack.addWidget(self.matrix_rain_page)

        # Layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.stack)
        self.setLayout(self.layout)

        # Show main menu initially
        self.stack.setCurrentWidget(self.main_menu)

    def show_matrix_rain(self):
        """Switch to Matrix Rain Page"""
        self.stack.setCurrentWidget(self.matrix_rain_page)

    def show_main_menu(self):
        """Switch back to Main Menu"""
        self.stack.setCurrentWidget(self.main_menu)

    def open_video(self):
        """Open Rick Roll in the browser"""
        webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")


# ---------------- MAIN MENU ----------------

class MainMenu(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        # Title Label
        self.title_label = QLabel("Naiem's Delulu", self)
        self.title_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Buttons Layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title_label)

        # Horizontal Layout for Pills
        self.button_layout = QHBoxLayout()

        # Blue Pill Button (Go to Matrix Rain)
        self.blue_pill = QPushButton("Blue Pill")
        self.blue_pill.setStyleSheet(
            "background-color: blue; color: white; padding: 12px; border-radius: 25px; font-size: 16px; width: 100px;"
        )
        self.blue_pill.clicked.connect(self.main_app.show_matrix_rain)

        # Red Pill Button (Open Rick Roll)
        self.red_pill = QPushButton("Red Pill")
        self.red_pill.setStyleSheet(
            "background-color: red; color: white; padding: 12px; border-radius: 25px; font-size: 16px; width: 100px;"
        )
        self.red_pill.clicked.connect(self.main_app.open_video)

        # Add buttons side by side
        self.button_layout.addWidget(self.blue_pill)
        self.button_layout.addWidget(self.red_pill)

        # Add buttons layout to main layout
        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)


# ---------------- MATRIX RAIN PAGE ----------------

class MatrixRainPage(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        # Pygame Setup
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.FONT_SIZE = 18
        self.COLUMNS = int(self.WIDTH // (self.FONT_SIZE * 1.5))  # 🔥 FIX: Convert to int
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.DARK_GREEN = (0, 150, 0)

        self.screen = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.font = pygame.font.SysFont("Courier", self.FONT_SIZE, bold=True)
        self.title_font = pygame.font.SysFont("Courier New", 80, bold=True)

        self.drops = [{'y': random.randint(0, self.HEIGHT), 'trail': []} for _ in range(self.COLUMNS)]
        self.title = "NaieMatrix"
        self.title_size = 0
        self.title_max_size = 100
        self.title_growth = 0.5

        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()

        # Timer for updating Pygame
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_matrix)
        self.timer.start(35)

        # Layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Back Button
        self.back_button = QPushButton("Back")
        self.back_button.setStyleSheet(
            "background-color: gray; color: white; padding: 10px; border-radius: 15px; font-size: 14px;"
        )
        self.back_button.clicked.connect(self.main_app.show_main_menu)

        # Add Back Button
        self.layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

    def update_matrix(self):
        """Update Matrix Rain Effect"""
        self.screen.fill(self.BLACK)
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000

        for i, drop in enumerate(self.drops):
            x = i * self.FONT_SIZE * 1.5
            y = drop['y']

            char = chr(random.randint(33, 126))
            drop['trail'].append((x, y, char))

            if len(drop['trail']) > 15:
                drop['trail'].pop(0)

            for j, (tx, ty, tchar) in enumerate(drop['trail']):
                alpha = int(255 * (j / len(drop['trail'])))
                color = (0, alpha, 0)
                text = self.font.render(tchar, True, color)
                self.screen.blit(text, (tx, ty))

            if y > self.HEIGHT and random.random() > 0.975:
                drop['y'] = 0
                drop['trail'] = []
            else:
                drop['y'] += self.FONT_SIZE

        if elapsed_time > 3:
            if self.title_size < self.title_max_size:
                self.title_size += self.title_growth + (self.title_max_size - self.title_size) * 0.05

            shadow_surface = self.title_font.render(self.title, True, self.DARK_GREEN)
            shadow_surface = pygame.transform.scale(shadow_surface, (int(self.title_size * 4), int(self.title_size)))
            self.screen.blit(shadow_surface, shadow_surface.get_rect(center=(self.WIDTH // 2 + 3, self.HEIGHT // 3 + 3)))

            title_surface = self.title_font.render(self.title, True, self.GREEN)
            title_surface = pygame.transform.scale(title_surface, (int(self.title_size * 4), int(self.title_size)))
            self.screen.blit(title_surface, title_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 3)))

        self.update()

    def paintEvent(self, event):
        """Render Pygame Surface inside PyQt"""
        painter = QPainter(self)
        qimage = QImage(self.screen.get_buffer(), self.WIDTH, self.HEIGHT, QImage.Format.Format_RGB32)
        painter.drawImage(0, 0, qimage)


# ---------------- APP START ----------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec())
