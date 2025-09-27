import random
from datetime import datetime
from type import Point, CurvePoint, KolamCurvePattern, GridCell, KolamGrid, Line, Dot, KolamPattern
from kolamPattern import KOLAM_CURVE_PATTERNS


class KolamGenerator:
    CELL_SPACING = 45

    pt_dn = [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1]
    pt_rt = [0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1]

    mate_pt_dn = {
        1: [2, 3, 5, 6, 9, 10, 12],
        2: [4, 7, 8, 11, 13, 14, 15, 16]
    }

    mate_pt_rt = {
        1: [2, 3, 4, 6, 7, 11, 13],
        2: [5, 8, 9, 10, 12, 14, 15, 16]
    }

    h_inv = [1, 2, 5, 4, 3, 9, 8, 7, 6, 10, 11, 12, 15, 14, 13, 16]
    v_inv = [1, 4, 3, 2, 5, 7, 6, 9, 8, 10, 11, 14, 13, 12, 15, 16]

    h_self = [i+1 for i, val in enumerate(h_inv) if val == i+1]
    v_self = [i+1 for i, val in enumerate(v_inv) if val == i+1]

    @staticmethod
    def intersect(a, b):
        return [x for x in a if x in b]

    @staticmethod
    def random_choice(arr):
        return random.choice(arr) if arr else 1

    @staticmethod
    def ones(size):
        return [[1 for _ in range(size)] for _ in range(size)]

    @classmethod
    def propose_kolam_1d(cls, size_of_kolam):
        odd = size_of_kolam % 2 != 0
        hp = (size_of_kolam - 1) // 2 if odd else size_of_kolam // 2
        Mat = cls.ones(hp + 2)

        for i in range(1, hp + 1):
            for j in range(1, hp + 1):
                Valid_by_Up = cls.mate_pt_dn[cls.pt_dn[Mat[i - 1][j] - 1] + 1]
                Valid_by_Lt = cls.mate_pt_rt[cls.pt_rt[Mat[i][j - 1] - 1] + 1]
                Valids = cls.intersect(Valid_by_Up, Valid_by_Lt)
                Mat[i][j] = cls.random_choice(Valids)

        # Edge filling
        Mat[hp + 1][0] = 1
        Mat[0][hp + 1] = 1

        for j in range(1, hp + 1):
            Valids = cls.intersect(
                cls.mate_pt_dn[cls.pt_dn[Mat[hp][j] - 1] + 1],
                cls.mate_pt_rt[cls.pt_rt[Mat[hp + 1][j - 1] - 1] + 1]
            )
            Valids = cls.intersect(Valids, cls.v_self)
            Mat[hp + 1][j] = cls.random_choice(Valids)

        for i in range(1, hp + 1):
            Valids = cls.intersect(
                cls.mate_pt_dn[cls.pt_dn[Mat[i - 1][hp + 1] - 1] + 1],
                cls.mate_pt_rt[cls.pt_rt[Mat[i][hp] - 1] + 1]
            )
            Valids = cls.intersect(Valids, cls.h_self)
            Mat[i][hp + 1] = cls.random_choice(Valids)

        Valids = cls.intersect(
            cls.mate_pt_dn[cls.pt_dn[Mat[hp][hp + 1] - 1] + 1],
            cls.mate_pt_rt[cls.pt_rt[Mat[hp + 1][hp] - 1] + 1]
        )
        Valids = cls.intersect(Valids, cls.h_self)
        Valids = cls.intersect(Valids, cls.v_self)
        Mat[hp + 1][hp + 1] = cls.random_choice(Valids)

        Mat1 = [[Mat[i][j] for j in range(1, hp + 1)]
                for i in range(1, hp + 1)]
        Mat3 = [[cls.v_inv[Mat1[hp - 1 - i][j] - 1]
                 for j in range(hp)] for i in range(hp)]
        Mat2 = [[cls.h_inv[Mat1[i][hp - 1 - j] - 1]
                 for j in range(hp)] for i in range(hp)]
        Mat4 = [[cls.v_inv[Mat2[hp - 1 - i][j] - 1]
                 for j in range(hp)] for i in range(hp)]

        if odd:
            size = 2 * hp + 1
            M = [[1 for _ in range(size)] for _ in range(size)]
            for i in range(hp):
                for j in range(hp):
                    M[i][j] = Mat1[i][j]
                    M[i][hp + 1 + j] = Mat2[i][j]
                    M[hp + 1 + i][j] = Mat3[i][j]
                    M[hp + 1 + i][hp + 1 + j] = Mat4[i][j]

            for i in range(hp):
                M[i][hp] = Mat[i + 1][hp + 1]
                M[hp][i] = Mat[hp + 1][i + 1]
                M[hp][hp + i] = cls.h_inv[Mat[hp + 1][hp - i] - 1]
                M[hp + i][hp] = cls.v_inv[Mat[hp - i][hp + 1] - 1]
        else:
            size = 2 * hp
            M = [[1 for _ in range(size)] for _ in range(size)]
            for i in range(hp):
                for j in range(hp):
                    M[i][j] = Mat1[i][j]
                    M[i][hp + j] = Mat2[i][j]
                    M[hp + i][j] = Mat3[i][j]
                    M[hp + i][hp + j] = Mat4[i][j]

        return M

    @classmethod
    def draw_kolam(cls, M):
        m, n = len(M), len(M[0])
        flippedM = [M[m - 1 - i][:] for i in range(m)]
        dots = []
        curves = []

        for i in range(m):
            for j in range(n):
                if flippedM[i][j] > 0:
                    dots.append(Dot(
                        id=f"dot-{i}-{j}",
                        center=Point(x=(j + 1) * cls.CELL_SPACING,
                                     y=(i + 1) * cls.CELL_SPACING),
                        radius=3, color="#ffffff", filled=True
                    ))
                    idx = flippedM[i][j] - 1
                    if 0 <= idx < len(KOLAM_CURVE_PATTERNS):
                        pattern = KOLAM_CURVE_PATTERNS[idx]
                        curvePoints = [CurvePoint(
                            x=(j + 1 + p.x) * cls.CELL_SPACING,
                            y=(i + 1 + p.y) * cls.CELL_SPACING,
                            controlX=(j + 1 + p.controlX) *
                            cls.CELL_SPACING if p.controlX else None,
                            controlY=(i + 1 + p.controlY) *
                            cls.CELL_SPACING if p.controlY else None
                        ) for p in pattern.points]
                        curves.append(Line(
                            id=f"curve-{i}-{j}",
                            start=curvePoints[0],
                            end=curvePoints[-1],
                            curvePoints=curvePoints,
                            strokeWidth=1.5,
                            color="#ffffff"
                        ))

        grid = KolamGrid(
            size=max(m, n),
            cells=[[GridCell(
                    row=i, col=j, patternId=flippedM[i][j],
                    dotCenter=Point(x=(j + 1) * cls.CELL_SPACING,
                                    y=(i + 1) * cls.CELL_SPACING)
                    ) for j in range(n)] for i in range(m)],
            cellSpacing=cls.CELL_SPACING
        )

        return KolamPattern(
            id=f"kolam-{m}x{n}",
            name=f"Kolam {m}×{n}",
            grid=grid,
            curves=curves,
            dots=dots,
            symmetryType="1D",
            dimensions={"width": (n + 1) * cls.CELL_SPACING,
                        "height": (m + 1) * cls.CELL_SPACING},
            created=datetime.now(),
            modified=datetime.now()
        )

    @classmethod
    def generate_kolam_1d(cls, size):
        matrix = cls.propose_kolam_1d(size)
        return cls.draw_kolam(matrix)


