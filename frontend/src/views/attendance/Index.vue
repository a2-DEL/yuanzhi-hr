<template>
  <el-row :gutter="16">
    <el-col :span="12">
      <el-card>
        <template #header>
          <div style="display:flex;justify-content:space-between;align-items:center">
            <span>打卡</span>
            <el-button type="primary" @click="handleClockIn">上班打卡</el-button>
          </div>
        </template>
        <div style="text-align:center;padding:20px 0">
          <div style="font-size:36px;font-weight:bold;color:#4f6ef7">{{ today }}</div>
          <div style="color:#999;margin-top:8px">{{ time }}</div>
        </div>
      </el-card>
    </el-col>
    <el-col :span="12">
      <el-card>
        <template #header>
          <div style="display:flex;justify-content:space-between;align-items:center">
            <span>请假申请</span>
            <el-button type="primary" @click="dialogVisible = true">新增请假</el-button>
          </div>
        </template>
        <el-table :data="leaveList" size="small">
          <el-table-column prop="employee_id" label="员工ID" width="80" />
          <el-table-column prop="leave_type" label="类型" width="90">
            <template #default="{ row }">
              <el-tag size="small">{{ typeMap[row.leave_type] || row.leave_type }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="start_date" label="开始" width="100" />
          <el-table-column prop="end_date" label="结束" width="100" />
          <el-table-column prop="days" label="天数" width="70" />
          <el-table-column prop="status" label="状态" width="80">
            <template #default="{ row }">
              <el-tag size="small" :type="row.status === 'approved' ? 'success' : row.status === 'rejected' ? 'danger' : 'warning'">
                {{ row.status === 'approved' ? '已批准' : row.status === 'rejected' ? '已拒绝' : '待审批' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="140">
            <template #default="{ row }">
              <el-button v-if="row.status === 'pending'" size="small" type="success" @click="approve(row, 'approve')">批</el-button>
              <el-button v-if="row.status === 'pending'" size="small" type="danger" @click="approve(row, 'reject')">拒</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </el-col>
  </el-row>

  <el-dialog v-model="dialogVisible" title="新增请假" width="450px">
    <el-form :model="form" label-width="80px">
      <el-form-item label="员工ID"><el-input v-model="form.employee_id" /></el-form-item>
      <el-form-item label="类型">
        <el-select v-model="form.leave_type">
          <el-option label="年假" value="annual" />
          <el-option label="事假" value="personal" />
          <el-option label="病假" value="sick" />
          <el-option label="婚假" value="marriage" />
        </el-select>
      </el-form-item>
      <el-form-item label="开始日期"><el-date-picker v-model="form.start_date" type="date" /></el-form-item>
      <el-form-item label="结束日期"><el-date-picker v-model="form.end_date" type="date" /></el-form-item>
      <el-form-item label="天数"><el-input v-model="form.days" /></el-form-item>
      <el-form-item label="事由"><el-input v-model="form.reason" type="textarea" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" @click="submitLeave">提交</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { getLeaveList, addLeave, approveLeave, clockIn } from '../../api'
import { ElMessage } from 'element-plus'

const leaveList = ref([])
const dialogVisible = ref(false)
const form = reactive({ employee_id: 1, leave_type: 'annual', start_date: '', end_date: '', days: 1, reason: '' })
const typeMap = { annual: '年假', personal: '事假', sick: '病假', marriage: '婚假' }

const today = new Date().toLocaleDateString()
const time = new Date().toLocaleTimeString()

async function loadData() {
  const res = await getLeaveList()
  leaveList.value = res.data || []
}

async function handleClockIn() {
  await clockIn({ employee_id: 1 })
  ElMessage.success('打卡成功')
}

async function submitLeave() {
  await addLeave(form)
  ElMessage.success('请假已提交')
  dialogVisible.value = false
  loadData()
}

async function approve(row, action) {
  await approveLeave(row.id, action)
  ElMessage.success('审批完成')
  loadData()
}

onMounted(loadData)
</script>
