# Automatic Spiral Galaxy Generator — Google Colab Edition
# Converted from:
# https://github.com/Tangle10/Python-Galaxy-Generator
#
# Python 3 / Colab-compatible rewrite.
# Run this entire file in Google Colab with:
#   %run Automatic_Spiral_Galaxy_Generator_Colab.py

from __future__ import annotations

import math
import random
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
from PIL import Image
from IPython.display import display

try:
    import ipywidgets as widgets
except ImportError:
    widgets = None


GALAXY_TYPES: Dict[str, int] = {
    "Spiral": 0,
    "Ring": 1,
    "Lenticular with hub": 2,
    "Elliptical": 3,
    "Lenticular without hub": 4,
    "Starfield": 5,
}

SIZE_BRACKETS: Dict[str, Tuple[int, int]] = {
    "Small (400–600 px)": (400, 600),
    "Medium (700–1000 px)": (700, 1000),
    "Large (1100–1600 px)": (1100, 1600),
    "Very large (1700–2400 px)": (1700, 2400),
}


@dataclass
class GalaxyResult:
    image: Image.Image
    image_path: Path
    metadata_path: Path
    galaxy_name: str
    galaxy_type: str
    seed: int
    star_count: int
    cluster_count: int
    radius: float
    image_size: int


def _safe_name(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip())
    return cleaned.strip("._") or "Galaxy"


def _hex_to_rgb(values: np.ndarray) -> np.ndarray:
    palette = np.array(
        [
            [255, 128, 128],
            [255, 206, 122],
            [255, 239, 195],
            [255, 255, 215],
            [255, 255, 255],
            [231, 255, 255],
            [181, 225, 255],
        ],
        dtype=np.uint8,
    )
    return palette[values]


def _add_glow(canvas: np.ndarray, x: np.ndarray, y: np.ndarray, rgb: np.ndarray) -> None:
    """Draw stars with a bright center and a faint one-pixel halo."""
    height, width, _ = canvas.shape
    x = np.clip(x.astype(np.int32), 0, width - 1)
    y = np.clip(y.astype(np.int32), 0, height - 1)

    halo = (rgb.astype(np.float32) * 0.20).astype(np.uint8)
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        xx = np.clip(x + dx, 0, width - 1)
        yy = np.clip(y + dy, 0, height - 1)
        np.maximum.at(canvas, (yy, xx, slice(None)), halo)

    np.maximum.at(canvas, (y, x, slice(None)), rgb)


