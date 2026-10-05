<template>
  <el-tabs v-model="activeTab">
    <!-- 编制管理 -->
    <el-tab-pane label="编制管理" name="headcount">
      <el-card>
        <template #header>
          <div style="display:flex;justify-content:space-between;align-items:center">
            <span>各部门编制与实际人数</span>
            <el-button type="primary" @click="budgetDialog = true">设置编制</el-button>
          </div>
        </template>
        <el-table :data="headcountList" border>
          <el-table-column prop="dept_name" label="部门" />
          <el-table-column prop="budget" label="编制人数" width="120" />
          <el-table-column prop="actual" label="实际人数" width="120" />
          <el-table-column prop="difference" label="余缺" width="100">
            <template #default="{ row }">
              <el-tag :type="row.over_budget ? 'danger' : row.difference > 0 ? 'warning' : 'success'">
                {{ row.difference > 0 ? `余${row.difference}` : row.difference < 0 ? `缺${-row.difference}` : '满编' }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </el-tab-pane>

    <!-- 岗位说明书 -->
    <el-tab-pane label="岗位说明书" name="jobs">
      <el-card>
        <template #header>
          <div style="display:flex;justify-content:space-between;align-items:center">
            <span>岗位说明书库</span>
            <el-button type="primary" @click="jobDialog = true">新增岗位</el-button>
          </div>
        </template>
        <el-table :data="jobs" border>
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="title" label="岗位名称" width="180" />
          <el-table-column prop="salary_range" label="薪资范围" width="150" />
          <el-table-column prop="responsibilities" label="岗位职责" show-overflow-tooltip />
          <el-table-column prop="requirements" label="任职要求" show-overflow-tooltip />
        </el-table>
      </el-card>
    </el-tab-pane>

    <!-- 制度文档 -->
    <el-tab-pane label="制度文档库" name="policies">
      <el-card>
        <template #header>
          <div style="display:flex;justify-content:space-between;align-items:center">
            <span>HR制度文档</span>
            <el-button type="primary" @click="policyDialog = true">新增制度</el-button>
          </div>
        </template>
        <el-table :data="policies" border>
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="title" label="制度名称" width="200" />
          <el-table-column prop="category" label="类别" width="120">
            <template #default="{ row }">
              <el-tag size="small">{{ row.category }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="version" label="版本" width="100" />
          <el-table-column prop="create_time" label="更新时间" width="120" />
        </el-table>
      </el-card>
    </el-tab-pane>
  </el-tabs>

  <!-- 设置编制弹窗 -->
  <el-dialog v-model="budgetDialog" title="设置部门编制" width="450px">
    <el-form :model="budgetForm" label-width="100px">
      <el-form-item label="部门">
        <el-select v-model="budgetForm.dept_id" style="width:100%">
          <el-option v-for="d in depts" :key="d.id" :label="d.dept_name" :value="d.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="编制人数"><el-input v-model.number="budgetForm.budget_count" /></el-form-item>
      <el-form-item label="成本预算(万)"><el-input v-model.number="budgetForm.budget_cost" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="budgetDialog = false">取消</el-button>
      <el-button type="primary" @click="saveBudget">保存</el-button>
    </template>
  </el-dialog>

  <!-- 新增岗位弹窗 -->
  <el-dialog v-model="jobDialog" title="新增岗位说明书" width="500px">
    <el-form :model="jobForm" label-width="100px">
      <el-form-item label="岗位名称"><el-input v-model="jobForm.title" /></el-form-item>
      <el-form-item label="薪资范围"><el-input v-model="jobForm.salary_range" placeholder="如 15k-25k" /></el-form-item>
      <el-form-item label="岗位职责"><el-input v-model="jobForm.responsibilities" type="textarea" /></el-form-item>
      <el-form-item label="任职要求"><el-input v-model="jobForm.requirements" type="textarea" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="jobDialog = false">取消</el-button>
      <el-button type="primary" @click="saveJob">保存</el-button>
    </template>
  </el-dialog>

  <!-- 新增制度弹窗 -->
  <el-dialog v-model="policyDialog" title="新增制度文档" width="500px">
    <el-form :model="policyForm" label-width="100px">
      <el-form-item label="制度名称"><el-input v-model="policyForm.title" /></el-form-item>
      <el-form-item label="类别">
        <el-select v-model="policyForm.category">
          <el-option label="考勤" value="考勤" />
          <el-option label="奖惩" value="奖惩" />
          <el-option label="晋升" value="晋升" />
          <el-option label="薪酬" value="薪酬" />
          <el-option label="福利" value="福利" />
        </el-select>
      </el-form-item>
      <el-form-item label="内容"><el-input v-model="policyForm.content" type="textarea" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="policyDialog = false">取消</el-button>
      <el-button type="primary" @click="savePolicy">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getHeadcount, setHeadcount, getJobs, addJob, getPolicies, addPolicy, getDeptTree } from '../../api'
import { ElMessage } from 'element-plus'

const activeTab = ref('headcount')
const headcountList = ref([])
const jobs = ref([])
const policies = ref([])
const depts = ref([])

const budgetDialog = ref(false)
const budgetForm = reactive({ dept_id: null, budget_count: 0, budget_cost: 0 })

const jobDialog = ref(false)
const jobForm = reactive({ title: '', salary_range: '', responsibilities: '', requirements: '' })

const policyDialog = ref(false)
const policyForm = reactive({ title: '', category: '考勤', content: '' })

async function loadAll() {
  const [h, j, p, d] = await Promise.all([getHeadcount(), getJobs(), getPolicies(), getDeptTree()])
  headcountList.value = h.data || []
  jobs.value = j.data || []
  policies.value = p.data || []
  depts.value = flattenDepts(d.data || [])
}

function flattenDepts(list) {
  let result = []
  list.forEach(d => {
    result.push({ id: d.id, dept_name: d.label })
    if (d.children) result = result.concat(flattenDepts(d.children))
  })
  return result
}

async function saveBudget() {
  await setHeadcount(budgetForm)
  ElMessage.success('编制已保存')
  budgetDialog.value = false
  loadAll()
}

async function saveJob() {
  await addJob(jobForm)
  ElMessage.success('岗位已创建')
  jobDialog.value = false
  loadAll()
}

async function savePolicy() {
  await addPolicy(policyForm)
  ElMessage.success('制度已保存')
  policyDialog.value = false
  loadAll()
}

onMounted(loadAll)
</script>
