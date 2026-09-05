import sqlite3

def create_or_update_table():
    try:
        conn = sqlite3.connect('bookings.db')
        cursor = conn.cursor()
        
        # Verificar si la tabla existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='bookings'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("La tabla 'bookings' no existe.")
            print("Reinicia el servidor primero y luego ejecuta este script nuevamente.")
            conn.close()
            return
        
        # Verificar si la columna existe
        cursor.execute("PRAGMA table_info(bookings)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'status' in columns:
            print("✅ La columna 'status' ya existe")
            conn.close()
            return
        
        # Agregar la columna
        print("Agregando columna 'status'...")
        cursor.execute("ALTER TABLE bookings ADD COLUMN status VARCHAR DEFAULT 'active'")
        conn.commit()
        print("✅ Columna 'status' agregada correctamente")
        
    except sqlite3.OperationalError as e:
        print(f"❌ Error de SQLite: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_or_update_table()