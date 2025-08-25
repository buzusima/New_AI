"""
🚀 Modern AI Gold Grid Trading GUI
main.py
GUI สำหรับ Modern Rule-based Trading System - Production Ready
** NO MOCK DATA - REAL DATA ONLY **
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import threading
import time
from datetime import datetime
import os

# Import modern components - NO MOCK
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
    print(f"⚠️ Import error: {e}")
    print("💡 Please ensure all modules are available")

class ModernRuleBasedTradingGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.init_variables()
        self.load_config()
        self.create_gui()
        self.start_gui_updates()
        
    def setup_window(self):
        """Setup main window - เก็บ style เดิม"""
        self.root.title("🚀 Modern AI Gold Grid Trading - Rule-based Edition")
        self.root.geometry("1450x950")
        self.root.configure(bg='#1a1a2e')
        
        # Center window
        self.root.update_idletasks()
        width = 1450
        height = 950
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Window icon (optional)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
    def init_variables(self):
        """Initialize variables - Modern Architecture"""
        # Connection states
        self.is_connected = False
        self.is_trading = False
        self.account_info = {}
        
        # Modern Rule-based Components - NO MOCK
        self.mt5_connector = None
        self.rule_engine = None
        self.market_analyzer = None
        self.order_manager = None
        self.position_manager = None
        self.spacing_manager = None
        self.lot_calculator = None
        self.performance_tracker = None
        self.api_connector = None
        
        # GUI state
        self.selected_mt5_index = None
        self.last_update_time = datetime.now()
        
        # System status
        self.system_status = {
            'rule_confidence': 0.0,
            'market_condition': 'UNKNOWN',
            'portfolio_health': 0.5,
            'total_profit': 0.0,
            'active_positions': 0,
            'pending_orders': 0,
            'risk_level': 0.0,
            'last_action': 'NONE',
            'action_reason': 'System initializing...',
            'survivability_usage': 0.0,
            'engine_running': False
        }
        
        # GUI Colors - เก็บ scheme เดิม
        self.bg_color = '#1a1a2e'
        self.card_color = '#16213e'
        self.accent_color = '#00d4ff'
        self.success_color = '#00ff88'
        self.error_color = '#ff3366'
        self.warning_color = '#ffb800'
        self.text_color = '#ffffff'
        
        # Trading mode
        self.trading_mode = tk.StringVar(value="BALANCED")
        
    def load_config(self):
        """Load configuration files"""
        try:
            # Load main config
            if os.path.exists('config.json'):
                with open('config.json', 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                self.config = self.get_default_config()
                
            # Load rules config  
            if os.path.exists('rules_config.json'):
                with open('rules_config.json', 'r', encoding='utf-8') as f:
                    self.rules_config = json.load(f)
            else:
                self.rules_config = self.get_default_rules_config()
                
            self.log("✅ Configuration loaded successfully")
            
        except Exception as e:
            self.log(f"⚠️ Config load error: {e}")
            self.config = self.get_default_config()
            self.rules_config = self.get_default_rules_config()
            
    def get_default_config(self):
        """Default configuration"""
        return {
            "system": {
                "mode": "PRODUCTION",
                "enable_real_trading": True
            },
            "trading": {
                "symbol": "XAUUSD",
                "base_lot_size": 0.01,
                "max_positions": 20,
                "max_risk_percentage": 5.0,
                "min_spacing_points": 80,
                "max_spacing_points": 300
            },
            "api": {
                "backend_url": "http://123.253.62.50:8080/api",
                "timeout": 10
            },
            "risk_management": {
                "max_drawdown_percentage": 20.0,
                "margin_usage_limit": 70.0
            }
        }
        
    def get_default_rules_config(self):
        """Default rules configuration"""
        return {
            "rules": {
                "trend_following": {
                    "enabled": True,
                    "weight": 0.3,
                    "confidence_threshold": 0.6
                },
                "mean_reversion": {
                    "enabled": True,
                    "weight": 0.25,
                    "confidence_threshold": 0.7
                },
                "support_resistance": {
                    "enabled": True,
                    "weight": 0.2,
                    "confidence_threshold": 0.6
                },
                "volatility_breakout": {
                    "enabled": True,
                    "weight": 0.15,
                    "confidence_threshold": 0.8
                },
                "portfolio_balance": {
                    "enabled": True,
                    "weight": 0.1,
                    "confidence_threshold": 0.5
                }
            }
        }
        
    def create_gui(self):
        """Create GUI - เก็บ layout เดิม + Modern features"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Header
        self.create_header(main_frame)
        
        # Content - 3 column layout
        content_frame = tk.Frame(main_frame, bg=self.bg_color)
        content_frame.pack(fill='both', expand=True, pady=15)
        
        # Left Panel - Controls
        left_frame = tk.Frame(content_frame, bg=self.card_color, relief='ridge', borderwidth=2)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 8))
        
        # Middle Panel - Rules Monitor  
        middle_frame = tk.Frame(content_frame, bg=self.card_color, relief='ridge', borderwidth=2)
        middle_frame.pack(side='left', fill='both', expand=True, padx=4)
        
        # Right Panel - System Monitor
        right_frame = tk.Frame(content_frame, bg=self.card_color, relief='ridge', borderwidth=2)
        right_frame.pack(side='right', fill='both', expand=True, padx=(8, 0))
        
        # Create panels
        self.create_controls_panel(left_frame)
        self.create_rules_monitor_panel(middle_frame)
        self.create_system_monitor_panel(right_frame)
        
    def create_header(self, parent):
        """Create header section"""
        header = tk.Frame(parent, bg='#16213e', height=90, relief='ridge', borderwidth=2)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Left - Title
        left_header = tk.Frame(header, bg='#16213e')
        left_header.pack(side='left', fill='both', expand=True, padx=20, pady=12)
        
        title = tk.Label(left_header, text="🚀 Modern AI Gold Grid Trading",
                        bg='#16213e', fg=self.accent_color,
                        font=('Arial', 20, 'bold'))
        title.pack(anchor='w')
        
        subtitle = tk.Label(left_header, text="Rule-based Architecture • Adaptive Learning Engine",
                          bg='#16213e', fg='#888888',
                          font=('Arial', 11))
        subtitle.pack(anchor='w')
        
        # Center - Engine Status
        center_header = tk.Frame(header, bg='#16213e')
        center_header.pack(side='left', fill='y', padx=20, pady=12)
        
        tk.Label(center_header, text="🧠 Rule Engine:",
                bg='#16213e', fg=self.text_color,
                font=('Arial', 11, 'bold')).pack()
        
        self.rule_status_label = tk.Label(center_header, text="● Initializing",
                                        bg='#16213e', fg=self.warning_color,
                                        font=('Arial', 11))
        self.rule_status_label.pack()
        
        # Right - Connection Status  
        right_header = tk.Frame(header, bg='#16213e')
        right_header.pack(side='right', padx=20, pady=12)
        
        tk.Label(right_header, text="📡 MT5 Connection:",
                bg='#16213e', fg=self.text_color,
                font=('Arial', 11, 'bold')).pack()
        
        self.connection_status_label = tk.Label(right_header, text="● Disconnected",
                                              bg='#16213e', fg=self.error_color,
                                              font=('Arial', 12, 'bold'))
        self.connection_status_label.pack()
        
    def create_controls_panel(self, parent):
        """Create control panel"""
        # Panel title
        title_frame = tk.Frame(parent, bg=self.card_color)
        title_frame.pack(fill='x', padx=15, pady=(15, 10))
        
        title = tk.Label(title_frame, text="🎛️ Trading Controls",
                        bg=self.card_color, fg=self.text_color,
                        font=('Arial', 16, 'bold'))
        title.pack(anchor='w')
        
        # MT5 Connection Section
        self.create_mt5_connection_section(parent)
        
        # Trading Mode Section
        self.create_trading_mode_section(parent)
        
        # Rule Engine Section
        self.create_rule_engine_section(parent)
        
        # Trading Control Section
        self.create_trading_control_section(parent)
        
    def create_mt5_connection_section(self, parent):
        """Create MT5 connection section"""
        # Section frame
        conn_frame = tk.Frame(parent, bg=self.card_color)
        conn_frame.pack(fill='x', padx=15, pady=15)
        
        # Section title
        tk.Label(conn_frame, text="📡 MT5 Connection",
                bg=self.card_color, fg=self.text_color,
                font=('Arial', 13, 'bold')).pack(anchor='w', pady=(0, 8))
        
        # MT5 Selection
        select_frame = tk.Frame(conn_frame, bg=self.card_color)
        select_frame.pack(fill='x', pady=(0, 8))
        
        tk.Label(select_frame, text="🖥️ Select Running MT5:",
                bg=self.card_color, fg=self.text_color,
                font=('Arial', 10)).pack(anchor='w')
        
        self.mt5_var = tk.StringVar(value="Click 'Scan' to find MT5...")
        self.mt5_dropdown = ttk.Combobox(select_frame, 
                                        textvariable=self.mt5_var,
                                        state='readonly',
                                        font=('Arial', 10),
                                        width=50)
        self.mt5_dropdown.pack(fill='x', pady=(3, 8))
        self.mt5_dropdown.bind('<<ComboboxSelected>>', self.on_mt5_selected)
        
        # Buttons frame
        btn_frame = tk.Frame(conn_frame, bg=self.card_color)
        btn_frame.pack(fill='x')
        
        # Scan button
        self.scan_btn = tk.Button(btn_frame, text="🔍 Scan Running MT5",
                                 command=self.scan_mt5_installations,
                                 bg='#4a90e2', fg='white',
                                 font=('Arial', 10, 'bold'),
                                 relief='flat', padx=15, pady=8)
        self.scan_btn.pack(side='left', padx=(0, 10))
        
        # Connect button
        self.connect_btn = tk.Button(btn_frame, text="🔌 Connect to Selected",
                                   command=self.connect_mt5,
                                   bg=self.accent_color, fg='black',
                                   font=('Arial', 10, 'bold'),
                                   relief='flat', padx=15, pady=8,
                                   state='disabled')
        self.connect_btn.pack(side='left')
        
        # Status label
        self.scan_status_label = tk.Label(conn_frame, text="Ready to scan",
                                         bg=self.card_color, fg='#888888',
                                         font=('Arial', 9))
        self.scan_status_label.pack(anchor='w', pady=(5, 0))
        
        # Account info
        self.account_info_label = tk.Label(conn_frame, text="No account connected",
                                         bg=self.card_color, fg='#888888',
                                         font=('Arial', 10))
        self.account_info_label.pack(anchor='w', pady=(3, 0))
        
    def create_trading_mode_section(self, parent):
        """Create trading mode section"""
        mode_frame = tk.Frame(parent, bg=self.card_color)
        mode_frame.pack(fill='x', padx=15, pady=15)
        
        tk.Label(mode_frame, text="🎯 Trading Mode",
                bg=self.card_color, fg=self.text_color,
                font=('Arial', 13, 'bold')).pack(anchor='w', pady=(0, 8))
        
        modes = [
            ("🛡️ Conservative (Safe)", "CONSERVATIVE"),
            ("⚖️ Balanced (Recommended)", "BALANCED"), 
            ("🚀 Aggressive (High Risk)", "AGGRESSIVE"),
            ("🧪 Adaptive (AI Learning)", "ADAPTIVE")
        ]
        
        for text, value in modes:
            rb = tk.Radiobutton(mode_frame, text=text, 
                              variable=self.trading_mode, value=value,
                              bg=self.card_color, fg=self.text_color,
                              selectcolor=self.bg_color, activebackground=self.card_color,
                              font=('Arial', 10), command=self.on_mode_changed)
            rb.pack(anchor='w', pady=2)
            
    def create_rule_engine_section(self, parent):
        """Create rule engine section"""
        rule_frame = tk.Frame(parent, bg=self.card_color)
        rule_frame.pack(fill='x', padx=15, pady=15)
        
        tk.Label(rule_frame, text="🧠 Rule Engine Control",
                bg=self.card_color, fg=self.text_color,
                font=('Arial', 13, 'bold')).pack(anchor='w', pady=(0, 8))
        
        # Initialize button
        self.init_rules_btn = tk.Button(rule_frame, text="🔧 Initialize Rule Engine",
                                      command=self.initialize_rule_engine,
                                      bg=self.warning_color, fg='black',
                                      font=('Arial', 11, 'bold'),
                                      relief='flat', padx=20, pady=10,
                                      state='disabled')
        self.init_rules_btn.pack(fill='x', pady=(0, 8))
        
        # Calculate parameters
        self.calc_params_btn = tk.Button(rule_frame, text="🧮 Calculate Parameters",
                                       command=self.calculate_parameters,
                                       bg='#6c5ce7', fg='white',
                                       font=('Arial', 11, 'bold'),
                                       relief='flat', padx=20, pady=10,
                                       state='disabled')
        self.calc_params_btn.pack(fill='x')
        
    def create_trading_control_section(self, parent):
        """Create trading control section"""
        control_frame = tk.Frame(parent, bg=self.card_color)
        control_frame.pack(fill='x', padx=15, pady=15)
        
        tk.Label(control_frame, text="🎮 Trading Control",
                bg=self.card_color, fg=self.text_color,
                font=('Arial', 13, 'bold')).pack(anchor='w', pady=(0, 8))
        
        # Start trading
        self.start_trading_btn = tk.Button(control_frame, text="🚀 Start AI Trading",
                                         command=self.start_trading,
                                         bg=self.success_color, fg='black',
                                         font=('Arial', 12, 'bold'),
                                         relief='flat', padx=20, pady=12,
                                         state='disabled')
        self.start_trading_btn.pack(fill='x', pady=(0, 8))
        
        # Stop trading
        self.stop_trading_btn = tk.Button(control_frame, text="⏹️ Stop Trading",
                                        command=self.stop_trading,
                                        bg=self.error_color, fg='white',
                                        font=('Arial', 11, 'bold'),
                                        relief='flat', padx=20, pady=10,
                                        state='disabled')
        self.stop_trading_btn.pack(fill='x')
        
    def create_rules_monitor_panel(self, parent):
        """Create rules monitoring panel"""
        # Panel title
        title_frame = tk.Frame(parent, bg=self.card_color)
        title_frame.pack(fill='x', padx=15, pady=(15, 10))
        
        title = tk.Label(title_frame, text="🧠 Rule Engine Monitor",
                        bg=self.card_color, fg=self.text_color,
                        font=('Arial', 16, 'bold'))
        title.pack(anchor='w')
        
        # Monitor content
        monitor_frame = tk.Frame(parent, bg=self.card_color)
        monitor_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # Overall confidence
        conf_frame = tk.Frame(monitor_frame, bg=self.card_color)
        conf_frame.pack(fill='x', pady=(0, 15))
        
        self.confidence_label = tk.Label(conf_frame, text="📊 Overall Confidence: --%",
                                       bg=self.card_color, fg=self.accent_color,
                                       font=('Arial', 12, 'bold'))
        self.confidence_label.pack(anchor='w')
        
        # Market condition
        self.market_condition_label = tk.Label(conf_frame, text="🌍 Market Condition: Unknown",
                                             bg=self.card_color, fg=self.text_color,
                                             font=('Arial', 11))
        self.market_condition_label.pack(anchor='w', pady=(5, 0))
        
        # Individual rules
        rules_title_frame = tk.Frame(monitor_frame, bg=self.card_color)
        rules_title_frame.pack(fill='x', pady=(15, 5))
        
        tk.Label(rules_title_frame, text="📋 Rule Status & Performance:",
                bg=self.card_color, fg=self.text_color,
                font=('Arial', 12, 'bold')).pack(anchor='w')
        
        # Rules listbox with scrollbar
        listbox_frame = tk.Frame(monitor_frame, bg=self.card_color)
        listbox_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        # Create scrollbar
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.rules_listbox = tk.Listbox(listbox_frame, 
                                      bg='#0f0f23', fg=self.text_color,
                                      selectbackground=self.accent_color,
                                      font=('Consolas', 10),
                                      yscrollcommand=scrollbar.set)
        self.rules_listbox.pack(fill='both', expand=True)
        scrollbar.config(command=self.rules_listbox.yview)
        
        # Last decision info
        decision_frame = tk.Frame(monitor_frame, bg=self.card_color)
        decision_frame.pack(fill='x')
        
        tk.Label(decision_frame, text="🎯 Latest Decision:",
                bg=self.card_color, fg=self.text_color,
                font=('Arial', 12, 'bold')).pack(anchor='w')
        
        self.last_decision_label = tk.Label(decision_frame, text="NONE",
                                          bg=self.card_color, fg='#888888',
                                          font=('Arial', 11, 'bold'))
        self.last_decision_label.pack(anchor='w', pady=(3, 0))
        
        self.decision_reason_label = tk.Label(decision_frame, text="System initializing...",
                                            bg=self.card_color, fg='#888888',
                                            font=('Arial', 10), wraplength=350)
        self.decision_reason_label.pack(anchor='w', pady=(2, 0))
        
    def create_system_monitor_panel(self, parent):
        """Create system monitor panel"""
        # Panel title
        title_frame = tk.Frame(parent, bg=self.card_color)
        title_frame.pack(fill='x', padx=15, pady=(15, 10))
        
        title = tk.Label(title_frame, text="📊 System Monitor",
                        bg=self.card_color, fg=self.text_color,
                        font=('Arial', 16, 'bold'))
        title.pack(anchor='w')
        
        # Portfolio stats
        stats_frame = tk.Frame(parent, bg=self.card_color)
        stats_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # Portfolio health
        self.portfolio_health_label = tk.Label(stats_frame, text="💚 Portfolio Health: --%",
                                             bg=self.card_color, fg=self.success_color,
                                             font=('Arial', 12, 'bold'))
        self.portfolio_health_label.pack(anchor='w', pady=3)
        
        # Total P&L
        self.total_pnl_label = tk.Label(stats_frame, text="💰 Total P&L: $0.00",
                                      bg=self.card_color, fg=self.text_color,
                                      font=('Arial', 12, 'bold'))
        self.total_pnl_label.pack(anchor='w', pady=3)
        
        # Active positions
        self.active_positions_label = tk.Label(stats_frame, text="📈 Active Positions: 0",
                                             bg=self.card_color, fg=self.warning_color,
                                             font=('Arial', 11))
        self.active_positions_label.pack(anchor='w', pady=2)
        
        # Pending orders
        self.pending_orders_label = tk.Label(stats_frame, text="⏳ Pending Orders: 0",
                                           bg=self.card_color, fg=self.text_color,
                                           font=('Arial', 11))
        self.pending_orders_label.pack(anchor='w', pady=2)
        
        # Risk level
        self.risk_level_label = tk.Label(stats_frame, text="🛡️ Risk Level: --%",
                                       bg=self.card_color, fg=self.text_color,
                                       font=('Arial', 11))
        self.risk_level_label.pack(anchor='w', pady=2)
        
        # Survivability
        self.survivability_label = tk.Label(stats_frame, text="🔋 Survivability: --%",
                                          bg=self.card_color, fg=self.success_color,
                                          font=('Arial', 11))
        self.survivability_label.pack(anchor='w', pady=2)
        
        # System log
        log_frame = tk.Frame(parent, bg=self.card_color)
        log_frame.pack(fill='both', expand=True, padx=15, pady=(15, 15))
        
        tk.Label(log_frame, text="📋 System Log:",
                bg=self.card_color, fg=self.text_color,
                font=('Arial', 12, 'bold')).pack(anchor='w', pady=(0, 5))
        
        # Log text with scrollbar
        log_text_frame = tk.Frame(log_frame, bg=self.card_color)
        log_text_frame.pack(fill='both', expand=True)
        
        log_scrollbar = tk.Scrollbar(log_text_frame)
        log_scrollbar.pack(side='right', fill='y')
        
        self.log_text = scrolledtext.ScrolledText(log_text_frame, 
                                                height=20,
                                                bg='#0f0f23', fg=self.text_color,
                                                font=('Consolas', 9),
                                                wrap='word',
                                                yscrollcommand=log_scrollbar.set)
        self.log_text.pack(fill='both', expand=True)
        log_scrollbar.config(command=self.log_text.yview)
        
    # === Event Handlers ===
    
    def scan_mt5_installations(self):
        """Scan for running MT5 installations"""
        try:
            self.log("🔍 Scanning for running MT5 installations...")
            self.scan_status_label.config(text="Scanning...", fg=self.warning_color)
            
            # Disable button during scan
            self.scan_btn.config(state='disabled', text="🔄 Scanning...")
            self.root.update()
            
            # Initialize MT5 connector
            if not self.mt5_connector:
                self.mt5_connector = MT5Connector()
            
            # Find installations
            installations = self.mt5_connector.find_running_mt5_installations()
            
            if not installations:
                self.scan_status_label.config(text="❌ No running MT5 found", fg=self.error_color)
                self.log("❌ No running MT5 installations found")
                self.mt5_dropdown['values'] = ["No running MT5 found"]
                self.mt5_var.set("No running MT5 found")
                
            else:
                # Update dropdown with found installations
                installation_list = self.mt5_connector.get_installation_list()
                display_names = [f"{inst['display_name']} {'🟢' if inst['is_running'] else '⚫'}" 
                               for inst in installation_list]
                
                self.mt5_dropdown['values'] = display_names
                
                # Auto-select first one
                if display_names:
                    self.mt5_var.set(display_names[0])
                    self.selected_mt5_index = 0
                    self.connect_btn.config(state='normal')
                
                self.scan_status_label.config(text=f"✅ Found {len(installations)} MT5", 
                                            fg=self.success_color)
                self.log(f"✅ Found {len(installations)} running MT5 installations")
                
                for i, inst in enumerate(installation_list):
                    status = "🟢 Running" if inst['is_running'] else "⚫ Stopped"
                    self.log(f"   📍 {i}: {inst['broker']} - {status}")
                    
        except Exception as e:
            self.scan_status_label.config(text="❌ Scan error", fg=self.error_color)
            self.log(f"❌ Scan error: {e}")
            
        finally:
            # Re-enable button
            self.scan_btn.config(state='normal', text="🔍 Scan Running MT5")
    
    def on_mt5_selected(self, event=None):
        """Handle MT5 selection from dropdown"""
        try:
            selected_text = self.mt5_var.get()
            
            if "No running" in selected_text or "Click" in selected_text:
                self.connect_btn.config(state='disabled')
                return
                
            # Find index of selected MT5
            if self.mt5_connector:
                installation_list = self.mt5_connector.get_installation_list()
                
                for i, inst in enumerate(installation_list):
                    display_with_status = f"{inst['display_name']} {'🟢' if inst['is_running'] else '⚫'}"
                    if display_with_status == selected_text:
                        self.selected_mt5_index = i
                        self.connect_btn.config(state='normal')
                        self.log(f"📱 Selected: {inst['display_name']}")
                        break
                        
        except Exception as e:
            self.log(f"❌ Selection error: {e}")
    
    def connect_mt5(self):
        """Connect to selected MT5"""
        try:
            if self.is_connected:
                # Disconnect
                self.disconnect_mt5()
                return
                
            if not self.mt5_connector or self.selected_mt5_index is None:
                self.log("⚠️ Please scan and select MT5 first")
                return
                
            self.log(f"🔗 Connecting to selected MT5...")
            
            if self.mt5_connector.connect_to_installation(self.selected_mt5_index):
                self._handle_successful_connection()
            else:
                self.log("❌ Failed to connect to MT5")
                self.show_message("Connection Error", "Failed to connect to selected MT5", "error")
                
        except Exception as e:
            self.log(f"❌ Connection error: {e}")
            self.show_message("Error", f"Connection error: {e}", "error")
    
    def _handle_successful_connection(self):
        """Handle successful MT5 connection"""
        try:
            self.is_connected = True
            self.account_info = self.mt5_connector.get_account_info()
            
            # Update GUI
            self.connection_status_label.config(text="● Connected", fg=self.success_color)
            self.account_info_label.config(
                text=f"Account: {self.account_info.get('login', 'Unknown')} | "
                     f"Balance: ${self.account_info.get('balance', 0):,.2f} | "
                     f"Broker: {self.account_info.get('company', 'Unknown')[:15]}",
                fg=self.text_color
            )
            
            # Update button
            self.connect_btn.config(text="🔌 Disconnect", bg=self.error_color, fg='white')
            
            # Enable next step
            self.init_rules_btn.config(state='normal')
            
            # Disable scan controls
            self.scan_btn.config(state='disabled')
            self.mt5_dropdown.config(state='disabled')
            
            self.log("✅ MT5 connection successful!")
            self.log(f"💰 Account: {self.account_info.get('login')} | Balance: ${self.account_info.get('balance', 0):,.2f}")
            self.log(f"🏦 Broker: {self.account_info.get('company', 'Unknown')}")
            
            if self.mt5_connector.gold_symbol:
                self.log(f"🥇 Gold Symbol: {self.mt5_connector.gold_symbol}")
                
        except Exception as e:
            self.log(f"❌ Handle connection error: {e}")
    
    def disconnect_mt5(self):
        """Disconnect from MT5"""
        try:
            self.log("🔌 Disconnecting from MT5...")
            
            # Stop trading first
            if self.is_trading:
                self.stop_trading()
            
            # Disconnect
            if self.mt5_connector:
                self.mt5_connector.disconnect()
            
            # Reset state
            self.is_connected = False
            self.account_info = {}
            
            # Update GUI
            self.connection_status_label.config(text="● Disconnected", fg=self.error_color)
            self.account_info_label.config(text="No account connected", fg='#888888')
            
            # Reset buttons
            self.connect_btn.config(text="🔌 Connect to Selected", bg=self.accent_color, fg='black')
            
            # Enable scan controls
            self.scan_btn.config(state='normal')
            self.mt5_dropdown.config(state='readonly')
            
            # Disable other controls
            self.init_rules_btn.config(state='disabled')
            self.calc_params_btn.config(state='disabled')
            self.start_trading_btn.config(state='disabled')
            
            self.log("✅ Disconnected successfully")
            
        except Exception as e:
            self.log(f"❌ Disconnect error: {e}")
    
    def on_mode_changed(self):
        """Handle trading mode change"""
        mode = self.trading_mode.get()
        self.log(f"🎯 Trading mode changed to: {mode}")
        
        if self.rule_engine:
            self.rule_engine.set_trading_mode(mode)
    
    def initialize_rule_engine(self):
        """Initialize the rule engine and components - NO MOCK"""
        if not self.is_connected:
            self.show_message("Warning", "Please connect to MT5 first", "warning")
            return
            
        try:
            self.log("🧠 Initializing Modern Rule Engine...")
            
            # Initialize REAL components
            if not self.mt5_connector:
                self.log("❌ MT5 connector not available")
                return
            
            # Initialize market analyzer with REAL data
            self.market_analyzer = MarketAnalyzer(self.mt5_connector, self.config)
            
            # Initialize spacing manager
            self.spacing_manager = SpacingManager(self.config)
            
            # Initialize lot calculator
            self.lot_calculator = LotCalculator(self.account_info, self.config)
            
            # Initialize order manager
            self.order_manager = OrderManager(
                self.mt5_connector, self.spacing_manager, 
                self.lot_calculator, self.config
            )
            
            # Initialize position manager
            self.position_manager = PositionManager(self.mt5_connector, self.config)
            
            # Initialize performance tracker
            self.performance_tracker = PerformanceTracker(self.config)
            
            # Initialize rule engine with REAL components
            self.rule_engine = ModernRuleEngine(
                config=self.rules_config,
                market_analyzer=self.market_analyzer,
                order_manager=self.order_manager,
                position_manager=self.position_manager,
                performance_tracker=self.performance_tracker
            )
            
            # Set initial mode
            self.rule_engine.set_trading_mode(self.trading_mode.get())
            
            self.log("✅ Rule Engine initialized successfully")
            self.rule_status_label.config(text="● Active", fg=self.success_color)
            
            # Enable parameter calculation
            self.calc_params_btn.config(state='normal')
            
            # Update display
            self.update_rules_display()
            
        except Exception as e:
            self.log(f"❌ Rule initialization error: {e}")
            self.show_message("Error", f"Rule initialization error: {e}", "error")
    
    def calculate_parameters(self):
        """Calculate trading parameters"""
        if not self.rule_engine:
            self.show_message("Warning", "Please initialize rule engine first", "warning")
            return
            
        try:
            self.log("🧮 Calculating AI trading parameters...")
            
            # Get REAL market data for parameter calculation
            if self.market_analyzer:
                market_data = self.market_analyzer.get_comprehensive_analysis()
                
                if market_data.get("error"):
                    self.log(f"⚠️ Market analysis unavailable: {market_data['error']}")
                    market_data = None
            else:
                market_data = None
            
            # Get account balance for calculations
            balance = self.account_info.get('balance', 10000)
            
            self.trading_params = {
                'base_lot': self.config.get('trading', {}).get('base_lot_size', 0.01),
                'dynamic_spacing': self.config.get('trading', {}).get('min_spacing_points', 100),
                'risk_level': self.config.get('risk_management', {}).get('max_risk_percentage', 2.5),
                'max_positions': min(20, max(5, int(balance / 2000) * 2)),
                'survivability_points': int(balance * 15),
                'market_condition': market_data.get('condition', 'UNKNOWN') if market_data else 'UNKNOWN',
                'volatility_factor': market_data.get('volatility_factor', 1.0) if market_data else 1.0
            }
            
            self.log("✅ Parameters calculated successfully")
            self.log(f"📊 Base Lot: {self.trading_params['base_lot']:.3f}")
            self.log(f"📏 Dynamic Spacing: {self.trading_params['dynamic_spacing']} points")
            self.log(f"🛡️ Risk Level: {self.trading_params['risk_level']:.1f}%")
            self.log(f"🔢 Max Positions: {self.trading_params['max_positions']}")
            
            # Enable trading
            self.start_trading_btn.config(state='normal')
            
        except Exception as e:
            self.log(f"❌ Parameter calculation error: {e}")
            self.show_message("Error", f"Parameter calculation error: {e}", "error")
    
    def start_trading(self):
        """Start AI trading - แบบใหม่ ไม่ใช้ Threading"""
        if not self.rule_engine or not hasattr(self, 'trading_params'):
            self.show_message("Warning", "Please complete initialization first", "warning")
            return
            
        try:
            self.log("🚀 Starting Modern AI Trading System...")
            
            self.is_trading = True
            
            # เปลี่ยนจาก threading เป็น GUI timer
            self.log("🔄 Using GUI-based execution (no threading)")
            self.rule_engine.is_running = True
            
            # Update GUI
            self.start_trading_btn.config(state='disabled')
            self.stop_trading_btn.config(state='normal')
            
            mode = self.trading_mode.get()
            self.log(f"🎯 Trading Mode: {mode}")
            self.log("🧠 Rule Engine: ACTIVE (GUI-based)")
            self.log("📊 Market Analyzer: MONITORING")
            self.log("🎯 Order Manager: READY")
            self.log("💰 Position Manager: MONITORING")
            self.log("📈 System fully operational!")
            
            # Update system status
            self.system_status['engine_running'] = True
            
            # เริ่ม GUI-based rule execution
            self.log("🔄 Starting GUI-based rule execution...")
            self.execute_rule_cycle()  # เรียกทันที
            
        except Exception as e:
            self.log(f"❌ Trading start error: {e}")
            self.show_message("Error", f"Trading start error: {e}", "error")

    def execute_rule_cycle(self):
        """Execute one rule cycle (แทน threading)"""
        try:
            if not self.is_trading or not self.rule_engine:
                return
                
            self.log("🔄 Executing rule cycle...")
            
            # Get market and portfolio data
            try:
                if self.market_analyzer:
                    market_data = self.market_analyzer.get_comprehensive_analysis()
                    self.rule_engine.last_market_data = market_data
                    self.log(f"📊 Market data: {market_data.get('condition', 'UNKNOWN')}")
                else:
                    self.log("⚠️ No market analyzer")
                    
            except Exception as e:
                self.log(f"⚠️ Market data error: {e}")
            
            try:
                if self.position_manager:
                    portfolio_data = self.position_manager.get_portfolio_status()
                    self.rule_engine.last_portfolio_data = portfolio_data
                    self.log(f"💰 Portfolio: {portfolio_data.get('total_positions', 0)} positions")
                else:
                    self.log("⚠️ No position manager")
                    
            except Exception as e:
                self.log(f"⚠️ Portfolio data error: {e}")
            
            # Execute rule-based decision
            try:
                decision_result = self.rule_engine._execute_rule_based_decision()
                
                if decision_result:
                    self.log(f"🎯 Rule Decision: {decision_result.decision.value} (confidence: {decision_result.confidence:.1%})")
                    self.log(f"💭 Reasoning: {decision_result.reasoning}")
                    
                    # Execute the decision
                    self.rule_engine._execute_trading_decision(decision_result)
                    
                    # Track decision
                    if hasattr(self.rule_engine, 'decision_history'):
                        self.rule_engine.decision_history.append(decision_result)
                    if hasattr(self.rule_engine, 'recent_decisions'):
                        self.rule_engine.recent_decisions.append(decision_result)
                        
                else:
                    self.log("🔄 No decision made this cycle")
                    
            except Exception as e:
                self.log(f"❌ Rule execution error: {e}")
            
            # Update rule performances
            try:
                if hasattr(self.rule_engine, '_update_rule_performances'):
                    self.rule_engine._update_rule_performances()
            except Exception as e:
                self.log(f"⚠️ Performance update error: {e}")
            
            # Schedule next cycle (แทน threading)
            if self.is_trading:
                self.root.after(5000, self.execute_rule_cycle)  # ทุก 5 วินาที
                
        except Exception as e:
            self.log(f"❌ Rule cycle error: {e}")
            # ยัง schedule ต่อไปแม้มี error
            if self.is_trading:
                self.root.after(10000, self.execute_rule_cycle)  # รอนานกว่าเมื่อมี error

    def stop_trading(self):
        """Stop AI trading - แบบใหม่"""
        if not self.is_trading:
            return
            
        try:
            self.log("⏹️ Stopping AI Trading System...")
            
            self.is_trading = False
            
            if self.rule_engine:
                self.rule_engine.is_running = False
                # ไม่ต้อง stop thread เพราะใช้ GUI timer
                
            # Update GUI
            self.start_trading_btn.config(state='normal')
            self.stop_trading_btn.config(state='disabled')
            
            # Update system status
            self.system_status['engine_running'] = False
            
            self.log("✅ AI Trading stopped successfully (GUI-based)")
            
        except Exception as e:
            self.log(f"❌ Stop error: {e}")

    # === GUI Update Methods ===
    
    def start_gui_updates(self):
        """Start GUI update loop"""
        self.update_display()
        
    def update_display(self):
        """Update all display elements - NO MOCK DATA"""
        try:
            # Update system status if rule engine is active
            if self.rule_engine and self.is_trading:
                try:
                    self.system_status = self.rule_engine.get_system_status()
                except Exception as e:
                    self.log(f"⚠️ Cannot get system status: {e}")
            
            # Update system monitor
            self.update_system_monitor()
            
            # Update rules monitor
            if self.rule_engine:
                self.update_rules_display()
            
            # Schedule next update
            self.root.after(2000, self.update_display)  # Update every 2 seconds
            
        except Exception as e:
            self.log(f"❌ Display update error: {e}")
            # Still schedule next update
            self.root.after(5000, self.update_display)
    
    def update_system_monitor(self):
        """Update system monitor panel - NO MOCK DATA"""
        try:
            status = self.system_status
            
            # Portfolio health
            health = status.get('portfolio_health', 0) * 100
            health_color = (self.success_color if health > 70 else 
                          self.warning_color if health > 40 else self.error_color)
            self.portfolio_health_label.config(text=f"💚 Portfolio Health: {health:.1f}%", 
                                             fg=health_color)
            
            # Total P&L
            profit = status.get('total_profit', 0)
            profit_color = (self.success_color if profit > 0 else 
                          self.error_color if profit < 0 else self.text_color)
            self.total_pnl_label.config(text=f"💰 Total P&L: ${profit:.2f}", 
                                      fg=profit_color)
            
            # Active positions
            positions = status.get('active_positions', 0)
            self.active_positions_label.config(text=f"📈 Active Positions: {positions}")
            
            # Pending orders
            orders = status.get('pending_orders', 0)
            self.pending_orders_label.config(text=f"⏳ Pending Orders: {orders}")
            
            # Risk level
            risk = status.get('risk_level', 0) * 100
            risk_color = (self.success_color if risk < 30 else 
                         self.warning_color if risk < 70 else self.error_color)
            self.risk_level_label.config(text=f"🛡️ Risk Level: {risk:.1f}%", 
                                       fg=risk_color)
            
            # Survivability
            surv = (1 - status.get('survivability_usage', 0)) * 100
            surv_color = (self.success_color if surv > 70 else 
                         self.warning_color if surv > 40 else self.error_color)
            self.survivability_label.config(text=f"🔋 Survivability: {surv:.1f}%", 
                                          fg=surv_color)
            
        except Exception as e:
            self.log(f"❌ System monitor update error: {e}")
    
    def update_rules_display(self):
        """Update rules monitoring display - NO MOCK DATA"""
        try:
            if not self.rule_engine:
                return
                
            # Overall confidence
            try:
                confidence = self.rule_engine.get_overall_confidence() * 100
                conf_color = (self.success_color if confidence > 70 else 
                             self.warning_color if confidence > 40 else self.error_color)
                self.confidence_label.config(text=f"📊 Overall Confidence: {confidence:.1f}%", 
                                           fg=conf_color)
            except Exception as e:
                self.log(f"⚠️ Cannot get rule confidence: {e}")
                self.confidence_label.config(text="📊 Overall Confidence: --% (unavailable)", 
                                           fg='#888888')
            
            # Market condition
            market_condition = self.system_status.get('market_condition', 'UNKNOWN')
            condition_colors = {
                'TRENDING_UP': self.success_color,
                'TRENDING_DOWN': self.error_color,
                'RANGING': self.warning_color,
                'HIGH_VOLATILITY': '#ff6b35',
                'LOW_VOLATILITY': '#4ecdc4',
                'UNKNOWN': '#888888'
            }
            condition_color = condition_colors.get(market_condition, self.text_color)
            self.market_condition_label.config(text=f"🌍 Market Condition: {market_condition}", 
                                             fg=condition_color)
            
            # Individual rules
            try:
                rules_status = self.rule_engine.get_rules_status()
                self.rules_listbox.delete(0, tk.END)
                
                for rule_name, rule_data in rules_status.items():
                    confidence_pct = rule_data.get('confidence', 0) * 100
                    weight_pct = rule_data.get('weight', 0) * 100
                    active = "🟢" if rule_data.get('active', False) else "🔴"
                    
                    status_text = f"{active} {rule_name.replace('_', ' ').title()}"
                    detail_text = f"    Confidence: {confidence_pct:.0f}% | Weight: {weight_pct:.0f}%"
                    
                    self.rules_listbox.insert(tk.END, status_text)
                    self.rules_listbox.insert(tk.END, detail_text)
                    self.rules_listbox.insert(tk.END, "")  # Separator
                    
            except Exception as e:
                self.log(f"⚠️ Cannot get rules status: {e}")
                self.rules_listbox.delete(0, tk.END)
                self.rules_listbox.insert(tk.END, "Rules status unavailable")
            
            # Last decision
            last_action = self.system_status.get('last_action', 'NONE')
            action_reason = self.system_status.get('action_reason', 'Waiting...')
            
            action_colors = {
                'BUY': self.success_color,
                'SELL': self.error_color,
                'CLOSE_PROFITABLE': self.warning_color,
                'CLOSE_LOSING': '#ff6b35',
                'WAIT': self.text_color,
                'NONE': '#888888'
            }
            action_color = action_colors.get(last_action, self.text_color)
            
            self.last_decision_label.config(text=last_action, fg=action_color)
            self.decision_reason_label.config(text=action_reason)
            
        except Exception as e:
            self.log(f"❌ Rules display update error: {e}")
    
    # === Utility Methods ===
    
    def log(self, message):
        """Add message to system log"""
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_entry = f"[{timestamp}] {message}\n"
            
            self.log_text.insert(tk.END, log_entry)
            self.log_text.see(tk.END)
            
            # Keep log manageable (last 1000 lines)
            lines = int(self.log_text.index('end-1c').split('.')[0])
            if lines > 1000:
                self.log_text.delete('1.0', '100.0')
            
            # Print to console as well for debugging
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
    
    def on_closing(self):
        """Handle window closing"""
        try:
            if self.is_trading:
                if messagebox.askokcancel("Quit", "Trading is active. Stop trading and quit?"):
                    self.stop_trading()
                    self.disconnect_mt5()
                    self.root.destroy()
            else:
                if self.is_connected:
                    self.disconnect_mt5()
                self.root.destroy()
        except Exception as e:
            print(f"Closing error: {e}")
            self.root.destroy()
    
    def run(self):
        """Run the GUI"""
        try:
            # Handle window closing
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            
            # Initial log messages
            self.log("🚀 Modern AI Gold Grid Trading System")
            self.log("🧠 Rule-based Architecture Loaded")
            self.log("⚡ Ready for intelligent trading")
            self.log("")
            self.log("📋 Getting Started:")
            self.log("   1. Click 'Scan Running MT5' to find MT5")
            self.log("   2. Select your preferred MT5 from dropdown")
            self.log("   3. Click 'Connect to Selected'")
            self.log("   4. Initialize Rule Engine")
            self.log("   5. Calculate Parameters")
            self.log("   6. Start AI Trading")
            self.log("")
            
            # Run GUI
            self.root.mainloop()
            
        except Exception as e:
            print(f"GUI error: {e}")


def main():
    """Main function"""
    try:
        print("🚀 Modern AI Gold Grid Trading System")
        print("=" * 60)
        print("✅ Modern Rule-based Architecture")
        print("✅ Adaptive Learning Engine")
        print("✅ Intelligent Order Management") 
        print("✅ Dynamic Risk Management")
        print("✅ Multi-MT5 Support")
        print("⚠️ NO MOCK DATA - PRODUCTION READY")
        print("=" * 60)
        
        # Create and run GUI
        app = ModernRuleBasedTradingGUI()
        app.run()
        
    except Exception as e:
        print(f"❌ Application error: {e}")
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()