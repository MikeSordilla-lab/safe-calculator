import flet as ft
import datetime

# --- Logic from your original script ---


def calculate_cycle_data(lmp_date, cycle_length):
    """
    Performs the rhythm method calculations.
    """
    # 1. Calculate Next Period Start
    next_period_start = lmp_date + datetime.timedelta(days=cycle_length)

    # 2. Calculate Ovulation (Standard assumption: 14 days before next period)
    ovulation_date = next_period_start - datetime.timedelta(days=14)

    # 3. Calculate Fertile Window
    # Sperm can survive up to 5 days; Egg survives 12-24 hours (approx 1-2 days margin)
    fertile_start = ovulation_date - datetime.timedelta(days=5)
    fertile_end = ovulation_date + datetime.timedelta(days=2)

    # Safe days logic
    safe_phase_1_end = fertile_start - datetime.timedelta(days=1)
    safe_phase_2_start = fertile_end + datetime.timedelta(days=1)
    safe_phase_2_end = next_period_start - datetime.timedelta(days=1)

    return {
        "lmp": lmp_date,
        "cycle_length": cycle_length,
        "next_period": next_period_start,
        "ovulation": ovulation_date,
        "fertile_start": fertile_start,
        "fertile_end": fertile_end,
        "safe_1_end": safe_phase_1_end,
        "safe_2_start": safe_phase_2_start,
        "safe_2_end": safe_phase_2_end
    }

# --- Mobile App UI ---


def main(page: ft.Page):
    page.title = "Safe Days Calculator"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 390  # Approximate width of a mobile phone
    page.window_height = 844
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20

    # State variables
    selected_date = datetime.date.today()

    # UI Components

    def handle_date_change(e):
        # Update the button text to show selected date
        date_picker_btn.text = e.control.value.strftime("%Y-%m-%d")
        nonlocal selected_date
        selected_date = e.control.value
        page.update()

    date_picker = ft.DatePicker(
        on_change=handle_date_change,
        first_date=datetime.datetime(2020, 1, 1),
        last_date=datetime.datetime(2030, 12, 31),
    )
    # page.overlay.append(date_picker)

    date_picker_btn = ft.ElevatedButton(
        "Select Last Period Date",
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=lambda _: page.open(date_picker),
        width=300
    )

    cycle_slider = ft.Slider(
        min=21, max=35, divisions=14, value=28, label="{value} days"
    )

    cycle_label = ft.Text("Cycle Length: 28 days", size=16)

    def handle_slider_change(e):
        cycle_label.value = f"Cycle Length: {int(e.control.value)} days"
        page.update()

    cycle_slider.on_change = handle_slider_change

    # Results Container
    results_column = ft.Column(visible=False)

    def calculate_click(e):
        try:
            cycle_len = int(cycle_slider.value)

            # Perform calculation
            data = calculate_cycle_data(selected_date, cycle_len)

            # Format dates for display
            fmt = "%a, %b %d"

            # Clear previous results
            results_column.controls.clear()

            # Helper to create result cards
            def create_card(title, date_str, color, icon):
                return ft.Container(
                    content=ft.Row([
                        ft.Icon(icon, color=ft.Colors.WHITE, size=30),
                        ft.Column([
                            ft.Text(title, color=ft.Colors.WHITE70, size=12),
                            ft.Text(date_str, color=ft.Colors.WHITE,
                                    size=16, weight=ft.FontWeight.BOLD),
                        ], spacing=2)
                    ], alignment=ft.MainAxisAlignment.START),
                    bgcolor=color,
                    padding=15,
                    border_radius=10,
                    width=300,
                )

            # Add result cards
            results_column.controls.extend([
                ft.Divider(),
                ft.Text("Your Cycle Report", size=20,
                        weight=ft.FontWeight.BOLD),

                create_card("Next Period Starts",
                            data['next_period'].strftime(fmt),
                            ft.Colors.RED_400,
                            ft.Icons.WATER_DROP),

                create_card("Estimated Ovulation",
                            data['ovulation'].strftime(fmt),
                            ft.Colors.PURPLE_400,
                            ft.Icons.EGG_ALT),

                ft.Container(
                    content=ft.Column([
                        ft.Row([ft.Icon(ft.Icons.CHILD_CARE, color=ft.Colors.WHITE), ft.Text(
                            "Fertile Window (High Risk)", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)]),
                        ft.Text(
                            f"{data['fertile_start'].strftime(fmt)} - {data['fertile_end'].strftime(fmt)}", color=ft.Colors.WHITE, size=16)
                    ]),
                    bgcolor=ft.Colors.ORANGE_400,
                    padding=15,
                    border_radius=10,
                    width=300
                ),

                ft.Text("Safe Days (Lower Risk)", size=16,
                        weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN),

                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            f"Phase 1: Until {data['safe_1_end'].strftime(fmt)}"),
                        ft.Text(
                            f"Phase 2: From {data['safe_2_start'].strftime(fmt)}"),
                    ]),
                    bgcolor=ft.Colors.GREEN_50,
                    padding=10,
                    border_radius=10,
                    border=ft.border.all(1, ft.Colors.GREEN_200),
                    width=300
                ),

                ft.Text("Disclaimer: Estimation only. Not medical advice.",
                        size=10, italic=True, color=ft.Colors.GREY)
            ])

            results_column.visible = True
            page.update()

        except Exception as ex:
            print(f"Error: {ex}")

    calc_button = ft.ElevatedButton(
        "Calculate Safe Days",
        icon=ft.Icons.CALCULATE,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.PINK_500,
            color=ft.Colors.WHITE,
            padding=15,
        ),
        width=300,
        on_click=calculate_click
    )

    # Layout
    page.add(
        ft.Column(
            [
                ft.Container(
                    content=ft.Icon(ft.Icons.HEALTH_AND_SAFETY,
                                    size=60, color=ft.Colors.PINK_400),
                    alignment=ft.alignment.center,
                    padding=20
                ),
                ft.Text("Safe Cycle Tracker", size=24,
                        weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),

                ft.Text("1. Select Last Period Date",
                        weight=ft.FontWeight.BOLD),
                date_picker_btn,

                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),

                ft.Text("2. Average Cycle Length", weight=ft.FontWeight.BOLD),
                cycle_label,
                cycle_slider,

                ft.Divider(height=30, color=ft.Colors.TRANSPARENT),

                calc_button,
                results_column
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
