import matplotlib.pyplot as plt
import matplotlib.patches as patches


def build_demo_shafts():
    """Return the reference shaft definitions used in the release figures."""

    return [
        (
            "Shaft A (Input)",
            [
                (50, 25, "coupling"),
                (30, 30, "bearing"),
                (100, 36, "gear"),
                (30, 30, "bearing"),
            ],
            [
                (10, 30, 7),
                (90, 80, 7),
            ],
            210,
            "Shaft_A_Technical.png",
        ),
        (
            "Shaft B (Intermediate)",
            [
                (50, 35, "bearing"),
                (100, 42, "gear"),
                (100, 35, "spacer"),
                (100, 42, "gear"),
                (50, 35, "bearing"),
            ],
            [
                (60, 80, 8),
                (260, 80, 8),
            ],
            400,
            "Shaft_B_Technical.png",
        ),
        (
            "Shaft C (Output)",
            [
                (50, 25, "bearing"),
                (100, 30, "gear"),
                (50, 25, "bearing"),
                (60, 22, "coupling"),
            ],
            [
                (60, 80, 7),
                (210, 40, 7),
            ],
            260,
            "Shaft_C_Technical.png",
        ),
    ]

def draw_technical_shaft(shaft_name, segments, keyways, total_len, output_filename):

    # Set figure size (approx. A4 landscape ratio)
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Adjust margins
    plt.subplots_adjust(left=0.05, right=0.95, top=0.90, bottom=0.10)
    ax.set_aspect('equal')
    ax.axis('off') # Hide axis lines
    
    current_x = 0
    max_d = 0
    
    # Find max diameter (for setting plot limits)
    for _, d, _ in segments:
        if d > max_d: max_d = d
    
    # --- 1. Draw Shaft Body ---
    # Lists to store coordinates
    x_coords_top = []
    y_coords_top = []
    
    for length, diameter, type_ in segments:
        radius = diameter / 2
        
        # Draw starting line for the first segment
        if current_x == 0:
            ax.plot([current_x, current_x], [-radius, radius], 'k-', linewidth=2)
            y_coords_top.append(radius)
        
        # Shoulder transitions
        if len(y_coords_top) > 0:
            prev_y = y_coords_top[-1]
            if prev_y != radius:
                # Vertical transition line
                ax.plot([current_x, current_x], [prev_y, radius], 'k-', linewidth=2)
                ax.plot([current_x, current_x], [-prev_y, -radius], 'k-', linewidth=2)
                
                # Simple Fillet representation (only on diameter increase)
                if radius > prev_y:
                    # Add a small arc to the corner
                    arc = patches.Arc((current_x, prev_y), width=2, height=2, theta1=90, theta2=180, color='blue', linewidth=1)
                    ax.add_patch(arc)
                    
        # Horizontal lines (Shaft OD)
        ax.plot([current_x, current_x + length], [radius, radius], 'k-', linewidth=2)
        ax.plot([current_x, current_x + length], [-radius, -radius], 'k-', linewidth=2)
        
        # Optional: Light segment separation line
        # ax.plot([current_x + length, current_x + length], [-radius, radius], 'k:', linewidth=0.5)
        
        current_x += length
        y_coords_top.append(radius)

    # Close the shaft end
    last_r = segments[-1][1] / 2
    ax.plot([current_x, current_x], [-last_r, last_r], 'k-', linewidth=2)

    # --- 2. Centerline ---
    ax.plot([-10, total_len + 10], [0, 0], 'k-.', linewidth=1)

    # --- 3. Keyways ---
    for kx, klen, kdepth in keyways:
        # Determine current segment diameter
        temp_x = 0
        seg_r = 0
        for sl, sd, _ in segments:
            if kx >= temp_x and kx < temp_x + sl:
                seg_r = sd / 2
                break
            temp_x += sl
            
        # Keyway top view representation (pocket style)
        # Position: Slightly below the top surface
        key_y_pos = seg_r - (kdepth * 0.5) 
        
        # Keyway profile
        rect = patches.Rectangle((kx, key_y_pos - kdepth), klen, kdepth, 
                                 linewidth=1.2, edgecolor='black', facecolor='none', hatch='////')
        ax.add_patch(rect)
        
        # Keyway centerline
        ax.plot([kx - 2, kx + klen + 2], [key_y_pos - kdepth/2, key_y_pos - kdepth/2], 'k-', linewidth=0.5)

    # --- 4. Dimensions ---
    # Helper function to draw arrows
    def draw_arrow(x1, y1, x2, y2, text, vertical=False):
        ax.annotate("", xy=(x1, y1), xytext=(x2, y2), 
                    arrowprops=dict(arrowstyle='<|-|>', lw=1, color='black'))
        
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        
        if vertical: # Diameter dimensions
            ax.text(x1, y1 + 3, text, ha='center', va='bottom', fontsize=10, fontweight='bold', color='black')
        else: # Length dimensions
            ax.text(mid_x, mid_y + 2, text, ha='center', va='bottom', fontsize=10, color='black')
            # Extension lines
            ax.plot([x1, x1], [0, y1], 'k-', linewidth=0.3, alpha=0.5)
            ax.plot([x2, x2], [0, y2], 'k-', linewidth=0.3, alpha=0.5)

    curr_x_dim = 0
    # Length Dimensions (Bottom)
    dim_base_y = -max_d/2 - 15
    
    for l, d, t in segments:
        draw_arrow(curr_x_dim, dim_base_y, curr_x_dim + l, dim_base_y, f"{l}")
        curr_x_dim += l
    
    # Total Length
    draw_arrow(0, dim_base_y - 15, total_len, dim_base_y - 15, f"TOTAL: {total_len}")

    # Diameter Dimensions (Top)
    curr_x_dia = 0
    for l, d, t in segments:
        # Diameter text (Centered on segment)
        mid_seg = curr_x_dia + l/2
        text_y = d/2 + 5
        ax.text(mid_seg, text_y, f"Ø{d}", ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        # Fillet note (only for specific types)
        if t in ['gear', 'bearing']:
            ax.text(curr_x_dia, -d/2 - 5, "r1.5", ha='center', va='top', fontsize=8, color='blue')
            
        curr_x_dia += l

    # --- 5. Title Block & Info ---
    # Position the title block at a fixed location in the top-left
    
    info_text = (
        f"PART NAME: {shaft_name.upper()}\n"
        f"MATERIAL: AISI 4140 Q&T\n"
        f"UNIT: mm  |  SCALE: 1:1 (Ref)\n"
        f"--------------------------------\n"
        f"NOTES:\n"
        f"1. All unspecified fillets R1.5\n"
        f"2. Keyways acc. to DIN 6885\n"
        f"3. General Tolerances: ISO 2768-m"
    )
    
    # Safe positioning for the text box
    text_box_y = max_d/2 + 30 
    
    ax.text(0, text_box_y, info_text, fontsize=12, 
            verticalalignment='bottom', horizontalalignment='left',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#f0f0f0', edgecolor='black', alpha=1))

    # Set manual plot limits to ensure everything fits
    ax.set_ylim(-max_d/2 - 40, max_d/2 + 60)
    ax.set_xlim(-20, total_len + 20)

    # Save output
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Successfully generated: {output_filename}")

def render_demo_figures():
    for shaft_name, segments, keyways, total_len, filename in build_demo_shafts():
        draw_technical_shaft(shaft_name, segments, keyways, total_len, filename)


if __name__ == "__main__":
    render_demo_figures()
