<template>
  <el-tabs v-model="activeTab">
    <!-- 招聘漏斗 -->
    <el-tab-pane label="招聘漏斗" name="funnel">
      <el-card>
        <h3 style="margin-top:0">招聘转化漏斗</h3>
        <div class="funnel-container">
          <div class="funnel-step" :style="{ width: funnel.total ? funnel.total*2 + 20 + '%' : '20%' }">
            <div class="funnel-label">简历总数</div>
            <div class="funnel-value">{{ funnel.total }}</div>
          </div>
          <div class="funnel-step bg-blue" :style="{ width: funnel.total ? funnel.screening*2 + 20 + '%' : '15%' }">
            <div class="funnel-label">筛选通过</div>
            <div class="funnel-value">{{ funnel.screening }}</div>
          </div>
          <div class="funnel-step bg-cyan" :style="{ width: funnel.total ? funnel.interview*2 + 20 + '%' : '12%' }">
            <div class="funnel-label">面试</div>
            <div class="funnel-value">{{ funnel.interview }}</div>
          </div>
          <div class="funnel-step bg-teal" :style="{ width: funnel.total ? funnel.offer*2 + 20 + '%' : '10%' }">
            <div class="funnel-label">Offer</div>
            <div class="funnel-value">{{ funnel.offer }}</div>
          </div>
          <div class="funnel-step bg-green" :style="{ width: funnel.total ? funnel.hired*2 + 20 + '%' : '8%' }">
            <div class="funnel-label">已入职</div>
            <div class="funnel-value">{{ funnel.hired }}</div>
          </div>
        </div>
      </el-card>
    </el-tab-pane>

    <!-- 招聘需求 -->
    <el-tab-pane label="招聘需求" name="demands">
      <el-card>
        <template #header>
          <div style="display:flex;justify-content:space-between;align-items:center">
            <span>在招职位</span>
            <el-button type="primary" @click="demandDialog = true">发布需求</el-button>
          </div>
        </template>
        <el-table :data="demands" border>
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="title" label="职位名称" />
          <el-table-column prop="headcount" label="招聘人数" width="90" />
          <el-table-column prop="salary_range" label="薪资范围" width="120" />
          <el-table-column prop="channel" label="渠道" width="110" />
          <el-table-column prop="expected_date" label="期望到岗" width="120" />
          <el-table-column prop="status" label="状态" width="90">
            <template #default="{ row }">
              <el-tag :type="row.status === 'open' ? 'success' : 'info'">
                {{ row.status === 'open' ? '招聘中' : '已关闭' }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </el-tab-pane>

    <!-- 简历库 -->
    <el-tab-pane label="简历库" name="resumes">
      <el-card>
        <template #header>
          <div style="display:flex;justify-content:space-between;align-items:center">
            <span>候选人简历</span>
            <el-button type="primary" @click="resumeDialog = true">录入简历</el-button>
          </div>
        </template>
        <el-table :data="resumes" border>
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="candidate_name" label="姓名" width="100" />
          <el-table-column prop="phone" label="电话" width="130" />
          <el-table-column prop="education" label="学历" width="80" />
          <el-table-column prop="school" label="毕业院校" />
          <el-table-column prop="current_company" label="当前公司" />
          <el-table-column prop="current_position" label="当前职位" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <el-tag size="small">{{ statusMap[row.status] || row.status }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="180">
            <template #default="{ row }">
              <el-select v-model="row.status" size="small" style="width:100px" @change="changeStatus(row)">
                <el-option label="新简历" value="new" />
                <el-option label="筛选中" value="screening" />
                <el-option label="面试" value="interview" />
                <el-option label="Offer" value="offer" />
                <el-option label="已入职" value="hired" />
                <el-option label="已拒绝" value="rejected" />
              </el-select>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </el-tab-pane>

    <!-- 面试安排 -->
    <el-tab-pane label="面试安排" name="interviews">
      <el-card>
        <template #header>
          <div style="display:flex;justify-content:space-between;align-items:center">
            <span>面试日程</span>
            <el-button type="primary" @click="interviewDialog = true">安排面试</el-button>
          </div>
        </template>
        <el-table :data="interviews" border>
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="candidate_name" label="候选人" width="120" />
          <el-table-column prop="interviewer" label="面试官" width="120" />
          <el-table-column prop="interview_time" label="面试时间" width="180" />
          <el-table-column prop="location" label="地点/链接" />
          <el-table-column prop="result" label="结果" width="100">
            <template #default="{ row }">
              <el-tag :type="row.result === 'pass' ? 'success' : row.result === 'fail' ? 'danger' : 'warning'">
                {{ row.result === 'pass' ? '通过' : row.result === 'fail' ? '未通过' : '待面' }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </el-tab-pane>
  </el-tabs>

  <!-- 发布需求弹窗 -->
  <el-dialog v-model="demandDialog" title="发布招聘需求" width="500px">
    <el-form :model="demandForm" label-width="100px">
      <el-form-item label="职位名称"><el-input v-model="demandForm.title" /></el-form-item>
      <el-form-item label="招聘人数"><el-input v-model.number="demandForm.headcount" /></el-form-item>
      <el-form-item label="薪资范围"><el-input v-model="demandForm.salary_range" placeholder="如 15k-25k" /></el-form-item>
      <el-form-item label="渠道">
        <el-select v-model="demandForm.channel">
          <el-option label="BOSS直聘" value="BOSS直聘" />
          <el-option label="智联招聘" value="智联招聘" />
          <el-option label="内部推荐" value="内部推荐" />
          <el-option label="校园招聘" value="校园招聘" />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="demandDialog = false">取消</el-button>
      <el-button type="primary" @click="saveDemand">发布</el-button>
    </template>
  </el-dialog>

  <!-- 录入简历弹窗 -->
  <el-dialog v-model="resumeDialog" title="录入候选人简历" width="500px">
    <el-form :model="resumeForm" label-width="100px">
      <el-form-item label="姓名"><el-input v-model="resumeForm.candidate_name" /></el-form-item>
      <el-form-item label="电话"><el-input v-model="resumeForm.phone" /></el-form-item>
      <el-form-item label="学历">
        <el-select v-model="resumeForm.education">
          <el-option label="大专" value="大专" />
          <el-option label="本科" value="本科" />
          <el-option label="硕士" value="硕士" />
          <el-option label="博士" value="博士" />
        </el-select>
      </el-form-item>
      <el-form-item label="毕业院校"><el-input v-model="resumeForm.school" /></el-form-item>
      <el-form-item label="当前公司"><el-input v-model="resumeForm.current_company" /></el-form-item>
      <el-form-item label="当前职位"><el-input v-model="resumeForm.current_position" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="resumeDialog = false">取消</el-button>
      <el-button type="primary" @click="saveResume">保存</el-button>
    </template>
  </el-dialog>

  <!-- 安排面试弹窗 -->
  <el-dialog v-model="interviewDialog" title="安排面试" width="500px">
    <el-form :model="interviewForm" label-width="100px">
      <el-form-item label="候选人"><el-input v-model="interviewForm.candidate_name" /></el-form-item>
      <el-form-item label="面试官"><el-input v-model="interviewForm.interviewer" /></el-form-item>
      <el-form-item label="面试时间"><el-input v-model="interviewForm.interview_time" placeholder="2026-10-10 14:00" /></el-form-item>
      <el-form-item label="地点"><el-input v-model="interviewForm.location" placeholder="会议室/会议链接" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="interviewDialog = false">取消</el-button>
      <el-button type="primary" @click="saveInterview">安排</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getFunnel, getDemands, addDemand, getResumes, addResume, updateResumeStatus, getInterviews, addInterview } from '../../api'
import { ElMessage } from 'element-plus'

const activeTab = ref('funnel')
const funnel = ref({ total: 0, screening: 0, interview: 0, offer: 0, hired: 0 })
const demands = ref([])
const resumes = ref([])
const interviews = ref([])
const statusMap = { new: '新简历', screening: '筛选中', interview: '面试', offer: 'Offer', hired: '已入职', rejected: '已拒绝' }

const demandDialog = ref(false)
const demandForm = reactive({ title: '', headcount: 1, salary_range: '', channel: 'BOSS直聘' })

const resumeDialog = ref(false)
const resumeForm = reactive({ candidate_name: '', phone: '', education: '本科', school: '', current_company: '', current_position: '' })

const interviewDialog = ref(false)
const interviewForm = reactive({ candidate_name: '', interviewer: '', interview_time: '', location: '' })

async function loadAll() {
  const [f, d, r, i] = await Promise.all([getFunnel(), getDemands(), getResumes(), getInterviews()])
  funnel.value = f.data
  demands.value = d.data || []
  resumes.value = r.data || []
  interviews.value = i.data || []
}

async function saveDemand() {
  await addDemand(demandForm)
  ElMessage.success('招聘需求已发布')
  demandDialog.value = false
  loadAll()
}

async function saveResume() {
  await addResume(resumeForm)
  ElMessage.success('简历已录入')
  resumeDialog.value = false
  loadAll()
}

async function saveInterview() {
  await addInterview(interviewForm)
  ElMessage.success('面试已安排')
  interviewDialog.value = false
  loadAll()
}

async function changeStatus(row) {
  await updateResumeStatus(row.id, row.status)
  ElMessage.success('状态已更新')
}

onMounted(loadAll)
</script>

<style scoped>
.funnel-container { padding: 20px 0; display: flex; flex-direction: column; align-items: center; gap: 8px; }
.funnel-step {
  background: #4f6ef7; color: #fff; padding: 14px; border-radius: 8px;
  text-align: center; transition: width 0.3s;
}
.funnel-step.bg-blue { background: #3b82f6; }
.funnel-step.bg-cyan { background: #06b6d4; }
.funnel-step.bg-teal { background: #14b8a6; }
.funnel-step.bg-green { background: #22c55e; }
.funnel-label { font-size: 13px; opacity: 0.9; }
.funnel-value { font-size: 22px; font-weight: bold; margin-top: 4px; }
</style>
