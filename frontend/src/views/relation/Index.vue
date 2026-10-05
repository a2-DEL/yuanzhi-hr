<template>
  <el-tabs v-model="activeTab">
    <!-- 劳动合同 -->
    <el-tab-pane label="劳动合同" name="contracts">
      <el-card>
        <template #header>
          <div style="display:flex;justify-content:space-between;align-items:center">
            <span>合同管理 <el-tag v-if="expiringCount" type="danger" size="small" style="margin-left:8px">{{ expiringCount }}份即将到期</el-tag></span>
            <el-button type="primary" @click="contractDialog = true">登记合同</el-button>
          </div>
        </template>
        <el-table :data="contracts" border>
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="employee_name" label="员工" width="110" />
          <el-table-column prop="contract_type" label="类型" width="110" />
          <el-table-column prop="start_date" label="开始" width="110" />
          <el-table-column prop="end_date" label="到期" width="120" />
          <el-table-column prop="days_left" label="剩余天数" width="100">
            <template #default="{ row }">
              <el-tag v-if="row.expiring_soon" type="danger" size="small">{{ row.days_left }}天</el-tag>
              <span v-else-if="row.days_left !== null">{{ row.days_left }}天</span>
              <span v-else>-</span>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </el-tab-pane>

    <!-- 入转调离 -->
    <el-tab-pane label="入转调离" name="transfers">
      <el-card>
        <template #header>
          <div style="display:flex;justify-content:space-between;align-items:center">
            <span>异动记录</span>
            <el-button type="primary" @click="transferDialog = true">登记异动</el-button>
          </div>
        </template>
        <el-table :data="transfers" border>
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="employee_name" label="员工" width="100" />
          <el-table-column prop="change_type" label="类型" width="90">
            <template #default="{ row }">
              <el-tag size="small" :type="typeColor(row.change_type)">{{ row.change_type }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="from_dept" label="原部门" />
          <el-table-column prop="to_dept" label="新部门" />
          <el-table-column prop="effective_date" label="生效日期" width="110" />
          <el-table-column prop="reason" label="原因" show-overflow-tooltip />
        </el-table>
      </el-card>
    </el-tab-pane>

    <!-- 奖惩记录 -->
    <el-tab-pane label="奖惩记录" name="disciplines">
      <el-card>
        <template #header>
          <div style="display:flex;justify-content:space-between;align-items:center">
            <span>奖惩记录</span>
            <el-button type="primary" @click="disciplineDialog = true">登记奖惩</el-button>
          </div>
        </template>
        <el-table :data="disciplines" border>
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="employee_name" label="员工" width="110" />
          <el-table-column prop="type" label="类型" width="100">
            <template #default="{ row }">
              <el-tag size="small" :type="row.type === '奖励' ? 'success' : 'danger'">{{ row.type }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="title" label="事项" />
          <el-table-column prop="occur_date" label="日期" width="110" />
        </el-table>
      </el-card>
    </el-tab-pane>

    <!-- 离职管理 -->
    <el-tab-pane label="离职管理" name="offboardings">
      <el-card>
        <template #header>
          <div style="display:flex;justify-content:space-between;align-items:center">
            <span>离职记录（共{{ attrition.total }}人）</span>
            <el-button type="primary" @click="offboardDialog = true">登记离职</el-button>
          </div>
        </template>
        <el-descriptions :column="4" border style="margin-bottom:16px">
          <el-descriptions-item label="薪资原因">{{ attrition.by_reason?.['薪资'] || 0 }}</el-descriptions-item>
          <el-descriptions-item label="发展原因">{{ attrition.by_reason?.['发展'] || 0 }}</el-descriptions-item>
          <el-descriptions-item label="家庭原因">{{ attrition.by_reason?.['家庭'] || 0 }}</el-descriptions-item>
          <el-descriptions-item label="其他">{{ attrition.by_reason?.['其他'] || 0 }}</el-descriptions-item>
        </el-descriptions>
        <el-table :data="offboardings" border>
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="employee_name" label="员工" width="110" />
          <el-table-column prop="dept_name" label="部门" />
          <el-table-column prop="last_day" label="最后工作日" width="120" />
          <el-table-column prop="reason_category" label="原因分类" width="110" />
          <el-table-column prop="reason_detail" label="面谈记录" show-overflow-tooltip />
        </el-table>
      </el-card>
    </el-tab-pane>
  </el-tabs>

  <!-- 登记合同弹窗 -->
  <el-dialog v-model="contractDialog" title="登记劳动合同" width="450px">
    <el-form :model="contractForm" label-width="100px">
      <el-form-item label="员工姓名"><el-input v-model="contractForm.employee_name" /></el-form-item>
      <el-form-item label="合同类型">
        <el-select v-model="contractForm.contract_type">
          <el-option label="固定期限" value="固定期限" />
          <el-option label="无固定期限" value="无固定期限" />
          <el-option label="实习协议" value="实习协议" />
        </el-select>
      </el-form-item>
      <el-form-item label="开始日期"><el-input v-model="contractForm.start_date" placeholder="2026-10-01" /></el-form-item>
      <el-form-item label="到期日期"><el-input v-model="contractForm.end_date" placeholder="2029-09-30（无固定期限留空）" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="contractDialog = false">取消</el-button>
      <el-button type="primary" @click="saveContract">保存</el-button>
    </template>
  </el-dialog>

  <!-- 登记异动弹窗 -->
  <el-dialog v-model="transferDialog" title="登记异动" width="450px">
    <el-form :model="transferForm" label-width="100px">
      <el-form-item label="员工姓名"><el-input v-model="transferForm.employee_name" /></el-form-item>
      <el-form-item label="异动类型">
        <el-select v-model="transferForm.change_type">
          <el-option label="入职" value="入职" />
          <el-option label="转正" value="转正" />
          <el-option label="调岗" value="调岗" />
          <el-option label="晋升" value="晋升" />
          <el-option label="离职" value="离职" />
        </el-select>
      </el-form-item>
      <el-form-item label="新部门"><el-input v-model="transferForm.to_dept" /></el-form-item>
      <el-form-item label="新职位"><el-input v-model="transferForm.to_position" /></el-form-item>
      <el-form-item label="生效日期"><el-input v-model="transferForm.effective_date" placeholder="2026-10-15" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="transferDialog = false">取消</el-button>
      <el-button type="primary" @click="saveTransfer">保存</el-button>
    </template>
  </el-dialog>

  <!-- 登记奖惩弹窗 -->
  <el-dialog v-model="disciplineDialog" title="登记奖惩" width="450px">
    <el-form :model="disciplineForm" label-width="100px">
      <el-form-item label="员工姓名"><el-input v-model="disciplineForm.employee_name" /></el-form-item>
      <el-form-item label="类型">
        <el-select v-model="disciplineForm.type">
          <el-option label="奖励" value="奖励" />
          <el-option label="警告" value="警告" />
          <el-option label="记过" value="记过" />
          <el-option label="开除" value="开除" />
        </el-select>
      </el-form-item>
      <el-form-item label="事项"><el-input v-model="disciplineForm.title" /></el-form-item>
      <el-form-item label="说明"><el-input v-model="disciplineForm.description" type="textarea" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="disciplineDialog = false">取消</el-button>
      <el-button type="primary" @click="saveDiscipline">保存</el-button>
    </template>
  </el-dialog>

  <!-- 登记离职弹窗 -->
  <el-dialog v-model="offboardDialog" title="登记离职" width="450px">
    <el-form :model="offboardForm" label-width="100px">
      <el-form-item label="员工姓名"><el-input v-model="offboardForm.employee_name" /></el-form-item>
      <el-form-item label="部门"><el-input v-model="offboardForm.dept_name" /></el-form-item>
      <el-form-item label="最后工作日"><el-input v-model="offboardForm.last_day" placeholder="2026-10-31" /></el-form-item>
      <el-form-item label="原因分类">
        <el-select v-model="offboardForm.reason_category">
          <el-option label="薪资" value="薪资" />
          <el-option label="发展" value="发展" />
          <el-option label="家庭" value="家庭" />
          <el-option label="不适应" value="不适应" />
          <el-option label="其他" value="其他" />
        </el-select>
      </el-form-item>
      <el-form-item label="面谈记录"><el-input v-model="offboardForm.reason_detail" type="textarea" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="offboardDialog = false">取消</el-button>
      <el-button type="primary" @click="saveOffboard">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { getContracts, addContract, getTransfers, addTransfer, getDisciplines, addDiscipline, getOffboardings, addOffboarding, getAttritionStats } from '../../api'
import { ElMessage } from 'element-plus'

const activeTab = ref('contracts')
const contracts = ref([])
const transfers = ref([])
const disciplines = ref([])
const offboardings = ref([])
const attrition = ref({ total: 0, by_reason: {} })

const expiringCount = computed(() => contracts.value.filter(c => c.expiring_soon).length)

const contractDialog = ref(false)
const contractForm = reactive({ employee_name: '', contract_type: '固定期限', start_date: '', end_date: '' })

const transferDialog = ref(false)
const transferForm = reactive({ employee_name: '', change_type: '入职', to_dept: '', to_position: '', effective_date: '' })

const disciplineDialog = ref(false)
const disciplineForm = reactive({ employee_name: '', type: '奖励', title: '', description: '' })

const offboardDialog = ref(false)
const offboardForm = reactive({ employee_name: '', dept_name: '', last_day: '', reason_category: '其他', reason_detail: '' })

function typeColor(t) {
  return { '入职': 'success', '转正': 'primary', '调岗': 'warning', '晋升': 'success', '离职': 'danger' }[t] || 'info'
}

async function loadAll() {
  const [c, t, d, o, a] = await Promise.all([
    getContracts(), getTransfers(), getDisciplines(), getOffboardings(), getAttritionStats()
  ])
  contracts.value = c.data || []
  transfers.value = t.data || []
  disciplines.value = d.data || []
  offboardings.value = o.data || []
  attrition.value = a.data || attrition.value
}

async function saveContract() {
  await addContract(contractForm)
  ElMessage.success('合同已登记')
  contractDialog.value = false
  loadAll()
}

async function saveTransfer() {
  await addTransfer(transferForm)
  ElMessage.success('异动已记录')
  transferDialog.value = false
  loadAll()
}

async function saveDiscipline() {
  await addDiscipline(disciplineForm)
  ElMessage.success('奖惩已登记')
  disciplineDialog.value = false
  loadAll()
}

async function saveOffboard() {
  await addOffboarding(offboardForm)
  ElMessage.success('离职已登记')
  offboardDialog.value = false
  loadAll()
}

onMounted(loadAll)
</script>
