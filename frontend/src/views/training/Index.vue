<template>
  <el-tabs v-model="activeTab">
    <!-- 课程库 -->
    <el-tab-pane label="课程库" name="courses">
      <el-card>
        <template #header>
          <div style="display:flex;justify-content:space-between;align-items:center">
            <span>培训课程</span>
            <el-button type="primary" @click="courseDialog = true">新增课程</el-button>
          </div>
        </template>
        <el-table :data="courses" border>
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="title" label="课程名称" />
          <el-table-column prop="category" label="类别" width="110">
            <template #default="{ row }"><el-tag size="small">{{ row.category }}</el-tag></template>
          </el-table-column>
          <el-table-column prop="lecturer" label="讲师" width="120" />
          <el-table-column prop="hours" label="课时" width="80" />
          <el-table-column prop="max_students" label="上限" width="80" />
        </el-table>
      </el-card>
    </el-tab-pane>

    <!-- 培训计划 -->
    <el-tab-pane label="培训计划" name="plans">
      <el-card>
        <template #header>
          <div style="display:flex;justify-content:space-between;align-items:center">
            <span>开班计划</span>
            <el-button type="primary" @click="planDialog = true">创建计划</el-button>
          </div>
        </template>
        <el-table :data="plans" border>
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="course_title" label="课程" />
          <el-table-column prop="start_date" label="开始" width="120" />
          <el-table-column prop="end_date" label="结束" width="120" />
          <el-table-column prop="location" label="地点" />
          <el-table-column prop="student_count" label="已报名" width="90" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="row.status === 'completed' ? 'success' : row.status === 'ongoing' ? 'warning' : 'info'">
                {{ row.status === 'completed' ? '已完成' : row.status === 'ongoing' ? '进行中' : '计划中' }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </el-tab-pane>

    <!-- 人才梯队 -->
    <el-tab-pane label="人才梯队" name="pipeline">
      <el-card>
        <template #header>
          <div style="display:flex;justify-content:space-between;align-items:center">
            <span>储备干部/继任计划</span>
            <el-button type="primary" @click="pipelineDialog = true">加入梯队</el-button>
          </div>
        </template>
        <el-table :data="pipeline" border>
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="employee_name" label="姓名" width="120" />
          <el-table-column prop="dept_name" label="部门" />
          <el-table-column prop="target_position" label="目标岗位" />
          <el-table-column prop="level" label="层级" width="100">
            <template #default="{ row }"><el-tag size="small">{{ row.level }}</el-tag></template>
          </el-table-column>
          <el-table-column prop="readiness" label="就绪度" width="180">
            <template #default="{ row }">
              <el-progress :percentage="row.readiness" :color="row.readiness > 70 ? '#67c23a' : row.readiness > 40 ? '#e6a23c' : '#f56c6c'" />
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </el-tab-pane>
  </el-tabs>

  <!-- 新增课程弹窗 -->
  <el-dialog v-model="courseDialog" title="新增培训课程" width="450px">
    <el-form :model="courseForm" label-width="100px">
      <el-form-item label="课程名称"><el-input v-model="courseForm.title" /></el-form-item>
      <el-form-item label="类别">
        <el-select v-model="courseForm.category">
          <el-option label="新员工培训" value="新员工" />
          <el-option label="岗位技能" value="岗位技能" />
          <el-option label="管理培训" value="管理" />
          <el-option label="安全培训" value="安全" />
        </el-select>
      </el-form-item>
      <el-form-item label="讲师"><el-input v-model="courseForm.lecturer" /></el-form-item>
      <el-form-item label="课时"><el-input v-model.number="courseForm.hours" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="courseDialog = false">取消</el-button>
      <el-button type="primary" @click="saveCourse">保存</el-button>
    </template>
  </el-dialog>

  <!-- 创建计划弹窗 -->
  <el-dialog v-model="planDialog" title="创建培训计划" width="450px">
    <el-form :model="planForm" label-width="100px">
      <el-form-item label="课程">
        <el-select v-model="planForm.course_id" style="width:100%" @change="onCourseChange">
          <el-option v-for="c in courses" :key="c.id" :label="c.title" :value="c.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="开始日期"><el-input v-model="planForm.start_date" placeholder="2026-10-15" /></el-form-item>
      <el-form-item label="地点"><el-input v-model="planForm.location" placeholder="会议室/线上" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="planDialog = false">取消</el-button>
      <el-button type="primary" @click="savePlan">创建</el-button>
    </template>
  </el-dialog>

  <!-- 加入梯队弹窗 -->
  <el-dialog v-model="pipelineDialog" title="加入人才梯队" width="450px">
    <el-form :model="pipelineForm" label-width="100px">
      <el-form-item label="姓名"><el-input v-model="pipelineForm.employee_name" /></el-form-item>
      <el-form-item label="部门"><el-input v-model="pipelineForm.dept_name" /></el-form-item>
      <el-form-item label="目标岗位"><el-input v-model="pipelineForm.target_position" /></el-form-item>
      <el-form-item label="层级">
        <el-select v-model="pipelineForm.level">
          <el-option label="储备" value="储备" />
          <el-option label="后备" value="后备" />
          <el-option label="继任" value="继任" />
        </el-select>
      </el-form-item>
      <el-form-item label="就绪度"><el-input v-model.number="pipelineForm.readiness" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="pipelineDialog = false">取消</el-button>
      <el-button type="primary" @click="savePipeline">加入</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getCourses, addCourse, getPlans, addPlan, getPipeline, addPipeline } from '../../api'
import { ElMessage } from 'element-plus'

const activeTab = ref('courses')
const courses = ref([])
const plans = ref([])
const pipeline = ref([])

const courseDialog = ref(false)
const courseForm = reactive({ title: '', category: '岗位技能', lecturer: '', hours: 1 })

const planDialog = ref(false)
const planForm = reactive({ course_id: null, course_title: '', start_date: '', location: '' })

const pipelineDialog = ref(false)
const pipelineForm = reactive({ employee_name: '', dept_name: '', target_position: '', level: '储备', readiness: 50 })

function onCourseChange(id) {
  const c = courses.value.find(x => x.id === id)
  if (c) planForm.course_title = c.title
}

async function loadAll() {
  const [c, p, t] = await Promise.all([getCourses(), getPlans(), getPipeline()])
  courses.value = c.data || []
  plans.value = p.data || []
  pipeline.value = t.data || []
}

async function saveCourse() {
  await addCourse(courseForm)
  ElMessage.success('课程已创建')
  courseDialog.value = false
  loadAll()
}

async function savePlan() {
  await addPlan(planForm)
  ElMessage.success('培训计划已创建')
  planDialog.value = false
  loadAll()
}

async function savePipeline() {
  await addPipeline(pipelineForm)
  ElMessage.success('已加入人才梯队')
  pipelineDialog.value = false
  loadAll()
}

onMounted(loadAll)
</script>
