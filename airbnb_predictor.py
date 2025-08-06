import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QFormLayout, QMessageBox, QVBoxLayout, QHBoxLayout, QFrame,
    QComboBox, QScrollArea
)
from PyQt5.QtGui import QFont, QPalette, QColor, QPixmap, QPainter, QBrush
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
import pandas as pd
import joblib


class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._animation = QPropertyAnimation(self, b"color")
        self._animation.setDuration(200)
        self._animation.setEasingCurve(QEasingCurve.InOutQuad)
        
    def enterEvent(self, event):
        self._animation.setStartValue(QColor("#00d4ff"))
        self._animation.setEndValue(QColor("#ffffff"))
        self._animation.start()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self._animation.setStartValue(QColor("#ffffff"))
        self._animation.setEndValue(QColor("#00d4ff"))
        self._animation.start()
        super().leaveEvent(event)


class PricePredictorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🏠 Airbnb Price Prediction - AI Powered")
        self.resize(500, 700)
        self.setMinimumSize(500, 700)

        # تحميل النموذج
        try:
            self.model = joblib.load(r"C:\NTN\PY\AI\End_To_End project\Classification\Decision Tree Airbnb\model.pkl")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load model.pkl:\n{e}")
            sys.exit(1)

        # قاموس تحويل القيم الأصلية إلى رقمية
        self.encodings = {
            'host_identity_verified': {'No': 0, 'Yes': 1},
            'instant_bookable': {'No': 0, 'Yes': 1},
            'cancellation_policy': {
                'strict': 0, 
                'moderate': 1, 
                'flexible': 2, 
                'super_strict_30': 3,
                'super_strict_60': 4
            },
            'room type': {
                'Private room': 0,
                'Entire home/apt': 1,
                'Shared room': 2,
                'Hotel room': 3
            }
        }

        # تطبيق التصميم الداكن المحسن
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a2e, stop:0.5 #16213e, stop:1 #0f3460);
                font-family: 'Segoe UI', 'Roboto', sans-serif;
                color: #ffffff;
            }
            
            QLabel {
                font-size: 13px;
                color: #e8e8e8;
                font-weight: 500;
                padding: 5px;
            }
            
            QLineEdit, QComboBox {
            background: rgba(20, 25, 40, 0.9);
            border: 2px solid rgba(0, 212, 255, 0.3);
            border-radius: 8px;
            padding: 12px 15px;
            font-size: 13px;
            color: #000000;
            backdrop-filter: blur(10px);
            }

            QLineEdit:focus, QComboBox:focus {
            border: 2px solid #00d4ff;
            background: rgba(30, 35, 50, 0.95);
            outline: none;
            }

            QLineEdit::placeholder {
            color: rgba(200, 200, 200, 0.7);
            }
            
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #00d4ff;
            }
            
            QComboBox QAbstractItemView {
                background: #2a2a3e;
                border: 1px solid #00d4ff;
                border-radius: 5px;
                color: #ffffff;
                selection-background-color: #00d4ff;
            }
            
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d4ff, stop:1 #0099cc);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 15px 30px;
                font-weight: bold;
                font-size: 16px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00b8e6, stop:1 #0086b3);
                transform: translateY(-2px);
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0099cc, stop:1 #007399);
            }
            
            QScrollArea {
                border: none;
                background: transparent;
            }
            
            QFrame#titleFrame {
                background: rgba(0, 212, 255, 0.1);
                border-radius: 15px;
                padding: 20px;
                margin: 10px;
            }
        """)

        self.setup_ui()

    def setup_ui(self):
        # إعداد منطقة التمرير
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # الحاوية الرئيسية
        main_widget = QWidget()
        scroll_area.setWidget(main_widget)
        
        # التخطيط الرئيسي
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # إطار العنوان
        title_frame = QFrame()
        title_frame.setObjectName("titleFrame")
        title_layout = QVBoxLayout(title_frame)
        
        # العنوان الرئيسي
        title = QLabel("🏠 AIRBNB PRICE PREDICTOR")
        title.setFont(QFont('Segoe UI', 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #00d4ff; margin: 10px;")

        subtitle = QLabel("✨ AI-Powered Property Valuation ✨")
        subtitle.setFont(QFont('Segoe UI', 12))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #ffffff; margin-bottom: 10px; font-style: italic;")

        description = QLabel("Enter your property details below and get an instant price prediction")
        description.setFont(QFont('Segoe UI', 10))
        description.setAlignment(Qt.AlignCenter)
        description.setStyleSheet("color: rgba(255, 255, 255, 0.8);")

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        title_layout.addWidget(description)

        # نموذج الإدخال
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 15px;
                padding: 20px;
            }
        """)
        
        form_layout = QFormLayout(form_frame)
        form_layout.setLabelAlignment(Qt.AlignLeft)
        form_layout.setVerticalSpacing(15)
        form_layout.setHorizontalSpacing(20)

        self.inputs = {}
        
        # تعريف الحقول مع أنواعها
        fields = [
            ('🏆 Host Identity Verified', 'combo', 'host_identity_verified', ['No', 'Yes']),
            ('⚡ Instant Bookable', 'combo', 'instant_bookable', ['No', 'Yes']),
            ('📋 Cancellation Policy', 'combo', 'cancellation_policy', 
             ['flexible', 'moderate', 'strict', 'super_strict_30', 'super_strict_60']),
            ('🏠 Room Type', 'combo', 'room type', 
             ['Private room', 'Entire home/apt', 'Shared room', 'Hotel room']),
            ('🏗️ Construction Year', 'input', 'Construction year', None),
            ('💰 Service Fee ($)', 'input', 'service fee', None),
            ('🌙 Minimum Nights', 'input', 'minimum nights', None),
            ('⭐ Number of Reviews', 'input', 'number of reviews', None),
            ('📊 Review Rate (1-5)', 'input', 'review rate number', None),
            ('📈 Host Listings Count', 'input', 'calculated host listings count', None),
            ('📅 Availability (days/year)', 'input', 'availability 365', None),
        ]

        for label_text, field_type, key, options in fields:
            label = QLabel(label_text)
            label.setFont(QFont('Segoe UI', 12, QFont.Medium))
            
            if field_type == 'combo':
                widget = QComboBox()
                widget.addItems(options)
                widget.setFixedHeight(45)
                self.inputs[key] = (widget, 'combo')
            else:
                widget = QLineEdit()
                widget.setPlaceholderText(f"Enter {label_text.split(' ', 1)[1].lower()}")
                widget.setFixedHeight(45)
                if 'year' in key.lower():
                    self.inputs[key] = (widget, int)
                elif 'fee' in key.lower() or 'rate' in key.lower():
                    self.inputs[key] = (widget, float)
                else:
                    self.inputs[key] = (widget, int)
            
            form_layout.addRow(label, widget)

        # زر التنبؤ المحسن
        self.predict_button = QPushButton("🔮 PREDICT PRICE")
        self.predict_button.clicked.connect(self.predict_price)
        self.predict_button.setFixedHeight(60)
        self.predict_button.setFont(QFont('Segoe UI', 14, QFont.Bold))

        # التجميع النهائي
        main_layout.addWidget(title_frame)
        main_layout.addWidget(form_frame)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.predict_button, alignment=Qt.AlignCenter)
        main_layout.addStretch()

        # التخطيط النهائي للنافذة
        window_layout = QVBoxLayout(self)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.addWidget(scroll_area)

    def predict_price(self):
        try:
            data = {}
            
            for key, (widget, dtype) in self.inputs.items():
                if dtype == 'combo':
                    # تحويل القيمة المختارة إلى رقم
                    selected_value = widget.currentText()
                    if key in self.encodings:
                        data[key] = self.encodings[key][selected_value]
                    else:
                        data[key] = selected_value
                else:
                    # إدخال نصي
                    text = widget.text().strip()
                    if text == '':
                        # عرض اسم الحقل بطريقة أوضح
                        field_name = key.replace('_', ' ').title()
                        raise ValueError(f"Please enter a value for '{field_name}'")
                    data[key] = dtype(text)

            # إنشاء DataFrame وتنفيذ التنبؤ
            df = pd.DataFrame([data])
            prediction = self.model.predict(df)[0]

            # عرض النتيجة بتصميم محسن
            msg = QMessageBox(self)
            msg.setWindowTitle("🎉 Prediction Result")
            msg.setIcon(QMessageBox.Information)
            msg.setText(f"💰 Predicted Price: ${prediction:.2f}")
            msg.setInformativeText(f"Based on the property details you provided,\nour AI model estimates the nightly rate.")
            
            # تخصيص تصميم MessageBox
            msg.setStyleSheet("""
                QMessageBox {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #1a1a2e, stop:1 #0f3460);
                    color: #ffffff;
                }
                QMessageBox QPushButton {
                    background: #00d4ff;
                    color: white;
                    border-radius: 5px;
                    padding: 8px 16px;
                    font-weight: bold;
                }
            """)
            
            msg.exec_()

        except ValueError as e:
            self.show_error("Input Error", str(e))
        except Exception as e:
            self.show_error("Prediction Error", f"An error occurred during prediction:\n{str(e)}")

    def show_error(self, title, message):
        msg = QMessageBox(self)
        msg.setWindowTitle(f"⚠️ {title}")
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a2e, stop:1 #0f3460);
                color: #ffffff;
            }
            QMessageBox QPushButton {
                background: #ff4444;
                color: white;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
        """)
        msg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # تطبيق تصميم عام للتطبيق
    app.setStyle('Fusion')
    
    window = PricePredictorApp()
    window.show()
    
    sys.exit(app.exec_())