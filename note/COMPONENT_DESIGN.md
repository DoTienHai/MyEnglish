# 🧩 Component Design Pattern

## Component là gì?

Component là Flet widget **có state riêng** + **reusable** + **encapsulated logic**.

```python
class MyComponent(ft.Container):
    """
    - Có state riêng (editing_vocab_id, edit_fields, ...)
    - Manage riêng lifecycle
    - Reusable across screens
    - Encapsulate UI + logic
    """
```

## Ví dụ: VocabularyTable Component

```python
# view/components/vocabulary_table.py
import flet as ft
from view.theme import *

class VocabularyTable(ft.Container):
    """
    Reusable component để display + edit vocabulary table
    - Encapsulate: state, logic, UI
    - Manage: editing mode, validation
    """
    
    def __init__(self, home_vm):
        super().__init__(expand=True)
        self.home_vm = home_vm
        
        # ✅ Component state
        self.editing_vocab_id = None
        self.edit_fields = {}  # {vocab_id: {field_name: TextField}}
        
        # ✅ Build initial UI
        self.content = self._build_table()
    
    # ═══════════════════════════════════════════
    # UI Building Methods
    # ═══════════════════════════════════════════
    
    def _build_table(self):
        """Rebuild table từ ViewModel data"""
        all_vocabulary = self.home_vm.get_all_vocabulary()
        
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Word", weight="bold")),
                ft.DataColumn(ft.Text("Vietnamese Meaning", weight="bold")),
                ft.DataColumn(ft.Text("Example", weight="bold")),
                ft.DataColumn(ft.Text("", weight="bold")),
            ],
            rows=[
                self._build_vocabulary_row(v)
                for v in all_vocabulary
            ],
        )
    
    def _build_vocabulary_row(self, vocab_dict):
        """Row có thể ở view mode hoặc edit mode"""
        if self.editing_vocab_id == vocab_dict["id"]:
            return self._build_edit_row(vocab_dict)
        else:
            return self._build_view_row(vocab_dict)
    
    def _build_view_row(self, vocab_dict):
        """View mode: hiển thị Text + Edit button"""
        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(vocab_dict["word"])),
                ft.DataCell(ft.Text(vocab_dict["vi_meaning"])),
                ft.DataCell(ft.Text(vocab_dict["example"])),
                ft.DataCell(
                    ft.IconButton(
                        icon=ft.Icons.EDIT,
                        tooltip="Edit vocabulary",
                        on_click=lambda e, vid=vocab_dict["id"]: self._on_edit_click(vid)
                    )
                ),
            ]
        )
    
    def _build_edit_row(self, vocab_dict):
        """Edit mode: convert thành TextFields"""
        field_word = ft.TextField(
            value=vocab_dict["word"],
            border_color=PRIMARY,
            focused_border_color=PRIMARY_DARK,
            min_lines=1,
            max_lines=1,
            dense=True,
        )
        field_vi_meaning = ft.TextField(
            value=vocab_dict["vi_meaning"],
            border_color=PRIMARY,
            focused_border_color=PRIMARY_DARK,
            min_lines=1,
            max_lines=2,
            dense=True,
        )
        field_example = ft.TextField(
            value=vocab_dict["example"],
            border_color=PRIMARY,
            focused_border_color=PRIMARY_DARK,
            min_lines=2,
            max_lines=3,
            dense=True,
        )
        
        # ✅ Store references để lấy value sau
        self.edit_fields[vocab_dict["id"]] = {
            'word': field_word,
            'vi_meaning': field_vi_meaning,
            'example': field_example,
        }
        
        # ✅ Action buttons: Save (✓ green) & Cancel (✗ red)
        action_cell = ft.Row(
            spacing=4,
            controls=[
                ft.IconButton(
                    icon=ft.Icons.CHECK,
                    icon_color="green",
                    tooltip="Save",
                    on_click=lambda e: self._on_save_click(vocab_dict["id"])
                ),
                ft.IconButton(
                    icon=ft.Icons.CLOSE,
                    icon_color="red",
                    tooltip="Cancel",
                    on_click=lambda e: self._on_cancel_click()
                ),
            ]
        )
        
        return ft.DataRow(
            cells=[
                ft.DataCell(field_word),
                ft.DataCell(field_vi_meaning),
                ft.DataCell(field_example),
                ft.DataCell(action_cell),
            ]
        )
    
    # ═══════════════════════════════════════════
    # Event Handlers
    # ═══════════════════════════════════════════
    
    def _on_edit_click(self, vocab_id: int):
        """Bắt đầu edit mode"""
        if self.editing_vocab_id is not None:
            self._cancel_edit()
        
        self.editing_vocab_id = vocab_id
        self.refresh()
    
    def _on_save_click(self, vocab_id: int):
        """Lưu changes"""
        try:
            fields = self.edit_fields.get(vocab_id, {})
            
            # Get values
            new_word = fields['word'].value.strip()
            new_vi_meaning = fields['vi_meaning'].value.strip()
            new_example = fields['example'].value.strip()
            
            # Validate (UI level)
            if not new_word or not new_vi_meaning:
                print("Error: Fields cannot be empty")
                return
            
            # ✅ Update via ViewModel (Service will validate)
            self.home_vm.save_vocabulary_edit(
                vocab_id, new_word, new_vi_meaning, new_example
            )
            
            # ✅ Clear state
            self.editing_vocab_id = None
            self.edit_fields.clear()
            
            # ✅ Refresh UI
            self.refresh()
            
        except ValueError as e:
            # ✅ Service validation error
            print(f"Validation error: {e}")
        except Exception as ex:
            print(f"Error: {ex}")
    
    def _on_cancel_click(self):
        """Hủy edit"""
        self._cancel_edit()
    
    # ═══════════════════════════════════════════
    # State Management
    # ═══════════════════════════════════════════
    
    def _cancel_edit(self):
        """Internal: reset edit state"""
        self.editing_vocab_id = None
        self.edit_fields.clear()
        self.refresh()
    
    def refresh(self):
        """Rebuild table từ fresh data"""
        self.content = self._build_table()
        self.update()
```

