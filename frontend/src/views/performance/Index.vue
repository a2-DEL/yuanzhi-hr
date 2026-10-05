<template>
  <el-tabs v-model="activeTab">
    <!-- 绩效分布 -->
    <el-tab-pane label="绩效分布" name="dist">
      <el-card>
        <h3 style="margin-top:0">等级分布（S/A/B/C/D）</h3>
        <div style="display:flex;gap:20px;align-items:flex-end;height:200px;padding:20px">
          <div v-for="g in ['S','A','B','C','D']" :key="g" style="text-align:center;flex:1">
            <div style="font-size:28px;font-weight:bold;color:{{ gradeColor(g) }}">
              {{ dist.distribution[g] || 0 }}
            </div>
            <div :style="{
              height: Math.max(dist.distribution[g] || 0 * 20, 4) + 'px',
              background: gradeColor(g), borderRadius: '4px 4px 0 0', marginTop: '8px'
            }"></div>
            <div style="margin-top:8px;font-weight:bold">{{ g }}</div>
          </div>
        </div>
        <p style="text-align:center;color:#999">共 {{ dist.total }} 人参与考核</p>
      </el-card>
    </el-tab-pane>

    <!-- KPI指标库 -->
    <el-tab-pane label="KPI指标" name="indicators">
      <el-card>
        <template #header>
          <div style="display:flex;justify-content:space-between;align-items:center">
            <span>考核指标库</span>
            <el-button type="primary" @click="indicatorDialog = true">新增指标</el-button>
          </div>
        </template>
        <el-table :data="indicators" border>
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="name" label="指标名称" />
          <el-table-column prop="department" label="适用部门" width="120" />
          <el-table-column prop="weight" label="权重%" width="90" />
          <el-table-column prop="target" label="考核标准" show-overflow-tooltip />
        </el-table>
      </el-card>
    </el-tab-pane>

    <!-- 考核周期 -->
    <el-tab-pane label="考核周期" name="cycles">
      <el-card>
        <template #header>
          <div style="display:flex;justify-content:space-between;align-items:center">
            <span>考核周期</span>
            <el-button type="primary" @click="cycleDialog = true">创建周期</el-button>
          </div>
        </template>
        <el-table :data="cycles" border>
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="name" label="周期名称" />
          <el-table-column prop="type" label="类型" width="100">
            <template #default="{ row }">
              <el-tag size="small">{{ row.type === 'yearly' ? '年度' : row.type === 'monthly' ? '月度' : '季度' }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="start_date" label="开始" width="120" />
          <el-table-column prop="end_date" label="结束" width="120" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="row.status === 'completed' ? 'success' : row.status === 'ongoing' ? 'warning' : 'info'">
                {{ row.status === 'completed' ? '已完成' : row.status === 'ongoing' ? '进行中' : '草稿' }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </el-tab-pane>

    <!-- 绩效评分 -->
    <el-tab-pane label="绩效评分" name="scores">
      <el-card>
        <template #header>
          <div style="display:flex;justify-content:space-between;align-items:center">
            <span>员工绩效评分</span>
            <el-button type="primary" @click="scoreDialog = true">录入评分</el-button>
          </div>
        </template>
        <el-table :data="scores" border>
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="employee_name" label="姓名" width="110" />
          <el-table-column prop="dept_name" label="部门" />
          <el-table-column prop="self_score" label="自评" width="80" />
          <el-table-column prop="manager_score" label="上级评" width="80" />
          <el-table-column prop="final_score" label="最终分" width="80" />
          <el-table-column prop="grade" label="等级" width="80">
            <template #default="{ row }">
              <el-tag :style="{ background: gradeColor(row.grade), color: '#fff', border: 'none' }">
                {{ row.grade || '-' }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </el-tab-pane>
  </el-tabs>

  <!-- 新增指标弹窗 -->
  <el-dialog v-model="indicatorDialog" title="新增KPI指标" width="450px">
    <el-form :model="indicatorForm" label-width="100px">
      <el-form-item label="指标名称"><el-input v-model="indicatorForm.name" /></el-form-item>
      <el-form-item label="适用部门"><el-input v-model="indicatorForm.department" /></el-form-item>
      <el-form-item label="权重%"><el-input v-model.number="indicatorForm.weight" /></el-form-item>
      <el-form-item label="考核标准"><el-input v-model="indicatorForm.target" type="textarea" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="indicatorDialog = false">取消</el-button>
      <el-button type="primary" @click="saveIndicator">保存</el-button>
    </template>
  </el-dialog>

  <!-- 创建周期弹窗 -->
  <el-dialog v-model="cycleDialog" title="创建考核周期" width="450px">
    <el-form :model="cycleForm" label-width="100px">
      <el-form-item label="周期名称"><el-input v-model="cycleForm.name" placeholder="如 2026年Q3" /></el-form-item>
      <el-form-item label="类型">
        <el-select v-model="cycleForm.type">
          <el-option label="月度" value="monthly" />
          <el-option label="季度" value="quarterly" />
          <el-option label="年度" value="yearly" />
        </el-select>
      </el-form-item>
      <el-form-item label="开始日期"><el-input v-model="cycleForm.start_date" placeholder="2026-07-01" /></el-form-item>
      <el-form-item label="结束日期"><el-input v-model="cycleForm.end_date" placeholder="2026-09-30" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="cycleDialog = false">取消</el-button>
      <el-button type="primary" @click="saveCycle">创建</el-button>
    </template>
  </el-dialog>

  <!-- 录入评分弹窗 -->
  <el-dialog v-model="scoreDialog" title="录入绩效评分" width="450px">
    <el-form :model="scoreForm" label-width="100px">
      <el-form-item label="员工姓名"><el-input v-model="scoreForm.employee_name" /></el-form-item>
      <el-form-item label="部门"><el-input v-model="scoreForm.dept_name" /></el-form-item>
      <el-form-item label="自评分"><el-input v-model.number="scoreForm.self_score" placeholder="0-100" /></el-form-item>
      <el-form-item label="上级评"><el-input v-model.number="scoreForm.manager_score" placeholder="0-100" /></el-form-item>
      <el-form-item label="评语"><el-input v-model="scoreForm.comment" type="textarea" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="scoreDialog = false">取消</el-button>
      <el-button type="primary" @click="saveScore">提交</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getIndicators, addIndicator, getCycles, addCycle, getScores, addScore, getDistribution } from '../../api'
import { ElMessage } from 'element-plus'

const activeTab = ref('dist')
const indicators = ref([])
const cycles = ref([])
const scores = ref([])
const dist = ref({ distribution: { S: 0, A: 0, B: 0, C: 0, D: 0 }, total: 0 })

const indicatorDialog = ref(false)
const indicatorForm = reactive({ name: '', department: '', weight: 0, target: '' })

const cycleDialog = ref(false)
const cycleForm = reactive({ name: '', type: 'quarterly', start_date: '', end_date: '' })

const scoreDialog = ref(false)
const scoreForm = reactive({ cycle_id: 1, employee_name: '', dept_name: '', self_score: null, manager_score: null, comment: '' })

function gradeColor(g) {
  return { S: '#f56c6c', A: '#e6a23c', B: '#409eff', C: '#67c23a', D: '#909399' }[g] || '#909399'
}

async function loadAll() {
  const [i, c, s, d] = await Promise.all([getIndicators(), getCycles(), getScores(), getDistribution()])
  indicators.value = i.data || []
  cycles.value = c.data || []
  scores.value = s.data || []
  dist.value = d.data || dist.value
}

async function saveIndicator() {
  await addIndicator(indicatorForm)
  ElMessage.success('指标已创建')
  indicatorDialog.value = false
  loadAll()
}

async function saveCycle() {
  await addCycle(cycleForm)
  ElMessage.success('考核周期已创建')
  cycleDialog.value = false
  loadAll()
}

async function saveScore() {
  const res = await addScore(scoreForm)
  ElMessage.success(`已提交，等级：${res.data.grade}`)
  scoreDialog.value = false
  loadAll()
}

onMounted(loadAll)
</script>
