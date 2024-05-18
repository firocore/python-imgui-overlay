
import imgui


class ImVec4:
    def __init__(self, r: float, g: float, b: float, a: float) -> None:
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __repr__(self):
        return f"ImVec4({self.r}, {self.g}, {self.b}, {self.a})"

    def __iter__(self):
        return iter((self.r, self.g, self.b, self.a))

    def __len__(self):
        return 4

    def __getitem__(self, index):
        return (self.r, self.g, self.b, self.a)[index]

def rgba(r: int, g: int, b: int, a: float) -> ImVec4:
    return ImVec4(r / 255.0, g / 255.0, b / 255.0, a)

def convert_to_imvec4(vec) -> ImVec4:
    if isinstance(vec, ImVec4):
        return vec
    return ImVec4(vec[0], vec[1], vec[2], vec[3])

class ImLerp(ImVec4):
    def __init__(self, vec_a, vec_b, t: float) -> None:
        a = convert_to_imvec4(vec_a)
        b = convert_to_imvec4(vec_b)
        r = a.r + (b.r - a.r) * t
        g = a.g + (b.g - a.g) * t
        b_val = a.b + (b.b - a.b) * t
        a_val = a.a + (b.a - a.a) * t
        super().__init__(r, g, b_val, a_val)


def custom_color_style():
    style = imgui.get_style() # override active style
    colors = style.colors

    colors[imgui.COLOR_TEXT]                            = ImVec4(1.0, 1.0, 1.0, 1.0)
    colors[imgui.COLOR_TEXT_DISABLED]                   = rgba(93, 93, 99, 1)
    colors[imgui.COLOR_WINDOW_BACKGROUND]               = rgba(14, 16, 17, 0.5)
    colors[imgui.COLOR_CHILD_BACKGROUND]                = rgba(40, 41, 52, 1)
    colors[imgui.COLOR_POPUP_BACKGROUND]                = ImVec4(0.08, 0.08, 0.08, 0.94)
    colors[imgui.COLOR_BORDER]                          = ImVec4(0.43, 0.43, 0.50, 0.50)
    colors[imgui.COLOR_BORDER_SHADOW]                   = ImVec4(0.00, 0.00, 0.00, 0.00)
    colors[imgui.COLOR_FRAME_BACKGROUND]                = rgba(40, 41, 52, 1)
    colors[imgui.COLOR_FRAME_BACKGROUND_HOVERED]        = rgba(50, 51, 62, 1)
    colors[imgui.COLOR_FRAME_BACKGROUND_ACTIVE]         = rgba(252, 210, 62, 1)
    colors[imgui.COLOR_TITLE_BACKGROUND]                = ImVec4(0.04, 0.04, 0.04, 0.70)
    colors[imgui.COLOR_TITLE_BACKGROUND_ACTIVE]         = ImVec4(0.16, 0.29, 0.48, 1.00)
    colors[imgui.COLOR_TITLE_BACKGROUND_COLLAPSED]      = ImVec4(0.00, 0.00, 0.00, 0.51)
    colors[imgui.COLOR_MENUBAR_BACKGROUND]              = ImVec4(0.14, 0.14, 0.14, 1.00)
    colors[imgui.COLOR_SCROLLBAR_BACKGROUND]            = ImVec4(0.02, 0.02, 0.02, 0.53)
    colors[imgui.COLOR_SCROLLBAR_GRAB]                  = ImVec4(0.31, 0.31, 0.31, 1.00)
    colors[imgui.COLOR_SCROLLBAR_GRAB_HOVERED]          = ImVec4(0.41, 0.41, 0.41, 1.00)
    colors[imgui.COLOR_SCROLLBAR_GRAB_ACTIVE]           = ImVec4(0.51, 0.51, 0.51, 1.00)
    colors[imgui.COLOR_CHECK_MARK]                      = ImVec4(0.26, 0.59, 0.98, 1.00)
    colors[imgui.COLOR_SLIDER_GRAB]                     = ImVec4(0.24, 0.52, 0.88, 1.00)
    colors[imgui.COLOR_SLIDER_GRAB_ACTIVE]              = ImVec4(0.26, 0.59, 0.98, 1.00)
    colors[imgui.COLOR_BUTTON]                          = rgba(40, 41, 52, 0.7)
    colors[imgui.COLOR_BUTTON_HOVERED]                  = rgba(40, 41, 52, 0.85)
    colors[imgui.COLOR_BUTTON_ACTIVE]                   = rgba(40, 41, 52, 1.0)
    colors[imgui.COLOR_HEADER]                          = ImVec4(0.055, 0.063, 0.067, 1.0)
    colors[imgui.COLOR_HEADER_HOVERED]                  = ImVec4(0.26, 0.59, 0.98, 0.80)
    colors[imgui.COLOR_HEADER_ACTIVE]                   = ImVec4(0.26, 0.59, 0.98, 1.00)
    colors[imgui.COLOR_SEPARATOR]                       = colors[imgui.COLOR_BORDER]
    colors[imgui.COLOR_SEPARATOR_HOVERED]               = ImVec4(0.10, 0.40, 0.75, 0.78)
    colors[imgui.COLOR_SEPARATOR_ACTIVE]                = ImVec4(0.10, 0.40, 0.75, 1.00)
    colors[imgui.COLOR_RESIZE_GRIP]                     = ImVec4(0.26, 0.59, 0.98, 0.20)
    colors[imgui.COLOR_RESIZE_GRIP_HOVERED]             = ImVec4(0.26, 0.59, 0.98, 0.67)
    colors[imgui.COLOR_RESIZE_GRIP_ACTIVE]              = ImVec4(0.26, 0.59, 0.98, 0.95)
    colors[imgui.COLOR_TAB]                             = ImLerp(colors[imgui.COLOR_HEADER], colors[imgui.COLOR_TITLE_BACKGROUND_ACTIVE], 0.80)
    colors[imgui.COLOR_TAB_HOVERED]                     = colors[imgui.COLOR_HEADER_HOVERED]
    colors[imgui.COLOR_TAB_ACTIVE]                      = ImLerp(colors[imgui.COLOR_HEADER_ACTIVE], colors[imgui.COLOR_TITLE_BACKGROUND_ACTIVE], 0.60)
    colors[imgui.COLOR_TAB_UNFOCUSED]                   = ImLerp(colors[imgui.COLOR_TAB], colors[imgui.COLOR_TITLE_BACKGROUND], 0.60)
    colors[imgui.COLOR_TAB_UNFOCUSED_ACTIVE]            = ImLerp(colors[imgui.COLOR_TAB_ACTIVE], colors[imgui.COLOR_TITLE_BACKGROUND], 0.60)
    colors[imgui.COLOR_PLOT_LINES]                      = ImVec4(0.61, 0.61, 0.61, 1.00)
    colors[imgui.COLOR_PLOT_LINES_HOVERED]              = ImVec4(1.00, 0.43, 0.35, 1.00)
    colors[imgui.COLOR_PLOT_HISTOGRAM]                  = ImVec4(0.90, 0.70, 0.00, 1.00)
    colors[imgui.COLOR_PLOT_HISTOGRAM_HOVERED]          = ImVec4(1.00, 0.60, 0.00, 1.00)
    colors[imgui.COLOR_TABLE_HEADER_BACKGROUND]         = ImVec4(1.00, 0.60, 0.00, 1.00)
    colors[imgui.COLOR_TABLE_BORDER_STRONG]             = ImVec4(0.31, 0.31, 0.35, 1.00)
    colors[imgui.COLOR_TABLE_BORDER_LIGHT]              = ImVec4(0.23, 0.23, 0.25, 1.00)
    colors[imgui.COLOR_TABLE_ROW_BACKGROUND]            = ImVec4(0.00, 0.00, 0.00, 0.00)
    colors[imgui.COLOR_TABLE_ROW_BACKGROUND_ALT]        = ImVec4(1.00, 1.00, 1.00, 0.06)
    colors[imgui.COLOR_TEXT_SELECTED_BACKGROUND]        = ImVec4(0.26, 0.59, 0.98, 0.35)
    colors[imgui.COLOR_DRAG_DROP_TARGET]                = ImVec4(1.00, 1.00, 0.00, 0.90)
    colors[imgui.COLOR_NAV_HIGHLIGHT]                   = ImVec4(0.26, 0.59, 0.98, 1.00)
    colors[imgui.COLOR_NAV_WINDOWING_HIGHLIGHT]         = ImVec4(1.00, 1.00, 1.00, 0.70)
    colors[imgui.COLOR_NAV_WINDOWING_DIM_BACKGROUND]    = ImVec4(0.80, 0.80, 0.80, 0.20)
    colors[imgui.COLOR_MODAL_WINDOW_DIM_BACKGROUND]     = ImVec4(0.80, 0.80, 0.80, 0.35)

def menu():
    custom_color_style()
    io = imgui.get_io()
    style = imgui.get_style() # override active style
    imgui.set_next_window_size(250, 250)
    imgui.begin(
        "Hello World",
        # imgui.WINDOW_NO_MOVE
        flags=imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_SAVED_SETTINGS | imgui.WINDOW_NO_TITLE_BAR)
    
    imgui.text("Welcome to Hell")

    if imgui.button("Click me!"):
        print("Click")

    imgui.end()
