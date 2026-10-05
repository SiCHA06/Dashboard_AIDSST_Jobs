# Style Requirements & UI Override (Dark Neon Aesthetic)

**Target System:** Antigravity (Dashboard Generation Agent)
**Reference Material:** "image_d14a62.jpg"
**Objective:** Override the default UI and styling of the existing Python/Dash application to exactly match the deep dark theme, neon gradients, and flat component design shown in the reference image.

## 1. Global Color Palette

Define these variables in your CSS or Python layout dictionaries to ensure consistency across the entire application.

**Backgrounds:**
*   **App/Body Background:** `#12131F` (Deep dark indigo/slate)
*   **Sidebar Background:** `#0B0C15` (Slightly darker than the body)
*   **Card/Chart Container Background:** `#1C1D2D` (Elevated dark slate)

**Typography:**
*   **Primary Text (Values, Main Titles):** `#FFFFFF` (Pure White)
*   **Secondary Text (Labels, Axis, Sidebar Items):** `#8C8E9F` (Muted gray/blue)

**Accent Colors & Gradients (Neon/Cyberpunk Vibe):**
*   **Accent 1 (Magenta/Purple):** Solid: `#C738FF` | Gradient: `linear-gradient(135deg, #FF6BFF 0%, #C738FF 100%)`
*   **Accent 2 (Cyan/Aqua):** Solid: `#00E5FF` | Gradient: `linear-gradient(135deg, #00E5FF 0%, #0088FF 100%)`

## 2. Layout & Component Styling (CSS / Dash Bootstrap)

Apply these rules to the standard `dash-bootstrap-components` or custom HTML elements.

*   **Global Font:** Use a modern, geometric sans-serif font (e.g., `Inter`, `Poppins`, or `Roboto`).
*   **Cards (`dbc.Card` or custom div):**
    *   `background-color: #1C1D2D;`
    *   `border: none;` (No visible borders)
    *   `border-radius: 16px;` (Pronounced rounded corners)
    *   `box-shadow: 0px 8px 24px rgba(0, 0, 0, 0.2);`
    *   `padding: 20px;`
*   **KPI / Metric Cards (Top Row):**
    *   Instead of the standard card background, apply the gradient backgrounds directly to the card container.
    *   Card 1: `background: linear-gradient(135deg, #FF6BFF, #C738FF);`
    *   Card 2: `background: linear-gradient(135deg, #00E5FF, #0088FF);`
    *   Ensure all text inside these specific metric cards is `#FFFFFF`.
*   **Sidebar Menu:**
    *   Active menu items should have a left border accent (`border-left: 4px solid #C738FF;`) and a subtle linear gradient background (e.g., `linear-gradient(90deg, rgba(199,56,255,0.2) 0%, transparent 100%)`).

## 3. Plotly Chart Styling (CRITICAL for "Neon" Look)

To make Plotly charts look like the reference image, you MUST update the `layout` and `traces` with the following parameters.

### General Plotly Layout Update (`fig.update_layout`)
```python
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
    paper_bgcolor='rgba(0,0,0,0)', # Transparent paper background
    font=dict(color='#8C8E9F', family='Inter, sans-serif'),
    margin=dict(l=20, r=20, t=40, b=20),
    xaxis=dict(
        showgrid=True, 
        gridcolor='#28293D', # Very subtle dark gridlines
        gridwidth=1, 
        zeroline=False,
        showline=False
    ),
    yaxis=dict(
        showgrid=True, 
        gridcolor='#28293D', 
        gridwidth=1,
        zeroline=False,
        showline=False
    )
)
```

### Specific Chart Trace Styling

**1. Line & Area Charts (Neon Glow Effect):**
*   Use `line_shape='spline'` for smooth, curved lines.
*   Set `line=dict(width=3, color='#00E5FF')`.
*   To achieve the glowing fill effect beneath the lines (as seen in the reference), use `fill='tozeroy'` and set the fill color to a highly transparent version of the line color: `fillcolor='rgba(0, 229, 255, 0.1)'`.

**2. Donut / Pie Charts:**
*   Set `hole=0.7` for a thin, modern ring.
*   Use the solid accent colors (`#00E5FF`, `#0088FF`, `#C738FF`).
*   Set `marker=dict(line=dict(color='#1C1D2D', width=4))` to create spacing/gaps between the donut segments that match the card background.

**3. Bar Charts (Gradient-like aesthetics):**
*   Since Plotly doesn't natively support true CSS gradients inside bars easily, use a solid bright cyan (`#00E5FF`) and reduce opacity slightly (`opacity=0.8`), or map a continuous color scale (e.g., `blues` or `purples`) mapped to the Y-value to simulate a gradient effect across the bars.
*   Remove bar borders.

## 4. Execution Command for Antigravity

Apply this styling guide to the previously generated Python/Dash code. Inject a custom CSS string or external stylesheet for the layout elements, and meticulously update every `px` or `go` figure with the transparent backgrounds, custom gridlines, and neon color palettes defined above. Do not use default Plotly themes (like `plotly_white` or `plotly_dark`); you must manually configure the layout as specified to match "image_d14a62.jpg".