import flet as ft
from view.services.Alert import AlertService

class ParagraphTable(ft.Container):
    def __init__(self,
                 paragraph_list: list[dict],
                 on_continue_click=None,
                 on_edit_click=None,
                 on_delete_click=None,
                 alert_service: AlertService = None,
                 update_callback=None):
        self.paragraph_list = paragraph_list
        self.on_continue_click = on_continue_click
        self.on_edit_click = on_edit_click
        self.on_delete_click = on_delete_click
        self.alert_service = alert_service
        self.update_callback = update_callback
        self.editing_id = None
        super().__init__(
            content=self.build_table(),
            expand=True,
            padding=10
        )

    def build_table(self):
        rows = []
        
        # Header row
        header_row = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("Title", weight="bold", expand=True),
                    ft.Text("Progress", weight="bold", width=80),
                    ft.Text("Status", weight="bold", width=100),
                    ft.Text("Score", weight="bold", width=60),
                    ft.Text("Actions", weight="bold", width=200),
                ],
                spacing=10,
            ),
            padding=10,
            bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_100,
        )
        rows.append(header_row)

        # Data rows
        if not self.paragraph_list:
            empty_row = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text("No paragraphs yet. Create one to get started!", 
                               style=ft.TextThemeStyle.BODY_MEDIUM),
                    ]
                ),
                padding=20,
                alignment=ft.alignment.center,
            )
            rows.append(empty_row)
            return ft.Column(controls=rows, expand=True, scroll=ft.ScrollMode.AUTO)

        for paragraph in self.paragraph_list:
            # Determine status (Open, In-Progress, Completed)
            completed_pct = paragraph.get("completed", 0)
            if completed_pct == 0:
                status = "Open"
                status_color = ft.Colors.GREY_300
            elif completed_pct < 100:
                status = "In-Progress"
                status_color = ft.Colors.ORANGE_300
            else:
                status = "Completed"
                status_color = ft.Colors.GREEN_300

            # Format progress as percentage
            progress_text = f"{int(completed_pct)}%"

            # Format score
            score_text = f"{paragraph.get('score', 0):.1f}" if paragraph.get('score') else "-"

            # Check if this row is in edit mode
            if self.editing_id == paragraph.get("id"):
                title_field = ft.TextField(value=paragraph["title"], expand=True)
                
                action_buttons = [
                    ft.ElevatedButton(
                        text="Save",
                        width=60,
                        on_click=lambda e, pid=paragraph.get("id"), tf=title_field: self._save_edit(pid, tf),
                    ),
                    ft.TextButton(
                        text="Cancel",
                        width=70,
                        on_click=lambda e: self._cancel_edit(),
                    ),
                ]
            else:
                action_buttons = [
                    ft.ElevatedButton(
                        text="Continue" if completed_pct < 100 else "View",
                        width=80,
                        on_click=lambda e, p=paragraph: self._on_continue(p),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.EDIT,
                        tooltip="Edit Title",
                        on_click=lambda e, p=paragraph: self._start_edit(p),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        tooltip="Delete",
                        on_click=lambda e, p=paragraph: self._on_delete(p),
                    ),
                ]

            # Title display or edit
            if self.editing_id == paragraph.get("id"):
                title_widget = title_field
            else:
                title_widget = ft.Text(paragraph["title"], expand=True)

            row = ft.Container(
                content=ft.Row(
                    controls=[
                        title_widget,
                        ft.Text(progress_text, width=80),
                        ft.Container(
                            content=ft.Text(status, color=ft.Colors.BLACK, size=12),
                            bgcolor=status_color,
                            padding=5,
                            border_radius=5,
                            width=100,
                            alignment=ft.alignment.center,
                        ),
                        ft.Text(score_text, width=60),
                        ft.Row(
                            controls=action_buttons,
                            spacing=5,
                            width=200,
                        ),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=10,
                border=ft.border.only(
                    bottom=ft.border.BorderSide(1, ft.Colors.GREY_300)
                ),
            )
            rows.append(row)

        return ft.Column(controls=rows, expand=True, scroll=ft.ScrollMode.AUTO)

    def _on_continue(self, paragraph: dict):
        """Continue or view paragraph - navigate to translation practice view"""
        if self.on_continue_click:
            self.on_continue_click(paragraph)

    def _start_edit(self, paragraph: dict):
        """Enter inline edit mode for paragraph title"""
        self.editing_id = paragraph.get("id")
        self.render()

    def _cancel_edit(self):
        """Cancel inline edit without saving"""
        self.editing_id = None
        self.render()

    def _save_edit(self, paragraph_id: int, title_field: ft.TextField):
        """Save edited title"""
        new_title = (title_field.value or "").strip()
        
        if not new_title:
            title_field.error_text = "Title is required"
            title_field.update()
            return
        
        # Call edit callback
        if self.on_edit_click:
            self.on_edit_click({
                "id": paragraph_id,
                "title": new_title
            })
        
        # Exit edit mode and refresh
        self.editing_id = None
        self.render()

    def _on_delete(self, paragraph: dict):
        """Show delete confirmation dialog"""
        confirm_alert = ft.AlertDialog(
            title=ft.Text("Confirm Deletion"),
            content=ft.Text(f"Are you sure you want to delete the paragraph '{paragraph['title']}'?\n\nThis action cannot be undone."),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: self.alert_service.close(confirm_alert)),
                ft.TextButton("Delete", on_click=lambda e: self._confirm_delete(paragraph, confirm_alert)),
            ],
        )
        if self.alert_service:
            self.alert_service.open(confirm_alert)

    def _confirm_delete(self, paragraph: dict, dialog: ft.AlertDialog):
        """Confirm and execute delete"""
        self.alert_service.close(dialog)
        if self.on_delete_click:
            self.on_delete_click({"id": paragraph["id"]})

    def render(self):
        self.content = self.build_table()
        if self.update_callback:
            self.update_callback()
