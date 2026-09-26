#!/usr/bin/env python3
"""Build the low-poly AC3D airframe shipped with this source package."""
from math import cos, pi, sin
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "Models" / "A350.ac"
MATERIAL = 'MATERIAL "A350 white" rgb 0.82 0.85 0.88 amb 0.25 0.27 0.30 emis 0 0 0 spec 0.35 0.35 0.35 shi 32 trans 0\n'


def object_block(name, vertices, faces):
    lines = ["OBJECT poly", f'name "{name}"', "crease 30.0", "numvert " + str(len(vertices))]
    # AC3D aircraft convention used here: local X points aft, Y starboard,
    # Z up. The source geometry is authored nose-forward, so invert X on export.
    lines.extend(f"{-x:.4f} {y:.4f} {z:.4f}" for x, y, z in vertices)
    lines.append("numsurf " + str(len(faces)))
    for face in faces:
        lines.extend(("SURF 0x30", "mat 0", f"refs {len(face)}"))
        lines.extend(f"{index} {u:.4f} {v:.4f}" for index, (u, v) in face)
    lines.extend(("kids 0", ""))
    return "\n".join(lines)


def extruded_polygon(name, points, thickness=0.16):
    # points are a plan-view polygon (x,y,z); create simple upper/lower skins.
    verts = [(x, y, z + thickness / 2) for x, y, z in points]
    verts += [(x, y, z - thickness / 2) for x, y, z in points]
    n = len(points)
    faces = [([(i, (i / max(1, n - 1), 0)) for i in range(n)]),
             ([(n + i, (i / max(1, n - 1), 1)) for i in reversed(range(n))])]
    for i in range(n):
        j = (i + 1) % n
        faces.append([(i, (0, 0)), (j, (1, 0)), (n + j, (1, 1)), (n + i, (0, 1))])
    return object_block(name, verts, faces)


def body_mesh():
    stations = [
        (31.2, 0.04, 0.04), (30.0, 1.00, 1.00), (27.0, 2.05, 2.15),
        (23.0, 2.65, 2.65), (16.0, 2.95, 2.95), (4.0, 2.98, 2.98),
        (-12.0, 2.90, 2.90), (-24.0, 2.60, 2.60), (-30.0, 1.70, 1.80),
        (-34.8, 0.55, 0.65), (-35.6, 0.05, 0.05),
    ]
    count = 12
    verts = []
    for x, ry, rz in stations:
        for i in range(count):
            a = 2 * pi * i / count
            verts.append((x, ry * cos(a), 2.8 + rz * sin(a)))
    faces = []
    for s in range(len(stations) - 1):
        for i in range(count):
            j = (i + 1) % count
            a, b = s * count + i, s * count + j
            c, d = (s + 1) * count + j, (s + 1) * count + i
            faces.append([(a, (0, 0)), (b, (1, 0)), (c, (1, 1)), (d, (0, 1))])
    faces.append([(i, (i / count, 0)) for i in reversed(range(count))])
    end = (len(stations) - 1) * count
    faces.append([(end + i, (i / count, 1)) for i in range(count)])
    return object_block("Fuselage", verts, faces)


def tube_x(name, x0, x1, yc, zc, radius, sections=12):
    verts = []
    for x in (x0, x1):
        for i in range(sections):
            a = 2 * pi * i / sections
            verts.append((x, yc + radius * cos(a), zc + radius * sin(a)))
    faces = []
    for i in range(sections):
        j = (i + 1) % sections
        faces.append([(i, (0, 0)), (j, (1, 0)), (sections + j, (1, 1)), (sections + i, (0, 1))])
    faces += [[(i, (0, 0)) for i in reversed(range(sections))],
              [(sections + i, (1, 1)) for i in range(sections)]]
    return object_block(name, verts, faces)


