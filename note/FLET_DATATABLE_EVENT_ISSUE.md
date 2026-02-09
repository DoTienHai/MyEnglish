# Flet DataTable Event Handler Issue

## 🔴 Problem

**DataTable with nested event handlers doesn't work reliably in embedded contexts**

```python
# ❌ DON'T USE THIS - Event handlers don't fire
ft.DataTable(
    rows=[
        ft.DataRow(
            cells=[
                ft.DataCell(
                    ft.IconButton(
                        icon=ft.Icons.EDIT,
                        on_click=lambda e: handle_click()  # ❌ Doesn't work in HomeView
                    )
                )
            ]
        )
    ]
)
```

## 📝 Symptoms

- Works fine when component is standalone (in `__main__` block)
- **Stops working when embedded in complex views** (e.g., HomeScreen → Tabs → Tab → VocabularyTable)
- Button appears but click doesn't trigger `on_click` handler
- Console shows no errors

Example:
```
VocabularyTable.py (standalone) ✅ Button works
HomeScreen → build_vocabulary_table() ❌ Button doesn't work
```

## 🔍 Root Cause

**Flet DataTable has event handler nesting issue:**

1. Event is nested 4+ layers deep:
   ```
   IconButton
   ↑ (on_click event)
   DataCell (doesn't forward events well)
   ↑
   DataRow (doesn't forward events well)
   ↑
   DataTable
   ```

2. When DataTable is deeply nested in view hierarchy:
   ```
   Page
   ↓
   Column (HomeScreen.content)
   ↓
   Tabs
   ↓
   Tab.content
   ↓
   VocabularyTable (Container)
   ↓
   DataTable ← Event bubble gets lost here
   ```

3. **DataCell and DataRow don't properly forward click events up the tree**
   - They consume the event or block propagation
   - Works in simple render trees, fails in complex nested structures
   - This is a Flet framework limitation

## ✅ Solution: Use Column + Row instead of DataTable

```python
# ✅ USE THIS - Works reliably
def build_table(self):
    rows = []
    
    # Header row
    rows.append(ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("Word", weight="bold", width=100),
                ft.Text("Action", weight="bold", width=60),
            ]
        ),
        padding=10,
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_100,
    ))
    
    # Data rows
    for vocab in self.vocabulary_list:
        rows.append(ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(vocab["word"], width=100),
                    ft.IconButton(
                        icon=ft.Icons.EDIT,
                        on_click=lambda e, v=vocab: self.on_edit(v),  # ✅ Works!
                    ),
                ]
            ),
            padding=10,
            border=ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.GREY_300)),
        ))
    
    return ft.Column(controls=rows, expand=True, scroll=ft.ScrollMode.AUTO)
```

## Why This Works

- **Fewer nesting layers**: IconButton → Row → Container (3 layers vs 4+)
- **Column and Row are layout containers** - they reliably forward events
- **Container forwards events** - acts as transparent wrapper
- Event bubble path is simple and direct

## 📋 Nesting Comparison

```
DATATABLE (❌ Broken)          COLUMN+ROW (✅ Works)
─────────────────────────────────────────────────────
IconButton                      IconButton
  ↓                              ↓
DataCell (blocks events)        Row (forwards events)
  ↓                              ↓
DataRow (blocks events)         Container (transparent)
  ↓                              ↓
DataTable (consumes)            Column (forwards)
```

## 🛑 When Caching Doesn't Help

**Important:** Caching component instance helps with state/callback preservation, but **does NOT fix the DataTable nesting issue**:

```python
# ❌ This still won't work, even with caching
if self.vocabulary_table is None:
    self.vocabulary_table = VocabularyTable(DataTable(...))  # Still broken
    
# ✅ Must change to Column+Row structure
if self.vocabulary_table is None:
    self.vocabulary_table = VocabularyTable(Column+Row(...))  # Now works
```

## ✨ Best Practices

1. **Avoid DataTable for interactive rows** - use Column + Row + Container instead
2. **Keep event handler nesting shallow** - max 3-4 layers
3. **Use layout containers (Column/Row) between interactive elements and deeply nested views**
4. **Always cache components with callbacks** in parent views:
   ```python
   class HomeScreen(ft.Container):
       def __init__(self):
           self.vocabulary_table = None  # Cache
           
       def build_vocabulary_table(self):
           if self.vocabulary_table is None:
               self.vocabulary_table = VocabularyTable(
                   data,
                   on_edit_click=self._handle_edit
               )
           return self.vocabulary_table
   ```

## 📌 Recommendation for MyEnglish

- **Replace all DataTables with Column+Row+Container** when they contain interactive elements
- DataTable is fine for **read-only** display
- Use Column+Row pattern for **any table with buttons/inputs**
- Always cache components with callbacks

## Example: Before vs After

### Before (Broken)
```python
class VocabularyTable(ft.Container):
    def build_table(self):
        return ft.DataTable(
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(vocab["word"])),
                        ft.DataCell(
                            ft.IconButton(
                                on_click=lambda e, v=vocab: self.on_edit(v)  # ❌
                            )
                        ),
                    ]
                )
                for vocab in self.vocabulary_list
            ]
        )
```

### After (Working)
```python
class VocabularyTable(ft.Container):
    def build_table(self):
        rows = []
        for vocab in self.vocabulary_list:
            rows.append(ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(vocab["word"]),
                        ft.IconButton(
                            on_click=lambda e, v=vocab: self.on_edit(v)  # ✅
                        ),
                    ]
                ),
                padding=10,
            ))
        return ft.Column(controls=rows, expand=True)
```

---

**Related:** See `QUICK_REFERENCE.md` for Flet component best practices
