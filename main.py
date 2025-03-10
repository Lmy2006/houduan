from fastapi import FastAPI
from .database import init_db
from .routers import students, introduction, announcements

app = FastAPI()

# 初始化数据库
init_db()

# 集成路由
app.include_router(students.router)
app.include_router(introduction.router)
app.include_router(announcements.router)

@app.get("/")
async def root():
    return {"message": "云顶书院学生管理系统"}

if __name__ == "__main__":
    init_db()

class StudentCreate(BaseModel):
    name: str
    age: int
    grade: str
    category: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/students/")
def read_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students

@app.get("/students/{student_id}")
def read_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.post("/students/")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = Student(name=student.name, age=student.age, grade=student.grade)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.put("/students/{student_id}")
def update_student(student_id: int, student: StudentCreate, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db_student.name = student.name
    db_student.age = student.age
    db_student.grade = student.grade
    db.commit()
    db.refresh(db_student)
    return db_student

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted"}
