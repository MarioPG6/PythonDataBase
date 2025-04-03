import sqlite3

def create_connection():
    """Crea una conexión a la base de datos SQLite."""
    return sqlite3.connect("school.db")

def create_table():
    """Crea la tabla 'students' si no existe."""
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER
        );
    ''')
    conn.commit()
    conn.close()

def insert_student():
    """Solicita datos y agrega un nuevo estudiante."""
    name = input("Ingrese el nombre del estudiante: ")
    age = input("Ingrese la edad del estudiante: ")
    
    if not age.isdigit():
        print("Error: La edad debe ser un número.")
        return
    
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO students(name, age) VALUES(?, ?)", (name, int(age)))
    conn.commit()
    conn.close()
    print(f"Estudiante {name} agregado correctamente.")

def select_all_students():
    """Muestra todos los estudiantes."""
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    conn.close()
    
    print("\nLista de Estudiantes:")
    for row in rows:
        print(f"ID: {row[0]} | Nombre: {row[1]} | Edad: {row[2]}")
    print()

def update_student():
    """Solicita un ID y actualiza los datos de un estudiante."""
    select_all_students()
    student_id = input("Ingrese el ID del estudiante a actualizar: ")
    
    if not student_id.isdigit():
        print("Error: El ID debe ser un número.")
        return

    name = input("Ingrese el nuevo nombre: ")
    age = input("Ingrese la nueva edad: ")
    
    if not age.isdigit():
        print("Error: La edad debe ser un número.")
        return
    
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("UPDATE students SET name = ?, age = ? WHERE id = ?", (name, int(age), int(student_id)))
    conn.commit()
    conn.close()
    print(f"Estudiante con ID {student_id} actualizado correctamente.")

def delete_student():
    """Solicita un ID y elimina un estudiante."""
    select_all_students()
    student_id = input("Ingrese el ID del estudiante a eliminar: ")
    
    if not student_id.isdigit():
        print("Error: El ID debe ser un número.")
        return

    conn = create_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id = ?", (int(student_id),))
    conn.commit()
    conn.close()
    print(f"Estudiante con ID {student_id} eliminado correctamente.")

def main():
    create_table()
    
    while True:
        print("\n📚 Menú de Gestión de Estudiantes 📚")
        print("1. Agregar Estudiante")
        print("2. Ver Estudiantes")
        print("3. Actualizar Estudiante")
        print("4. Eliminar Estudiante")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            insert_student()
        elif opcion == "2":
            select_all_students()
        elif opcion == "3":
            update_student()
        elif opcion == "4":
            delete_student()
        elif opcion == "5":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
