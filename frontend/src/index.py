"""
Course: CST 205
Title: Driscoll's R&D Platform
Authors: Juan Zavala, Alan Olvera, Antonio Navarro, David J. Salinas-Villafuerte
Date: May 14, 2026

GitHub Repository:
https://github.com/Navanator1215/Team-7621.git

Description:
This file defines the Theme class that manages light/dark mode colors and fonts for the frontend UI.

Team Contribuitons for this file: 

David J. Salinas-Villafuerte - Worked on creating the Theme class that manages light/dark mode colors and fonts for the frontend UI.
(Still needs implementation in the actual frontend routes and templates, but the class is defined here for future use.)

"""

# index.py

class Theme:
    def _init_(self, mode="light"):
        self.mode = mode

        # Light theme
        self.light = {
            "text": "#6b6375",
            "text_h": "#08060d",
            "bg": "#ffffff",
            "border": "#e5e4e7",
            "code_bg": "#f4f3ec",
            "accent": "#aa3bff",
            "accent_bg": (170, 59, 255, 0.1),
            "accent_border": (170, 59, 255, 0.5),
            "social_bg": (244, 243, 236, 0.5),
            "shadow": 
            [
                (0, 0, 0, 0.1, 0, 10, 15, -3),
                (0, 0, 0, 0.05, 0, 4, 6, -2)
            ]
        }    

        # Dark theme
        self.dark = {
            "text": "#9ca3af",
            "text_h": "#f3f4f6",
            "bg": "#16171d",
            "border": "#2e303a",
            "code_bg": "#1f2028",
            "accent": "#c084fc",
            "accent_bg": (192, 132, 252, 0.15),
            "accent_border": (192, 132, 252, 0.5),
            "social_bg": (47, 48, 58, 0.5),
            "shadow": 
            [
                (0, 0, 0, 0.4, 0, 10, 15, -3),
                (0, 0, 0, 0.25, 0, 4, 6, -2)
            ]
        }

        # Fonts
        self.fonts = {
            "sans": ["system-ui", "Segoe UI", "Roboto", "sans-serif"],
            "heading": ["system-ui", "Segoe UI", "Roboto", "sans-serif"],
            "mono": ["ui-monospace", "Consolas", "monospace"]
        }

    def get(self, key):
        if self.mode == "dark":
            return self.dark.get(key)
        return self.light.get(key)
    
    def switch_mode(self):
        self.mode = "dark" if self.mode == "light" else "light"

# Example usage
if __name__ == "__main__":
    theme = Theme("light")

    print("Text Color:", theme.get("text"))
    print("Background Color:", theme.get("bg"))
    print("Accent Color:", theme.get("accent"))

    theme.switch_mode()

    print("\nAfter switching to dark mode:")
    print("Text Color:", theme.get("text"))