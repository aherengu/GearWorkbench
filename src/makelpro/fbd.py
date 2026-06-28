import matplotlib.pyplot as plt
import matplotlib.patches as patches


def build_demo_cases():
    """Return the reference free-body diagram cases used in the release figures."""

    return [
        (
            "Shaft A (Input)",
            200,
            [(0, "Ray", 1085), (200, "Rby", 1085)],
            [(100, "Gear 2 Load", 2170, True)],
            "FBD_Shaft_A.png",
        ),
        (
            "Shaft B (Intermediate)",
            400,
            [(0, "Left Brg", 1518), (400, "Right Brg", 217)],
            [
                (100, "Gear 3 (Input)", 2170, True),
                (300, "Gear 4 (Output)", 434, False),
            ],
            "FBD_Shaft_B.png",
        ),
        (
            "Shaft C (Output)",
            200,
            [(0, "Rey", 217), (200, "Rfy", 217)],
            [(100, "Gear 5 Load", 434, True)],
            "FBD_Shaft_C.png",
        ),
    ]

def draw_fbd(shaft_name, length, supports, loads, filename):
    """
    Draws a simple and clean Free Body Diagram (FBD).
    supports: [(x_pos, 'name', reaction_val_N), ...]
    loads: [(x_pos, 'name', load_val_N, is_down_dir), ...]
    """
    fig, ax = plt.subplots(figsize=(10, 4))
    
    # 1. Draw Shaft (Simple Line)
    ax.plot([0, length], [0, 0], 'k-', linewidth=3, zorder=1)
    
    # 2. Draw Supports (Triangles and Reaction Arrows)
    for x, name, value in supports:
        # Support Triangle
        triangle = patches.Polygon([[x-5, -15], [x+5, -15], [x, 0]], closed=True, facecolor='#cccccc', edgecolor='black')
        ax.add_patch(triangle)
        
        # Reaction Arrow (Upward)
        ax.arrow(x, -60, 0, 40, head_width=3, head_length=5, fc='blue', ec='blue', width=0.5)
        ax.text(x, -75, f"{name}\nR={value:.0f} N", ha='center', va='top', color='blue', fontweight='bold')

    # 3. Draw Loads (Force Arrows)
    for x, name, value, is_down in loads:
        if is_down:
            # Downward Force
            ax.arrow(x, 60, 0, -55, head_width=3, head_length=5, fc='red', ec='red', width=0.8)
            ax.text(x, 70, f"{name}\nF={value:.0f} N", ha='center', va='bottom', color='red', fontweight='bold')
        else:
            # Upward Force (e.g., Opposing gear load on Shaft B)
            ax.arrow(x, -60, 0, 55, head_width=3, head_length=5, fc='green', ec='green', width=0.8)
            ax.text(x, -75, f"{name}\nF={value:.0f} N", ha='center', va='top', color='green', fontweight='bold')
            
        # Position marker
        ax.plot(x, 0, 'ko', markersize=5)
        ax.text(x, -5, f"{x}mm", ha='center', va='top', fontsize=8)

    # Settings
    ax.set_xlim(-20, length + 20)
    ax.set_ylim(-100, 100)
    ax.axis('off') # Hide axes
    
    # Title
    plt.title(f"Free Body Diagram: {shaft_name}", fontsize=14, fontweight='bold', pad=20)
    
    # Save
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"Successfully generated: {filename}")

def render_demo_figures():
    for shaft_name, length, supports, loads, filename in build_demo_cases():
        draw_fbd(shaft_name, length, supports, loads, filename)


if __name__ == "__main__":
    render_demo_figures()
