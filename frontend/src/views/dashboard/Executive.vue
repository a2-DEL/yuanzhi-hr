<template>
  <div class="dashboard-page">
    <h2 style="text-align:center;margin:0 0 20px;color:#fff;font-size:22px">📊 源智HR · 人力经营大屏</h2>

    <!-- KPI卡片行 -->
    <el-row :gutter="16" style="margin-bottom:16px">
      <el-col :span="4" v-for="kpi in kpiCards" :key="kpi.label">
        <div class="kpi-card">
          <div class="kpi-icon">{{ kpi.icon }}</div>
          <div class="kpi-value">{{ kpi.value }}</div>
          <div class="kpi-label">{{ kpi.label }}</div>
        </div>
      </el-col>
    </el-row>

    <!-- 图表第一行 -->
    <el-row :gutter="16">
      <el-col :span="8">
        <el-card class="chart-card">
          <template #header><span class="chart-title">🏢 部门人数分布（点击下钻）</span></template>
          <div v-for="d in data.dept_distribution" :key="d.name" class="bar-row" style="cursor:pointer" @click="drillDept(d)">
            <span class="bar-label">{{ d.name }}</span>
            <div class="bar-track">
              <div class="bar-fill" :style="{ width: barWidth(d.value) + '%' }"></div>
            </div>
            <span class="bar-value">{{ d.value }}人</span>
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card class="chart-card">
          <template #header><span class="chart-title">📈 绩效等级分布</span></template>
          <div style="display:flex;justify-content:space-around;align-items:flex-end;height:200px;padding-top:20px">
            <div v-for="g in ['S','A','B','C','D']" :key="g" style="text-align:center">
              <div style="font-size:26px;font-weight:bold;color:{{ gradeColor(g) }}">{{ data.performance[g] || 0 }}</div>
              <div :style="{ height: Math.max((data.performance[g]||0)*30, 6)+'px', background: gradeColor(g), borderRadius:'4px 4px 0 0', marginTop:'8px' }"></div>
              <div style="margin-top:6px;font-weight:bold;color:#ccc">{{ g }}</div>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card class="chart-card">
          <template #header><span class="chart-title">🎯 招聘漏斗</span></template>
          <div class="funnel-v">
            <div class="f-step" :style="{width: funnelWidth(data.recruitment.resume_total)}">
              <b>简历总数</b> {{ data.recruitment.resume_total }}
            </div>
            <div class="f-step bg-c" :style="{width: funnelWidth(data.recruitment.in_interview)}">
              <b>面试中</b> {{ data.recruitment.in_interview }}
            </div>
            <div class="f-step bg-g" :style="{width: funnelWidth(data.recruitment.hired)}">
              <b>已入职</b> {{ data.recruitment.hired }}
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表第二行 -->
    <el-row :gutter="16" style="margin-top:16px">
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header><span class="chart-title">💰 人力成本概览</span></template>
          <el-descriptions :column="3" border>
            <el-descriptions-item label="月人力成本">
              <span style="color:#38bdf8;font-size:20px;font-weight:bold">¥{{ data.cost.monthly_total.toLocaleString() }}</span>
            </el-descriptions-item>
            <el-descriptions-item label="人均成本/月">
              <span style="color:#34d399;font-size:20px;font-weight:bold">¥{{ data.cost.per_capita.toLocaleString() }}</span>
            </el-descriptions-item>
            <el-descriptions-item label="员工总数">
              <span style="color:#fbbf24;font-size:20px;font-weight:bold">{{ data.headcount.total }}人</span>
            </el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card class="chart-card">
          <template #header><span class="chart-title">⚠️ 待办预警</span></template>
          <div style="display:flex;gap:12px;flex-wrap:wrap">
            <el-tag v-if="data.compliance.expiring_contracts > 0" type="danger" size="large" effect="dark">
              📄 {{ data.compliance.expiring_contracts }}份合同即将到期
            </el-tag>
            <el-tag v-if="data.attendance.leave_pending > 0" type="warning" size="large" effect="dark">
              📋 {{ data.attendance.leave_pending }}条请假待审批
            </el-tag>
            <el-tag v-if="data.recruitment.in_interview > 0" type="primary" size="large" effect="dark">
              🎯 {{ data.recruitment.in_interview }}人面试中
            </el-tag>
            <el-tag v-if="data.training.completed > 0" type="success" size="large" effect="dark">
              ✅ 培训完成 {{ data.training.completed }}人次
            </el-tag>
            <span v-if="!hasWarning" style="color:#666">一切正常，暂无待办</span>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 部门下钻抽屉 -->
    <el-drawer v-model="drillVisible" :title="`${drillDeptName} · 人员明细`" size="500px" direction="rtl">
      <el-table :data="drillEmployees" border size="small">
        <el-table-column prop="name" label="姓名" />
        <el-table-column prop="position" label="职位" />
        <el-table-column prop="entry_date" label="入职日期" />
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag size="small" :type="row.status === 'active' ? 'success' : 'info'">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-drawer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getExecutiveDashboard, getEmpList } from '../../api'

