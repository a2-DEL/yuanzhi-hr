<template>
  <div>
    <!-- 欢迎卡片 -->
    <el-card style="margin-bottom:16px;background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;border:none">
      <h2 style="margin:0">👋 {{ profile.name || '员工' }}，欢迎回来</h2>
      <p style="margin:8px 0 0;opacity:0.9">{{ profile.dept }} · {{ profile.position }} · 工号 {{ profile.emp_no }}</p>
    </el-card>

    <!-- 假期余额卡片 -->
    <el-row :gutter="16" style="margin-bottom:16px">
      <el-col :span="8">
        <el-card shadow="hover">
          <div style="text-align:center">
            <div style="font-size:32px;font-weight:bold;color:#67c23a">{{ dash.year_leave_balance || 0 }}</div>
            <div style="color:#999">年假余额（天）</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <div style="text-align:center">
            <div style="font-size:32px;font-weight:bold;color:#e6a23c">{{ dash.sick_leave_balance || 0 }}</div>
            <div style="color:#999">病假余额（天）</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <div style="text-align:center">
            <div style="font-size:32px;font-weight:bold;color:#409eff">{{ dash.pending_leaves || 0 }}</div>
            <div style="color:#999">待审批申请</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-tabs v-model="activeTab">
      <!-- 我的工资条 -->
      <el-tab-pane label="💰 我的工资条" name="salary">
        <el-table :data="salaryList" border stripe>
          <el-table-column prop="period" label="薪资周期" />
          <el-table-column prop="base" label="基本工资">
            <template #default="{ row }">¥{{ row.base }}</template>
          </el-table-column>
          <el-table-column prop="bonus" label="奖金">
            <template #default="{ row }">¥{{ row.bonus }}</template>
          </el-table-column>
          <el-table-column prop="social" label="社保">
            <template #default="{ row }">-¥{{ row.social }}</template>
          </el-table-column>
          <el-table-column prop="housing" label="公积金">
            <template #default="{ row }">-¥{{ row.housing }}</template>
          </el-table-column>
          <el-table-column prop="tax" label="个税">
            <template #default="{ row }">-¥{{ row.tax }}</template>
          </el-table-column>
          <el-table-column prop="net" label="实发工资">
            <template #default="{ row }">
              <b style="color:#67c23a">¥{{ row.net }}</b>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <!-- 我的考勤 -->
      <el-tab-pane label="📅 我的考勤" name="attendance">
        <el-table :data="attendance.records || []" border stripe size="small">
          <el-table-column prop="date" label="日期" />
          <el-table-column prop="check_in" label="上班打卡" />
          <el-table-column prop="check_out" label="下班打卡" />
          <el-table-column prop="status" label="状态">
            <template #default="{ row }">
              <el-tag :type="row.status === 'normal' ? 'success' : 'warning'" size="small">{{ row.status }}</el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <!-- 我的请假 -->
      <el-tab-pane label="📝 我的请假" name="leave">
        <div style="margin-bottom:12px">
          <el-button type="primary" @click="leaveDialog = true">申请请假</el-button>
        </div>
        <el-table :data="leaveList" border stripe>
          <el-table-column prop="type" label="假别" />
          <el-table-column prop="start_date" label="开始日期" />
          <el-table-column prop="end_date" label="结束日期" />
          <el-table-column prop="days" label="天数" />
          <el-table-column prop="reason" label="事由" />
          <el-table-column prop="status" label="状态">
            <template #default="{ row }">
              <el-tag :type="row.status === 'approved' ? 'success' : row.status === 'pending' ? 'warning' : 'danger'" size="small">
                {{ row.status }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <!-- 我的绩效 -->
      <el-tab-pane label="🏆 我的绩效" name="performance">
        <el-table :data="perfList" border stripe>
          <el-table-column prop="period" label="考核周期" />
          <el-table-column prop="level" label="绩效等级">
            <template #default="{ row }">
              <el-tag :type="{S:'danger',A:'warning',B:'primary',C:'success',D:'info'}[row.level]" size="small">{{ row.level }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="score" label="得分" />
          <el-table-column prop="comment" label="评语" />
        </el-table>
      </el-tab-pane>
    </el-tabs>

    <!-- 请假弹窗 -->
    <el-dialog v-model="leaveDialog" title="申请请假" width="500px">
      <el-form :model="leaveForm" label-width="80px">
        <el-form-item label="假别">
          <el-select v-model="leaveForm.type" style="width:100%">
            <el-option label="事假" value="事假" />
            <el-option label="年假" value="年假" />
            <el-option label="病假" value="病假" />
            <el-option label="调休" value="调休" />
          </el-select>
        </el-form-item>
        <el-form-item label="开始日期">
          <el-date-picker v-model="leaveForm.start_date" type="date" value-format="YYYY-MM-DD" style="width:100%" />
        </el-form-item>
        <el-form-item label="结束日期">
          <el-date-picker v-model="leaveForm.end_date" type="date" value-format="YYYY-MM-DD" style="width:100%" />
        </el-form-item>
        <el-form-item label="天数">
          <el-input-number v-model="leaveForm.days" :min="0.5" :step="0.5" />
        </el-form-item>
        <el-form-item label="事由">
          <el-input v-model="leaveForm.reason" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="leaveDialog = false">取消</el-button>
        <el-button type="primary" @click="submitLeave">提交</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import request from '../../api/request'
import { ElMessage } from 'element-plus'

const activeTab = ref('salary')
const profile = ref({})
const dash = ref({})
const salaryList = ref([])
const attendance = ref({ records: [] })
const leaveList = ref([])
const perfList = ref([])
const leaveDialog = ref(false)
const leaveForm = ref({ type: '事假', days: 1 })

async function load() {
  try {
    const [p, d, s, a, l, pf] = await Promise.all([
      request.get('/api/self/profile'),
      request.get('/api/self/dashboard'),
      request.get('/api/self/salary'),
      request.get('/api/self/attendance'),
      request.get('/api/self/leaves'),
      request.get('/api/self/performance'),
    ])
    profile.value = p.data
    dash.value = d.data
    salaryList.value = s.data || []
    attendance.value = a.data
    leaveList.value = l.data || []
    perfList.value = pf.data || []
  } catch (e) {}
}

async function submitLeave() {
  await request.post('/api/self/leave', leaveForm.value)
  ElMessage.success('请假申请已提交')
  leaveDialog.value = false
  load()
}

onMounted(load)
</script>
