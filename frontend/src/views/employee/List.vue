<template>
  <el-card>
    <template #header>
      <div style="display:flex;justify-content:space-between;align-items:center">
        <span>员工档案</span>
        <el-button type="primary" @click="dialogVisible = true">新增员工</el-button>
      </div>
    </template>

    <el-input v-model="keyword" placeholder="搜索员工姓名" style="width:250px;margin-bottom:16px" clearable @keyup.enter="loadData" />

    <el-table :data="list" border stripe>
      <el-table-column prop="emp_no" label="工号" width="100" />
      <el-table-column prop="name" label="姓名" width="100" />
      <el-table-column prop="gender" label="性别" width="70">
        <template #default="{ row }">{{ row.gender === 1 ? '男' : '女' }}</template>
      </el-table-column>
      <el-table-column prop="phone" label="手机号" width="130" />
      <el-table-column prop="position" label="岗位" />
      <el-table-column prop="employee_type" label="用工类型" width="100" />
      <el-table-column prop="entry_date" label="入职日期" width="120" />
      <el-table-column prop="status" label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="row.status === 'active' ? 'success' : 'info'">
            {{ row.status === 'active' ? '在职' : row.status === 'probation' ? '试用' : '离职' }}
          </el-tag>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" title="新增员工" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="工号"><el-input v-model="form.emp_no" /></el-form-item>
        <el-form-item label="姓名"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="手机号"><el-input v-model="form.phone" /></el-form-item>
        <el-form-item label="岗位"><el-input v-model="form.position" /></el-form-item>
        <el-form-item label="用工类型">
          <el-select v-model="form.employee_type">
            <el-option label="正式" value="正式" />
            <el-option label="实习" value="实习" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="save">保存</el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getEmpList, addEmp } from '../../api'
import { ElMessage } from 'element-plus'

const list = ref([])
const keyword = ref('')
const dialogVisible = ref(false)
const form = ref({ emp_no: '', name: '', phone: '', position: '', employee_type: '正式' })

async function loadData() {
  const res = await getEmpList({ keyword: keyword.value })
  list.value = res.data || []
}

async function save() {
  await addEmp(form.value)
  ElMessage.success('新增成功')
  dialogVisible.value = false
  loadData()
}

onMounted(loadData)
</script>
