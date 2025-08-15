import ezdxf

def generate_dxf(geometry: dict, output_path: str):
    doc = ezdxf.new()
    msp = doc.modelspace()

    for room in geometry.get("rooms", []):
        label = room["label"]
        x, y = room["position"]
        width, height = room["size"]

        # Draw rectangle
        msp.add_lwpolyline([
            (x, y),
            (x + width, y),
            (x + width, y + height),
            (x, y + height),
            (x, y)
        ], close=True)

        # Add room label
        text = msp.add_text(label, dxfattribs={"height": 5})
        text.dxf.insert = (x + 5, y + 5)

    doc.saveas(output_path)
