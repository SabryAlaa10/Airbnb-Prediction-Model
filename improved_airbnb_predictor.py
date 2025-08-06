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
        self._animation.setDuration(250)
        self._animation.setEasingCurve(QEasingCurve.InOutCubic)
        
    def enterEvent(self, event):
        self._animation.setStartValue(QColor("#6366f1"))
        self._animation.setEndValue(QColor("#8b5cf6"))
        self._animation.start()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self._animation.setStartValue(QColor("#8b5cf6"))
        self._animation.setEndValue(QColor("#6366f1"))
        self._animation.start()
        super().leaveEvent(event)


class PricePredictorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🏠 Airbnb Price Prediction - AI Powered")
        self.resize(550, 750)
        self.setMinimumSize(550, 750)

        # تحميل النموذج
        try:
            import warnings
            warnings.filterwarnings("ignore", category=UserWarning)
            # جرب مسارات مختلفة للنموذج
            possible_paths = [
                r"C:\NTN\PY\AI\End_To_End project\Classification\Decision Tree Airbnb\model.pkl",
                "model.pkl",
                "./model.pkl"
            ]
            
            self.model = None
            for path in possible_paths:
                try:
                    self.model = joblib.load(path)
                    print(f"Model loaded successfully from: {path}")
                    break
                except:
                    continue
                    
            if self.model is None:
                raise FileNotFoundError("Could not find model.pkl in any of the expected locations")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load model.pkl:\n{e}\n\nPlease ensure model.pkl is in the same directory as this script.")
            sys.exit(1)

        # قاموس تحويل القيم الأصلية إلى رقمية
        self.encodings = {
            'host_identity_verified': {'No': 0, 'Yes': 1},
            'instant_bookable': {'No': 0, 'Yes': 1},
            'cancellation_policy': {
                'strict': 0, 
                'moderate': 1, 
                'flexible': 2
            },
            'room type': {
                'Private room': 0,
                'Entire home/apt': 1,
                'Shared room': 2,
                'Hotel room': 3
            }
        }

        # تطبيق التصميم المحسن بألوان عصرية
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0f172a, stop:0.3 #1e293b, stop:0.7 #334155, stop:1 #475569);
                font-family: 'Inter', 'Segoe UI', 'SF Pro Display', sans-serif;
                color: #f8fafc;
            }
            
            QLabel {
                font-size: 14px;
                color: #e2e8f0;
                font-weight: 600;
                padding: 8px 5px;
                letter-spacing: 0.5px;
            }
            
            QLineEdit, QComboBox {
                background: rgba(15, 23, 42, 0.8);
                border: 2px solid rgba(100, 116, 139, 0.3);
                border-radius: 12px;
                padding: 16px 20px;
                font-size: 14px;
                color: #f8fafc;
                font-weight: 500;
                backdrop-filter: blur(20px);
            }

            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #6366f1;
                background: rgba(15, 23, 42, 0.95);
                outline: none;
            }

            QLineEdit:hover, QComboBox:hover {
                border-color: rgba(139, 92, 246, 0.5);
                background: rgba(15, 23, 42, 0.9);
            }

            QLineEdit::placeholder {
                color: rgba(148, 163, 184, 0.8);
                font-style: italic;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 35px;
                background: transparent;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 8px solid #8b5cf6;
                margin-right: 10px;
            }
            
            QComboBox QAbstractItemView {
                background: rgba(15, 23, 42, 0.95);
                border: 2px solid #6366f1;
                border-radius: 12px;
                color: #f8fafc;
                selection-background-color: #6366f1;
                selection-color: #ffffff;
                padding: 8px;
                backdrop-filter: blur(20px);
            }
            
            QComboBox QAbstractItemView::item {
                padding: 12px 16px;
                border-radius: 8px;
                margin: 2px;
            }
            
            QComboBox QAbstractItemView::item:hover {
                background: rgba(99, 102, 241, 0.3);
            }
            
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6366f1, stop:0.5 #8b5cf6, stop:1 #a855f7);
                color: #ffffff;
                border: none;
                border-radius: 16px;
                padding: 18px 40px;
                font-weight: 700;
                font-size: 16px;
                text-transform: uppercase;
                letter-spacing: 1.2px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4f46e5, stop:0.5 #7c3aed, stop:1 #9333ea);
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4338ca, stop:0.5 #6d28d9, stop:1 #7e22ce);
            }
            
            QScrollArea {
                border: none;
                background: transparent;
            }
            
            QScrollArea QScrollBar:vertical {
                background: rgba(51, 65, 85, 0.3);
                width: 8px;
                border-radius: 4px;
            }
            
            QScrollArea QScrollBar::handle:vertical {
                background: rgba(99, 102, 241, 0.6);
                border-radius: 4px;
                min-height: 20px;
            }
            
            QScrollArea QScrollBar::handle:vertical:hover {
                background: rgba(99, 102, 241, 0.8);
            }
            
            QFrame#titleFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(99, 102, 241, 0.1), 
                    stop:0.5 rgba(139, 92, 246, 0.1), 
                    stop:1 rgba(168, 85, 247, 0.1));
                border: 2px solid rgba(99, 102, 241, 0.2);
                border-radius: 20px;
                padding: 25px;
                margin: 15px 5px;
                backdrop-filter: blur(20px);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            }
            
            QFrame#formFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(30, 41, 59, 0.4), 
                    stop:1 rgba(51, 65, 85, 0.4));
                border: 2px solid rgba(71, 85, 105, 0.3);
                border-radius: 20px;
                padding: 30px;
                margin: 10px 5px;
                backdrop-filter: blur(20px);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
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
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(25, 25, 25, 25)

        # إطار العنوان المحسن
        title_frame = QFrame()
        title_frame.setObjectName("titleFrame")
        title_layout = QVBoxLayout(title_frame)
        
        # العنوان الرئيسي
        title = QLabel("🏠 AIRBNB PRICE PREDICTOR")
        title.setFont(QFont('Inter', 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #6366f1, stop:0.5 #8b5cf6, stop:1 #a855f7);
            margin: 15px;
        """)

        subtitle = QLabel("✨ AI-Powered Property Valuation System ✨")
        subtitle.setFont(QFont('Inter', 14, QFont.DemiBold))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            color: #e2e8f0; 
            margin-bottom: 15px; 
            font-style: italic;
            letter-spacing: 1px;
        """)

        description = QLabel("Enter your property details below and get an instant AI-powered price prediction")
        description.setFont(QFont('Inter', 12))
        description.setAlignment(Qt.AlignCenter)
        description.setStyleSheet("""
            color: rgba(226, 232, 240, 0.8);
            line-height: 1.5;
        """)

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        title_layout.addWidget(description)

        # نموذج الإدخال المحسن
        form_frame = QFrame()
        form_frame.setObjectName("formFrame")
        
        form_layout = QFormLayout(form_frame)
        form_layout.setLabelAlignment(Qt.AlignLeft)
        form_layout.setVerticalSpacing(20)
        form_layout.setHorizontalSpacing(25)

        self.inputs = {}
        
        # تعريف الحقول مع أيقونات محسنة
        fields = [
            ('🎖️ Host Identity Verified', 'combo', 'host_identity_verified', ['No', 'Yes']),
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
            label.setFont(QFont('Inter', 13, QFont.DemiBold))
            
            if field_type == 'combo':
                widget = QComboBox()
                widget.addItems(options)
                widget.setFixedHeight(55)
                self.inputs[key] = (widget, 'combo')
            else:
                widget = QLineEdit()
                widget.setPlaceholderText(f"Enter {label_text.split(' ', 1)[1].lower()}...")
                widget.setFixedHeight(55)
                if 'year' in key.lower():
                    self.inputs[key] = (widget, int)
                elif 'fee' in key.lower() or 'rate' in key.lower():
                    self.inputs[key] = (widget, float)
                else:
                    self.inputs[key] = (widget, int)
            
            form_layout.addRow(label, widget)

        # زر التنبؤ المحسن
        self.predict_button = QPushButton("🔮 PREDICT PRICE NOW")
        self.predict_button.clicked.connect(self.predict_price)
        self.predict_button.setFixedHeight(65)
        self.predict_button.setFont(QFont('Inter', 16, QFont.Bold))

        # التجميع النهائي
        main_layout.addWidget(title_frame)
        main_layout.addWidget(form_frame)
        main_layout.addSpacing(15)
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
            msg.setText(f"💰 Predicted Nightly Price: ${prediction:.2f}")
            msg.setInformativeText(f"Based on your property details,\nour advanced AI model estimates this competitive rate.")
            
            # تخصيص تصميم MessageBox
            msg.setStyleSheet("""
                QMessageBox {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #0f172a, stop:1 #1e293b);
                    color: #f8fafc;
                    border-radius: 15px;
                }
                QMessageBox QLabel {
                    color: #e2e8f0;
                    font-size: 14px;
                    padding: 10px;
                }
                QMessageBox QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #10b981, stop:1 #059669);
                    color: white;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-weight: bold;
                    min-width: 80px;
                }
                QMessageBox QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #059669, stop:1 #047857);
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
                    stop:0 #0f172a, stop:1 #1e293b);
                color: #f8fafc;
                border-radius: 15px;
            }
            QMessageBox QLabel {
                color: #fbbf24;
                font-size: 14px;
                padding: 10px;
            }
            QMessageBox QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ef4444, stop:1 #dc2626);
                color: white;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #dc2626, stop:1 #b91c1c);
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