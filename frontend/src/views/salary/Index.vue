<template>
  <el-card>
    <template #header>
      <div style="display:flex;justify-content:space-between;align-items:center">
        <span>工资核算</span>
        <div>
          <el-input v-model="month" placeholder="2026-10" style="width:120px;margin-right:8px" />
          <el-button type="primary" @click="handleCalculate">一键核算</el-button>
        </div>
      </div>
    </template>

    <el-alert type="info" :closable="false" style="margin-bottom:16px">
      点击"一键核算"自动计算当月所有在职员工工资（基本工资-社保-公积金-个税）。管理员可见明细，其他角色仅看到总额。
    </el-alert>

    <el-table :data="list" border stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="employee_id" label="员工ID" width="90" />
      <el-table-column prop="month" label="月份" width="100" />
      <el-table-column prop="base" label="基本工资" />
      <el-table-column prop="performance" label="绩效" />
      <el-table-column prop="allowance" label="补贴" />
      <el-table-column prop="social" label="社保" />
      <el-table-column prop="fund" label="公积金" />
      <el-table-column prop="tax" label="个税" />
      <el-table-column prop="gross" label="应发" />
      <el-table-column prop="net" label="实发" />
      <el-table-column prop="status" label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="row.status === 'paid' ? 'success' : 'info'">
            {{ row.status === 'paid' ? '已发放' : '已核算' }}
          </el-tag>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getSalaryRecords, calculateSalary } from '../../api'
import { ElMessage } from 'element-plus'

const list = ref([])
const month = ref('2026-10')

async function loadData() {
  const res = await getSalaryRecords({ month: month.value })
  list.value = res.data || []
}

async function handleCalculate() {
  const res = await calculateSalary(month.value)
  ElMessage.success(res.message)
  loadData()
}

onMounted(loadData)
</script>
