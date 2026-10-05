"""灌入模拟测试数据"""
from app.core.database import SessionLocal, init_db
from app.modules.organization.models import Department
from app.modules.employee.models import Employee
from app.modules.attendance.models import AttendanceRecord, LeaveRequest
from app.modules.salary.models import SalaryRecord
from app.modules.recruitment.models import Resume, RecruitmentDemand
from app.modules.training.models import TrainingPlan, TrainingRecord, TrainingCourse
from app.modules.performance.models import PerformanceScore
from app.modules.employee_relation.models import LaborContract, Offboarding
from datetime import date, datetime, timedelta

init_db()
db = SessionLocal()

# 清理旧数据（保留admin用户和模型配置）
for m in [Employee, Department, AttendanceRecord, LeaveRequest, SalaryRecord,
          Resume, RecruitmentDemand, TrainingPlan, TrainingRecord, TrainingCourse,
          PerformanceScore, LaborContract, Offboarding]:
    db.query(m).delete()

# 部门
depts = [
    Department(dept_name="技术部", parent_id=None, sort=1, status=1),
    Department(dept_name="产品部", parent_id=None, sort=2, status=1),
    Department(dept_name="市场部", parent_id=None, sort=3, status=1),
    Department(dept_name="人事部", parent_id=None, sort=4, status=1),
    Department(dept_name="财务部", parent_id=None, sort=5, status=1),
]
db.add_all(depts)
db.flush()
dept_map = {d.dept_name: d.id for d in depts}

# 员工
employees = [
    ("E001", "张伟", "男", "1990-05-15", "110101199005150011", "13800138001", "技术部", "高级前端工程师", "正式"),
    ("E002", "李娜", "女", "1992-08-22", "110101199208220022", "13800138002", "技术部", "后端工程师", "正式"),
    ("E003", "王强", "男", "1988-03-10", "110101198803100033", "13800138003", "技术部", "技术经理", "正式"),
    ("E004", "赵敏", "女", "1993-11-05", "110101199311050044", "13800138004", "产品部", "产品经理", "正式"),
    ("E005", "陈杰", "男", "1991-07-18", "110101199107180055", "13800138005", "产品部", "产品助理", "正式"),
    ("E006", "刘洋", "男", "1989-02-28", "110101198902280066", "13800138006", "市场部", "市场总监", "正式"),
    ("E007", "孙丽", "女", "1994-09-12", "110101199409120077", "13800138007", "市场部", "市场专员", "正式"),
    ("E008", "周婷", "女", "1990-12-01", "110101199012010088", "13800138008", "人事部", "HR经理", "正式"),
    ("E009", "吴磊", "男", "1995-04-20", "110101199504200099", "13800138009", "人事部", "招聘专员", "正式"),
    ("E010", "郑爽", "女", "1992-06-30", "110101199206300010", "13800138010", "财务部", "会计", "正式"),
    ("E011", "冯刚", "男", "1987-10-08", "110101198710080011", "13800138011", "技术部", "测试工程师", "正式"),
    ("E012", "陈思", "女", "1996-01-15", "110101199601150012", "13800138012", "市场部", "新媒体运营", "试用"),
]
for emp in employees:
    y, m, d = map(int, emp[3].split("-"))
    db.add(Employee(
        emp_no=emp[0], name=emp[1], gender=emp[2], birthday=date(y, m, d),
        id_card=emp[4], phone=emp[5], dept_id=dept_map[emp[6]],
        position=emp[7], employee_type=emp[8],
        entry_date=date.today() - timedelta(days=365*2),
        status="active", education="本科",
        base_salary=15000,
    ))

# 招聘需求和简历
db.add(RecruitmentDemand(title="前端工程师", dept_id=dept_map["技术部"], headcount=2,
                         salary_range="15k-25k", channel="BOSS直聘", status="open"))
db.add(RecruitmentDemand(title="产品经理", dept_id=dept_map["产品部"], headcount=1,
                         salary_range="18k-30k", channel="内推", status="open"))

resumes = [
    Resume(candidate_name="马小明", phone="13900139001", education="本科", school="北京大学",
           current_company="百度", current_position="前端工程师", status="screening", match_score=85),
    Resume(candidate_name="杨丽", phone="13900139002", education="硕士", school="清华大学",
           current_company="阿里", current_position="产品经理", status="interview", match_score=92),
    Resume(candidate_name="周杰", phone="13900139003", education="本科", school="浙江大学",
           current_company="腾讯", current_position="后端工程师", status="new", match_score=78),
    Resume(candidate_name="吴倩", phone="13900139004", education="本科", school="复旦大学",
           current_company="美团", current_position="运营", status="hired", match_score=88),
    Resume(candidate_name="郑浩", phone="13900139005", education="大专", school="深职院",
           current_company="创业公司", current_position="前端", status="rejected", match_score=55),
]
for r in resumes:
    db.add(r)

# 培训课程和计划
db.add(TrainingCourse(title="新员工入职培训", category="新员工", lecturer="周婷", hours=8))
db.add(TrainingCourse(title="管理技能提升", category="管理", lecturer="外部讲师", hours=16))
db.add(TrainingPlan(course_id=1, course_title="新员工入职培训", start_date=date.today(),
                    end_date=date.today()+timedelta(days=1), location="一楼会议室", student_count=3, status="ongoing"))

# 绩效评分
grades_data = [
    ("张伟", "技术部", 92, "S"), ("李娜", "技术部", 85, "A"),
    ("王强", "技术部", 88, "A"), ("赵敏", "产品部", 78, "B"),
    ("陈杰", "产品部", 65, "C"), ("刘洋", "市场部", 90, "S"),
    ("孙丽", "市场部", 72, "B"), ("周婷", "人事部", 82, "A"),
    ("吴磊", "人事部", 75, "B"), ("郑爽", "财务部", 80, "A"),
    ("冯刚", "技术部", 60, "C"), ("陈思", "市场部", 55, "D"),
]
for name, dept, score, grade in grades_data:
    db.add(PerformanceScore(cycle_id=1, employee_name=name, dept_name=dept,
                            self_score=score-5, manager_score=score, final_score=score, grade=grade))

# 合同
for emp in employees[:10]:
    db.add(LaborContract(employee_name=emp[1], contract_type="固定期限",
                         start_date=date.today()-timedelta(days=365),
                         end_date=date.today()+timedelta(days=200),
                         sign_date=date.today()-timedelta(days=365)))

# 离职记录
db.add(Offboarding(employee_name="前员工A", dept_name="市场部", position="市场专员",
                   resign_date=date.today()-timedelta(days=30),
                   last_day=date.today()-timedelta(days=15),
                   reason_category="发展", reason_detail="寻求更好的职业发展机会"))

# 薪资记录
for emp in employees:
    db.add(SalaryRecord(employee_id=1, salary_month="2026-10",
                        base_salary=12000, performance_salary=3000, allowance=500,
                        social_insurance=1260, housing_fund=840, tax=200,
                        gross_salary=15500, net_salary=13200, status="calculated"))

db.commit()
print("模拟数据灌入完成！")
print(f"部门: {len(depts)}个")
print(f"员工: {len(employees)}人")
print(f"简历: {len(resumes)}份")
print(f"绩效评分: {len(grades_data)}条")
print(f"合同: 10份")
