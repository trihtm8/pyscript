import pygame
import os
from abc import ABC, abstractmethod


class Audio:
    """
    Lớp Audio cung cấp các phương thức để phát âm thanh trong pygame.
    The Audio class provides methods for playing sound in pygame.
    """

    SOUND_DIRECTORY = os.path.join(os.path.dirname(__file__), 'static', 'sounds')

    @staticmethod
    def play_sound(sound_filename):
        """
        Phát một âm thanh từ tệp âm thanh đã cho.
        Play a sound from the given sound file.
        Parameters:
            sound_filename (str): Tên tệp âm thanh (không bao gồm đường dẫn).
        """
        sound_path = os.path.join(Audio.SOUND_DIRECTORY, sound_filename)
        pygame.mixer.Sound(sound_path).play()

    @staticmethod
    def play_music(music_filename, loop=-1):
        """
        Phát một bản nhạc từ tệp nhạc đã cho.
        Play music from the given music file.
        Parameters:
            music_filename (str): Tên tệp nhạc (không bao gồm đường dẫn).
            loop (int): Số lần lặp lại (mặc định là -1 cho lặp vô hạn).
        """
        music_path = os.path.join(Audio.SOUND_DIRECTORY, music_filename)
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(loop)

    @staticmethod
    def stop_music():
        """
        Dừng phát nhạc.
        Stop playing music.
        """
        pygame.mixer.music.stop()


class Widget(ABC):
    """
    Abstract Base Class đại diện cho một widget trong giao diện người dùng.
    This Abstract Base Class represents a widget in the user interface.
    """

    _used_ids = set()

    def __init__(self, id=None):
        """
        Khởi tạo một widget mới.
        Initializes a new widget.
        """
        self.children = []
        self.SURFACE = None
        if id is None:
            self.id = self._generate_unique_id()
        else:
            if id in Widget._used_ids:
                raise ValueError(f"ID '{id}' đã được sử dụng.")
            self.id = id
            Widget._used_ids.add(id)

    @staticmethod
    def _generate_unique_id():
        """
        Tạo một ID duy nhất cho đối tượng mới.
        Generate a unique ID for a new object.
        Returns:
            str: ID duy nhất.
        """
        new_id = str(len(Widget._used_ids))
        while new_id in Widget._used_ids:
            new_id = str(int(new_id) + 1)
        Widget._used_ids.add(new_id)
        return new_id

    @abstractmethod
    def print(self):
        """
        Phương thức trừu tượng để vẽ widget.
        Abstract method to draw the widget.
        """
        pass

    def add_child(self, location, child_object):
        """
        Thêm một đối tượng con vào widget.
        Add a child object to the widget.
        Parameters:
            location (tuple): Vị trí của đối tượng con trên widget.
            child_object (Widget): Đối tượng con cần thêm.
        """
        if not hasattr(self, 'children'):
            self.children = []
        self.children.append((location, child_object))

    def _draw_children(self):
        """
        Vẽ tất cả các đối tượng con của widget.
        Draw all child objects of the widget.
        """
        if self.SURFACE and hasattr(self, 'children'):
            for location, child in self.children:
                self.SURFACE.blit(child.print(), location)
                if isinstance(child, Widget):
                    child._draw_children()


