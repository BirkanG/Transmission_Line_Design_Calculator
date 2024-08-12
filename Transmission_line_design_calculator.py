from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import math

def set_dark_theme(app):
    app.setStyle("Fusion")

    dark_palette = QPalette()
    
    # Base colors
    dark_palette.setColor(QPalette.Window, QColor(30,30,30))
    dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Base, QColor(45,45,45))
    dark_palette.setColor(QPalette.AlternateBase, QColor(60,60,60))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.PlaceholderText, QColor(156, 155, 152))
    dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Button, QColor(45,45,45))
    dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    
    # Highlight colors
    dark_palette.setColor(QPalette.Highlight, QColor(57,57,57))
    dark_palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    
    # Disabled colors
    dark_palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(127, 127, 127))
    dark_palette.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 127, 127))
    dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127))
    
    app.setPalette(dark_palette)

limits = {
    "Type-1: Narrow Base Tower": {
        "x_coordinates_a": (-4.0, -2.2),
        "y_coordinates_a": (23, 39),  
        "x_coordinates_b": (2.2, 4.0),
        "y_coordinates_b": (23, 39),
        "x_coordinates_c": (2.2, 4.0),
        "y_coordinates_c": (23, 39),
        "number_of_conductors": (1, 3)
    },
    "Type-2: Single Circuit Delta Tower": {
        "x_coordinates_a": (-11.5, -9.4),
        "y_coordinates_a": (38.25, 43),
        "x_coordinates_b": (-8.9, 8.9),
        "y_coordinates_b": (38.25, 43),
        "x_coordinates_c": (9.4, 11.5),
        "y_coordinates_c": (38.25, 43),
        "number_of_conductors": (1,4)
    },
    "Type-3: Double Circuit Vertical Tower": {
        
        "x_coordinates_a": (1.8, 5.35),
        "y_coordinates_a": (36, 48.8),
        "x_coordinates_b": (1.8, 5.35),
        "y_coordinates_b": (36, 48.8),
        "x_coordinates_c": (1.8, 5.35),
        "y_coordinates_c": (36, 48.8),
        "number_of_conductors": (1,3)
    }
}

class TransmissionLineGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transmission Line Design Calculator")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        widget = QWidget()
        self.setCentralWidget(widget)

        grid_layout = QGridLayout()
        widget.setLayout(grid_layout)

        # layout for the input/output fields
        grid_layout.addWidget(QLabel("Tower Type:"), 0, 0)
        self.tower_type = QComboBox()
        self.tower_type.addItems(
            ["Type-1: Narrow Base Tower", "Type-2: Single Circuit Delta Tower",
             "Type-3: Double Circuit Vertical Tower"])

        grid_layout.addWidget(self.tower_type, 0, 1, 1, 2)

        grid_layout.addWidget(QLabel("Number of Circuits:"), 1, 0)
        self.number_of_circuits = QComboBox()
        self.number_of_circuits.addItems(["1", "2"])  # Added combobox for circuit selection
        self.number_of_circuits.setEnabled(False)  # Disable by default
        self.number_of_circuits.setToolTip("For Type-1 and Type-3 towers, only single circuit can be deployed.")
        grid_layout.addWidget(self.number_of_circuits, 1, 1, 1, 2)

        line_top = QFrame()
        line_top.setFrameShape(QFrame.HLine)
        line_top.setFrameShadow(QFrame.Sunken)
        line_top.setStyleSheet("background-color: rgb(60,60,60);")
        grid_layout.addWidget(line_top, 2, 0, 1, 3)

        label_xy_coordinates = QLabel("X-Y Coordinates of the Phase Lines (m):")
        grid_layout.addWidget(label_xy_coordinates, 3, 0)
        label_xy_coordinates.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        label_xy_coordinates_circ1 = QLabel(" 1. Circuit X-Y Coordinates ")
        label_xy_coordinates_circ1.setStyleSheet("border: none; border-bottom: 1px groove gray;")
        grid_layout.addWidget(label_xy_coordinates_circ1, 3, 1)
        self.label_xa = QLabel("Phase A, X coordinate:")
        grid_layout.addWidget(self.label_xa, 4, 0)
        self.x_coordinates_a = QLineEdit()
        grid_layout.addWidget(self.x_coordinates_a, 4, 1)
        self.label_ya = QLabel("Phase A, Y coordinate:")
        grid_layout.addWidget(self.label_ya, 5, 0)
        self.y_coordinates_a = QLineEdit()
        grid_layout.addWidget(self.y_coordinates_a, 5, 1)
        self.label_xb = QLabel("Phase B, X coordinate:")
        grid_layout.addWidget(self.label_xb, 6, 0)
        self.x_coordinates_b = QLineEdit()
        grid_layout.addWidget(self.x_coordinates_b, 6, 1)
        self.label_yb = QLabel("Phase B, Y coordinate:")
        grid_layout.addWidget(self.label_yb, 7, 0)
        self.y_coordinates_b = QLineEdit()
        grid_layout.addWidget(self.y_coordinates_b, 7, 1)
        self.label_xc = QLabel("Phase C, X coordinate:")
        grid_layout.addWidget(self.label_xc, 8, 0)
        self.x_coordinates_c = QLineEdit()
        grid_layout.addWidget(self.x_coordinates_c, 8, 1)
        self.label_yc = QLabel("Phase C, Y coordinate:")
        grid_layout.addWidget(self.label_yc, 9, 0)
        self.y_coordinates_c = QLineEdit()
        grid_layout.addWidget(self.y_coordinates_c, 9, 1)

        # Additional fields for second circuit
        label_xy_coordinates_circ2 = QLabel(" 2. Circuit X-Y Coordinates ")
        label_xy_coordinates_circ2.setStyleSheet("border: none; border-bottom: 1px groove gray;")
        grid_layout.addWidget(label_xy_coordinates_circ2, 3, 2)
        self.x_coordinates_a_2 = QLineEdit()
        grid_layout.addWidget(self.x_coordinates_a_2, 4, 2)
        self.y_coordinates_a_2 = QLineEdit()
        grid_layout.addWidget(self.y_coordinates_a_2, 5, 2)
        self.x_coordinates_b_2 = QLineEdit()
        grid_layout.addWidget(self.x_coordinates_b_2, 6, 2)
        self.y_coordinates_b_2 = QLineEdit()
        grid_layout.addWidget(self.y_coordinates_b_2, 7, 2)
        self.x_coordinates_c_2 = QLineEdit()
        grid_layout.addWidget(self.x_coordinates_c_2, 8, 2)
        self.y_coordinates_c_2 = QLineEdit()
        grid_layout.addWidget(self.y_coordinates_c_2, 9, 2)

        line_bottom = QFrame()
        line_bottom.setFrameShape(QFrame.HLine)
        line_bottom.setFrameShadow(QFrame.Sunken)
        line_bottom.setStyleSheet("background-color: rgb(60,60,60);")
        grid_layout.addWidget(line_bottom, 10, 0, 1, 3)

        self.label_number_of_conductors = QLabel("Number of Conductors in Bundle:")
        grid_layout.addWidget(self.label_number_of_conductors, 11, 0)
        self.number_of_conductors = QLineEdit()
        grid_layout.addWidget(self.number_of_conductors, 11, 1, 1, 2)

        self.label_distance_between_conductors = QLabel("Distance Between Conductors in Bundle (cm):")
        grid_layout.addWidget(self.label_distance_between_conductors, 12, 0)
        self.distance_between_conductors = QLineEdit()
        grid_layout.addWidget(self.distance_between_conductors, 12, 1, 1, 2)

        grid_layout.addWidget(QLabel("Conductor Type:"), 13, 0)
        self.conductor_type = QComboBox()
        self.conductor_type.addItems(["Hawk", "Drake", "Cardinal", "Rail", "Pheasant"])
        grid_layout.addWidget(self.conductor_type, 13, 1, 1, 2)

        self.label_line_length = QLabel("Length of Transmission Line (km):")
        grid_layout.addWidget(self.label_line_length, 14, 0)
        self.line_length = QLineEdit()
        grid_layout.addWidget(self.line_length, 14, 1, 1, 2)

        self.calculate_button = QPushButton("Calculate")
        grid_layout.addWidget(self.calculate_button, 15, 0, 1, 3)  
        self.calculate_button.clicked.connect(self.calculate_parameters) # calculate the parameters when the button is clicked

        self.output_R = QLineEdit()
        self.output_R.setDisabled(True)
        self.output_R.setStyleSheet("color: white;")
        grid_layout.addWidget(QLabel("Line Resistance R (Ω):"), 16, 0)
        grid_layout.addWidget(self.output_R, 16, 1, 1, 2)

        self.output_L = QLineEdit()
        self.output_L.setDisabled(True)
        self.output_L.setStyleSheet("color: white;")
        grid_layout.addWidget(QLabel("Line Inductance L (mH):"), 17, 0)
        grid_layout.addWidget(self.output_L, 17, 1, 1, 2)

        self.output_C = QLineEdit()
        self.output_C.setDisabled(True)
        self.output_C.setStyleSheet("color: white;")
        grid_layout.addWidget(QLabel("Line Charging Capacitance C (µF):"), 18, 0)
        grid_layout.addWidget(self.output_C, 18, 1, 1, 2)

        self.output_capacity = QLineEdit()
        self.output_capacity.setDisabled(True)
        self.output_capacity.setStyleSheet("color: white;")
        grid_layout.addWidget(QLabel("Line Capacity (MVA):"), 19, 0)
        grid_layout.addWidget(self.output_capacity, 19, 1, 1, 2)

        self.image_frame = QFrame()
        self.image_frame.setFrameShape(QFrame.StyledPanel)
        self.image_frame.setFrameShadow(QFrame.Raised)
        self.image_frame.setStyleSheet("background-color: rgb(45,45,45);")
        self.image_frame.setLineWidth(2)
        self.image_layout = QVBoxLayout(self.image_frame)
        grid_layout.addWidget(self.image_frame, 0, 3, 17, 1)

        self.title_label = QLabel("Tower Type") # change the title according to (temporary name)
        self.title_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.title_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.image_layout.addWidget(self.title_label)

        self.image_label = QLabel()
        grid_layout.addWidget(self.image_label, 0, 3, 18, 1)

        grid_layout.setColumnStretch(0, 1)
        total_rows = 20
        for i in range(total_rows):
            grid_layout.setRowStretch(i, 1)

        self.tower_type.currentIndexChanged.connect(self.update_circuits_input)
        self.number_of_circuits.currentIndexChanged.connect(self.update_circuits_input)
        self.update_circuits_input()

    def update_circuits_input(self):
        # Clear input/output fields
        coordinates = [
            self.x_coordinates_a, self.y_coordinates_a, self.x_coordinates_b, self.y_coordinates_b,
            self.x_coordinates_c, self.y_coordinates_c, self.x_coordinates_a_2, self.y_coordinates_a_2,
            self.x_coordinates_b_2, self.y_coordinates_b_2, self.x_coordinates_c_2, self.y_coordinates_c_2,
            self.number_of_conductors, self.output_R, self.output_L, self.output_C, self.output_capacity
        ]

        for coordinate in coordinates:
            coordinate.clear()

        # Reset styles
        for coordinate in coordinates:
            coordinate.setStyleSheet("")

        # Reset labels' styles
        labels = [
            self.label_number_of_conductors, self.label_xa, self.label_ya,
            self.label_xb, self.label_yb, self.label_xc, self.label_yc,
            self.label_distance_between_conductors, self.label_line_length
        ]

        for label in labels:
            label.setText(f"{label.text().strip('* ')}")

        # Reset additional styles
        self.line_length.setStyleSheet("")
        self.distance_between_conductors.setStyleSheet("")


        # change the limits of the coordinates based on the tower type
        tower_type = self.tower_type.currentText()
        limits_dict = limits[tower_type]
        self.x_coordinates_a.setValidator(QDoubleValidator(limits_dict["x_coordinates_a"][0], limits_dict["x_coordinates_a"][1], 2))
        self.y_coordinates_a.setValidator(QDoubleValidator(limits_dict["y_coordinates_a"][0], limits_dict["y_coordinates_a"][1], 2))
        self.x_coordinates_b.setValidator(QDoubleValidator(limits_dict["x_coordinates_b"][0], limits_dict["x_coordinates_b"][1], 2))
        self.y_coordinates_b.setValidator(QDoubleValidator(limits_dict["y_coordinates_b"][0], limits_dict["y_coordinates_b"][1], 2))
        self.x_coordinates_c.setValidator(QDoubleValidator(limits_dict["x_coordinates_c"][0], limits_dict["x_coordinates_c"][1], 2))
        self.y_coordinates_c.setValidator(QDoubleValidator(limits_dict["y_coordinates_c"][0], limits_dict["y_coordinates_c"][1], 2))
        self.x_coordinates_a_2.setValidator(QDoubleValidator(-1*limits_dict["x_coordinates_a"][1], -1*limits_dict["x_coordinates_a"][0], 2))
        self.y_coordinates_a_2.setValidator(QDoubleValidator(limits_dict["y_coordinates_a"][0], limits_dict["y_coordinates_a"][1], 2))
        self.x_coordinates_b_2.setValidator(QDoubleValidator(-1*limits_dict["x_coordinates_b"][1], -1*limits_dict["x_coordinates_b"][0], 2))
        self.y_coordinates_b_2.setValidator(QDoubleValidator(limits_dict["y_coordinates_b"][0], limits_dict["y_coordinates_b"][1], 2))
        self.x_coordinates_c_2.setValidator(QDoubleValidator(-1*limits_dict["x_coordinates_c"][1], -1*limits_dict["x_coordinates_c"][0], 2))
        self.y_coordinates_c_2.setValidator(QDoubleValidator(limits_dict["y_coordinates_c"][0], limits_dict["y_coordinates_c"][1], 2))
        self.number_of_conductors.setValidator(QIntValidator(limits_dict["number_of_conductors"][0], limits_dict["number_of_conductors"][1]))

        # change the placeholder text based on the tower type
        self.x_coordinates_a.setPlaceholderText(f"{limits_dict['x_coordinates_a'][0]} - {limits_dict['x_coordinates_a'][1]}")
        self.y_coordinates_a.setPlaceholderText(f"{limits_dict['y_coordinates_a'][0]} - {limits_dict['y_coordinates_a'][1]}")
        self.x_coordinates_b.setPlaceholderText(f"{limits_dict['x_coordinates_b'][0]} - {limits_dict['x_coordinates_b'][1]}")
        self.y_coordinates_b.setPlaceholderText(f"{limits_dict['y_coordinates_b'][0]} - {limits_dict['y_coordinates_b'][1]}")
        self.x_coordinates_c.setPlaceholderText(f"{limits_dict['x_coordinates_c'][0]} - {limits_dict['x_coordinates_c'][1]}")
        self.y_coordinates_c.setPlaceholderText(f"{limits_dict['y_coordinates_c'][0]} - {limits_dict['y_coordinates_c'][1]}")
        self.number_of_conductors.setPlaceholderText(f"{limits_dict['number_of_conductors'][0]} - {limits_dict['number_of_conductors'][1]}")
        
        # Enable the number of circuits input if the tower type is Type-3
        if self.tower_type.currentText() == "Type-3: Double Circuit Vertical Tower":
            self.number_of_circuits.setEnabled(True)
        else:
            self.number_of_circuits.setEnabled(False)
            self.number_of_circuits.setCurrentIndex(0)  # Default to 1 circuit when disabled

        #Determine if the second circuit inputs should be changable or not when the number of circuits is changed 
        if self.number_of_circuits.currentText() == "2":
            self.x_coordinates_a_2.setReadOnly(False)
            self.y_coordinates_a_2.setReadOnly(False)
            self.x_coordinates_b_2.setReadOnly(False)
            self.y_coordinates_b_2.setReadOnly(False)
            self.x_coordinates_c_2.setReadOnly(False)
            self.y_coordinates_c_2.setReadOnly(False)
            self.x_coordinates_a_2.setStyleSheet("")
            self.y_coordinates_a_2.setStyleSheet("")
            self.x_coordinates_b_2.setStyleSheet("")
            self.y_coordinates_b_2.setStyleSheet("")
            self.x_coordinates_c_2.setStyleSheet("")
            self.y_coordinates_c_2.setStyleSheet("")
            self.x_coordinates_a_2.setPlaceholderText(f"{-1*limits_dict['x_coordinates_a'][1]} - {-1*limits_dict['x_coordinates_a'][0]}")
            self.y_coordinates_a_2.setPlaceholderText(f"{limits_dict['y_coordinates_a'][0]} - {limits_dict['y_coordinates_a'][1]}")
            self.x_coordinates_b_2.setPlaceholderText(f"{-1*limits_dict['x_coordinates_b'][1]} - {-1*limits_dict['x_coordinates_b'][0]}")
            self.y_coordinates_b_2.setPlaceholderText(f"{limits_dict['y_coordinates_b'][0]} - {limits_dict['y_coordinates_b'][1]}")
            self.x_coordinates_c_2.setPlaceholderText(f"{-1*limits_dict['x_coordinates_c'][1]} - {-1*limits_dict['x_coordinates_c'][0]}")
            self.y_coordinates_c_2.setPlaceholderText(f"{limits_dict['y_coordinates_c'][0]} - {limits_dict['y_coordinates_c'][1]}")
        else:
            self.x_coordinates_a_2.setReadOnly(True)
            self.y_coordinates_a_2.setReadOnly(True)
            self.x_coordinates_b_2.setReadOnly(True)
            self.y_coordinates_b_2.setReadOnly(True)
            self.x_coordinates_c_2.setReadOnly(True)
            self.y_coordinates_c_2.setReadOnly(True)
            self.x_coordinates_a_2.setStyleSheet("background-color: black; border: none; QlineEdit::placeholder {color: light gray;}")
            self.y_coordinates_a_2.setStyleSheet("background-color: black; border: none;")
            self.x_coordinates_b_2.setStyleSheet("background-color: black; border: none;")
            self.y_coordinates_b_2.setStyleSheet("background-color: black; border: none;")
            self.x_coordinates_c_2.setStyleSheet("background-color: black; border: none;")
            self.y_coordinates_c_2.setStyleSheet("background-color: black; border: none;")
            self.x_coordinates_a_2.setPlaceholderText("N/A")
            self.y_coordinates_a_2.setPlaceholderText("N/A")
            self.x_coordinates_b_2.setPlaceholderText("N/A")
            self.y_coordinates_b_2.setPlaceholderText("N/A")
            self.x_coordinates_c_2.setPlaceholderText("N/A")
            self.y_coordinates_c_2.setPlaceholderText("N/A")
        
        # Determine the image path based on the tower type
        if tower_type == "Type-1: Narrow Base Tower":
            self.image_path = "type1.png"
            self.title_text = "Type-1: Narrow Base Tower"
        elif tower_type == "Type-2: Single Circuit Delta Tower":
            self.image_path = "type2.png"
            self.title_text = "Type-2: Single Circuit Delta Tower"
        elif tower_type == "Type-3: Double Circuit Vertical Tower":
            self.image_path = "type3.png"
            self.title_text = "Type-3: Double Circuit Vertical Tower"
        else:
            self.image_path = ""  # Default
            self.title_text = "Unknown Tower Type"
        # Set the title label text
        self.title_label.setText(self.title_text)
        # Set the image
        pixmap = QPixmap(self.image_path)
        self.image_label.setPixmap(pixmap)

    def validate_input(self):
        inputs = [
            (self.label_distance_between_conductors, self.distance_between_conductors),
            (self.label_line_length, self.line_length),
        ]

        error_messages = []
        
        # Reset the style of all line edits and in the dictionary
        for label, line_edit in inputs:
            line_edit.setStyleSheet("")
            label.setText(f"{label.text().strip('* ')}")
        self.label_number_of_conductors.setText(f"{self.label_number_of_conductors.text().strip('* ')}")
        self.number_of_conductors.setStyleSheet("")
        self.label_xa.setText(f"{self.label_xa.text().strip('* ')}")
        self.x_coordinates_a.setStyleSheet("QlineEdit {color: black;} QlineEdit::placeholder {color: light gray;} QLineEdit {border: 1px solid black;}")
        self.label_ya.setText(f"{self.label_ya.text().strip('* ')}")
        self.y_coordinates_a.setStyleSheet("")
        self.label_xb.setText(f"{self.label_xb.text().strip('* ')}")
        self.x_coordinates_b.setStyleSheet("")
        self.label_yb.setText(f"{self.label_yb.text().strip('* ')}")
        self.y_coordinates_b.setStyleSheet("")
        self.label_xc.setText(f"{self.label_xc.text().strip('* ')}")
        self.x_coordinates_c.setStyleSheet("")
        self.label_yc.setText(f"{self.label_yc.text().strip('* ')}")
        self.y_coordinates_c.setStyleSheet("")
        if self.number_of_circuits.currentText() == "2":
            self.x_coordinates_a_2.setStyleSheet("")
            self.y_coordinates_a_2.setStyleSheet("")
            self.x_coordinates_b_2.setStyleSheet("")
            self.y_coordinates_b_2.setStyleSheet("")
            self.x_coordinates_c_2.setStyleSheet("")
            self.y_coordinates_c_2.setStyleSheet("")
        else:
            self.x_coordinates_a_2.setStyleSheet("background-color: black; border: none;")
            self.y_coordinates_a_2.setStyleSheet("background-color: black; border: none;")
            self.x_coordinates_b_2.setStyleSheet("background-color: black; border: none;")
            self.y_coordinates_b_2.setStyleSheet("background-color: black; border: none;")
            self.x_coordinates_c_2.setStyleSheet("background-color: black; border: none;")
            self.y_coordinates_c_2.setStyleSheet("background-color: black; border: none;")

        # Check if all inputs are within limits and convert to float (except for coordinates)
        for label, line_edit in inputs:
            value = line_edit.text()
            if not value:
                error_messages.append(f"Please enter {label.text()}.")
                line_edit.setStyleSheet("QlineEdit {color: red;} QlineEdit::placeholder {color: red;} QLineEdit {border: 1px solid red;}")
                label.setText(f"{label.text().strip('* ')} *")
            else:
                try:
                    float_value = float(value)
                    if float_value <= 0:
                        error_messages.append(f"{label.text()} must be a positive number.")
                        line_edit.setStyleSheet("QlineEdit {color: red;} QlineEdit::placeholder {color: red;} QLineEdit {border: 1px solid red;}")
                        label.setText(f"{label.text().strip('* ')} *")
                except ValueError:
                    error_messages.append(f"{label.text()} must be a number.")
                    line_edit.setStyleSheet("QlineEdit {color: red;} QlineEdit::placeholder {color: red;} QLineEdit {border: 1px solid red;}")
                    label.setText(f"{label.text().strip('* ')} *")
        
        # Checks if the number of conductors in bundle is in the limit and its not empty
        if not self.number_of_conductors.hasAcceptableInput():
            error_messages.append("Invalid number of conductors in bundle.")
            self.label_number_of_conductors.setText(f"{self.label_number_of_conductors.text().strip('* ')} *")
            self.number_of_conductors.setStyleSheet("QlineEdit {color: red;} QlineEdit::placeholder {color: red;} QLineEdit {border: 1px solid red;}")
        
        # check the validity of the coordinates
        if not (self.x_coordinates_a.hasAcceptableInput() and self.y_coordinates_a.hasAcceptableInput()):
            error_messages.append("Invalid coordinates for Phase A.")
            self.label_xa.setText(f"{self.label_xa.text().strip('* ')} *")
            self.x_coordinates_a.setStyleSheet("QlineEdit {color: red;} QlineEdit::placeholder {color: red;} QLineEdit {border: 1px solid red;}")
            self.label_ya.setText(f"{self.label_ya.text().strip('* ')} *")
            self.y_coordinates_a.setStyleSheet("QlineEdit {color: red;} QlineEdit::placeholder {color: red;} QLineEdit {border: 1px solid red;}")
        if not (self.x_coordinates_b.hasAcceptableInput() and self.y_coordinates_b.hasAcceptableInput()):
            error_messages.append("Invalid coordinates for Phase B.")
            self.label_xb.setText(f"{self.label_xb.text().strip('* ')} *")
            self.x_coordinates_b.setStyleSheet("QlineEdit {color: red;} QlineEdit::placeholder {color: red;} QLineEdit {border: 1px solid red;}")
            self.label_yb.setText(f"{self.label_yb.text().strip('* ')} *")
            self.y_coordinates_b.setStyleSheet("QlineEdit {color: red;} QlineEdit::placeholder {color: red;} QLineEdit {border: 1px solid red;}")
        if not (self.x_coordinates_c.hasAcceptableInput() and self.y_coordinates_c.hasAcceptableInput()):
            error_messages.append("Invalid coordinates for Phase C.")
            self.label_xc.setText(f"{self.label_xc.text().strip('* ')} *")
            self.x_coordinates_c.setStyleSheet("QlineEdit {color: red;} QlineEdit::placeholder {color: red;} QLineEdit {border: 1px solid red;}")
            self.label_yc.setText(f"{self.label_yc.text().strip('* ')} *")
            self.y_coordinates_c.setStyleSheet("QlineEdit {color: red;} QlineEdit::placeholder {color: red;} QLineEdit {border: 1px solid red;}")
        if self.number_of_circuits.currentText() == "2" and not (self.x_coordinates_a_2.hasAcceptableInput() and self.y_coordinates_a_2.hasAcceptableInput()):
            error_messages.append("Invalid coordinates for Phase A in the second circuit.")
            self.label_xa.setText(f"{self.label_xa.text().strip('* ')} *")
            self.x_coordinates_a_2.setStyleSheet("QlineEdit {color: red;} QlineEdit::placeholder {color: red;} QLineEdit {border: 1px solid red;}")
            self.label_ya.setText(f"{self.label_ya.text().strip('* ')} *")
            self.y_coordinates_a_2.setStyleSheet("QlineEdit {color: red;} QlineEdit::placeholder {color: red;} QLineEdit {border: 1px solid red;}")
        if self.number_of_circuits.currentText() == "2" and not (self.x_coordinates_b_2.hasAcceptableInput() and self.y_coordinates_b_2.hasAcceptableInput()):
            error_messages.append("Invalid coordinates for Phase B in the second circuit.")
            self.label_xb.setText(f"{self.label_xb.text().strip('* ')} *")
            self.x_coordinates_b_2.setStyleSheet("QlineEdit {color: red;} QlineEdit::placeholder {color: red;} QLineEdit {border: 1px solid red;}")
            self.label_yb.setText(f"{self.label_yb.text().strip('* ')} *")
            self.y_coordinates_b_2.setStyleSheet("QlineEdit {color: red;} QlineEdit::placeholder {color: red;} QLineEdit {border: 1px solid red;}")
        if self.number_of_circuits.currentText() == "2" and not (self.x_coordinates_c_2.hasAcceptableInput() and self.y_coordinates_c_2.hasAcceptableInput()):
            error_messages.append("Invalid coordinates for Phase C in the second circuit.")
            self.label_xc.setText(f"{self.label_xc.text().strip('* ')} *")
            self.x_coordinates_c_2.setStyleSheet("QlineEdit {color: red;} QlineEdit::placeholder {color: red;} QLineEdit {border: 1px solid red;}")
            self.label_yc.setText(f"{self.label_yc.text().strip('* ')} *")
            self.y_coordinates_c_2.setStyleSheet("QlineEdit {color: red;} QlineEdit::placeholder {color: red;} QLineEdit {border: 1px solid red;}")
        
        # Show error messages if any
        if error_messages:
            QMessageBox.critical(self, "Invalid Input", "\n".join(error_messages))
            return False
        
        return True

    def get_conductor_parameters(self):     # Returns the conductor parameters based on the selected type
        if self.conductor_type.currentText() == "Hawk":
            diameter = 21.793 * 10**(-3)   # in m
            radius = diameter / 2          # in m
            r_GMR = 8.809 * 10**(-3)       # in m
            ac_resistance = 0.132          # in ohm/km 
            current_capacity = 659         # in A
            return radius, r_GMR, ac_resistance, current_capacity
        
        elif self.conductor_type.currentText() == "Drake":
            diameter = 28.143 * 10**(-3)   # in m
            radius = diameter / 2          # in m
            r_GMR = 11.369 * 10**(-3)      # in m
            ac_resistance = 0.080          # in ohm/km
            current_capacity = 907         # in A
            return radius, r_GMR, ac_resistance, current_capacity
        
        elif self.conductor_type.currentText() == "Cardinal":
            diameter = 30.378 * 10**(-3)   # in m
            radius = diameter / 2          # in m
            r_GMR = 12.253 * 10**(-3)      # in m
            ac_resistance = 0.067          # in ohm/km
            current_capacity = 996         # in A
            return radius, r_GMR, ac_resistance, current_capacity
        
        elif self.conductor_type.currentText() == "Rail":
            diameter = 29.591 * 10**(-3)   # in m
            radius = diameter / 2          # in m
            r_GMR = 11.765 * 10**(-3)      # in m
            ac_resistance = 0.068          # in ohm/km
            current_capacity = 993         # in A
            return radius, r_GMR, ac_resistance, current_capacity

        elif self.conductor_type.currentText() == "Pheasant":
            diameter = 35.103 * 10**(-3)   # in m
            radius = diameter / 2          # in m
            r_GMR = 14.204 * 10**(-3)      # in m
            ac_resistance = 0.051          # in ohm/km
            current_capacity = 1187        # in A
            return radius, r_GMR, ac_resistance, current_capacity

    def calculate_parameters(self):
        # Check if the inputs are valid
        if not self.validate_input():
            self.output_R.setText("N/A")
            self.output_L.setText("N/A")
            self.output_C.setText("N/A")
            self.output_capacity.setText("N/A")
            return

        # Set the input values for calculation
        conductor_radius, conductor_GMR, conductor_resistance, conductor_capacity = self.get_conductor_parameters()
        distance_between_conductors = float(self.distance_between_conductors.text()) / 100  # Convert cm to m
        line_length_km = float(self.line_length.text())
        number_of_conductors = int(self.number_of_conductors.text())
        x_coordinates_a = float(self.x_coordinates_a.text())
        y_coordinates_a = float(self.y_coordinates_a.text())
        x_coordinates_b = float(self.x_coordinates_b.text())
        y_coordinates_b = float(self.y_coordinates_b.text())
        x_coordinates_c = float(self.x_coordinates_c.text())
        y_coordinates_c = float(self.y_coordinates_c.text())

        if self.number_of_circuits.currentText() == "2":
            x_coordinates_a_2 = float(self.x_coordinates_a_2.text())
            y_coordinates_a_2 = float(self.y_coordinates_a_2.text())
            x_coordinates_b_2 = float(self.x_coordinates_b_2.text())
            y_coordinates_b_2 = float(self.y_coordinates_b_2.text())
            x_coordinates_c_2 = float(self.x_coordinates_c_2.text())
            y_coordinates_c_2 = float(self.y_coordinates_c_2.text())
        
        # Compute Bundle Geometric Mean Radius (GMR)
        if number_of_conductors == 4:
            bundle_GMR = (conductor_GMR * (distance_between_conductors ** 3) * math.sqrt(2)) ** (1/4)  # in m
            r_eq_bundle = (conductor_radius * (distance_between_conductors ** 3) * math.sqrt(2)) ** (1/4)  # in m
        else:
            bundle_GMR = (conductor_GMR * (distance_between_conductors ** (number_of_conductors - 1))) ** (1/number_of_conductors)  # in m
            r_eq_bundle = (conductor_radius * (distance_between_conductors ** (number_of_conductors - 1))) ** (1/number_of_conductors) # in m

        # Compute distances between phases and GMD values
        if self.tower_type.currentText() == "Type-1: Narrow Base Tower" or self.tower_type.currentText() == "Type-2: Single Circuit Delta Tower":
            Dab = math.sqrt((y_coordinates_b - y_coordinates_a)**2 + (x_coordinates_b + (-x_coordinates_a))**2)
            Dbc = math.sqrt((y_coordinates_c - y_coordinates_b)**2 + (x_coordinates_c - x_coordinates_b)**2)
            Dca = math.sqrt((y_coordinates_a - y_coordinates_c)**2 + ((-x_coordinates_a) + x_coordinates_c)**2)
            gmd = (Dab * Dbc * Dca) ** (1 / 3)
        else:
            if self.number_of_circuits.currentText() == "1":
                Dab = math.sqrt((y_coordinates_a - y_coordinates_b)**2 + (x_coordinates_b - x_coordinates_a)**2)
                Dbc = math.sqrt((y_coordinates_b - y_coordinates_c)**2 + (x_coordinates_c - x_coordinates_b)**2)
                Dca = math.sqrt((y_coordinates_a - y_coordinates_c)**2 + (x_coordinates_a - x_coordinates_c)**2)
                gmd = (Dab * Dbc * Dca) ** (1 / 3)
            else: # For double circuit
                #self gmr of phase a,b,c to find new equivalent gmr
                Dsa = math.sqrt(bundle_GMR * (math.sqrt((y_coordinates_a - y_coordinates_a_2)**2 + (x_coordinates_a - x_coordinates_a_2)**2)))
                Dsb = math.sqrt(bundle_GMR * (math.sqrt((y_coordinates_b - y_coordinates_b_2)**2 + (x_coordinates_b - x_coordinates_b_2)**2)))
                Dsc = math.sqrt(bundle_GMR * (math.sqrt((y_coordinates_c - y_coordinates_c_2)**2 + (x_coordinates_c - x_coordinates_c_2)**2)))
                bundle_GMR = (Dsa * Dsb * Dsc) ** (1/3)
                Dsa_r = math.sqrt(r_eq_bundle * (math.sqrt((y_coordinates_a - y_coordinates_a_2)**2 + (x_coordinates_a - x_coordinates_a_2)**2)))
                Dsb_r = math.sqrt(r_eq_bundle * (math.sqrt((y_coordinates_b - y_coordinates_b_2)**2 + (x_coordinates_b - x_coordinates_b_2)**2)))
                Dsc_r = math.sqrt(r_eq_bundle * (math.sqrt((y_coordinates_c - y_coordinates_c_2)**2 + (x_coordinates_c - x_coordinates_c_2)**2)))
                r_eq_bundle = (Dsa_r * Dsb_r * Dsc_r) ** (1/3)

                #mutual GMDs of ab, bc, ca to find GMD    (ab distance * ab' distance)^1/2 etc
                Dab = math.sqrt(math.sqrt((y_coordinates_a - y_coordinates_b)**2 + (x_coordinates_b - x_coordinates_a)**2) * math.sqrt((y_coordinates_a - y_coordinates_b_2)**2 + (x_coordinates_a - x_coordinates_b_2)**2))
                Dbc = math.sqrt(math.sqrt((y_coordinates_b - y_coordinates_c)**2 + (x_coordinates_c - x_coordinates_b)**2) * math.sqrt((y_coordinates_b - y_coordinates_c_2)**2 + (x_coordinates_b - x_coordinates_c_2)**2))
                Dca = math.sqrt(math.sqrt((y_coordinates_a - y_coordinates_c)**2 + (x_coordinates_c - x_coordinates_a)**2) * math.sqrt((y_coordinates_a - y_coordinates_c_2)**2 + (x_coordinates_a - x_coordinates_c_2)**2))
                gmd = (Dab * Dbc * Dca) ** (1 / 3)

        # Calculate parameters
        R = conductor_resistance / number_of_conductors  # Resistance in ohms per km
        L = (2e-7) * math.log(gmd / bundle_GMR) * 1e3  # Inductance in mH per meter
        C = (2 * math.pi * 8.854e-12) / math.log(gmd / bundle_GMR) * 1e6  # Capacitance in µF per meter

        # Calculate total parameters for the line length
        total_R = R * line_length_km
        total_L = L * line_length_km *1000 # since L is per meter and line length is in km
        total_C = C * line_length_km *1000 # since C is per meter and line length is in km

        # Calculate the capacity of the line       
        if self.tower_type.currentText() == "Type-1: Narrow Base Tower":
            output_capacity = math.sqrt(3) * conductor_capacity * number_of_conductors * 66000 / 1000000 # in MVA
        elif self.tower_type.currentText() == "Type-2: Single Circuit Delta Tower":
            output_capacity = math.sqrt(3) * conductor_capacity * number_of_conductors * 400000 / 1000000 # in MVA
        elif self.tower_type.currentText() == "Type-3: Double Circuit Vertical Tower" and self.number_of_circuits.currentText() == "1":
            output_capacity = math.sqrt(3) * conductor_capacity * number_of_conductors * 154000 / 1000000 # in MVA
        else:
            output_capacity = math.sqrt(3) * conductor_capacity * number_of_conductors * 2 * 154000 / 1000000 # in MVA for double circuit (*2) since there are 2 parallel circuits

        # Display the results
        self.output_R.setText(f"{total_R:.5f}")
        self.output_L.setText(f"{total_L:.5f}")
        self.output_C.setText(f"{total_C:.5f}")
        self.output_capacity.setText(f"{output_capacity:.3f}")

if __name__ == "__main__":
    app = QApplication([])

    #set dark mode
    set_dark_theme(app)

    window = TransmissionLineGUI()
    window.show()
    app.exec()
