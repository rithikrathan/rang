from dataclasses import dataclass
from typing import List, Optional, Dict, Set
from datetime import datetime

# Basic point
@dataclass
class Point:
    x: float
    y: float

# Curve point (optionally for Bezier curves)
@dataclass
class CurvePoint:
    x: float
    y: float
    controlX: Optional[float] = None
    controlY: Optional[float] = None

# Kolam pattern (1-16) with connectivity
@dataclass
class KolamCurvePattern:
    id: int  # 1-16
    points: List[CurvePoint]
    hasDownConnection: bool
    hasRightConnection: bool

# Each cell in the Kolam grid
@dataclass
class GridCell:
    row: int
    col: int
    patternId: int  # 1-16
    dotCenter: Point

# Full Kolam grid
@dataclass
class KolamGrid:
    size: int  # n x n
    cells: List[List[GridCell]]  # 2D grid
    cellSpacing: float

# Line / curve
@dataclass
class Line:
    id: str
    start: Point
    end: Point
    strokeWidth: Optional[float] = 1.5
    color: Optional[str] = "#ffffff"
    curvePoints: Optional[List[CurvePoint]] = None

# Dot on grid
@dataclass
class Dot:
    id: str
    center: Point
    radius: Optional[float] = 3
    color: Optional[str] = "#ffffff"
    filled: Optional[bool] = True

# Full Kolam pattern
@dataclass
class KolamPattern:
    id: str
    name: str
    grid: KolamGrid
    curves: List[Line]
    dots: List[Dot]
    symmetryType: str  # '1D' | '2D' | 'none'
    dimensions: Dict[str, float]  # {'width': float, 'height': float}
    created: datetime
    modified: datetime

# Animation steps (optional)
@dataclass
class AnimationStep:
    elementId: str
    elementType: str  # 'dot' | 'curve'
    delay: float
    duration: float
    drawOrder: int

@dataclass
class KolamAnimation:
    id: str
    patternId: str
    steps: List[AnimationStep]
    totalDuration: float
    loop: bool

# Export options
KolamExportFormat = str  # 'svg' | 'png' | 'gif' | 'json'

@dataclass
class ExportOptions:
    format: KolamExportFormat
    includeAnimation: Optional[bool] = False
    backgroundColor: Optional[str] = "#ffffff"
    scale: Optional[float] = 1.0

# Connectivity rules
@dataclass
class ConnectivityRules:
    downConnectors: Set[int]
    rightConnectors: Set[int]
    compatiblePatterns: Dict[int, List[int]]

