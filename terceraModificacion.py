import sqlite3

def create_connection():
    """Crea una conexión a la base de datos SQLite."""
    return sqlite3.connect("school.db")

def create_tables():
    """Crea las tablas si no existen."""
    conn = create_connection()
    c = conn.cursor()
    
    # Tabla de estudiantes
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER
        );
    ''')

    # Tabla de materias
    c.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
    ''')

    # Tabla de inscripción de estudiantes en materias
    c.execute('''
        CREATE TABLE IF NOT EXISTS student_subjects (
            student_id INTEGER,
            subject_id INTEGER,
            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
            FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
            PRIMARY KEY (student_id, subject_id)
        );
    ''')

    # Tabla de universidades
    c.execute('''
        CREATE TABLE IF NOT EXISTS universities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
    ''')

    # Tabla de materias ofrecidas por universidades
    c.execute('''
        CREATE TABLE IF NOT EXISTS offered_subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER,
            university_id INTEGER,
            FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
            FOREIGN KEY (university_id) REFERENCES universities(id) ON DELETE CASCADE
        );
    ''')

    conn.commit()
    conn.close()

def insert_university():
    """Solicita datos y agrega una nueva universidad."""
    name = input("Ingrese el nombre de la universidad: ")

    conn = create_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO universities(name) VALUES(?)", (name,))
    conn.commit()
    conn.close()
    print(f"Universidad '{name}' agregada correctamente.")


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


def insert_subject():
    """Solicita datos y agrega una nueva materia."""
    name = input("Ingrese el nombre de la materia: ")
    
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO subjects(name) VALUES(?)", (name,))
    conn.commit()
    conn.close()
    print(f"Materia '{name}' agregada correctamente.")



def select_all_universities():
    """Muestra todas las universidades."""
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM universities")
    rows = cur.fetchall()
    conn.close()
    
    print("\nLista de Universidades:")
    for row in rows:
        print(f"ID: {row[0]} | Nombre: {row[1]}")
    print()

def offer_subject():
    """Permite que una universidad ofrezca una materia."""
    select_all_subjects()
    subject_id = input("Ingrese el ID de la materia: ")

    select_all_universities()
    university_id = input("Ingrese el ID de la universidad que ofrece la materia: ")

    if not subject_id.isdigit() or not university_id.isdigit():
        print("Error: Los ID deben ser números.")
        return

    conn = create_connection()
    cur = conn.cursor()

    # Verificar si la materia ya está ofrecida por esa universidad
    cur.execute("SELECT 1 FROM offered_subjects WHERE subject_id = ? AND university_id = ?", 
                (int(subject_id), int(university_id)))

    if cur.fetchone():
        print(f"⚠️ La materia con ID {subject_id} ya es ofrecida por la universidad {university_id}.")
    else:
        cur.execute("INSERT INTO offered_subjects(subject_id, university_id) VALUES(?, ?)", 
                    (int(subject_id), int(university_id)))
        conn.commit()
        print(f"✅ Materia {subject_id} ofrecida en la universidad {university_id} correctamente.")

    conn.close()

def select_all_offered_subjects():
    """Muestra todas las materias ofrecidas por universidades."""
    conn = create_connection()
    cur = conn.cursor()
    
    cur.execute('''
        SELECT offered_subjects.id, subjects.name, universities.name 
        FROM offered_subjects
        JOIN subjects ON offered_subjects.subject_id = subjects.id
        JOIN universities ON offered_subjects.university_id = universities.id
    ''')
    
    rows = cur.fetchall()
    conn.close()
    
    print("\nLista de Materias Ofrecidas por Universidades:")
    for row in rows:
        print(f"ID Oferta: {row[0]} | Materia: {row[1]} | Universidad: {row[2]}")
    print()

def enroll_student_in_subject():
    """Permite a un estudiante inscribirse en una materia."""
    select_all_students()
    student_id = input("Ingrese el ID del estudiante: ")

    select_all_subjects()
    subject_id = input("Ingrese el ID de la materia: ")

    if not student_id.isdigit() or not subject_id.isdigit():
        print("❌ Error: Los ID deben ser números.")
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
        print(f"✅ Estudiante {student_id} inscrito en la materia {subject_id} correctamente.")

    conn.close()