def generate_galaxy(
    name: str = "Andromeda_Synthetic",
    galaxy_type: str = "Spiral",
    image_size: int = 900,
    star_count: int = 80_000,
    arm_count: int = 5,
    arm_rotations: float = 1.35,
    arm_spread: float = 0.28,
    hub_fraction: float = 0.22,
    inclination_deg: float = 18.0,
    seed: int | None = None,
    output_dir: str | Path = "/content",
) -> GalaxyResult:
    """Generate and save a synthetic galaxy image and metadata file."""
    if galaxy_type not in GALAXY_TYPES:
        raise ValueError(f"Unsupported galaxy type: {galaxy_type}")
    if image_size < 200:
        raise ValueError("image_size must be at least 200 pixels")
    if not 1_000 <= star_count <= 1_000_000:
        raise ValueError("star_count must be between 1,000 and 1,000,000")

    safe_name = _safe_name(name)
    seed = int(seed if seed is not None else random.randrange(0, 2**32 - 1))
    rng = np.random.default_rng(seed)

    galaxy_id = GALAXY_TYPES[galaxy_type]
    radius = 1.0
    hub_count = int(star_count * np.clip(hub_fraction, 0.02, 0.80))
    disk_count = star_count - hub_count
    cluster_count = max(0, min(30, star_count // 20_000))

    if galaxy_id == 5:
        x = rng.uniform(-1.0, 1.0, star_count)
        y = rng.uniform(-1.0, 1.0, star_count)
        z = rng.uniform(-0.25, 0.25, star_count)
        color_index = rng.integers(0, 7, star_count)

    else:
        hub_r = np.clip(rng.normal(0.0, 0.18, hub_count), -0.55, 0.55)
        hub_theta = rng.uniform(0.0, 2.0 * math.pi, hub_count)
        hub_flattening = 0.72 if galaxy_id == 3 else 0.90
        hx = hub_r * np.cos(hub_theta)
        hy = hub_r * np.sin(hub_theta) * hub_flattening
        hz = rng.normal(0.0, 0.10, hub_count)
        hub_colors = rng.choice(
            np.arange(7),
            size=hub_count,
            p=[0.12, 0.22, 0.24, 0.20, 0.14, 0.06, 0.02],
        )

        r = np.sqrt(rng.uniform(0.0, 1.0, disk_count))
        base_theta = rng.uniform(0.0, 2.0 * math.pi, disk_count)

        if galaxy_id == 0:
            arms = max(1, int(arm_count))
            arm_slot = rng.integers(0, arms, disk_count)
            theta = (
                arm_slot * (2.0 * math.pi / arms)
                + r * (2.0 * math.pi * arm_rotations)
                + rng.normal(0.0, max(0.01, arm_spread), disk_count)
            )
            dx = r * np.cos(theta)
            dy = r * np.sin(theta)

        elif galaxy_id == 1:
            ring_r = np.clip(rng.normal(0.72, 0.09, disk_count), 0.40, 1.0)
            dx = ring_r * np.cos(base_theta)
            dy = ring_r * np.sin(base_theta)

        elif galaxy_id == 2:
            dx = r * np.cos(base_theta)
            dy = 0.52 * r * np.sin(base_theta)

        elif galaxy_id == 3:
            ell_r = np.clip(np.abs(rng.normal(0.0, 0.47, disk_count)), 0.0, 1.0)
            dx = ell_r * np.cos(base_theta)
            dy = 0.60 * ell_r * np.sin(base_theta)

        else:
            dx = r * np.cos(base_theta)
            dy = 0.42 * r * np.sin(base_theta)

        dz = rng.normal(0.0, 0.025 if galaxy_id in (0, 1) else 0.06, disk_count)
        disk_colors = rng.choice(
            np.arange(7),
            size=disk_count,
            p=[0.02, 0.05, 0.12, 0.22, 0.25, 0.21, 0.13],
        )

        x = np.concatenate([hx, dx])
        y = np.concatenate([hy, dy])
        z = np.concatenate([hz, dz])
        color_index = np.concatenate([hub_colors, disk_colors])

        if cluster_count:
            points_per_cluster = max(40, min(350, star_count // 1200))
            cx_all, cy_all, cz_all, cc_all = [], [], [], []
            for _ in range(cluster_count):
                cr = rng.uniform(0.25, 0.95)
                ct = rng.uniform(0.0, 2.0 * math.pi)
                cx = cr * math.cos(ct)
                cy = cr * math.sin(ct)
                cx_all.append(rng.normal(cx, 0.018, points_per_cluster))
                cy_all.append(rng.normal(cy, 0.018, points_per_cluster))
                cz_all.append(rng.normal(0.0, 0.015, points_per_cluster))
                cc_all.append(rng.choice([4, 5, 6], points_per_cluster))

            x = np.concatenate([x, *cx_all])
            y = np.concatenate([y, *cy_all])
            z = np.concatenate([z, *cz_all])
            color_index = np.concatenate([color_index, *cc_all])

    inc = math.radians(float(inclination_deg))
    y_rot = y * math.cos(inc) - z * math.sin(inc)

    margin = max(12, int(image_size * 0.04))
    scale = (image_size - 2 * margin) / 2.15
    px = np.rint(image_size / 2 + x * scale)
    py = np.rint(image_size / 2 + y_rot * scale)

    rgb = _hex_to_rgb(color_index)
    canvas = np.zeros((image_size, image_size, 3), dtype=np.uint8)
    _add_glow(canvas, px, py, rgb)

    image = Image.fromarray(canvas, mode="RGB")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"spiralgalaxy-{seed}-{safe_name}"
    image_path = output_dir / f"{stem}.png"
    metadata_path = output_dir / f"{stem}.txt"

    image.save(image_path, optimize=True)
    metadata_path.write_text(
        "\n".join(
            [
                f"Galaxy seed: {seed}",
                f"Galaxy name: {name}",
                f"Galaxy type: {galaxy_type}",
                f"Number of plotted stars: {len(x)}",
                f"Base requested stars: {star_count}",
                f"Number of clusters: {cluster_count}",
                f"Normalized galaxy radius: {radius:.3f}",
                f"Image size: {image_size} x {image_size}",
                f"Arm count: {arm_count}",
                f"Arm rotations: {arm_rotations:.3f}",
                f"Arm spread: {arm_spread:.3f}",
                f"Hub fraction: {hub_fraction:.3f}",
                f"Inclination: {inclination_deg:.3f} degrees",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    return GalaxyResult(
        image=image,
        image_path=image_path,
        metadata_path=metadata_path,
        galaxy_name=name,
        galaxy_type=galaxy_type,
        seed=seed,
        star_count=len(x),
        cluster_count=cluster_count,
        radius=radius,
        image_size=image_size,
    )


def build_colab_widget():
    """Create the interactive control panel shown inside Colab."""
    if widgets is None:
        raise RuntimeError(
            "ipywidgets is required for the notebook interface. "
            "In Colab run: !pip -q install ipywidgets"
        )
    name = widgets.Text(
        value="Synthetic_Andromeda",
        description="Name:",
        layout=widgets.Layout(width="420px"),
    )
    galaxy_type = widgets.Dropdown(
        options=list(GALAXY_TYPES),
        value="Spiral",
        description="Type:",
        layout=widgets.Layout(width="420px"),
    )
    size_bracket = widgets.Dropdown(
        options=list(SIZE_BRACKETS),
        value="Medium (700–1000 px)",
        description="Size:",
        layout=widgets.Layout(width="420px"),
    )
    exact_size = widgets.IntSlider(
        value=900,
        min=300,
        max=2400,
        step=50,
        description="Pixels:",
        continuous_update=False,
        layout=widgets.Layout(width="620px"),
    )
    stars = widgets.IntSlider(
        value=80_000,
        min=5_000,
        max=400_000,
        step=5_000,
        description="Stars:",
        continuous_update=False,
        readout_format=",d",
        layout=widgets.Layout(width="620px"),
    )
    arms = widgets.IntSlider(
        value=5,
        min=1,
        max=12,
        step=1,
        description="Arms:",
        continuous_update=False,
        layout=widgets.Layout(width="620px"),
    )
    rotations = widgets.FloatSlider(
        value=1.35,
        min=0.2,
        max=3.0,
        step=0.05,
        description="Arm turns:",
        continuous_update=False,
        layout=widgets.Layout(width="620px"),
    )
    spread = widgets.FloatSlider(
        value=0.28,
        min=0.03,
        max=0.80,
        step=0.01,
        description="Arm spread:",
        continuous_update=False,
        layout=widgets.Layout(width="620px"),
    )
    hub = widgets.FloatSlider(
        value=0.22,
        min=0.02,
        max=0.75,
        step=0.01,
        description="Hub:",
        continuous_update=False,
        layout=widgets.Layout(width="620px"),
    )
    inclination = widgets.FloatSlider(
        value=18.0,
        min=0.0,
        max=85.0,
        step=1.0,
        description="Inclination:",
        continuous_update=False,
        layout=widgets.Layout(width="620px"),
    )
    seed = widgets.IntText(
        value=20260721,
        description="Seed:",
        layout=widgets.Layout(width="300px"),
    )
    random_seed = widgets.Checkbox(
        value=False,
        description="Use a new random seed",
        indent=False,
    )
    generate_button = widgets.Button(
        description="Generate Galaxy",
        button_style="primary",
        icon="star",
        layout=widgets.Layout(width="220px", height="42px"),
    )
    output = widgets.Output(
        layout=widgets.Layout(
            border="1px solid #444",
            padding="10px",
            width="100%",
        )
    )

    def update_size(change=None):
        low, high = SIZE_BRACKETS[size_bracket.value]
        exact_size.min = low
        exact_size.max = high
        exact_size.value = int(round((low + high) / 2 / 50) * 50)

    size_bracket.observe(update_size, names="value")

    def update_spiral_controls(change=None):
        enabled = galaxy_type.value == "Spiral"
        arms.disabled = not enabled
        rotations.disabled = not enabled
        spread.disabled = not enabled

    galaxy_type.observe(update_spiral_controls, names="value")

    def on_generate(_):
        generate_button.disabled = True
        with output:
            output.clear_output(wait=True)
            try:
                chosen_seed = None if random_seed.value else int(seed.value)
                result = generate_galaxy(
                    name=name.value,
                    galaxy_type=galaxy_type.value,
                    image_size=int(exact_size.value),
                    star_count=int(stars.value),
                    arm_count=int(arms.value),
                    arm_rotations=float(rotations.value),
                    arm_spread=float(spread.value),
                    hub_fraction=float(hub.value),
                    inclination_deg=float(inclination.value),
                    seed=chosen_seed,
                    output_dir="/content",
                )
                display(result.image)
                print(f"Galaxy type: {result.galaxy_type}")
                print(f"Stars plotted: {result.star_count:,}")
                print(f"Seed: {result.seed}")
                print(f"PNG: {result.image_path}")
                print(f"Metadata: {result.metadata_path}")
                print()
                print("Colab download commands:")
                print(f"from google.colab import files")
                print(f"files.download({str(result.image_path)!r})")
                print(f"files.download({str(result.metadata_path)!r})")
            except Exception as exc:
                print(f"Generation failed: {type(exc).__name__}: {exc}")
                raise
            finally:
                generate_button.disabled = False

    generate_button.on_click(on_generate)
    update_spiral_controls()

    title = widgets.HTML(
        """
        <h2 style="margin-bottom:4px">Automatic Galaxy Generator — Colab Edition</h2>
        <div style="color:#666;margin-bottom:12px">
          Choose the settings and press <b>Generate Galaxy</b>.
          The PNG and metadata file are saved under <code>/content</code>.
        </div>
        """
    )

    panel = widgets.VBox(
        [
            title,
            widgets.HBox([name, galaxy_type]),
            widgets.HBox([size_bracket, seed, random_seed]),
            exact_size,
            stars,
            arms,
            rotations,
            spread,
            hub,
            inclination,
            generate_button,
            output,
        ]
    )
    return panel


if widgets is not None:
    GALAXY_GENERATOR_WIDGET = build_colab_widget()
    display(GALAXY_GENERATOR_WIDGET)
else:
    GALAXY_GENERATOR_WIDGET = None
    print(
        "Galaxy generator functions loaded. Install ipywidgets to display "
        "the interactive notebook interface."
    )
