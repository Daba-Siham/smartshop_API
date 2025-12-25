from database import get_connection

def get_products():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_product(pid):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE id=?", (pid,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def add_product(name, price, description, imgPath):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO products (name, price, description, imgPath) VALUES (?, ?, ?, ?)",
        (name, price, description, imgPath),
    )

    conn.commit()
    pid = cur.lastrowid
    conn.close()
    return pid

def update_product(pid, name=None, price=None, description=None, imgPath=None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM products WHERE id=?", (pid,))
    row = cur.fetchone()
    if row is None:
        conn.close()
        return False

    current = dict(row)

    new_name = name if name is not None else current["name"]
    new_price = price if price is not None else current["price"]
    new_description = description if description is not None else current["description"]
    new_imgPath = imgPath if imgPath is not None else current["imgPath"]

    cur.execute(
        "UPDATE products SET name=?, price=?, description=?, imgPath=? WHERE id=?",
        (new_name, new_price, new_description, new_imgPath, pid),
    )

    conn.commit()
    conn.close()
    return True

def delete_product(pid):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id=?", (pid,))
    conn.commit()
    conn.close()
