#!/usr/bin/env python3

from src.Application import GraphicalInterface

if __name__ == "__main__":
    app = GraphicalInterface(title="Face auto screen lock")
    app.mainloop()
    app.add_button("test", "app_quit")

