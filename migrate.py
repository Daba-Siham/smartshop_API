from database import get_connection

def add_imgpath_column():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("ALTER TABLE products ADD COLUMN imgPath TEXT")
        conn.commit()
        print("✅ Colonne imgPath ajoutée")
    except Exception as e:
        print("⚠️ Erreur migration :", e)
    finally:
        conn.close()

if __name__ == "__main__":
    add_imgpath_column()
