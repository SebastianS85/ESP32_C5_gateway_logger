from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex

class CANTableModel(QAbstractTableModel):
    def __init__(self, frames=None):
        super().__init__()
        # Całkowita, nieograniczona historia sesji w tle
        self.full_history = []
        
        self._headers = ["No.", "Time / Delta", "Bus", "CAN ID (Hex)", "DLC", "Payload Data (Hex)", "DBC Signals"]
        self._is_delta_mode = False
        self._update_existing_ids = False
        self._enabled_ids = None
        
        # Parametry wirtualnego okna (widzimy np. max 20 000 wierszy naraz dla idealnej płynności)
        self._window_size = 20000
        self._window_offset = 0

    def rowCount(self, parent=None):
        # Tabela zgłasza systemowi tyle wierszy, ile wynosi CAŁA historia, 
        # dzięki czemu suwak przewijania ma poprawny rozmiar dla 2 milionów ramek!
        return len(self.full_history)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        
        row = index.row()
        if row >= len(self.full_history):
            return None

        # Pobieramy dane bezpośrednio z gigantycznej historii w tle
        frame = self.full_history[row]

        if role == Qt.ItemDataRole.DisplayRole:
            col = index.column()
            if col == 0:
                return str(frame['no'])
            elif col == 1:
                return frame['time']
            elif col == 2:
                return f"CAN {frame['node_id']}"
            elif col == 3:
                clean_id = frame['clean_id']
                return f"0x{clean_id:03X}" if clean_id <= 0x7FF else f"0x{clean_id:08X} (Ext)"
            elif col == 4:
                return str(frame['len'])
            elif col == 5:
                return " ".join(f"{b:02X}" for b in frame['raw_data'][:frame['len']])
            elif col == 6:
                return frame['dbc_str']

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            if 0 <= section < len(self._headers):
                return self._headers[section]
        return None

    def update_headers(self, new_headers):
        self.beginResetModel()
        self._headers = new_headers
        self.endResetModel()

    def set_max_frames(self, max_f):
        pass

    def set_enabled_ids(self, enabled_ids):
        self._enabled_ids = enabled_ids
        self.beginResetModel()
        self.endResetModel()

    def set_update_existing_ids(self, val):
        self._update_existing_ids = val

    def update_time_display(self, is_delta):
        self._is_delta_mode = is_delta
        self.beginResetModel()
        self.endResetModel()

    def add_frames(self, new_frames, autoscroll_active=True):
        """Dodaje nowe ramki z obsługą nadpisywania istniejących ID oraz autoscrolla."""
        if not new_frames:
            return
        
        filtered = []
        for fr in new_frames:
            if self._enabled_ids is not None and fr['clean_id'] not in self._enabled_ids:
                continue
            filtered.append(fr)

        if not filtered:
            return

        # Jeśli włączona jest opcja nadpisywania po ID (Update Existing IDs)
        if getattr(self, '_update_existing_ids', False):
            # Tworzymy słownik szybkiego dostępu do pozycji ID w pełnej historii
            # (zakładając, że szukamy ostatnio dodanych lub mapujemy ID -> indeks)
            updated_any = False
            
            for fr in filtered:
                target_id = fr['clean_id']
                # Szukamy czy to ID już istnieje w pełnej historii
                found_idx = -1
                for idx, existing_fr in enumerate(self.full_history):
                    if existing_fr['clean_id'] == target_id:
                        found_idx = idx
                        break
                
                if found_idx != -1:
                    # NADPISUJEMY w miejscu w pełnej historii
                    self.full_history[found_idx] = fr
                    updated_any = True
                else:
                    # Jeśli nie ma, dopisujemy na koniec historii
                    self.full_history.append(fr)
            
            # Jeśli coś się zmieniło, odświeżamy widok tabeli
            if updated_any:
                top_left = self.index(0, 0)
                bottom_right = self.index(len(self.full_history) - 1, len(self._headers) - 1)
                self.dataChanged.emit(top_left, bottom_right, [Qt.ItemDataRole.DisplayRole])
            else:
                self.beginResetModel()
                self.endResetModel()
            return

        # --- Standardowy tryb (bez nadpisywania) ---
        total_old_len = len(self.full_history)

        if autoscroll_active:
            # Tryb LIVE / Autoscroll WŁĄCZjony: nowe ramki idą na samą górę
            filtered.reverse()
            count = len(filtered)
            self.beginInsertRows(QModelIndex(), 0, count - 1)
            self.full_history[0:0] = filtered
            self.endInsertRows()
        else:
            # Tryb ZAMROŻONY / Autoscroll WYŁĄCZONY: ramki dopisują się na sam dół
            count = len(filtered)
            self.beginInsertRows(QModelIndex(), total_old_len, total_old_len + count - 1)
            self.full_history.extend(filtered)
            self.endInsertRows()
    def set_update_existing_ids(self, val):
        self._update_existing_ids = val
        
    def bulk_add_frames(self, new_frames):
        """Wczytywanie z pliku."""
        if not new_frames:
            return
        total_old_len = len(self.full_history)
        count = len(new_frames)
        self.beginInsertRows(QModelIndex(), total_old_len, total_old_len + count - 1)
        self.full_history.extend(new_frames)
        self.endInsertRows()

    def clear_data(self):
        self.beginResetModel()
        self.full_history.clear()
        self.endResetModel()

    