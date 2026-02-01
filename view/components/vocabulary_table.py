import flet as ft
from view.services.Alert import AlertService


class VocabularyTable(ft.Container):
    def __init__(self,
                 vocabulary_list: list[dict],
                 on_edit_click=None,
                 on_delete_click=None,
                 on_create_click=None,
                 alert_service: AlertService = None,
                 update_callback=None):
        self.vocabulary_list = vocabulary_list
        self.on_edit_click = on_edit_click
        self.on_delete_click = on_delete_click
        self.on_create_click = on_create_click
        self.alert_service = alert_service
        self.editing_id = None
        self.update_callback = update_callback
        super().__init__(
            content=self.build_table(),
            expand=True,
            padding=10
        )

    def build_table(self):
        rows = []
        # Create new vocabulary row
        create_row = ft.Container(
            content=ft.Row(
                controls=[
                    ft.ElevatedButton(
                        text="+ Create New Vocabulary",
                        expand=True,
                        on_click=lambda e: self.on_create(),
                    ),
                ],
                spacing=10,
            ),
            padding=10,
            bgcolor=ft.Colors.GREEN_100,
        )
        rows.append(create_row)

        # Header row
        header_row = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("Word", weight="bold", width=100),
                    ft.Text("Part of Speech", weight="bold", width=120),
                    ft.Text("Meaning", weight="bold", width=120),
                    ft.Text("English Description", weight="bold", expand=True),
                    ft.Text("Example", weight="bold", expand=True),
                    ft.Text("Edit/Delete", weight="bold", width=100),
                ],
                spacing=10,
            ),
            padding=10,
            bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_100,
        )
        rows.append(header_row)

        # Data rows
        for vocab in self.vocabulary_list:
            # if this row is in edit mode, render textfields + save/cancel
            if self.editing_id == vocab.get("id"):
                w_field = ft.TextField(value=vocab.get("word", ""), width=100)
                pos_field = ft.TextField(value=vocab.get("part_of_speech", ""), width=120)
                meaning_field = ft.TextField(value=vocab.get("vi_meaning", ""), width=120)
                eng_desc_field = ft.TextField(value=vocab.get("eng_description", ""), expand=True, multiline=True)
                example_field = ft.TextField(value=vocab.get("example", ""), expand=True, multiline=True)

                actions_row = ft.Row(
                    controls=[
                        ft.ElevatedButton("Save", on_click=lambda e, vid=vocab.get("id"), wf=w_field, pf=pos_field, mf=meaning_field, edf=eng_desc_field, exf=example_field: self._save_edit(vid, wf, pf, mf, edf, exf)),
                        ft.TextButton("Cancel", on_click=lambda e: self._cancel_edit()),
                    ],
                    spacing=6,
                    width=100,
                )

                row = ft.Container(
                    content=ft.Row(
                        controls=[
                            w_field,
                            pos_field,
                            meaning_field,
                            eng_desc_field,
                            example_field,
                            actions_row,
                        ],
                        spacing=10,
                    ),
                    padding=10,
                    border=ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.GREY_300)),
                )
                rows.append(row)
                continue

            row = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(vocab["word"], width=100),
                        ft.Text(vocab["part_of_speech"], width=120),
                        ft.Text(vocab["vi_meaning"], width=120),
                        ft.Text(vocab["eng_description"], expand=True),
                        ft.Text(vocab["example"], expand=True),
                        ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    tooltip="Edit",
                                    on_click=lambda e, v=vocab: self._start_edit(v),
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    tooltip="Delete",
                                    on_click=lambda e, v=vocab: self.on_delete(v),
                                ),
                            ],
                            spacing=5,
                            width=100,
                        ),
                    ],
                    spacing=10,
                ),
                padding=10,
                border=ft.border.only(
                    bottom=ft.border.BorderSide(1, ft.Colors.GREY_300)),
            )
            rows.append(row)

        return ft.Column(controls=rows, expand=True, scroll=ft.ScrollMode.AUTO)

    def on_create(self):
        # create a form to input new vocabulary and show via alert_service if available
        if not self.alert_service:
            # alert_service is required to open the create dialog — raise explicit error
            raise RuntimeError(
                "AlertService is required to open the create vocabulary dialog")

        word_field = ft.TextField(label="Word", autofocus=True)
        pos_field = ft.TextField(label="Part of speech")
        meaning_field = ft.TextField(label="Vietnamese meaning")
        eng_description_field = ft.TextField(
            label="English description", multiline=True)
        example_field = ft.TextField(label="Example", multiline=True)

        alert = ft.AlertDialog(
            title=ft.Text("Create new vocabulary"),
            content=ft.Container(
                content=ft.Column([word_field, pos_field, meaning_field,
                                  eng_description_field, example_field], spacing=8),
                    padding=10,
                    width=720,
                    height=420,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: self.alert_service.close(alert)),
                ft.TextButton("Create", on_click=lambda e: _create()),
            ],
        )
        self.alert_service.open(alert)

        def _create():
            word = (word_field.value or "").strip()
            part_of_speech = pos_field.value or ""
            vi_meaning = meaning_field.value or ""
            eng_description = eng_description_field.value or ""
            example = example_field.value or ""

            missing = False
            if not word:
                word_field.error_text = "Required"
                missing = True
            if not part_of_speech or not part_of_speech.strip():
                pos_field.error_text = "Required"
                missing = True
            if not vi_meaning or not vi_meaning.strip():
                meaning_field.error_text = "Required"
                missing = True

            if missing:
                try:
                    alert.update()
                except Exception:
                    raise RuntimeError(
                        "Failed to update alert dialog with validation errors")
                finally:
                    return

            # try calling callback with sensible argument patterns
            if self.on_create_click:
                # pass a single dict describing the new vocabulary
                try:
                    self.on_create_click({
                        "word": word,
                        "part_of_speech": part_of_speech,
                        "vi_meaning": vi_meaning,
                        "eng_description": eng_description,
                        "example": example,
                    })
                except Exception:
                    # if the callback fails, raise so caller can handle
                    raise

            self.alert_service.close(alert)

    def on_edit(self, vocabulary):
        if self.on_edit_click:
            payload = {"id": vocabulary["id"]}
            self.on_edit_click(payload)

    def _start_edit(self, vocabulary: dict):
        print(f"Starting edit for vocabulary id {vocabulary.get('id')}")
        # enter inline edit mode for a given vocabulary row
        self.editing_id = vocabulary.get("id")
        self.render()


    def _cancel_edit(self):
        # exit inline edit mode without saving
        self.editing_id = None
        self.render()


    def _save_edit(self, vid, w_field, pos_field, meaning_field, eng_desc_field, example_field):
        # validate inline edit fields
        word = (w_field.value or "").strip()
        part_of_speech = (pos_field.value or "").strip()
        vi_meaning = (meaning_field.value or "").strip()
        eng_description = eng_desc_field.value or ""
        example = example_field.value or ""

        missing = False
        if not word:
            w_field.error_text = "Required"
            missing = True
        if not part_of_speech:
            pos_field.error_text = "Required"
            missing = True
        if not vi_meaning:
            meaning_field.error_text = "Required"
            missing = True

        if missing:
            # show validation errors on the current inline TextFields
            try:
                # update the specific fields so their error_text becomes visible
                w_field.update()
                pos_field.update()
                meaning_field.update()
            except Exception:
                self.render()
            return

        payload = {
            "id": vid,
            "word": word,
            "part_of_speech": part_of_speech,
            "vi_meaning": vi_meaning,
            "eng_description": eng_description,
            "example": example,
        }

        # attempt to call edit callback (if any), but always exit edit mode and refresh
        try:
            if self.on_edit_click:
                self.on_edit_click(payload)
        except Exception:
            # keep validation behavior to caller; re-raise so caller can handle
            raise
        finally:
            # ensure we always leave edit mode and re-render the table
            self.editing_id = None
            self.render()
            
    def on_delete(self, vocabulary):
        # need a alert to confirm deletion
        confirm_alert = ft.AlertDialog(
            title=ft.Text("Confirm Deletion"),
            content=ft.Text(f"Are you sure you want to delete the vocabulary '{vocabulary['word']}'?"),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: self.alert_service.close(confirm_alert)),
                ft.TextButton("Delete", on_click=lambda e: _confirm_delete()),
            ],
        )
        self.alert_service.open(confirm_alert)
        def _confirm_delete():
            self.alert_service.close(confirm_alert)
            if self.on_delete_click:
                payload = {"id": vocabulary["id"]}
                self.on_delete_click(payload)
    

    def render(self):
        self.content = self.build_table()
        if self.update_callback:
            self.update_callback()


if __name__ == "__main__":
    import flet as ft

    def on_edit_click(vocabulary):
        print(f"Editing vocabulary: {vocabulary['word']}")

    sample_vocabulary = [
        {
            "id": 1,
            "word": "Aberration",
            "part_of_speech": "Noun",
            "vi_meaning": "Sự sai lệch",
            "example": "The test results showed an aberration from the norm.",
            "correct_count": 5,
            "wrong_count": 2,
        },
        {
            "id": 2,
            "word": "Cacophony",
            "part_of_speech": "Noun",
            "vi_meaning": "Âm thanh hỗn tạp",
            "example": "The cacophony of the city streets was overwhelming.",
            "correct_count": 3,
            "wrong_count": 4,
        },
    ]

    def main(page: ft.Page):
        vocab_table = VocabularyTable(
            sample_vocabulary, on_edit_click=on_edit_click)
        page.add(vocab_table)

    ft.app(target=main)