const data = ref({
  headcount: { total: 0, dept_count: 0, hired_this_month: 0, offboard_total: 0 },
  recruitment: { resume_total: 0, in_interview: 0, hired: 0 },
  attendance: { absent: 0, leave_pending: 0 },
  cost: { monthly_total: 0, per_capita: 0 },
  performance: { S: 0, A: 0, B: 0, C: 0, D: 0 },
  training: { completed: 0 },
  compliance: { expiring_contracts: 0 },
  dept_distribution: [],
})

// 下钻
const drillVisible = ref(false)
const drillDeptName = ref('')
const drillEmployees = ref([])

async function drillDept(d) {
  drillDeptName.value = d.name
  drillVisible.value = true
  // 拉取该部门员工
  const res = await getEmpList({ dept_id: d.dept_id })
  drillEmployees.value = res.data || []
}

const kpiCards = computed(() => [
  { icon: '👥', label: '员工总数', value: data.value.headcount.total + '人' },
  { icon: '🏢', label: '部门数', value: data.value.headcount.dept_count + '个' },
  { icon: '💰', label: '月人力成本', value: '¥' + data.value.cost.monthly_total.toLocaleString() },
  { icon: '📈', label: '人均成本', value: '¥' + data.value.cost.per_capita.toLocaleString() },
  { icon: '🎯', label: '简历总数', value: data.value.recruitment.resume_total },
  { icon: '✅', label: '培训完成', value: data.value.training.completed + '人次' },
])

const hasWarning = computed(() =>
  data.value.compliance.expiring_contracts > 0 ||
  data.value.attendance.leave_pending > 0 ||
  data.value.recruitment.in_interview > 0
)

function gradeColor(g) {
  return { S: '#f56c6c', A: '#e6a23c', B: '#409eff', C: '#67c23a', D: '#909399' }[g] || '#909399'
}

function barWidth(v) {
  const max = Math.max(...data.value.dept_distribution.map(d => d.value), 1)
  return (v / max) * 100
}

function funnelWidth(v) {
  const max = Math.max(data.value.recruitment.resume_total, 1)
  return Math.max((v / max) * 100, 15) + '%'
}

onMounted(async () => {
  const res = await getExecutiveDashboard()
  data.value = res.data
})
</script>

<style scoped>
.dashboard-page { background: #0f172a; min-height: 100%; padding: 20px; border-radius: 8px; }
.kpi-card { background: linear-gradient(135deg, #1e293b, #334155); border-radius: 12px; padding: 20px; text-align: center; }
.kpi-icon { font-size: 28px; }
.kpi-value { font-size: 22px; font-weight: bold; color: #38bdf8; margin: 8px 0; }
.kpi-label { font-size: 13px; color: #94a3b8; }
.chart-card { background: #1e293b !important; border: 1px solid #334155; color: #e2e8f0; }
.chart-card :deep(.el-card__header) { color: #e2e8f0; border-bottom: 1px solid #334155; }
.chart-card :deep(.el-descriptions__label) { color: #94a3b8 !important; }
.chart-card :deep(.el-descriptions__content) { color: #e2e8f0 !important; }
.chart-title { font-weight: bold; }
.bar-row { display: flex; align-items: center; margin-bottom: 12px; gap: 8px; }
.bar-label { width: 70px; font-size: 12px; color: #94a3b8; }
.bar-track { flex: 1; height: 18px; background: #334155; border-radius: 4px; overflow: hidden; }
.bar-fill { height: 100%; background: linear-gradient(90deg, #3b82f6, #22d3ee); border-radius: 4px; }
.bar-value { width: 50px; font-size: 12px; color: #38bdf8; }
.funnel-v { display: flex; flex-direction: column; align-items: center; gap: 10px; padding: 10px 0; }
.f-step { background: #3b82f6; color: #fff; padding: 14px; border-radius: 6px; text-align: center; transition: width .3s; font-size: 13px; }
.f-step.bg-c { background: #06b6d4; }
.f-step.bg-g { background: #22c55e; }
</style>
