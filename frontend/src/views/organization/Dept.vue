<template>
  <el-card>
    <template #header>
      <div style="display:flex;justify-content:space-between;align-items:center">
        <span>组织架构</span>
        <el-button type="primary" @click="dialogVisible = true">新增部门</el-button>
      </div>
    </template>
    <el-tree :data="tree" :props="{ label: 'label' }" default-expand-all />

    <el-dialog v-model="dialogVisible" title="新增部门" width="450px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="部门名称"><el-input v-model="form.dept_name" /></el-form-item>
        <el-form-item label="部门编码"><el-input v-model="form.dept_code" /></el-form-item>
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
import { getDeptTree, addDept } from '../../api'
import { ElMessage } from 'element-plus'

const tree = ref([])
const dialogVisible = ref(false)
const form = ref({ dept_name: '', dept_code: '' })

async function loadData() {
  const res = await getDeptTree()
  tree.value = res.data || []
}

async function save() {
  await addDept(form.value)
  ElMessage.success('部门创建成功')
  dialogVisible.value = false
  loadData()
}

onMounted(loadData)
</script>