def main():
    blocks = [body_mesh()]
    for sign, side in ((-1, "L"), (1, "R")):
        blocks.append(extruded_polygon(f"Wing_{side}", [
            (10.0, 3.0 * sign, 0.0), (-9.0, 3.0 * sign, 0.0),
            (-3.5, 32.38 * sign, -0.7), (5.0, 32.38 * sign, -0.7)], 0.34))
        blocks.append(extruded_polygon(f"Flap_{side}", [
            (-5.6, 6.2 * sign, 0.0), (-9.0, 6.2 * sign, 0.0),
            (-7.7, 18.5 * sign, -0.28), (-4.1, 18.5 * sign, -0.28)], 0.20))
        blocks.append(extruded_polygon(f"Aileron_{side}", [
            (-4.9, 20.5 * sign, -0.30), (-8.0, 20.5 * sign, -0.30),
            (-6.4, 31.4 * sign, -0.65), (-3.4, 31.4 * sign, -0.65)], 0.16))
        blocks.append(extruded_polygon(f"Tailplane_{side}", [
            (-28.0, 1.4 * sign, 4.2), (-33.4, 1.4 * sign, 4.2),
            (-32.3, 7.2 * sign, 4.0), (-27.0, 7.2 * sign, 4.0)], 0.25))
        blocks.append(extruded_polygon(f"Elevator_{side}", [
            (-31.8, 1.5 * sign, 4.05), (-33.4, 1.5 * sign, 4.05),
            (-32.3, 7.0 * sign, 3.85), (-30.5, 7.0 * sign, 3.85)], 0.18))
        blocks.append(tube_x(f"Engine_{side}", 2.0, 10.0, 5.5 * sign, -0.55, 1.42))
        blocks.append(extruded_polygon(f"Pylon_{side}", [
            (5.0, 4.2 * sign, -0.1), (2.5, 4.2 * sign, -0.1),
            (4.0, 5.7 * sign, -0.1), (7.0, 5.7 * sign, -0.1)], 1.1))
        # Main gear legs and paired wheel blocks; deliberately simplified.
        blocks.append(extruded_polygon(f"MainGear_{side}", [
            (-4.9, 6.0 * sign, -1.0), (-6.3, 6.0 * sign, -1.0),
            (-6.0, 6.0 * sign, -4.0), (-4.7, 6.0 * sign, -4.0)], 0.22))
        for wheel in (-0.45, 0.45):
            blocks.append(extruded_polygon(f"MainWheel_{side}_{'A' if wheel < 0 else 'B'}", [
                (-6.25, (6.0 + wheel) * sign, -3.7), (-5.1, (6.0 + wheel) * sign, -3.7),
                (-5.1, (6.0 + wheel) * sign, -4.5), (-6.25, (6.0 + wheel) * sign, -4.5)], 0.36))

    blocks += [
        extruded_polygon("Fin", [(-33.8, 0, 3.5), (-25.0, 0, 3.7), (-31.3, 0, 12.3), (-33.4, 0, 11.5)], 0.42),
        extruded_polygon("Rudder", [(-31.4, 0, 5.0), (-33.6, 0, 4.6), (-33.1, 0, 10.8), (-31.0, 0, 10.4)], 0.24),
        extruded_polygon("NoseGear", [(15.5, -0.12, -0.2), (14.7, -0.12, -0.2), (14.7, -0.12, -3.6), (15.5, -0.12, -3.6)], 0.24),
        extruded_polygon("NoseWheel", [(14.5, -0.45, -3.3), (15.7, -0.45, -3.3), (15.7, -0.45, -4.0), (14.5, -0.45, -4.0)], 0.30),
    ]
    parts = ["AC3Db", MATERIAL, "OBJECT world\nname \"world\"\nkids " + str(len(blocks))]
    OUT.write_text("\n".join(parts) + "\n" + "\n".join(blocks), encoding="utf-8")
    print(f"Wrote {OUT} ({len(blocks)} objects)")


if __name__ == "__main__":
    main()
