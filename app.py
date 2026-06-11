from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
app.secret_key = "laundrynow-secret-key"

DATABASE = "laundry.db"
VALID_STATUSES = ["空閒", "使用中", "故障"]


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def now_text():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def init_db():
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS machines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_number TEXT NOT NULL,
            location TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('空閒', '使用中', '故障')),
            remaining_time INTEGER DEFAULT 0 CHECK(remaining_time >= 0),
            updated_at TEXT NOT NULL
        )
        """
    )

    count = conn.execute("SELECT COUNT(*) FROM machines").fetchone()[0]

    if count == 0:
        sample_data = [
            ("A01", "福星宿舍 1 樓洗衣間", "空閒", 0, now_text()),
            ("A02", "福星宿舍 1 樓洗衣間", "使用中", 25, now_text()),
            ("B01", "福星宿舍 2 樓洗衣間", "故障", 0, now_text()),
            ("B02", "福星宿舍 2 樓洗衣間", "空閒", 0, now_text()),
            ("C01", "福星宿舍 3 樓洗衣間", "使用中", 40, now_text()),
        ]

        conn.executemany(
            """
            INSERT INTO machines
            (machine_number, location, status, remaining_time, updated_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            sample_data,
        )

    conn.commit()
    conn.close()


def normalize_remaining_time(status, remaining_time):
    if status != "使用中":
        return 0

    try:
        value = int(remaining_time)
    except (TypeError, ValueError):
        value = 0

    if value < 0:
        value = 0

    return value


def validate_machine_form(machine_number, location, status, remaining_time):
    errors = []

    if not machine_number or not machine_number.strip():
        errors.append("洗衣機編號不可空白。")

    if not location or not location.strip():
        errors.append("位置不可空白。")

    if status not in VALID_STATUSES:
        errors.append("狀態只能是空閒、使用中或故障。")

    try:
        time_value = int(remaining_time)
        if time_value < 0:
            errors.append("剩餘時間不可為負數。")
    except (TypeError, ValueError):
        errors.append("剩餘時間必須是數字。")

    return errors


@app.route("/")
def index():
    conn = get_db_connection()
    machines = conn.execute("SELECT * FROM machines ORDER BY id ASC").fetchall()

    total_free = conn.execute("SELECT COUNT(*) FROM machines WHERE status = '空閒'").fetchone()[0]
    total_busy = conn.execute("SELECT COUNT(*) FROM machines WHERE status = '使用中'").fetchone()[0]
    total_broken = conn.execute("SELECT COUNT(*) FROM machines WHERE status = '故障'").fetchone()[0]

    conn.close()

    return render_template(
        "index.html",
        machines=machines,
        total_free=total_free,
        total_busy=total_busy,
        total_broken=total_broken,
        valid_statuses=VALID_STATUSES,
    )


@app.route("/add", methods=["GET", "POST"])
def add_machine():
    if request.method == "POST":
        machine_number = request.form.get("machine_number", "").strip()
        location = request.form.get("location", "").strip()
        status = request.form.get("status", "")
        remaining_time = request.form.get("remaining_time", "0")

        errors = validate_machine_form(machine_number, location, status, remaining_time)

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template(
                "add_machine.html",
                valid_statuses=VALID_STATUSES,
                form=request.form,
            )

        remaining_time = normalize_remaining_time(status, remaining_time)

        conn = get_db_connection()
        conn.execute(
            """
            INSERT INTO machines
            (machine_number, location, status, remaining_time, updated_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (machine_number, location, status, remaining_time, now_text()),
        )
        conn.commit()
        conn.close()

        flash("洗衣機資料新增成功。", "success")
        return redirect(url_for("index"))

    return render_template(
        "add_machine.html",
        valid_statuses=VALID_STATUSES,
        form={},
    )


@app.route("/update/<int:machine_id>", methods=["POST"])
def update_machine(machine_id):
    status = request.form.get("status", "")
    remaining_time = request.form.get("remaining_time", "0")

    if status not in VALID_STATUSES:
        flash("狀態只能是空閒、使用中或故障。", "error")
        return redirect(url_for("index"))

    remaining_time = normalize_remaining_time(status, remaining_time)

    conn = get_db_connection()
    machine = conn.execute("SELECT * FROM machines WHERE id = ?", (machine_id,)).fetchone()

    if machine is None:
        conn.close()
        flash("找不到指定的洗衣機資料。", "error")
        return redirect(url_for("index"))

    conn.execute(
        """
        UPDATE machines
        SET status = ?, remaining_time = ?, updated_at = ?
        WHERE id = ?
        """,
        (status, remaining_time, now_text(), machine_id),
    )

    conn.commit()
    conn.close()

    flash("洗衣機狀態已更新。", "success")
    return redirect(url_for("index"))


@app.route("/edit/<int:machine_id>", methods=["GET", "POST"])
def edit_machine(machine_id):
    conn = get_db_connection()
    machine = conn.execute("SELECT * FROM machines WHERE id = ?", (machine_id,)).fetchone()

    if machine is None:
        conn.close()
        flash("找不到指定的洗衣機資料。", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        machine_number = request.form.get("machine_number", "").strip()
        location = request.form.get("location", "").strip()
        status = request.form.get("status", "")
        remaining_time = request.form.get("remaining_time", "0")

        errors = validate_machine_form(machine_number, location, status, remaining_time)

        if errors:
            conn.close()
            for error in errors:
                flash(error, "error")
            return render_template(
                "edit_machine.html",
                machine=machine,
                valid_statuses=VALID_STATUSES,
                form=request.form,
            )

        remaining_time = normalize_remaining_time(status, remaining_time)

        conn.execute(
            """
            UPDATE machines
            SET machine_number = ?, location = ?, status = ?, remaining_time = ?, updated_at = ?
            WHERE id = ?
            """,
            (machine_number, location, status, remaining_time, now_text(), machine_id),
        )

        conn.commit()
        conn.close()

        flash("洗衣機資料已修改。", "success")
        return redirect(url_for("index"))

    conn.close()

    return render_template(
        "edit_machine.html",
        machine=machine,
        valid_statuses=VALID_STATUSES,
        form=machine,
    )


@app.route("/delete/<int:machine_id>", methods=["POST"])
def delete_machine(machine_id):
    conn = get_db_connection()
    machine = conn.execute("SELECT * FROM machines WHERE id = ?", (machine_id,)).fetchone()

    if machine is None:
        conn.close()
        flash("找不到指定的洗衣機資料。", "error")
        return redirect(url_for("index"))

    conn.execute("DELETE FROM machines WHERE id = ?", (machine_id,))
    conn.commit()
    conn.close()

    flash("洗衣機資料已刪除。", "success")
    return redirect(url_for("index"))


@app.route("/reset-demo-data", methods=["POST"])
def reset_demo_data():
    conn = get_db_connection()
    conn.execute("DELETE FROM machines")

    sample_data = [
        ("A01", "福星宿舍 1 樓洗衣間", "空閒", 0, now_text()),
        ("A02", "福星宿舍 1 樓洗衣間", "使用中", 25, now_text()),
        ("B01", "福星宿舍 2 樓洗衣間", "故障", 0, now_text()),
        ("B02", "福星宿舍 2 樓洗衣間", "空閒", 0, now_text()),
        ("C01", "福星宿舍 3 樓洗衣間", "使用中", 40, now_text()),
    ]

    conn.executemany(
        """
        INSERT INTO machines
        (machine_number, location, status, remaining_time, updated_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        sample_data,
    )

    conn.commit()
    conn.close()

    flash("Demo 資料已重置。", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
