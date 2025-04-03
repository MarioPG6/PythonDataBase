import sqlite3

def create_connection():
    """Crea una conexión a la base de datos SQLite."""
    return sqlite3.connect("school.db")

def create_tables():
    """Crea las tablas si no existen."""
    conn = create_connection()
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER
        );
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS student_subjects (
            student_id INTEGER,
            subject_id INTEGER,
            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
            FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
            PRIMARY KEY (student_id, subject_id)
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

def insert_subject():
    """Solicita datos y agrega una nueva materia."""
    name = input("Ingrese el nombre de la materia: ")
    
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO subjects(name) VALUES(?)", (name,))
    conn.commit()
    conn.close()
    print(f"Materia '{name}' agregada correctamente.")

def select_all_subjects():
    """Muestra todas las materias."""
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM subjects")
    rows = cur.fetchall()
    conn.close()
    
    print("\nLista de Materias:")
    for row in rows:
        print(f"ID: {row[0]} | Nombre: {row[1]}")
    print()

def update_subject():
    """Solicita un ID y actualiza el nombre de una materia."""
    select_all_subjects()
    subject_id = input("Ingrese el ID de la materia a actualizar: ")
    
    if not subject_id.isdigit():
        print("Error: El ID debe ser un número.")
        return

    name = input("Ingrese el nuevo nombre de la materia: ")
    
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("UPDATE subjects SET name = ? WHERE id = ?", (name, int(subject_id)))
    conn.commit()
    conn.close()
    print(f"Materia con ID {subject_id} actualizada correctamente.")

def delete_subject():
    """Solicita un ID y elimina una materia."""
    select_all_subjects()
    subject_id = input("Ingrese el ID de la materia a eliminar: ")
    
    if not subject_id.isdigit():
        print("Error: El ID debe ser un número.")
        return

    conn = create_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM subjects WHERE id = ?", (int(subject_id),))
    conn.commit()
    conn.close()
    print(f"Materia con ID {subject_id} eliminada correctamente.")

def enroll_student_in_subject():
    """Asigna un estudiante a una materia evitando duplicados."""
    select_all_students()
    student_id = input("Ingrese el ID del estudiante: ")

    select_all_subjects()
    subject_id = input("Ingrese el ID de la materia: ")

    if not student_id.isdigit() or not subject_id.isdigit():
        print("Error: ID de estudiante y materia deben ser números.")
        return

    conn = create_connection()
    cur = conn.cursor()

    # Verificar si el estudiante ya está inscrito en la materia
    cur.execute("SELECT 1 FROM student_subjects WHERE student_id = ? AND subject_id = ?", 
                (int(student_id), int(subject_id)))
    
    if cur.fetchone():
        print(f"⚠️ El estudiante con ID {student_id} ya está inscrito en la materia {subject_id}.")
    else:
        cur.execute("INSERT INTO student_subjects(student_id, subject_id) VALUES(?, ?)", 
                    (int(student_id), int(subject_id)))
        conn.commit()
        print(f"✅ Estudiante {student_id} inscrito en materia {subject_id} correctamente.")

    conn.close()


def show_students_with_subjects():
    """Muestra todos los estudiantes con las materias en las que están inscritos."""
    conn = create_connection()
    cur = conn.cursor()
    
    cur.execute('''
        SELECT students.id, students.name, subjects.name 
        FROM students
        JOIN student_subjects ON students.id = student_subjects.student_id
        JOIN subjects ON student_subjects.subject_id = subjects.id
        ORDER BY students.id
    ''')
    
    rows = cur.fetchall()
    conn.close()
    
    print("\nLista de Estudiantes con Materias:")
    for row in rows:
        print(f"ID: {row[0]} | Nombre: {row[1]} | Materia: {row[2]}")
    print()

def main():
    create_tables()
    
    while True:
        print("\n📚 Menú de Gestión Escolar 📚")
        print("1. Agregar Estudiante")
        print("2. Ver Estudiantes")
        print("3. Actualizar Estudiante")
        print("4. Eliminar Estudiante")
        print("5. Agregar Materia")
        print("6. Ver Materias")
        print("7. Actualizar Materia")
        print("8. Eliminar Materia")
        print("9. Inscribir Estudiante en Materia")
        print("10. Ver Estudiantes con Materias")
        print("11. Salir")
        
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
            insert_subject()
        elif opcion == "6":
            select_all_subjects()
        elif opcion == "7":
            update_subject()
        elif opcion == "8":
            delete_subject()
        elif opcion == "9":
            enroll_student_in_subject()
        elif opcion == "10":
            show_students_with_subjects()
        elif opcion == "11":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
