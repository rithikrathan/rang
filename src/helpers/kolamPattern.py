import json
from typing import List, Dict, Set

# Load Kolam data from JSON
with open("kolamPatternsData.json", "r") as f:
    kolam_data = json.load(f)


class KolamCurvePattern:
    def __init__(self, id: int, points: List[List[int]], hasDownConnection: bool, hasRightConnection: bool):
        self.id = id
        self.points = points
        self.hasDownConnection = hasDownConnection
        self.hasRightConnection = hasRightConnection


# Convert JSON into KolamCurvePattern objects
KOLAM_CURVE_PATTERNS: List[KolamCurvePattern] = [
    KolamCurvePattern(
        patern["id"],
        patern["points"],
        patern.get("hasDownConnection", False),
        patern.get("hasRightConnection", False)
    )
    for patern in kolam_data["patterns"]
]

# Generate compatibility matrix


def generate_compatibility_matrix() -> Dict[int, List[int]]:
    matrix: Dict[int, List[int]] = {}
    for i in range(1, 17):
        current = next((p for p in KOLAM_CURVE_PATTERNS if p.id == i), None)
        if not current:
            continue

        compatible: List[int] = []
        for j in range(1, 17):
            if i == j:
                continue
            target = next((p for p in KOLAM_CURVE_PATTERNS if p.id == j), None)
            if not target:
                continue

            if current.hasRightConnection or current.hasDownConnection:
                if target.hasRightConnection or target.hasDownConnection or j == 1:
                    compatible.append(j)
            else:
                compatible.append(j)

        matrix[i] = compatible
    return matrix


# Connectivity rules
CONNECTIVITY_RULES = {
    "downConnectors": {p.id for p in KOLAM_CURVE_PATTERNS if p.hasDownConnection},
    "rightConnectors": {p.id for p in KOLAM_CURVE_PATTERNS if p.hasRightConnection},
    "compatiblePatterns": generate_compatibility_matrix()
}

# Symmetry transforms
SYMMETRY_TRANSFORMS = {
    "horizontalInverse": [1, 2, 5, 4, 3, 9, 8, 7, 6, 10, 11, 12, 15, 14, 13, 16],
    "verticalInverse":   [1, 4, 3, 2, 5, 7, 6, 9, 8, 10, 11, 14, 13, 12, 15, 16],
    "rotation90":        [1, 3, 2, 5, 4, 6, 9, 8, 7, 11, 10, 13, 12, 15, 14, 16],
    "diagonalSymmetric": [1, 6, 8, 16],
}

# Pattern stats
PATTERN_STATS = {
    "totalPatterns": kolam_data.get("totalPatterns"),
    "extractedAt": kolam_data.get("extractedAt"),
    "description": kolam_data.get("description"),
    "pointCounts": [{"id": p.id, "points": len(p.points)} for p in KOLAM_CURVE_PATTERNS],
    "connectionCounts": {
        "downConnectors": len(CONNECTIVITY_RULES["downConnectors"]),
        "rightConnectors": len(CONNECTIVITY_RULES["rightConnectors"]),
    }
}
