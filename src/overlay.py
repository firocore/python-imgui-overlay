import os

import pygame
import OpenGL.GL as gl
import imgui as imgui
from imgui.integrations.pygame import PygameRenderer
import win32api
import win32con
import win32gui
import win32process

from src.imgui_menu import menu


class Overlay():
    def __init__(self, target_process: str) -> None:

        # init pygame
        pygame.init()
        os.environ['SDL_VIDEO_WINDOW_POS'] = str(win32api.GetSystemMetrics(0)) + "," + str(win32api.GetSystemMetrics(1))

        # get hwnd tarrget procces
        self.target_window_hwnd = win32gui.FindWindow(None, target_process)

        # found target window
        if not self.target_window_hwnd:
            print(f'Could not find window with {target_process} title')
            raise Exception(f'Could not find window with {target_process} title')


        # Set main window paramms
        th = win32process.GetWindowThreadProcessId(self.target_window_hwnd)
        win32process.AttachThreadInput(win32api.GetCurrentThreadId(), int(th[0]), True)
        win32gui.ShowWindow(self.target_window_hwnd, 5)
        win32gui.SetForegroundWindow(self.target_window_hwnd)
        win32gui.SetFocus(self.target_window_hwnd)
        
        """ Параметры оверлея """

        # create overlay window
        self.overlay_screen = pygame.display.set_mode((0, 0), pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)

        # get hwnd overlay window
        self.overlay_hwnd = pygame.display.get_wm_info()['window']
        self.overlay_title = target_process + " overlay"
        pygame.display.set_caption(self.overlay_title)

        # get overlay window styles
        ex_style = win32gui.GetWindowLong(self.overlay_hwnd, win32con.GWL_EXSTYLE)

        # add WS_EX_LAYERED and WS_EX_TOOLWINDOW styles
        ex_style |= win32con.WS_EX_LAYERED
        ex_style |= win32con.WS_EX_TOOLWINDOW

        # intall new styles
        win32gui.SetWindowLong(self.overlay_hwnd, win32con.GWL_EXSTYLE, ex_style)

        # install window flags
        win32gui.SetLayeredWindowAttributes(self.overlay_hwnd, 0, 0, win32con.LWA_ALPHA)
        win32gui.SetLayeredWindowAttributes(self.overlay_hwnd, 0, 255, win32con.LWA_COLORKEY | win32con.LWA_ALPHA)
        win32gui.BringWindowToTop(self.overlay_hwnd)
        win32gui.SetWindowPos(self.overlay_hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, 1 | 2)
        win32gui.ShowWindow(self.overlay_hwnd, win32con.SW_SHOW)

        """ Интерфейс ImGui """

        # init ImGui
        imgui.create_context()
        self.impl = PygameRenderer()

        # set ImGui size
        self.io = imgui.get_io()
        self.io.display_size = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)

        # clear bacground OpenGL
        gl.glColorMask(True, True, True, True)
        gl.glClearColor(0, 0, 0, 0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        self.window_size_save = (0, 0)

    def update_overlay(self, visible):
        foreground = win32gui.FindWindow(None, win32gui.GetWindowText(win32gui.GetForegroundWindow())) in [self.target_window_hwnd, self.overlay_hwnd]
        win32gui.SetWindowPos(self.overlay_hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, 1 | 2)
        window_rect = win32gui.GetWindowRect(self.target_window_hwnd)
        window_rect = [window_rect[0], window_rect[1], window_rect[2], window_rect[3]]
        window_rect[0] += 9
        window_rect[1] += 22
        window_rect[2] -= 9
        window_rect[3] -= 9
        window_size = window_rect[2] - window_rect[0], window_rect[3] - window_rect[1]

        if self.window_size_save != window_size and foreground:
            pygame.display.set_mode(window_size, pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE | pygame.NOFRAME)    
            self.io.display_size = (window_size[0], window_size[1])

        self.window_size_save = window_size

        win32gui.MoveWindow(self.overlay_hwnd, window_rect[0], window_rect[1], window_size[0], window_size[1], True)

        for event in pygame.event.get():
            self.impl.process_event(event)
        
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
