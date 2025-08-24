"""
🚀 AI Gold Grid Trading - Modern Rule-based Edition
main.py
เก็บ GUI style เดิม + เพิ่ม Modern Rule-based Architecture
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import threading
import time
from datetime import datetime
import os

# Import modules - Modern Rule-based Architecture
try:
    from mt5_connector import MT5Connector
    from rule_engine import ModernRuleEngine
    from market_analyzer import MarketAnalyzer
    from order_manager import OrderManager
    from position_manager import PositionManager
    from spacing_manager import SpacingManager
    from lot_calculator import LotCalculator
    from performance_tracker import PerformanceTracker
    from api_connector import BackendAPIConnector
except ImportError as e:
    print(f"Import error: {e}")

class ModernAITradingGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.init_variables()
        self.load_config()
        self.create_gui()
        
    def setup_window(self):
        """Setup main window - เก็บ style เดิม"""
        self.root.title("🚀 AI Gold Grid Trading - Modern Rule-based")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a1a2e')
        
        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def init_variables(self):
        """Initialize variables - Modern Architecture"""
        # Connection states
        self.is_connected = False
        self.is_trading = False
        self.account_info = {}
        
        # Modern Rule-based Components
        self.mt5_connector = MT5Connector()    

        self.rule_engine = None
        self.market_analyzer = None
        self.order_manager = None
        self.position_manager = None
        self.spacing_manager = None
        self.lot_calculator = None
        self.performance_tracker = None
        self.api_connector = None
        
        # Trading state
        self.trading_params = {}
        self.system_status = {
            'rule_confidence': 0.0,
            'market_condition': 'UNKNOWN',
            'portfolio_health': 0.0,
            'total_profit': 0.0,
            'active_positions': 0,
            'pending_orders': 0,
            'risk_level': 0.0,
            'last_action': 'NONE',
            'action_reason': '',
            'survivability_usage': 0.0
        }
        
        # GUI Colors - เก็บ scheme เดิม
        self.bg_color = '#1a1a2e'
        self.card_color = '#16213E'
        self.accent_color = '#00D4FF'
        self.success_color = '#00FF88'
        self.error_color = '#FF3366'
        self.warning_color = '#FFB800'
        self.text_color = '#FFFFFF'
        
    def load_config(self):
        """Load configuration files"""
        try:
            # Load main config
            with open('config.json', 'r', encoding='utf-8') as f:
                self.config = json.load(f)
                
            # Load rules config  
            with open('rules_config.json', 'r', encoding='utf-8') as f:
                self.rules_config = json.load(f)
                
            self.log("✅ Configuration loaded successfully")
            
        except Exception as e:
            self.log(f"⚠️ Config load error: {e}")
            # Use default config
            self.config = self.get_default_config()
            self.rules_config = self.get_default_rules_config()
            
    def get_default_config(self):
        """Default configuration"""
        return {
            "trading": {
                "symbol": "XAUUSD",
                "base_lot_size": 0.01,
                "max_positions": 20,
                "max_risk_percentage": 5.0,
                "min_spacing_points": 80,
                "max_spacing_points": 300,
                "emergency_stop_loss": 15000
            },
            "api": {
                "backend_url": "http://123.253.62.50:8080/api",
                "timeout": 10,
                "check_interval": 30
            },
            "risk_management": {
                "max_drawdown_percentage": 20.0,
                "margin_usage_limit": 70.0,
                "balance_protection_threshold": 1000
            }
        }
        
    def get_default_rules_config(self):
        """Default rules configuration"""
        return {
            "rules": {
                "trend_following": {
                    "weight": 0.3,
                    "confidence_threshold": 0.6,
                    "parameters": {
                        "rsi_period": 14,
                        "rsi_oversold": 30,
                        "rsi_overbought": 70,
                        "trend_strength_threshold": 0.5
                    }
                },
                "mean_reversion": {
                    "weight": 0.25,
                    "confidence_threshold": 0.7,
                    "parameters": {
                        "bollinger_period": 20,
                        "bollinger_deviation": 2,
                        "reversal_confirmation_bars": 3
                    }
                },
                "support_resistance": {
                    "weight": 0.2,
                    "confidence_threshold": 0.6,
                    "parameters": {
                        "lookback_periods": 100,
                        "touch_tolerance": 5,
                        "strength_threshold": 3
                    }
                },
                "volatility_breakout": {
                    "weight": 0.15,
                    "confidence_threshold": 0.8,
                    "parameters": {
                        "atr_period": 14,
                        "volatility_threshold": 1.5,
                        "breakout_confirmation": 2
                    }
                },
                "portfolio_balance": {
                    "weight": 0.1,
                    "confidence_threshold": 0.5,
                    "parameters": {
                        "max_exposure_ratio": 0.7,
                        "position_correlation_limit": 0.8
                    }
                }
            },
            "adaptive_settings": {
                "learning_rate": 0.1,
                "performance_window": 50,
                "weight_adjustment_threshold": 0.1,
                "confidence_adjustment_rate": 0.05
            }
        }
        
    def create_gui(self):
        """Create GUI - เก็บ layout เดิม + เพิ่ม Modern features"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_frame)
        
        # Content
        content_frame = tk.Frame(main_frame, bg=self.bg_color)
        content_frame.pack(fill='both', expand=True, pady=20)
        
        # Three column layout - Modern
        left_frame = tk.Frame(content_frame, bg=self.card_color, relief='solid', borderwidth=1)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        middle_frame = tk.Frame(content_frame, bg=self.card_color, relief='solid', borderwidth=1)
        middle_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        right_frame = tk.Frame(content_frame, bg=self.card_color, relief='solid', borderwidth=1)
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Create panels
        self.create_controls(left_frame)
        self.create_rules_monitor(middle_frame)
        self.create_system_monitor(right_frame)
        
    def create_header(self, parent):
        """Create header - เก็บ style เดิม + เพิ่มข้อมูล"""
        header = tk.Frame(parent, bg='#16213E', height=100, relief='solid', borderwidth=1)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Left side - Title
        left_header = tk.Frame(header, bg='#16213E')
        left_header.pack(side='left', fill='both', expand=True, padx=20, pady=15)
        
        title = tk.Label(left_header, text="🚀 AI Gold Grid Trading",
                        bg='#16213E', fg=self.accent_color,
                        font=('Arial', 18, 'bold'))
        title.pack(anchor='w')
        
        subtitle = tk.Label(left_header, text="Modern Rule-based Architecture",
                          bg='#16213E', fg='#888888',
                          font=('Arial', 10))
        subtitle.pack(anchor='w')
        
        # Center - Rule Status
        center_header = tk.Frame(header, bg='#16213E')
        center_header.pack(side='left', fill='y', padx=20, pady=15)
        
        tk.Label(center_header, text="🧠 Rule Engine:",
                bg='#16213E', fg=self.text_color,
                font=('Arial', 10, 'bold')).pack()
        
        self.rule_status_label = tk.Label(center_header, text="● Initializing",
                                        bg='#16213E', fg=self.warning_color,
                                        font=('Arial', 10))
        self.rule_status_label.pack()
        
        # Right side - Connection Status
        right_header = tk.Frame(header, bg='#16213E')
        right_header.pack(side='right', padx=20, pady=15)
        
        tk.Label(right_header, text="📡 Connection:",
                bg='#16213E', fg=self.text_color,
                font=('Arial', 10, 'bold')).pack()
        
        self.status_label = tk.Label(right_header, text="● Disconnected",
                                   bg='#16213E', fg=self.error_color,
                                   font=('Arial', 12, 'bold'))
        self.status_label.pack()
        
    def create_controls(self, parent):
        """Create control panel - เก็บ style เดิม + เพิ่ม MT5 Selection"""
        # Title
        title = tk.Label(parent, text="🎛️ Trading Controls",
                        bg=self.card_color, fg=self.text_color,
                        font=('Arial', 14, 'bold'))
        title.pack(pady=20)
        
        # Connection section
        conn_frame = tk.Frame(parent, bg=self.card_color)
        conn_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(conn_frame, text="📡 Connection:",
                bg=self.card_color, fg=self.text_color,
                font=('Arial', 11, 'bold')).pack(anchor='w')
        
        # === MT5 Selection (ใหม่!) ===
        mt5_select_frame = tk.Frame(conn_frame, bg=self.card_color)
        mt5_select_frame.pack(fill='x', pady=(5, 0))
        
        # Label สำหรับ MT5 Selection
        tk.Label(mt5_select_frame, text="🖥️ Select Running MT5:",
                bg=self.card_color, fg=self.text_color,
                font=('Arial', 10)).pack(anchor='w')
        
        # Dropdown สำหรับเลือก MT5
        self.mt5_var = tk.StringVar(value="Scan for MT5...")
        self.mt5_dropdown = ttk.Combobox(mt5_select_frame, 
                                        textvariable=self.mt5_var,
                                        state='readonly',
                                        font=('Arial', 9),
                                        width=50)
        self.mt5_dropdown.pack(fill='x', pady=(2, 5))
        
        # Bind event เมื่อเลือก MT5
        self.mt5_dropdown.bind('<<ComboboxSelected>>', self.on_mt5_selected)
        
        # Button สำหรับ Scan MT5
        scan_frame = tk.Frame(mt5_select_frame, bg=self.card_color)
        scan_frame.pack(fill='x', pady=(0, 5))
        
        self.scan_btn = tk.Button(scan_frame, text="🔍 Scan Running MT5",
                                 command=self.scan_mt5_installations,
                                 bg='#4A90E2', fg='white',
                                 font=('Arial', 9, 'bold'),
                                 relief='flat', padx=15, pady=5)
        self.scan_btn.pack(side='left')
        
        # Status label สำหรับแสดงผล scan
        self.scan_status_label = tk.Label(scan_frame, text="",
                                         bg=self.card_color, fg='#888888',
                                         font=('Arial', 8))
        self.scan_status_label.pack(side='left', padx=(10, 0))
        
        # === Connect Button (ปรับปรุง) ===
        self.connect_btn = tk.Button(conn_frame, text="🔌 Connect to Selected MT5",
                                   command=self.connect_mt5,
                                   bg=self.accent_color, fg='black',
                                   font=('Arial', 10, 'bold'),
                                   relief='flat', padx=20, pady=10,
                                   state='disabled')  # Disabled จนกว่าจะเลือก MT5
        self.connect_btn.pack(fill='x', pady=(5, 0))
        
        # Account info
        self.account_label = tk.Label(conn_frame, text="No account connected",
                                    bg=self.card_color, fg='#888888',
                                    font=('Arial', 9))
        self.account_label.pack(anchor='w', pady=(5, 0))
        
        # Trading mode section
        mode_frame = tk.Frame(parent, bg=self.card_color)
        mode_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(mode_frame, text="🎯 Trading Mode:",
                bg=self.card_color, fg=self.text_color,
                font=('Arial', 11, 'bold')).pack(anchor='w')
        
        self.mode_var = tk.StringVar(value="BALANCED")
        
        modes = [
            ("🛡️ CONSERVATIVE", "CONSERVATIVE"), 
            ("⚖️ BALANCED", "BALANCED"), 
            ("🚀 AGGRESSIVE", "AGGRESSIVE"),
            ("🧪 ADAPTIVE", "ADAPTIVE")
        ]
        
        for text, value in modes:
            rb = tk.Radiobutton(mode_frame, text=text, variable=self.mode_var, value=value,
                              bg=self.card_color, fg=self.text_color,
                              selectcolor=self.bg_color,
                              font=('Arial', 10))
            rb.pack(anchor='w', pady=2)
        
        # Rule Engine section
        rule_frame = tk.Frame(parent, bg=self.card_color)
        rule_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(rule_frame, text="🧠 Rule Engine:",
                bg=self.card_color, fg=self.text_color,
                font=('Arial', 11, 'bold')).pack(anchor='w')
        
        self.init_rules_btn = tk.Button(rule_frame, text="🔧 Initialize Rules",
                                      command=self.initialize_rules,
                                      bg=self.warning_color, fg='black',
                                      font=('Arial', 10, 'bold'),
                                      relief='flat', padx=20, pady=10,
                                      state='disabled')
        self.init_rules_btn.pack(fill='x', pady=2)
        
        # Control buttons
        btn_frame = tk.Frame(parent, bg=self.card_color)
        btn_frame.pack(fill='x', padx=20, pady=20)
        
        self.calc_btn = tk.Button(btn_frame, text="🧮 Calculate Parameters",
                                command=self.calculate_params,
                                bg=self.warning_color, fg='black',
                                font=('Arial', 10, 'bold'),
                                relief='flat', padx=20, pady=10,
                                state='disabled')
        self.calc_btn.pack(fill='x', pady=2)
        
        self.start_btn = tk.Button(btn_frame, text="🚀 Start AI Trading",
                                 command=self.start_trading,
                                 bg=self.success_color, fg='black',
                                 font=('Arial', 11, 'bold'),
                                 relief='flat', padx=20, pady=15,
                                 state='disabled')
        self.start_btn.pack(fill='x', pady=5)
        
        self.stop_btn = tk.Button(btn_frame, text="⏹️ Stop Trading",
                                command=self.stop_trading,
                                bg=self.error_color, fg='white',
                                font=('Arial', 10, 'bold'),
                                relief='flat', padx=20, pady=10,
                                state='disabled')
        self.stop_btn.pack(fill='x', pady=2)

    # === เพิ่ม Methods ใหม่สำหรับ MT5 Selection ===
    
    def scan_mt5_installations(self):
        """สแกนหา MT5 installations ทั้งหมด"""
        try:
            self.log("🔍 กำลังสแกนหา MT5...")
            self.scan_status_label.config(text="Scanning...", fg=self.warning_color)
            
            # อัพเดท button state
            self.scan_btn.config(state='disabled', text="🔄 Scanning...")
            self.root.update()
            
            installations = self.mt5_connector.find_running_mt5_installations()
            
            if not installations:
                self.scan_status_label.config(text="❌ ไม่เจอ MT5", fg=self.error_color)
                self.log("❌ ไม่เจอ MT5 ในเครื่อง")
                
                # รีเซ็ต dropdown
                self.mt5_dropdown['values'] = ["ไม่เจอ MT5 ในเครื่อง"]
                self.mt5_var.set("ไม่เจอ MT5 ในเครื่อง")
                
            else:
                # เจอ MT5 แล้ว - อัพเดท dropdown
                installation_list = self.mt5_connector.get_installation_list()
                display_names = [f"{inst['display_name']} {'🟢' if inst['is_running'] else '⚫'}" 
                               for inst in installation_list]
                
                self.mt5_dropdown['values'] = display_names
                
                # เลือกตัวแรกโดยอัตโนมัติ
                self.mt5_var.set(display_names[0])
                
                # เปิดใช้งาน Connect button
                self.connect_btn.config(state='normal')
                
                self.scan_status_label.config(text=f"✅ เจอ {len(installations)} ตัว", 
                                            fg=self.success_color)
                self.log(f"✅ เจอ MT5 ทั้งหมด {len(installations)} ตัว")
                
                for inst in installation_list:
                    status = "🟢 กำลังทำงาน" if inst['is_running'] else "⚫ หยุดทำงาน"
                    self.log(f"   📍 {inst['broker']} - {status}")
                    
        except Exception as e:
            self.scan_status_label.config(text="❌ Error", fg=self.error_color)
            self.log(f"❌ Scan error: {e}")
            
        finally:
            # คืนสถานะ button
            self.scan_btn.config(state='normal', text="🔍 Scan MT5")
    
    def on_mt5_selected(self, event=None):
        """เมื่อเลือก MT5 จาก dropdown"""
        try:
            selected_text = self.mt5_var.get()
            
            if "ไม่เจอ" in selected_text or "Scan" in selected_text:
                self.connect_btn.config(state='disabled')
                return
                
            # หา index ของ MT5 ที่เลือก
            installation_list = self.mt5_connector.get_installation_list()
            
            for i, inst in enumerate(installation_list):
                display_with_status = f"{inst['display_name']} {'🟢' if inst['is_running'] else '⚫'}"
                if display_with_status == selected_text:
                    self.selected_mt5_index = i
                    self.connect_btn.config(state='normal')
                    self.log(f"📱 เลือก MT5: {inst['display_name']}")
                    break
                    
        except Exception as e:
            self.log(f"❌ Selection error: {e}")
    
    def connect_mt5(self):
        """Connect to MT5 - ปรับปรุงให้ใช้ตัวที่เลือก"""
        try:
            if not hasattr(self, 'selected_mt5_index'):
                # ถ้ายังไม่ได้เลือก ลอง auto-connect
                self.log("🔗 ลองเชื่อมต่อแบบอัตโนมัติ...")
                
                if self.mt5_connector.auto_connect():
                    # สำเร็จ
                    self._handle_successful_connection()
                else:
                    # ไม่สำเร็จ - อาจมีหลายตัว
                    self.log("⚠️ กรุณาเลือก MT5 ที่ต้องการใช้จาก dropdown ข้างบน")
                    self.scan_mt5_installations()  # Auto-scan
                return
            
            # เชื่อมต่อกับตัวที่เลือก
            self.log(f"🔗 กำลังเชื่อมต่อกับ MT5 ที่เลือก...")
            
            if self.mt5_connector.connect_to_installation(self.selected_mt5_index):
                self._handle_successful_connection()
            else:
                self.log("❌ การเชื่อมต่อ MT5 ไม่สำเร็จ")
                self.show_message("Error", "ไม่สามารถเชื่อมต่อ MT5 ได้", "error")
                
        except Exception as e:
            self.log(f"❌ Connection error: {e}")
            self.show_message("Error", f"Connection error: {e}", "error")
    
    def _handle_successful_connection(self):
        """จัดการเมื่อเชื่อมต่อสำเร็จ"""
        try:
            self.is_connected = True
            self.account_info = self.mt5_connector.account_info
            
            # อัพเดท GUI
            self.status_label.config(text="● Connected", fg=self.success_color)
            self.account_label.config(
                text=f"Account: {self.account_info.get('login', 'Unknown')} | "
                     f"Balance: ${self.account_info.get('balance', 0):,.2f} | "
                     f"Broker: {self.account_info.get('company', 'Unknown')}",
                fg=self.text_color
            )
            
            # เปิดใช้งานขั้นตอนถัดไป
            self.init_rules_btn.config(state='normal')
            
            # ปิดใช้งาน Connect button แล้วเปลี่ยนเป็น Disconnect
            self.connect_btn.config(text="🔌 Disconnect", 
                                   command=self.disconnect_mt5,
                                   bg=self.error_color, fg='white')
            
            # ปิด Scan button และ Dropdown
            self.scan_btn.config(state='disabled')
            self.mt5_dropdown.config(state='disabled')
            
            self.log(f"✅ เชื่อมต่อสำเร็จ!")
            self.log(f"💰 Balance: ${self.account_info.get('balance', 0):,.2f}")
            self.log(f"🏦 Broker: {self.account_info.get('company', 'Unknown')}")
            
            if self.mt5_connector.gold_symbol:
                self.log(f"🥇 Gold Symbol: {self.mt5_connector.gold_symbol}")
                
        except Exception as e:
            self.log(f"❌ Handle connection error: {e}")
    
    def disconnect_mt5(self):
        """ตัดการเชื่อมต่อ MT5"""
        try:
            self.log("🔌 กำลังตัดการเชื่อมต่อ...")
            
            # หยุดการเทรดก่อน
            if self.is_trading:
                self.stop_trading()
            
            # ตัดการเชื่อมต่อ
            if self.mt5_connector:
                self.mt5_connector.disconnect()
            
            # รีเซ็ต states
            self.is_connected = False
            self.account_info = {}
            
            # อัพเดท GUI
            self.status_label.config(text="● Disconnected", fg=self.error_color)
            self.account_label.config(text="No account connected", fg='#888888')
            
            # รีเซ็ต buttons
            self.connect_btn.config(text="🔌 Connect to Selected MT5",
                                   command=self.connect_mt5,
                                   bg=self.accent_color, fg='black',
                                   state='disabled')
            
            # เปิดใช้งาน Scan อีกครั้ง
            self.scan_btn.config(state='normal')
            self.mt5_dropdown.config(state='readonly')
            
            # ปิดใช้งานขั้นตอนอื่นๆ
            self.init_rules_btn.config(state='disabled')
            self.calc_btn.config(state='disabled')
            self.start_btn.config(state='disabled')
            
            self.log("✅ ตัดการเชื่อมต่อเรียบร้อย")
            
        except Exception as e:
            self.log(f"❌ Disconnect error: {e}")
        
    def create_rules_monitor(self, parent):
        """Create rules monitoring panel - ใหม่"""
        # Title
        title = tk.Label(parent, text="🧠 Rule Engine Monitor",
                        bg=self.card_color, fg=self.text_color,
                        font=('Arial', 14, 'bold'))
        title.pack(pady=20)
        
        # Rules status
        rules_frame = tk.Frame(parent, bg=self.card_color)
        rules_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Overall confidence
        self.confidence_label = tk.Label(rules_frame, text="📊 Overall Confidence: --%",
                                       bg=self.card_color, fg=self.accent_color,
                                       font=('Arial', 11, 'bold'))
        self.confidence_label.pack(anchor='w', pady=5)
        
        # Market condition
        self.market_condition_label = tk.Label(rules_frame, text="🌍 Market: UNKNOWN",
                                             bg=self.card_color, fg=self.text_color,
                                             font=('Arial', 11))
        self.market_condition_label.pack(anchor='w', pady=2)
        
        # Individual rules
        tk.Label(rules_frame, text="📋 Rule Status:",
                bg=self.card_color, fg=self.text_color,
                font=('Arial', 11, 'bold')).pack(anchor='w', pady=(20, 5))
        
        # Rules listbox
        self.rules_listbox = tk.Listbox(rules_frame, height=8,
                                      bg='#0f0f23', fg=self.text_color,
                                      selectbackground=self.accent_color,
                                      font=('Arial', 9))
        self.rules_listbox.pack(fill='x', pady=5)
        
        # Last action
        action_frame = tk.Frame(rules_frame, bg=self.card_color)
        action_frame.pack(fill='x', pady=(20, 0))
        
        tk.Label(action_frame, text="🎯 Last Action:",
                bg=self.card_color, fg=self.text_color,
                font=('Arial', 11, 'bold')).pack(anchor='w')
        
        self.last_action_label = tk.Label(action_frame, text="NONE",
                                        bg=self.card_color, fg='#888888',
                                        font=('Arial', 10))
        self.last_action_label.pack(anchor='w', pady=2)
        
        self.action_reason_label = tk.Label(action_frame, text="Waiting for initialization",
                                          bg=self.card_color, fg='#888888',
                                          font=('Arial', 9), wraplength=200)
        self.action_reason_label.pack(anchor='w', pady=2)
        
    def create_system_monitor(self, parent):
        """Create system monitor panel - ปรับปรุงจากเดิม"""
        # Title
        title = tk.Label(parent, text="📊 System Monitor",
                        bg=self.card_color, fg=self.text_color,
                        font=('Arial', 14, 'bold'))
        title.pack(pady=20)
        
        # Stats frame
        stats_frame = tk.Frame(parent, bg=self.card_color)
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        # Portfolio health
        self.health_label = tk.Label(stats_frame, text="💚 Portfolio Health: --%",
                                   bg=self.card_color, fg=self.success_color,
                                   font=('Arial', 11, 'bold'))
        self.health_label.pack(anchor='w', pady=3)
        
        # Profit/Loss
        self.profit_label = tk.Label(stats_frame, text="💰 Total P&L: $0.00",
                                   bg=self.card_color, fg=self.text_color,
                                   font=('Arial', 11, 'bold'))
        self.profit_label.pack(anchor='w', pady=3)
        
        # Positions
        self.positions_label = tk.Label(stats_frame, text="📈 Active Positions: 0",
                                      bg=self.card_color, fg=self.warning_color,
                                      font=('Arial', 11))
        self.positions_label.pack(anchor='w', pady=2)
        
        # Pending orders
        self.orders_label = tk.Label(stats_frame, text="⏳ Pending Orders: 0",
                                   bg=self.card_color, fg=self.text_color,
                                   font=('Arial', 11))
        self.orders_label.pack(anchor='w', pady=2)
        
        # Risk level
        self.risk_label = tk.Label(stats_frame, text="🛡️ Risk Level: --%",
                                 bg=self.card_color, fg=self.text_color,
                                 font=('Arial', 11))
        self.risk_label.pack(anchor='w', pady=2)
        
        # Survivability
        self.survivability_label = tk.Label(stats_frame, text="🔋 Survivability: --%",
                                          bg=self.card_color, fg=self.success_color,
                                          font=('Arial', 11))
        self.survivability_label.pack(anchor='w', pady=2)
        
        # System log
        log_frame = tk.Frame(parent, bg=self.card_color)
        log_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(log_frame, text="📋 System Log:",
                bg=self.card_color, fg=self.text_color,
                font=('Arial', 11, 'bold')).pack(anchor='w')
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15,
                                                bg='#0f0f23', fg=self.text_color,
                                                font=('Consolas', 9),
                                                wrap='word')
        self.log_text.pack(fill='both', expand=True, pady=(5, 0))
        
    # === Connection Methods ===
    
    def connect_mt5(self):
        """Connect to MT5 - เก็บ logic เดิม + เพิ่ม Modern features"""
        try:
            self.log("🔗 Connecting to MetaTrader 5...")
            
            if self.mt5_connector.auto_connect():
                self.is_connected = True
                self.account_info = self.mt5_connector.get_account_info()
                
                # Update GUI
                self.status_label.config(text="● Connected", fg=self.success_color)
                self.account_label.config(
                    text=f"Account: {self.account_info.get('login', 'Unknown')} | "
                         f"Balance: ${self.account_info.get('balance', 0):,.2f}",
                    fg=self.text_color
                )
                
                # Enable next steps
                self.init_rules_btn.config(state='normal')
                
                self.log(f"✅ Connected to account: {self.account_info.get('login', 'Unknown')}")
                self.log(f"💰 Balance: ${self.account_info.get('balance', 0):,.2f}")
                self.log(f"🏦 Broker: {self.account_info.get('company', 'Unknown')}")
                
                # Initialize API connector
                self.api_connector = BackendAPIConnector(
                    api_base_url=self.config["api"]["backend_url"],
                    timeout=self.config["api"]["timeout"]
                )
                
                self.log("🔗 Backend API connector initialized")
                
            else:
                self.log("❌ MT5 connection failed")
                self.show_message("Error", "Failed to connect to MT5", "error")
                
        except Exception as e:
            self.log(f"❌ Connection error: {e}")
            self.show_message("Error", f"Connection error: {e}", "error")
            
    def initialize_rules(self):
        """Initialize rule engine and components"""
        if not self.is_connected:
            self.show_message("Warning", "Please connect to MT5 first", "warning")
            return
            
        try:
            self.log("🧠 Initializing Modern Rule Engine...")
            
            # Initialize core components
            self.market_analyzer = MarketAnalyzer(
                mt5_connector=self.mt5_connector,
                config=self.config
            )
            
            self.spacing_manager = SpacingManager(
                config=self.config["trading"]
            )
            
            self.lot_calculator = LotCalculator(
                account_info=self.account_info,
                config=self.config
            )
            
            self.order_manager = OrderManager(
                mt5_connector=self.mt5_connector,
                spacing_manager=self.spacing_manager,
                lot_calculator=self.lot_calculator,
                config=self.config
            )
            
            self.position_manager = PositionManager(
                mt5_connector=self.mt5_connector,
                config=self.config
            )
            
            self.performance_tracker = PerformanceTracker()
            
            # Initialize rule engine
            self.rule_engine = ModernRuleEngine(
                config=self.rules_config,
                market_analyzer=self.market_analyzer,
                order_manager=self.order_manager,
                position_manager=self.position_manager,
                performance_tracker=self.performance_tracker
            )
            
            self.log("✅ Rule Engine initialized successfully")
            self.rule_status_label.config(text="● Active", fg=self.success_color)
            
            # Enable calculation
            self.calc_btn.config(state='normal')
            
            # Update rules display
            self.update_rules_display()
            
        except Exception as e:
            self.log(f"❌ Rule initialization error: {e}")
            self.show_message("Error", f"Rule initialization error: {e}", "error")
            
    def calculate_params(self):
        """Calculate trading parameters using rule engine"""
        if not self.rule_engine:
            self.show_message("Warning", "Please initialize rules first", "warning")
            return
            
        try:
            self.log("🧮 Calculating AI trading parameters...")
            
            # Get market analysis
            market_data = self.market_analyzer.get_comprehensive_analysis()
            
            # Calculate optimal parameters based on current conditions
            balance = self.account_info.get('balance', 1000)
            equity = self.account_info.get('equity', balance)
            
            # AI-driven parameter calculation
            self.trading_params = {
                'base_lot': self.lot_calculator.calculate_optimal_lot_size(),
                'dynamic_spacing': self.spacing_manager.get_current_spacing(),
                'risk_level': min(self.config["risk_management"]["max_drawdown_percentage"], 
                                balance * 0.05 / 100),
                'max_positions': min(self.config["trading"]["max_positions"],
                                   int(balance / 1000) * 2),
                'survivability_points': int(balance * 15),
                'market_condition': market_data.get('condition', 'RANGING'),
                'volatility_factor': market_data.get('volatility_factor', 1.0)
            }
            
            # Log results
            self.log("✅ Parameters calculated successfully")
            self.log(f"📊 Base Lot: {self.trading_params['base_lot']:.3f}")
            self.log(f"📏 Dynamic Spacing: {self.trading_params['dynamic_spacing']} points")
            self.log(f"🛡️ Risk Level: {self.trading_params['risk_level']:.2f}%")
            self.log(f"🔢 Max Positions: {self.trading_params['max_positions']}")
            self.log(f"🌍 Market: {self.trading_params['market_condition']}")
            
            # Enable trading
            self.start_btn.config(state='normal')
            
        except Exception as e:
            self.log(f"❌ Parameter calculation error: {e}")
            self.show_message("Error", f"Parameter calculation error: {e}", "error")
            
    def start_trading(self):
        """Start AI trading with rule engine"""
        if not self.rule_engine or not hasattr(self, 'trading_params'):
            self.show_message("Warning", "Please complete initialization and parameter calculation", "warning")
            return
            
        try:
            self.log("🚀 Starting Modern AI Trading System...")
            
            self.is_trading = True
            
            # Configure trading mode
            mode = self.mode_var.get()
            self.rule_engine.set_trading_mode(mode)
            
            # Start trading components
            self.rule_engine.start()
            
            # Update GUI
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            
            self.log(f"🎯 Trading Mode: {mode}")
            self.log("🧠 Rule Engine: ACTIVE")
            self.log("📊 Market Analyzer: MONITORING")
            self.log("🎯 Order Manager: READY")
            self.log("💰 Position Manager: MONITORING")
            self.log("📏 Spacing Manager: DYNAMIC")
            self.log("🔢 Lot Calculator: OPTIMIZING")
            
            # Start monitoring
            self.start_monitoring()
            
        except Exception as e:
            self.log(f"❌ Trading start error: {e}")
            self.show_message("Error", f"Trading start error: {e}", "error")
            
    def stop_trading(self):
        """Stop AI trading"""
        if not self.is_trading:
            return
            
        try:
            self.log("🛑 Stopping AI Trading System...")
            
            self.is_trading = False
            
            if self.rule_engine:
                self.rule_engine.stop()
                
            # Update GUI
            self.start_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            
            self.log("✅ AI Trading stopped successfully")
            self.log("📊 Final portfolio analysis will be generated...")
            
        except Exception as e:
            self.log(f"❌ Stop error: {e}")
            
    # === Monitoring Methods ===
    
    def start_monitoring(self):
        """Start monitoring thread"""
        def monitor():
            while self.is_trading:
                try:
                    # Update system status
                    if self.rule_engine:
                        self.system_status = self.rule_engine.get_system_status()
                        
                        # Update GUI
                        self.root.after(0, self.update_display)
                        
                        # Update rules display
                        self.root.after(0, self.update_rules_display)
                    
                    time.sleep(2)  # Update every 2 seconds
                    
                except Exception as e:
                    self.log(f"❌ Monitor error: {e}")
                    time.sleep(5)
        
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()
        
    def update_display(self):
        """Update system display"""
        try:
            status = self.system_status
            
            # Portfolio health
            health = status.get('portfolio_health', 0) * 100
            health_color = (self.success_color if health > 70 else 
                          self.warning_color if health > 40 else self.error_color)
            self.health_label.config(text=f"💚 Portfolio Health: {health:.1f}%", fg=health_color)
            
            # Profit/Loss
            profit = status.get('total_profit', 0)
            profit_color = (self.success_color if profit > 0 else 
                          self.error_color if profit < 0 else self.text_color)
            self.profit_label.config(text=f"💰 Total P&L: ${profit:.2f}", fg=profit_color)
            
            # Positions and orders
            positions = status.get('active_positions', 0)
            self.positions_label.config(text=f"📈 Active Positions: {positions}")
            
            orders = status.get('pending_orders', 0)
            self.orders_label.config(text=f"⏳ Pending Orders: {orders}")
            
            # Risk level
            risk = status.get('risk_level', 0) * 100
            risk_color = (self.success_color if risk < 30 else 
                         self.warning_color if risk < 70 else self.error_color)
            self.risk_label.config(text=f"🛡️ Risk Level: {risk:.1f}%", fg=risk_color)
            
            # Survivability
            survivability = (1 - status.get('survivability_usage', 0)) * 100
            surv_color = (self.success_color if survivability > 70 else 
                         self.warning_color if survivability > 40 else self.error_color)
            self.survivability_label.config(text=f"🔋 Survivability: {survivability:.1f}%", fg=surv_color)
            
        except Exception as e:
            self.log(f"❌ Display update error: {e}")
            
    def update_rules_display(self):
        """Update rules monitoring display"""
        try:
            if not self.rule_engine:
                return
                
            # Overall confidence
            confidence = self.rule_engine.get_overall_confidence() * 100
            conf_color = (self.success_color if confidence > 70 else 
                         self.warning_color if confidence > 40 else self.error_color)
            self.confidence_label.config(text=f"📊 Overall Confidence: {confidence:.1f}%", fg=conf_color)
            
            # Market condition
            market_condition = self.system_status.get('market_condition', 'UNKNOWN')
            condition_color = {
                'TRENDING_UP': self.success_color,
                'TRENDING_DOWN': self.error_color,
                'RANGING': self.warning_color,
                'HIGH_VOLATILITY': '#FF6B35',
                'LOW_VOLATILITY': '#4ECDC4'
            }.get(market_condition, self.text_color)
            
            self.market_condition_label.config(text=f"🌍 Market: {market_condition}", fg=condition_color)
            
            # Rules status
            rules_status = self.rule_engine.get_rules_status()
            self.rules_listbox.delete(0, tk.END)
            
            for rule_name, rule_data in rules_status.items():
                confidence = rule_data.get('confidence', 0) * 100
                weight = rule_data.get('weight', 0) * 100
                active = "🟢" if rule_data.get('active', False) else "🔴"
                
                status_text = f"{active} {rule_name}: {confidence:.0f}% (w:{weight:.0f}%)"
                self.rules_listbox.insert(tk.END, status_text)
            
            # Last action
            last_action = self.system_status.get('last_action', 'NONE')
            action_reason = self.system_status.get('action_reason', 'Waiting...')
            
            action_color = {
                'BUY': self.success_color,
                'SELL': self.error_color,
                'CLOSE': self.warning_color,
                'WAIT': self.text_color,
                'NONE': '#888888'
            }.get(last_action, self.text_color)
            
            self.last_action_label.config(text=last_action, fg=action_color)
            self.action_reason_label.config(text=action_reason)
            
        except Exception as e:
            self.log(f"❌ Rules display update error: {e}")
    
    # === Utility Methods ===
    
    def log(self, message):
        """Add message to log"""
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_entry = f"[{timestamp}] {message}\n"
            
            self.log_text.insert(tk.END, log_entry)
            self.log_text.see(tk.END)
            
            # Print to console as well
            print(log_entry.strip())
            
        except Exception as e:
            print(f"Log error: {e}")
            
    def show_message(self, title, message, msg_type="info"):
        """Show message dialog"""
        try:
            if msg_type == "error":
                messagebox.showerror(title, message)
            elif msg_type == "warning":
                messagebox.showwarning(title, message)
            else:
                messagebox.showinfo(title, message)
        except Exception as e:
            print(f"Message dialog error: {e}")
            
    def run(self):
        """Run the GUI"""
        try:
            self.log("🚀 Modern AI Trading System Started")
            self.log("🧠 Rule-based Architecture Loaded")
            self.log("⚡ Ready for intelligent trading")
            self.root.mainloop()
        except Exception as e:
            print(f"GUI error: {e}")

def main():
    """Main function"""
    try:
        print("🚀 Modern AI Gold Grid Trading System")
        print("=" * 50)
        print("✅ Modern Rule-based Architecture")
        print("✅ Adaptive Learning Engine")
        print("✅ Intelligent Order Management")
        print("✅ Dynamic Risk Management")
        print("=" * 50)
        
        app = ModernAITradingGUI()
        app.run()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()