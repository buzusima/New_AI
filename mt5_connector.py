"""
🔍  MT5 Multi-Installation Detector
แค่หา MT5 ทุกตัว แล้วให้ลูกค้าเลือกเอง - เรียบง่าย ไม่ซับซ้อน
"""

import MetaTrader5 as mt5
import os
import time
import re
from datetime import datetime
import psutil
import winreg
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class MT5Installation:
    """ข้อมูล MT5 Installation แบบง่ายๆ"""
    path: str
    broker: str = "Unknown"
    executable_type: str = ""  # terminal64.exe or terminal.exe
    is_running: bool = False
    data_path: str = ""

class MT5AutoConnector:
    """
    🔍  MT5 Multi-Installation Connector
    
    ฟีเจอร์:
    - หา MT5 ทุกตัวในเครื่อง
    - แสดงรายการให้เลือก
    - ไม่มีการให้คะแนน ไม่ซับซ้อน
    """
    
    def __init__(self):
        self.is_connected = False
        self.gold_symbol = None
        self.account_info = {}
        self.symbol_info = {}
        self.selected_mt5 = None
        
        # เก็บรายการ MT5 ทั้งหมดที่เจอ
        self.available_installations: List[MT5Installation] = []
        
        # Gold symbol variations
        self.gold_symbols = [
            "XAUUSD", "GOLD", "XAU/USD", "XAUUSD.cmd", "GOLD#", 
            "XAUUSD.", "XAUUSD-", "XAU-USD", "GOLD.", "GOLD_",
            "XAUUSD.raw", "XAUUSD.ecn", "GOLDmicro", "XAUUSD.m",
            "XAUUSD_", "XAUUSD#", "XAUUSDpro", "GOLD.std"
        ]
        
    def find_all_mt5_installations(self) -> List[MT5Installation]:
        """
        🔍 หา MT5 ทุกตัวในเครื่อง
        Returns: List ของ MT5Installation objects
        """
        installations = []
        found_paths = set()  # เพื่อป้องกัน duplicate
        
        print("🔍 หา MT5 ทุกตัวในเครื่อง...")
        
        # Method 1: Registry
        installations.extend(self._scan_registry(found_paths))
        
        # Method 2: Common directories
        installations.extend(self._scan_common_paths(found_paths))
        
        # Method 3: Running processes
        installations.extend(self._scan_running_processes(found_paths))
        
        # เพิ่มข้อมูลพื้นฐาน
        for installation in installations:
            installation.broker = self._detect_broker_name(installation.path)
            
        self.available_installations = installations
        
        if installations:
            print(f"✅ เจอ MT5 ทั้งหมด {len(installations)} ตัว")
        else:
            print("❌ ไม่เจอ MT5 เลย")
            
        return installations
    
    def _scan_registry(self, found_paths: set) -> List[MT5Installation]:
        """สแกน Registry หา MT5"""
        installations = []
        
        registry_paths = [
            (winreg.HKEY_CURRENT_USER, "SOFTWARE\\MetaQuotes\\Terminal"),
            (winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\MetaQuotes\\Terminal"),
            (winreg.HKEY_CURRENT_USER, "SOFTWARE\\WOW6432Node\\MetaQuotes\\Terminal"),
            (winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\WOW6432Node\\MetaQuotes\\Terminal")
        ]
        
        for root, base_path in registry_paths:
            try:
                with winreg.OpenKey(root, base_path) as terminal_key:
                    i = 0
                    while True:
                        try:
                            subkey_name = winreg.EnumKey(terminal_key, i)
                            subkey_path = f"{base_path}\\{subkey_name}"
                            
                            with winreg.OpenKey(root, subkey_path) as installation_key:
                                try:
                                    data_path = winreg.QueryValueEx(installation_key, "DataPath")[0]
                                    exe_dir = os.path.dirname(data_path)
                                    
                                    # หา executable
                                    for exe_name in ["terminal64.exe", "terminal.exe"]:
                                        exe_path = os.path.join(exe_dir, exe_name)
                                        if os.path.exists(exe_path) and exe_path not in found_paths:
                                            installation = MT5Installation(
                                                path=exe_path,
                                                data_path=data_path,
                                                executable_type=exe_name
                                            )
                                            installations.append(installation)
                                            found_paths.add(exe_path)
                                            break
                                except FileNotFoundError:
                                    pass
                                    
                            i += 1
                        except OSError:
                            break
                            
            except FileNotFoundError:
                continue
                
        return installations
    
    def _scan_common_paths(self, found_paths: set) -> List[MT5Installation]:
        """สแกนโฟลเดอร์ทั่วไป"""
        installations = []
        
        common_paths = [
            # User directories
            os.path.expanduser("~/AppData/Roaming/MetaQuotes/Terminal"),
            
            # Program Files
            "C:/Program Files/MetaTrader 5",
            "C:/Program Files (x86)/MetaTrader 5",
            "C:/Program Files/MetaQuotes/MetaTrader 5", 
            "C:/Program Files (x86)/MetaQuotes/MetaTrader 5",
            
            # Other common locations
            "D:/MetaTrader 5",
            "C:/MetaTrader5",
            "D:/MetaTrader5"
        ]
        
        for base_path in common_paths:
            if os.path.exists(base_path):
                # ลองในโฟลเดอร์หลัก
                for exe_name in ["terminal64.exe", "terminal.exe"]:
                    exe_path = os.path.join(base_path, exe_name)
                    if os.path.exists(exe_path) and exe_path not in found_paths:
                        installation = MT5Installation(
                            path=exe_path,
                            executable_type=exe_name
                        )
                        installations.append(installation)
                        found_paths.add(exe_path)
                
                # ลองใน subdirectories (broker folders)
                try:
                    for item in os.listdir(base_path):
                        item_path = os.path.join(base_path, item)
                        if os.path.isdir(item_path):
                            for exe_name in ["terminal64.exe", "terminal.exe"]:
                                exe_path = os.path.join(item_path, exe_name)
                                if os.path.exists(exe_path) and exe_path not in found_paths:
                                    installation = MT5Installation(
                                        path=exe_path,
                                        executable_type=exe_name
                                    )
                                    installations.append(installation)
                                    found_paths.add(exe_path)
                except OSError:
                    pass
                    
        return installations
    
    def _scan_running_processes(self, found_paths: set) -> List[MT5Installation]:
        """สแกนจาก running processes"""
        installations = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    if proc.info['name'] and 'terminal' in proc.info['name'].lower():
                        if proc.info['exe'] and proc.info['exe'] not in found_paths:
                            # ตรวจสอบว่าเป็น MT5 จริงๆ
                            if self._looks_like_mt5(proc.info['exe']):
                                installation = MT5Installation(
                                    path=proc.info['exe'],
                                    is_running=True,
                                    executable_type=os.path.basename(proc.info['exe'])
                                )
                                installations.append(installation)
                                found_paths.add(proc.info['exe'])
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception:
            pass
            
        return installations
    
    def _looks_like_mt5(self, exe_path: str) -> bool:
        """เช็คคร่าวๆ ว่าน่าจะเป็น MT5"""
        path_lower = exe_path.lower()
        return ('metatrader' in path_lower or 
                'terminal64' in path_lower or 
                'terminal.exe' in path_lower)
    
    def _detect_broker_name(self, exe_path: str) -> str:
        """ตรวจจับชื่อ broker จาก path"""
        path_lower = exe_path.lower()
        
        # รายชื่อ broker ที่รู้จัก
        known_brokers = {
            'exness': 'Exness',
            'icmarkets': 'IC Markets', 
            'ic markets': 'IC Markets',
            'pepperstone': 'Pepperstone',
            'fxtm': 'FXTM',
            'xm': 'XM',
            'fxpro': 'FXPro',
            'avatrade': 'AvaTrade',
            'tickmill': 'Tickmill',
            'admiral': 'Admiral Markets'
        }
        
        for key, name in known_brokers.items():
            if key in path_lower:
                return name
                
        return "Unknown"
    
    def connect_to_installation(self, installation_index: int) -> bool:
        """
        เชื่อมต่อไปยัง MT5 installation ตัวที่เลือก
        
        Args:
            installation_index: index ใน available_installations list
            
        Returns:
            True ถ้าเชื่อมต่อสำเร็จ
        """
        if installation_index < 0 or installation_index >= len(self.available_installations):
            print("❌ เลือก installation ไม่ถูกต้อง")
            return False
            
        installation = self.available_installations[installation_index]
        self.selected_mt5 = installation
        
        return self._attempt_connection(installation)
    
    def auto_connect(self) -> bool:
        """
        Auto-connect แบบใหม่:
        - ถ้ามี MT5 ตัวเดียว -> เชื่อมต่อเลย
        - ถ้ามีหลายตัว -> ให้เลือก
        """
        print("🔗 เริ่มการเชื่อมต่อ MT5...")
        
        # หา MT5 ทั้งหมด
        installations = self.find_all_mt5_installations()
        
        if not installations:
            print("❌ ไม่เจอ MT5 ในเครื่อง")
            return False
            
        # ถ้ามีตัวเดียว -> เชื่อมต่อเลย
        if len(installations) == 1:
            print(f"📱 เจอ MT5 ตัวเดียว: {installations[0].broker}")
            return self.connect_to_installation(0)
            
        # ถ้ามีหลายตัว -> แสดงให้เลือก
        print(f"\n📋 เจอ MT5 ทั้งหมด {len(installations)} ตัว:")
        for i, inst in enumerate(installations):
            status = "🟢 กำลังทำงาน" if inst.is_running else "⚫ หยุดทำงาน"
            exe_type = "64-bit" if "64" in inst.executable_type else "32-bit"
            
            print(f"  {i+1}. {inst.broker} ({exe_type}) - {status}")
            print(f"     📁 {inst.path}")
            
        print(f"\n❓ กรุณาเลือก MT5 ที่ต้องการใช้ (1-{len(installations)}):")
        print("   หรือใช้ connect_to_installation(index) ใน code")
        
        return False  # ให้ user เลือกเอง
    
    def _attempt_connection(self, installation: MT5Installation) -> bool:
        """ลองเชื่อมต่อกับ MT5 installation"""
        try:
            print(f"🔗 กำลังเชื่อมต่อ: {installation.broker}")
            print(f"📁 Path: {installation.path}")
            
            # Start MT5 ถ้ายังไม่ทำงาน
            if not installation.is_running:
                print(f"🚀 กำลังเริ่ม MT5...")
                os.startfile(installation.path)
                time.sleep(5)
                
            # Initialize MT5
            if not mt5.initialize():
                print(f"❌ ไม่สามารถ initialize MT5 ได้")
                return False
                
            # Get account info
            account_info = mt5.account_info()
            if account_info is None:
                print("❌ ไม่มี account login")
                return False
                
            print(f"✅ เชื่อมต่อ account: {account_info.login}")
            print(f"💰 ยอดเงิน: ${account_info.balance:,.2f}")
            print(f"🏦 โบรกเกอร์: {account_info.company}")
            
            # Detect gold symbol
            gold_symbol = self.detect_gold_symbol()
            if not gold_symbol:
                print("⚠️ ไม่เจอสัญลักษณ์ทองคำ")
                # ไม่ return False เพราะอาจจะเทรดอย่างอื่น
                
            if gold_symbol:
                print(f"🥇 สัญลักษณ์ทองคำ: {gold_symbol}")
            
            # เก็บข้อมูลการเชื่อมต่อ
            self.is_connected = True
            self.account_info = {
                'login': account_info.login,
                'balance': account_info.balance,
                'equity': account_info.equity,
                'margin': account_info.margin,
                'free_margin': account_info.margin_free,
                'leverage': account_info.leverage,
                'company': account_info.company,
                'currency': account_info.currency
            }
            
            self.gold_symbol = gold_symbol
            
            return True
            
        except Exception as e:
            print(f"❌ เชื่อมต่อไม่สำเร็จ: {e}")
            return False
    
    # === Gold Symbol Detection (ใช้โค้ดเดิม) ===
    
    def detect_gold_symbol(self):
        """ตรวจจับสัญลักษณ์ทองคำ"""
        try:
            all_symbols = mt5.symbols_get()
            if not all_symbols:
                return None
                
            symbol_names = [symbol.name for symbol in all_symbols]
            
            # Method 1: Exact match
            for gold_sym in self.gold_symbols:
                if gold_sym in symbol_names:
                    if self.verify_gold_symbol(gold_sym):
                        return gold_sym
                        
            # Method 2: Pattern matching
            gold_patterns = [
                r'^XAU.*USD.*$',
                r'^GOLD.*$',
                r'^.*GOLD.*$',
                r'^XAU.*$'
            ]
            
            for pattern in gold_patterns:
                for symbol_name in symbol_names:
                    if re.match(pattern, symbol_name, re.IGNORECASE):
                        if self.verify_gold_symbol(symbol_name):
                            return symbol_name
                            
            return None
            
        except Exception as e:
            print(f"Error detecting gold symbol: {e}")
            return None
    
    def verify_gold_symbol(self, symbol):
        """ตรวจสอบว่าเป็นสัญลักษณ์ทองคำจริง"""
        try:
            symbol_info = mt5.symbol_info(symbol)
            if not symbol_info:
                return False
                
            if not symbol_info.visible:
                if not mt5.symbol_select(symbol, True):
                    return False
                    
            tick = mt5.symbol_info_tick(symbol)
            if tick and tick.bid:
                price = tick.bid
                if 1000 <= price <= 5000:  # Gold price range
                    return True
                    
            return True
            
        except Exception as e:
            print(f"Error verifying gold symbol {symbol}: {e}")
            return False
    
    # === Utility Methods ===
    
    def get_installation_list(self) -> List[Dict]:
        """ส่งออกรายการ installations สำหรับ GUI"""
        return [
            {
                'index': i,
                'broker': inst.broker,
                'path': inst.path,
                'executable_type': inst.executable_type,
                'is_running': inst.is_running,
                'display_name': f"{inst.broker} ({'64-bit' if '64' in inst.executable_type else '32-bit'})"
            }
            for i, inst in enumerate(self.available_installations)
        ]
    
    def disconnect(self):
        """ตัดการเชื่อมต่อ"""
        try:
            if self.is_connected:
                mt5.shutdown()
                self.is_connected = False
                self.gold_symbol = None
                self.account_info = {}
                self.symbol_info = {}
                print("✅ ตัดการเชื่อมต่อเรียบร้อย")
                return True
        except Exception as e:
            print(f"Error disconnecting: {e}")
            
        return False

# === Test Function ===

def test_connector():
    """ทดสอบ  Connector"""
    print("🧪 ทดสอบ  MT5 Connector...")
    print("=" * 50)
    
    connector = MT5AutoConnector()
    
    # Test 1: หา installations ทั้งหมด
    installations = connector.find_all_mt5_installations()
    
    if not installations:
        print("❌ ไม่เจอ MT5")
        return
        
    # Test 2: แสดงรายการ
    print(f"\n📊 รายการ MT5 ที่เจอ:")
    for i, inst in enumerate(installations):
        status = "🟢" if inst.is_running else "⚫"
        exe_type = "64-bit" if "64" in inst.executable_type else "32-bit"
        print(f"  {i}: {status} {inst.broker} ({exe_type})")
        print(f"     {inst.path}")
    
    # Test 3: ทดสอบการเชื่อมต่อกับตัวแรก
    print(f"\n🔗 ทดสอบเชื่อมต่อกับตัวแรก...")
    if connector.connect_to_installation(0):
        print("🎉 เชื่อมต่อสำเร็จ!")
        print(f"   Account: {connector.account_info.get('login')}")
        print(f"   Broker: {connector.account_info.get('company')}")
        print(f"   Gold: {connector.gold_symbol}")
        
        # ทดสอบตัดการเชื่อมต่อ
        connector.disconnect()
    else:
        print("❌ เชื่อมต่อไม่สำเร็จ")

if __name__ == "__main__":
    test_connector()