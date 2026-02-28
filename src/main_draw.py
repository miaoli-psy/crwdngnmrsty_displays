"""
draw demo displays for closinggap2
"""

from src.draw_displays import drawEllipse_full, draw_disc_only, drawEllipses
import ast
from pathlib import Path
import pandas as pd


def excel_col_to_idx(col_letters: str) -> int:
    col_letters = col_letters.upper().strip()
    idx = 0
    for ch in col_letters:
        idx = idx * 26 + (ord(ch) - ord('A') + 1)
    return idx - 1  # 0-based


def get_cell_from_df(df: pd.DataFrame, excel_col: str, excel_row: int, header_rows: int = 1):
    r = excel_row - (header_rows + 1)  # Excel 行 -> pandas 行
    c = excel_col_to_idx(excel_col)  # Excel 列 -> pandas 列
    return df.iat[r, c]


def parse_pos_list(x):
    if isinstance(x, str):
        return ast.literal_eval(x)
    return x

def extract_condition_from_file(fp: Path, excel_row: int = 32, sep=","):
    df = pd.read_csv(fp, sep=sep)

    left_central_raw = get_cell_from_df(df, "J", excel_row)
    left_extra_raw = get_cell_from_df(df, "K", excel_row)
    right_central_raw = get_cell_from_df(df, "X", excel_row)
    right_extra_raw = get_cell_from_df(df, "Y", excel_row)

    return {
        "name": f"{fp.stem}_row{excel_row}",
        "left_central": parse_pos_list(left_central_raw),
        "left_extra": parse_pos_list(left_extra_raw),
        "right_central": parse_pos_list(right_central_raw),
        "right_extra": parse_pos_list(right_extra_raw),
    }


def extract_all_conditions(data_dir, excel_row=32, pattern="*.csv", sep=","):
    data_dir = Path(data_dir)
    files = sorted(data_dir.glob(pattern))
    print(f"Found {len(files)} files.")
    return [extract_condition_from_file(fp, excel_row=excel_row, sep=sep) for fp in files]


def batch_draw_from_conditions(
    conditions,
    ka=0.25,
    kb=0.1,
    plot_axis_limit_fixed=False,
    zoomin=False,
    savefig=True,
):
    for cond in conditions:
        name = cond.get("name", "cond")
        print(f"Drawing {name}...")

        central = cond["left_central"] + cond["right_central"]
        extra   = cond["left_extra"]   + cond["right_extra"]

        drawEllipse_full(
            central,
            extra,
            ka=ka,
            kb=kb,
            plot_axis_limit_fixed=plot_axis_limit_fixed,
            zoomin=zoomin,
            savefig=savefig,
        )

        draw_disc_only(
            central,
            extra,
            savefig=savefig,
        )

if __name__ == "__main__":
    # read displays for closing gap2 - radial vs. neutral and tangential vs. neutral
    DATA_DIR = r"D:\OneDrive\projects\numerosity_closing_gap\src\generate_displays\merged2"

    conditions = extract_all_conditions(DATA_DIR, excel_row=14, pattern="*.csv", sep=",")

    batch_draw_from_conditions(
        conditions,
        ka=0.25,
        kb=0.1,
        plot_axis_limit_fixed=False,
        zoomin=False,
        savefig=True,
    )



