import os
import pygame
import OpenGL.GL as gl
import imgui as imgui
from imgui.integrations.pygame import PygameRenderer
import win32api
import win32con
import win32gui
import win32com.client

from src.imgui_menu import menu



class Overlay():
    def __init__(self, target_process: str) -> None:
        # Initialize Pygame
        pygame.init()
        
        # Set the initial position of the overlay window
        os.environ['SDL_VIDEO_WINDOW_POS'] = str(win32api.GetSystemMetrics(0)) + "," + str(win32api.GetSystemMetrics(1))
        
        # Find the handle of the target window by its title
        self.target_window_hwnd = win32gui.FindWindow(None, target_process)
        if not self.target_window_hwnd:
            print(f'Could not find window with {target_process} title')
            raise Exception(f'Could not find window with {target_process} title')
        
        # Setup the overlay window
        self.__setup_overlay_window(target_process)
        
        # Initialize ImGui
        self.__init_imgui()


    def __setup_overlay_window(self, target_process):
        # Show and maximize the target window
        win32gui.ShowWindow(self.target_window_hwnd, win32con.SW_MINIMIZE)
        win32gui.ShowWindow(self.target_window_hwnd, win32con.SW_MAXIMIZE)
        
        # Set the target window to the foreground
        self.__set_window_foreground(self.target_window_hwnd)
        
        # Create the overlay window
        self.overlay_screen = pygame.display.set_mode((0, 0), pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE | pygame.NOFRAME)
        self.overlay_hwnd = pygame.display.get_wm_info()['window']
        self.overlay_title = target_process + " overlay"
        pygame.display.set_caption(self.overlay_title)
        
        # Set window styles for the overlay
        ex_style = win32gui.GetWindowLong(self.overlay_hwnd, win32con.GWL_EXSTYLE)
        ex_style |= win32con.WS_EX_LAYERED | win32con.WS_EX_TOOLWINDOW
        win32gui.SetWindowLong(self.overlay_hwnd, win32con.GWL_EXSTYLE, ex_style)
        win32gui.SetLayeredWindowAttributes(self.overlay_hwnd, 0, 255, win32con.LWA_COLORKEY)
        win32gui.SetWindowPos(self.overlay_hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)


    def __set_window_foreground(self, hwnd):
        # Set the window with the specified handle to the foreground
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(hwnd)


    def __init_imgui(self):
        # Initialize ImGui context
        imgui.create_context()
        
        # Initialize ImGui renderer
        self.impl = PygameRenderer()
        
        # Get ImGui IO
        self.io = imgui.get_io()
        
        # Set display size for ImGui
        self.io.display_size = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
        
        # Clear OpenGL background
        gl.glColorMask(True, True, True, True)
        gl.glClearColor(0, 0, 0, 0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        
        # Initialize variable to store window size
        self.window_size_save = (0, 0)


    def update_overlay(self, visible):
        # Check if the overlay window or the target window is in the foreground
        foreground = win32gui.GetForegroundWindow() in [self.target_window_hwnd, self.overlay_hwnd]
        
        # Update position and size of overlay window
        self.__set_overlay_position_and_size(foreground)
        
        # Handle Pygame events
        self.__handle_events()
        
        # Render ImGui
        self.__render_imgui(visible, foreground)


    def __set_overlay_position_and_size(self, foreground):
        # Set position and size of the overlay window
        win32gui.SetWindowPos(self.overlay_hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)
        window_rect = win32gui.GetWindowRect(self.target_window_hwnd)
        window_rect = [window_rect[0], window_rect[1], window_rect[2], window_rect[3]]
        window_size = window_rect[2] - window_rect[0], window_rect[3] - window_rect[1]
        
        if foreground and self.window_size_save != window_size:
            pygame.display.set_mode(window_size, pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE | pygame.NOFRAME)    
            self.io.display_size = (window_size[0], window_size[1])
        
        if foreground and win32gui.WindowFromPoint(win32api.GetCursorPos()) == self.overlay_hwnd:
            self.__set_window_foreground(self.overlay_hwnd)
        
        self.window_size_save = window_size
        win32gui.MoveWindow(self.overlay_hwnd, window_rect[0], window_rect[1], window_size[0], window_size[1], True)


    def __handle_events(self):
        # Handle Pygame events
        for event in pygame.event.get():
            self.impl.process_event(event)


    def __render_imgui(self, visible, foreground):
        # Render ImGui
        imgui.new_frame()
        if visible and foreground:
            menu()
            imgui.show_test_window()

        gl.glClearColor(0, 0, 0, 0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        self.impl.render(imgui.get_draw_data())

        pygame.display.flip()
        win32gui.BringWindowToTop(self.overlay_hwnd)
        win32gui.ShowWindow(self.overlay_hwnd, win32con.SW_SHOW)