class Screen(Widget):
    """
    Lớp Screen đại diện cho màn hình hiển thị của ứng dụng.
    The Screen class represents the display app of the application.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Singleton: Trả về thể hiện duy nhất của lớp Screen.
        Singleton: Returns the single instance of the Screen class.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, width=800, height=600, caption="PyScript App"):
        """
        Khởi tạo màn hình với kích thước và tiêu đề đã cho.
        Initialize the app with the given size and caption.
        """
        if not hasattr(self, '_initialized'):
            super().__init__("_screen")
            self.width = width
            self.height = height
            self.caption = caption
            self.SURFACE = None
            self.children = []
            self._initialized = True

    def print(self):
        """
        Phương thức để vẽ màn hình và tất cả các đối tượng con trên đó.
        Method to draw the app and all the child objects on it.
        Returns:
            pygame.Surface: Bề mặt hiển thị của màn hình.
        """
        if self.SURFACE is None:
            self.SURFACE = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption(self.caption)
        self._draw_children()
        return self.SURFACE

    @staticmethod
    def getElementById(search_id):
        """
        Tìm và trả về đối tượng con dựa trên ID. (Chỉ có thể gọi từ Screen)
        Find and return the child object based on the ID. (Can only be called from Screen)
        Parameters:
            search_id (str): ID của đối tượng cần tìm.
        Returns:
            Widget or None: Đối tượng con có ID tương ứng hoặc None nếu không tìm thấy.
        """
        return Screen._getElementByIdHelper(search_id, Screen().children)

    @staticmethod
    def _getElementByIdHelper(search_id, children):
        """
        Phương thức trợ giúp để tìm kiếm đệ quy trong các đối tượng con.
        Helper method to recursively search within child objects.
        """
        for _, child in children:
            if child.id == search_id:
                return child
            else:
                result = Screen._getElementByIdHelper(search_id, child.children)
                if result:
                    return result
        return None


class Container(Widget):
    """
    Lớp Container đại diện cho một vùng chứa đối tượng trong giao diện người dùng.
    This class represents a container for objects in the user interface.
    """

    def __init__(self, width, height, background_color=pygame.Color('white'), id=None):
        """
        Khởi tạo một container mới với kích thước và màu nền đã cho.
        Initialize a new container with the given size and background color.
        Parameters:
            width (int): Chiều rộng của container.
            height (int): Chiều cao của container.
            background_color (pygame.Color): Màu nền của container.
        """
        super().__init__(id)
        self.width = width
        self.height = height
        self.background_color = background_color
        self.SURFACE = pygame.Surface((width, height))

    def print(self):
        """
        Phương thức để vẽ container và tất cả các đối tượng con trên đó.
        Method to draw the container and all the child objects on it.
        Returns:
            pygame.Surface: Bề mặt hiển thị của container.
        """
        self.SURFACE.fill(self.background_color)
        self._draw_children()
        return self.SURFACE


class Window(Widget):
    """
    Lớp Window đại diện cho một cửa sổ giống cửa sổ của hệ điều hành Windows.
    The Window class represents a window similar to a Windows operating system window.
    """

    def __init__(self, width, height, title="", background_color=pygame.Color('white'), id=None):
        """
        Khởi tạo một cửa sổ mới.
        Initializes a new window.
        Parameters:
            width (int): Chiều rộng của cửa sổ.
            height (int): Chiều cao của cửa sổ (không tính thanh tiêu đề).
            title (str): Tiêu đề của cửa sổ.
            background_color (pygame.Color): Màu nền của cửa sổ.
            id (str): ID của cửa sổ.
        """
        super().__init__(id)
        self.width = width
        self.height = height
        self.title = title
        self.background_color = background_color
        self.title_height = 20
        self.SURFACE = pygame.Surface((width, height + self.title_height))

        # Thêm thanh tiêu đề màu xanh
        self.title_bar = pygame.Surface((width, self.title_height))
        self.title_bar.fill((0, 128, 255))

        # Thêm tiêu đề của cửa sổ
        font = pygame.font.Font(None, 16)
        title_text = font.render(title, True, pygame.Color('white'))
        title_rect = title_text.get_rect(center=(width // 2, self.title_height // 2))
        self.title_bar.blit(title_text, title_rect)

        # Thêm nút đóng (nút X đỏ)
        self.close_button = pygame.Surface((20, 20))
        self.close_button.fill(pygame.Color('red'))
        pygame.draw.line(self.close_button, pygame.Color('white'), (5, 5), (15, 15), 2)
        pygame.draw.line(self.close_button, pygame.Color('white'), (5, 15), (15, 5), 2)
        close_button_rect = self.close_button.get_rect(topright=(width, 0))
        self.title_bar.blit(self.close_button, close_button_rect)

    def print(self):
        """
        Phương thức để vẽ cửa sổ và tất cả các đối tượng con trên đó.
        Method to draw the window and all the child objects on it.
        Returns:
            pygame.Surface: Bề mặt hiển thị của cửa sổ.
        """
        self.SURFACE.fill(self.background_color)
        self.SURFACE.blit(self.title_bar, (0, 0))
        self._draw_children()

        return self.SURFACE

    def _draw_children(self):
        if hasattr(self, 'children'):
            for location, child in self.children:
                self.SURFACE.blit(child.print(), (location[0], location[1] + self.title_height))


class Image(Widget):
    """
    Lớp Image đại diện cho một widget hiển thị hình ảnh.
    The Image class represents a widget displaying an image.
    """

    IMAGE_DIRECTORY = os.path.join(os.path.dirname(__file__), 'static', 'images')

    def __init__(self, image_filename, width, height, id=None):
        """
        Khởi tạo một widget hiển thị hình ảnh.
        Initializes an image widget.
        Parameters:
            image_filename (str): Tên tệp hình ảnh (không bao gồm đường dẫn).
            width (int): Chiều rộng của hình ảnh.
            height (int): Chiều cao của hình ảnh.
            id (str): ID của widget.
        """
        super().__init__(id)
        self.image_path = os.path.join(self.IMAGE_DIRECTORY, image_filename)
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.width = width
        self.height = height

    def print(self):
        """
        Phương thức để vẽ hình ảnh.
        Method to draw the image.
        Returns:
            pygame.Surface: Bề mặt hiển thị của hình ảnh.
        """
        return self.image


class Button(Widget):
    """
    Lớp Button đại diện cho một widget nút trong giao diện người dùng.
    The Button class represents a button widget in the user interface.
    """

    def __init__(self, text, width, height, background_color, text_color, font, id=None):
        """
        Khởi tạo một nút mới.
        Initializes a new button.
        Parameters:
            text (str): Nội dung văn bản của nút.
            width (int): Chiều rộng của nút.
            height (int): Chiều cao của nút.
            background_color (pygame.Color): Màu nền của nút.
            text_color (pygame.Color): Màu văn bản của nút.
            font (pygame.font.Font): Font chữ của văn bản nút.
            id (str): ID của nút.
        """
        super().__init__(id)
        self.text = text
        self.width = width
        self.height = height
        self.background_color = background_color
        self.text_color = text_color
        self.font = font

        self.surface = pygame.Surface((width, height))
        self.surface.fill(background_color)

        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(width // 2, height // 2))
        self.surface.blit(text_surface, text_rect)

    def print(self):
        """
        Phương thức để vẽ nút.
        Method to draw the button.
        Returns:
            pygame.Surface: Bề mặt hiển thị của nút.
        """
        return self.surface


class Text(Widget):
    """
    Lớp Text đại diện cho một widget hiển thị văn bản.
    The Text class represents a widget displaying text.
    """

    def __init__(self, text, font, color, id=None):
        """
        Khởi tạo một widget hiển thị văn bản.
        Initializes a text widget.
        Parameters:
            text (str): Nội dung văn bản.
            font (pygame.font.Font): Font chữ của văn bản.
            color (pygame.Color): Màu văn bản.
            id (str): ID của widget.
        """
        super().__init__(id)
        self.text = text
        self.font = font
        self.color = color

        self.surface = font.render(text, True, color)

    def print(self):
        """
        Phương thức để vẽ văn bản.
        Method to draw the text.
        Returns:
            pygame.Surface: Bề mặt hiển thị của văn bản.
        """
        return self.surface


class Rectangle(Widget):
    """
    Lớp Rectangle đại diện cho một widget hình chữ nhật trên giao diện người dùng.
    The Rectangle class represents a rectangle widget in the user interface.
    """

    def __init__(self, width, height, color, id=None):
        """
        Khởi tạo một widget hình chữ nhật.
        Initializes a rectangle widget.
        Parameters:
            width (int): Chiều rộng của hình chữ nhật.
            height (int): Chiều cao của hình chữ nhật.
            color (pygame.Color): Màu của hình chữ nhật.
            id (str): ID của widget.
        """
        super().__init__(id)
        self.width = width
        self.height = height
        self.color = color

        # Tạo bề mặt hình chữ nhật
        self.surface = pygame.Surface((width, height))
        self.surface.fill(color)

    def print(self):
        """
        Phương thức để vẽ hình chữ nhật.
        Method to draw the rectangle.
        Returns:
            pygame.Surface: Bề mặt hiển thị của hình chữ nhật.
        """
        return self.surface


class RectangleText(Widget):
    """
    Lớp RectangleText đại diện cho một widget hình chữ nhật với văn bản bên trong trên giao diện người dùng.
    The RectangleText class represents a rectangle widget with text inside in the user interface.
    """

    def __init__(self, text, width, height, color, text_color, font, id=None):
        """
        Khởi tạo một widget hình chữ nhật với văn bản bên trong.
        Initializes a rectangle widget with text inside.
        Parameters:
            text (str): Nội dung văn bản.
            width (int): Chiều rộng của hình chữ nhật.
            height (int): Chiều cao của hình chữ nhật.
            color (pygame.Color): Màu của hình chữ nhật.
            text_color (pygame.Color): Màu của văn bản.
            font (pygame.font.Font): Font chữ của văn bản.
            id (str): ID của widget.
        """
        super().__init__(id)
        self.text = text
        self.width = width
        self.height = height
        self.color = color
        self.text_color = text_color
        self.font = font

        # Tạo bề mặt hình chữ nhật
        self.surface = pygame.Surface((width, height))
        self.surface.fill(color)

        # Vẽ văn bản lên hình chữ nhật
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(width // 2, height // 2))
        self.surface.blit(text_surface, text_rect)

    def print(self):
        """
        Phương thức để vẽ hình chữ nhật với văn bản.
        Method to draw the rectangle with text.
        Returns:
            pygame.Surface: Bề mặt hiển thị của hình chữ nhật với văn bản.
        """
        return self.surface


class Circle(Widget):
    """
    Lớp Circle đại diện cho một widget hình tròn trên giao diện người dùng.
    The Circle class represents a circle widget in the user interface.
    """

    def __init__(self, radius, color, id=None):
        """
        Khởi tạo một widget hình tròn.
        Initializes a circle widget.
        Parameters:
            radius (int): Bán kính của hình tròn.
            color (pygame.Color): Màu của hình tròn.
            id (str): ID của widget.
        """
        super().__init__(id)
        self.radius = radius
        self.color = color

        # Tạo bề mặt hình tròn
        diameter = radius * 2
        self.surface = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        pygame.draw.circle(self.surface, color, (radius, radius), radius)

    def print(self):
        """
        Phương thức để vẽ hình tròn.
        Method to draw the circle.
        Returns:
            pygame.Surface: Bề mặt hiển thị của hình tròn.
        """
        return self.surface


class CircleText(Widget):
    """
    Lớp CircleText đại diện cho một widget hình tròn với văn bản bên trong trên giao diện người dùng.
    The CircleText class represents a circle widget with text inside in the user interface.
    """

    def __init__(self, text, radius, color, text_color, font, id=None):
        """
        Khởi tạo một widget hình tròn với văn bản bên trong.
        Initializes a circle widget with text inside.
        Parameters:
            text (str): Nội dung văn bản.
            radius (int): Bán kính của hình tròn.
            color (pygame.Color): Màu của hình tròn.
            text_color (pygame.Color): Màu của văn bản.
            font (pygame.font.Font): Font chữ của văn bản.
            id (str): ID của widget.
        """
        super().__init__(id)
        self.text = text
        self.radius = radius
        self.color = color
        self.text_color = text_color
        self.font = font

        # Tạo bề mặt hình tròn
        diameter = radius * 2
        self.surface = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        pygame.draw.circle(self.surface, color, (radius, radius), radius)

        # Vẽ văn bản lên hình tròn
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(radius, radius))
        self.surface.blit(text_surface, text_rect)

    def print(self):
        """
        Phương thức để vẽ hình tròn với văn bản.
        Method to draw the circle with text.
        Returns:
            pygame.Surface: Bề mặt hiển thị của hình tròn với văn bản.
        """
        return self.surface


class Textbox(Widget):
    """
    Lớp Textbox đại diện cho một ô nhập văn bản trong giao diện người dùng.
    The Textbox class represents a text input box in the user interface.
    """

    def __init__(self, width, height, text='', font_name='Arial', font_size=24, text_color=(0, 0, 0),
                 background_color=(255, 255, 255), id=None):
        """
        Khởi tạo một Textbox mới.
        Initializes a new Textbox.
        
        Parameters:
            width (int): Chiều rộng của textbox.
            height (int): Chiều cao của textbox.
            text (str): Văn bản mặc định của textbox.
            font_name (str): Tên phông chữ của văn bản.
            font_size (int): Kích thước phông chữ của văn bản.
            text_color (tuple): Màu của văn bản.
            background_color (tuple): Màu nền của textbox.
            id (str): ID của widget.
        """
        super().__init__(id)
        self.width = width
        self.height = height
        self.text = text
        self.font_name = font_name
        self.font_size = font_size
        self.text_color = text_color
        self.background_color = background_color
        self.font = pygame.font.SysFont(font_name, font_size)
        self.surface = pygame.Surface((width, height))
        self.render_text()

    def render_text(self):
        """
        Vẽ văn bản lên bề mặt textbox.
        Renders the text onto the textbox surface.
        """
        self.surface.fill(self.background_color)
        text_surface = self.font.render(self.text, True, self.text_color)
        self.surface.blit(text_surface, (5, (self.height - text_surface.get_height()) // 2 + 1))

    def print(self):
        """
        Phương thức để vẽ textbox.
        Method to draw the textbox.
        
        Returns:
            pygame.Surface: Bề mặt hiển thị của textbox.
        """
        self.render_text()
        return self.surface

    def set_text(self, text):
        """
        Đặt văn bản mới cho textbox.
        Sets new text for the textbox.
        
        Parameters:
            text (str): Văn bản mới.
        """
        self.text = text
        self.render_text()


class Checkbox(Widget):
    """
    Lớp Checkbox đại diện cho một hộp kiểm trong giao diện người dùng.
    The Checkbox class represents a checkbox in the user interface.
    """

    def __init__(self, size, is_checked=False, border_color=(0, 0, 0), check_color=(0, 0, 0),
                 background_color=(255, 255, 255), id=None):
        """
        Khởi tạo một Checkbox mới.
        Initializes a new Checkbox.
        
        Parameters:
            size (int): Kích thước của checkbox (chiều rộng và chiều cao).
            is_checked (bool): Trạng thái kiểm tra ban đầu của checkbox.
            border_color (tuple): Màu của viền checkbox.
            check_color (tuple): Màu của dấu kiểm.
            background_color (tuple): Màu nền của checkbox.
            id (str): ID của widget.
        """
        super().__init__(id)
        self.size = size
        self.is_checked = is_checked
        self.border_color = border_color
        self.check_color = check_color
        self.background_color = background_color
        self.surface = pygame.Surface((size, size))
        self.render_checkbox()

    def render_checkbox(self):
        """
        Vẽ checkbox lên bề mặt.
        Renders the checkbox onto the surface.
        """
        self.surface.fill(self.background_color)
        pygame.draw.rect(self.surface, self.border_color, (0, 0, self.size, self.size), 2)
        if self.is_checked:
            pygame.draw.line(self.surface, self.check_color, (4, self.size // 2), (self.size // 2, self.size - 4), 2)
            pygame.draw.line(self.surface, self.check_color, (self.size // 2, self.size - 4), (self.size - 4, 4), 2)

    def print(self):
        """
        Phương thức để vẽ checkbox.
        Method to draw the checkbox.
        
        Returns:
            pygame.Surface: Bề mặt hiển thị của checkbox.
        """
        self.render_checkbox()
        return self.surface

    def toggle(self):
        """
        Chuyển đổi trạng thái của checkbox.
        Toggles the state of the checkbox.
        """
        self.is_checked = not self.is_checked
        self.render_checkbox()


class Form(Widget):
    """
    Lớp Form đại diện cho một form với khung viền và header.
    The Form class represents a form with a border and header.
    """

    def __init__(self, width, height, title, targeted=False, id=None):
        """
        Khởi tạo một form mới với khung viền và header.
        Initializes a new form with a border and header.
        Parameters:
            width (int): Chiều rộng của form.
            height (int): Chiều cao của form (không tính chiều cao header).
            title (str): Tiêu đề của form.
            targeted (bool): Trạng thái của form (được target hay không).
            id (str): ID của form.
        """
        super().__init__(id)
        self.width = width
        self.height = height
        self.title = title
        self.targeted = targeted
        self.header_height = 20
        self.SURFACE = pygame.Surface((width, height + self.header_height))
        self.border_color = pygame.Color('black') if targeted else pygame.Color('gray')
        self.header_color = pygame.Color(230, 230, 230)
        self.header_font = pygame.font.Font(None, 16)

        # Vẽ header
        self.header = pygame.Surface((width, self.header_height))
        self.header.fill(self.header_color)
        title_text = self.header_font.render(title, True, pygame.Color('black'))
        self.header.blit(title_text, (5, 5))

    def print(self):
        """
        Phương thức để vẽ form và tất cả các đối tượng con trên đó.
        Method to draw the form and all the child objects on it.
        Returns:
            pygame.Surface: Bề mặt hiển thị của form.
        """
        self.SURFACE.fill(pygame.Color('white'))
        self.SURFACE.blit(self.header, (0, 0))
        pygame.draw.rect(self.SURFACE, self.border_color, self.SURFACE.get_rect(), 2)
        self._draw_children()

        return self.SURFACE

    def _draw_children(self):
        if hasattr(self, 'children'):
            for location, child in self.children:
                self.SURFACE.blit(child.print(), (location[0], location[1] + self.header_height))


class Input(Widget):
    """
    Lớp Input đại diện cho một widget input với label và textbox.
    The Input class represents an input widget with a label and a textbox.
    """

    def __init__(self, label_text, width, value='', font_size=16, targeted=False, background_color=(240, 255, 240),
                 targeted_color=(192, 192, 192), id=None):
        """
        Khởi tạo một input mới với label và textbox.
        Initializes a new input with a label and a textbox.
        Parameters:
            label_text (str): Văn bản của label.
            width (int): Chiều rộng của textbox.
            value (str): Giá trị mặc định của textbox.
            font_size (int): Cỡ chữ của label và textbox.
            targeted (bool): Trạng thái của input (được target hay không).
            background_color (tuple): Màu nền của textbox.
            targeted_color (tuple): Màu nền khi textbox được target.
            id (str): ID của input.
        """
        super().__init__(id)
        self.label_text = label_text
        self.width = width
        self.font_size = font_size
        self.targeted = targeted
        self.background_color = background_color
        self.targeted_color = targeted_color
        self.border_color = pygame.Color('black') if targeted else pygame.Color('gray')
        self.font = pygame.font.Font(None, font_size)
        label_width, label_height = self.font.size(label_text)
        self.height = label_height

        self.SURFACE = pygame.Surface((width + label_width + 10, self.height + 4))

        # Vẽ label
        self.label = self.font.render(label_text, True, pygame.Color('black'))

        # Sử dụng Textbox
        self.textbox = Textbox(self.width, self.height, value, id, font_size=self.font_size)
        self.textbox.background_color = pygame.Color(*background_color) if not targeted else pygame.Color(*
                                                                                                          targeted_color
                                                                                                          )

    def print(self):
        """
        Phương thức để vẽ input và tất cả các đối tượng con trên đó.
        Method to draw the input and all the child objects on it.
        Returns:
            pygame.Surface: Bề mặt hiển thị của input.
        """
        self.SURFACE.fill(pygame.Color('white'))
        self.SURFACE.blit(self.label, (3, 3))
        self.SURFACE.blit(self.textbox.print(), (self.label.get_width() + 10, 2))
        pygame.draw.rect(self.SURFACE, self.border_color, self.SURFACE.get_rect(), 2)
        return self.SURFACE

    @property
    def value(self):
        """
        Trả về giá trị của thuộc tính text của textbox.
        Returns the value of the text attribute of the textbox.
        """
        return self.textbox.text

    @value.setter
    def value(self, new_value):
        """
        Thiết lập giá trị của thuộc tính text của textbox.
        Sets the value of the text attribute of the textbox.
        """
        self.textbox.text = new_value