## Component Usage (ở Screen)

```python
# view/screens/home_view.py
class HomeScreen(ft.Container):
    def __init__(self, home_vm: HomeViewModel, switcher=None):
        super().__init__(expand=True, padding=20)
        self.home_vm = home_vm
        self.vocabulary_table_component = None
        self.render()
    
    def build_vocabulary_table(self):
        """Lấy/tạo component"""
        if self.vocabulary_table_component is None:
            # ✅ Inject ViewModel
            self.vocabulary_table_component = VocabularyTable(self.home_vm)
        return self.vocabulary_table_component
    
    def render(self):
        """Build UI"""
        self.content = ft.Column(
            controls=[
                # ✅ Use component
                self.build_vocabulary_table(),
            ]
        )
        self.update()
```

## Component Best Practices

### ✅ DO:

1. **Encapsulate State**
   ```python
   class VocabularyTable(ft.Container):
       def __init__(self, home_vm):
           self.editing_vocab_id = None  # ← State
           self.edit_fields = {}  # ← State
   ```

2. **Manage Lifecycle**
   ```python
   def refresh(self):
       """Rebuild component khi state thay đổi"""
       self.content = self._build_table()
       self.update()
   ```

3. **Call ViewModel Methods**
   ```python
   self.home_vm.save_vocabulary_edit(vocab_id, ...)  # ✅
   ```

4. **Validate Input (UI Level)**
   ```python
   if not new_word or not new_vi_meaning:
       print("Error: Fields cannot be empty")
       return
   ```

5. **Catch Exceptions**
   ```python
   try:
       self.home_vm.create_vocabulary(...)
   except ValueError as e:
       print(f"Error: {e}")
   ```

6. **Reusable (No hardcoded values)**
   ```python
   # ✅ Inject what you need
   def __init__(self, home_vm, theme=None):
       self.home_vm = home_vm
       self.theme = theme or default_theme
   ```

### ❌ DON'T:

1. **Access Service Trực Tiếp**
   ```python
   # ❌ BAD
   self.vocabulary_service.create_vocabulary(...)
   
   # ✅ GOOD
   self.home_vm.create_vocabulary(...)
   ```

2. **Contain Business Logic**
   ```python
   # ❌ BAD
   if vocab.correct_count > 5:  # Business logic ở Component
       self.show_badge()
   
   # ✅ GOOD - Transform in ViewModel
   class VocabularyDTO(TypedDict):
       is_mastered: bool  # ← ViewModel xử lý
   ```

3. **Modify ViewModel State**
   ```python
   # ❌ BAD
   self.home_vm.editing_vocab_id = vocab_id
   
   # ✅ GOOD - Manage trong Component
   self.editing_vocab_id = vocab_id
   ```

4. **Create Circular Dependencies**
   ```python
   # ❌ BAD
   # ViewModel → Component
   # Component → ViewModel
   
   # ✅ GOOD - One-way dependency
   # Screen → Component, Screen → ViewModel
   # Component use ViewModel (không có circular)
   ```

5. **Pass Model Objects**
   ```python
   # ❌ BAD
   def _build_row(self, vocab: Vocabulary):  # Model
       vocab.word  # Full access
   
   # ✅ GOOD
   def _build_row(self, vocab_dict: dict):  # DTO
       vocab_dict["word"]  # Controlled access
   ```

## Component Architecture

```
┌─────────────────────────────────┐
│ VocabularyTable (Component)     │
├─────────────────────────────────┤
│ State:                          │
│ - editing_vocab_id              │
│ - edit_fields                   │
├─────────────────────────────────┤
│ Methods:                        │
│ - _build_table()                │
│ - _build_view_row()             │
│ - _build_edit_row()             │
│ - _on_edit_click()              │
│ - _on_save_click()              │
│ - _on_cancel_click()            │
│ - refresh()                     │
├─────────────────────────────────┤
│ Dependencies:                   │
│ - home_vm (ViewModel) ←         │
└─────────────────────────────────┘
         ↑
    injected from
         ↑
┌─────────────────────────────────┐
│ HomeScreen                      │
├─────────────────────────────────┤
│ build_vocabulary_table()        │
│ → VocabularyTable(home_vm)      │
└─────────────────────────────────┘
```

## Summary

- Component là **reusable widget** với state riêng
- **Encapsulate** logic + UI + state
- **Inject** ViewModel (không Service/Repository)
- **Transform** Model → DTO ở ViewModel
- **Validate** ở Service (Component chỉ UI validation)
- **One-way** dependency (Screen → Component → ViewModel)
- **Refresh** khi state thay đổi