def show_student_subjects():
    """Permite seleccionar un estudiante y ver las materias en las que está inscrito."""
    select_all_students()
    student_id = input("Ingrese el ID del estudiante para ver sus materias: ")

    if not student_id.isdigit():
        print("❌ Error: El ID debe ser un número.")
        return

    conn = create_connection()
    cur = conn.cursor()

    # Obtener nombre del estudiante
    cur.execute("SELECT name FROM students WHERE id = ?", (int(student_id),))
    student = cur.fetchone()

    if not student:
        print(f"⚠️ No se encontró un estudiante con ID {student_id}.")
        conn.close()
        return

    print(f"\n📚 Materias inscritas de {student[0]}:\n")

    # Obtener las materias inscritas del estudiante
    cur.execute('''
        SELECT subjects.name, universities.name 
        FROM student_subjects
        JOIN subjects ON student_subjects.subject_id = subjects.id
        LEFT JOIN offered_subjects ON subjects.id = offered_subjects.subject_id
        LEFT JOIN universities ON offered_subjects.university_id = universities.id
        WHERE student_subjects.student_id = ?
    ''', (int(student_id),))

    subjects = cur.fetchall()
    conn.close()

    if not subjects:
        print("ℹ️ Este estudiante no está inscrito en ninguna materia.\n")
    else:
        for subject in subjects:
            university = subject[1] if subject[1] else "Universidad local"
            print(f"- {subject[0]} (Ofrecida por: {university})")
        print()


def enroll_student_in_offered_subject():
    """Permite a un estudiante inscribirse en una materia ofrecida por otra universidad."""
    select_all_students()
    student_id = input("Ingrese el ID del estudiante: ")

    select_all_offered_subjects()
    offered_subject_id = input("Ingrese el ID de la materia ofrecida en otra universidad: ")

    if not student_id.isdigit() or not offered_subject_id.isdigit():
        print("Error: Los ID deben ser números.")
        return

    conn = create_connection()
    cur = conn.cursor()

    # Obtener el ID real de la materia desde la oferta
    cur.execute("SELECT subject_id FROM offered_subjects WHERE id = ?", (int(offered_subject_id),))
    subject = cur.fetchone()

    if subject:
        subject_id = subject[0]

        # Verificar si el estudiante ya está inscrito en la materia
        cur.execute("SELECT 1 FROM student_subjects WHERE student_id = ? AND subject_id = ?", 
                    (int(student_id), subject_id))
        
        if cur.fetchone():
            print(f"⚠️ El estudiante con ID {student_id} ya está inscrito en la materia {subject_id}.")
        else:
            cur.execute("INSERT INTO student_subjects(student_id, subject_id) VALUES(?, ?)", 
                        (int(student_id), subject_id))
            conn.commit()
            print(f"✅ Estudiante {student_id} inscrito en la materia {subject_id} correctamente.")
    else:
        print("❌ Error: No se encontró la materia ofrecida.")

    conn.close()

def main():
    create_tables()
    
    while True:
        print("\n📚 Menú de Gestión Escolar 📚")
        print("1. Agregar Estudiante")
        print("2. Ver Estudiantes")
        print("3. Agregar Materia")
        print("4. Ver Materias")
        print("5. Agregar Universidad")
        print("6. Ver Universidades")
        print("7. Ofrecer Materia en Universidad")
        print("8. Ver Materias Ofrecidas")
        print("9. Inscribir Estudiante en Materia")
        print("10. Inscribir Estudiante en Materia de Otra Universidad")
        print("11. Estudiantes inscritos")
        print("12. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            insert_student()
        elif opcion == "2":
            select_all_students()
        elif opcion == "3":
            insert_subject()
        elif opcion == "4":
            select_all_subjects()
        elif opcion == "5":
            insert_university()
        elif opcion == "6":
            select_all_universities()
        elif opcion == "7":
            offer_subject()
        elif opcion == "8":
            select_all_offered_subjects()
        elif opcion == "9":
            enroll_student_in_subject()
        elif opcion == "10":
            enroll_student_in_offered_subject()
        elif opcion == "11":
            show_student_subjects()
        elif opcion == "12":
            print("Saliendo del programa....")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
