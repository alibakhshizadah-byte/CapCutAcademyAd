from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "capcut_academy.db"

app = FastAPI(title="CapCut Academy API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


init_db()


@app.get("/")
def home():
    return {
        "name": "CapCut Academy API",
        "status": "online"
    }


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "database": "connected"
    }


@app.post("/api/users")
def create_user(username: str):

    conn = get_db()

    try:
        cursor = conn.execute(
            "INSERT INTO users (username) VALUES (?)",
            (username,)
        )

        conn.commit()

        user_id = cursor.lastrowid

    except sqlite3.IntegrityError:
        conn.close()

        return {
            "success": False,
            "message": "username already exists"
        }

    conn.close()

    return {
        "success": True,
        "user_id": user_id,
        "username": username,
        "xp": 0,
        "level": 1
    }


@app.get("/api/users/{user_id}")
def get_user(user_id: int):

    conn = get_db()

    user = conn.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    conn.close()

    if not user:
        return {
            "success": False,
            "message": "user not found"
        }

    return dict(user)


@app.post("/api/users/{user_id}/xp")
def add_xp(user_id: int, amount: int):

    conn = get_db()

    user = conn.execute(
        "SELECT xp FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    if not user:
        conn.close()

        return {
            "success": False,
            "message": "user not found"
        }

    new_xp = user["xp"] + amount

    if new_xp >= 3500:
        level = 10
    elif new_xp >= 2500:
        level = 9
    elif new_xp >= 1900:
        level = 8
    elif new_xp >= 1400:
        level = 7
    elif new_xp >= 1000:
        level = 6
    elif new_xp >= 700:
        level = 5
    elif new_xp >= 450:
        level = 4
    elif new_xp >= 250:
        level = 3
    elif new_xp >= 100:
        level = 2
    else:
        level = 1

    conn.execute(
        """
        UPDATE users
        SET xp = ?, level = ?
        WHERE id = ?
        """,
        (new_xp, level, user_id)
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "user_id": user_id,
        "xp": new_xp,
        "level": level
    }


@app.get("/api/leaderboard")
def leaderboard():

    conn = get_db()

    users = conn.execute(
        """
        SELECT id, username, xp, level
        FROM users
        ORDER BY xp DESC
        """
    ).fetchall()

    conn.close()

    result = []

    for position, user in enumerate(users, start=1):
        result.append({
            "rank": position,
            "id": user["id"],
            "username": user["username"],
            "xp": user["xp"],
            "level": user["level"]
        })

    return result



# ===== CAPCUT ADMIN API =====

@app.get("/api/admin/stats")
def admin_stats():

    conn = get_db()

    users = conn.execute(
        "SELECT COUNT(*) AS count FROM users"
    ).fetchone()["count"]

    total_xp = conn.execute(
        "SELECT COALESCE(SUM(xp), 0) AS total FROM users"
    ).fetchone()["total"]

    achievements = conn.execute(
        "SELECT COUNT(*) AS count FROM achievements"
    ).fetchone()["count"]

    templates = conn.execute(
        "SELECT COUNT(*) AS count FROM template_usage"
    ).fetchone()["count"]

    exercises = conn.execute(
        "SELECT COUNT(*) AS count FROM exercise_completions"
    ).fetchone()["count"]

    conn.close()

    return {
        "users": users,
        "total_xp": total_xp,
        "achievements": achievements,
        "templates_used": templates,
        "exercises_completed": exercises
    }


@app.get("/api/admin/users")
def admin_users():

    conn = get_db()

    users = conn.execute(
        """
        SELECT
            id,
            username,
            xp,
            level,
            created_at
        FROM users
        ORDER BY xp DESC, id ASC
        """
    ).fetchall()

    conn.close()

    return [dict(user) for user in users]


@app.post("/api/admin/users/{user_id}/xp")
def admin_add_xp(user_id: int, amount: int):

    if amount < 0:
        return {
            "success": False,
            "message": "amount must be positive"
        }

    conn = get_db()

    user = conn.execute(
        "SELECT xp FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    if not user:

        conn.close()

        return {
            "success": False,
            "message": "user not found"
        }

    new_xp = user["xp"] + amount

    if new_xp >= 3500:
        level = 10
    elif new_xp >= 2500:
        level = 9
    elif new_xp >= 1900:
        level = 8
    elif new_xp >= 1400:
        level = 7
    elif new_xp >= 1000:
        level = 6
    elif new_xp >= 700:
        level = 5
    elif new_xp >= 450:
        level = 4
    elif new_xp >= 250:
        level = 3
    elif new_xp >= 100:
        level = 2
    else:
        level = 1

    conn.execute(
        """
        UPDATE users
        SET xp = ?, level = ?
        WHERE id = ?
        """,
        (new_xp, level, user_id)
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "user_id": user_id,
        "xp": new_xp,
        "level": level
    }


@app.get("/api/admin/achievements/{user_id}")
def admin_user_achievements(user_id: int):

    conn = get_db()

    rows = conn.execute(
        """
        SELECT achievement_key, unlocked_at
        FROM achievements
        WHERE user_id = ?
        ORDER BY unlocked_at DESC
        """,
        (user_id,)
    ).fetchall()

    conn.close()

    return [dict(row) for row in rows]


@app.get("/api/admin/activities/{user_id}")
def admin_user_activities(user_id: int):

    conn = get_db()

    rows = conn.execute(
        """
        SELECT text, created_at
        FROM activities
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT 50
        """,
        (user_id,)
    ).fetchall()

    conn.close()

    return [dict(row) for row in rows]

