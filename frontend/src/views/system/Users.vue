<template>
  <div>
    <el-card>
      <template #header>
        <div style="display:flex;justify-content:space-between;align-items:center">
          <span>用户管理</span>
          <el-button type="primary" @click="dialog = true">+ 新增用户</el-button>
        </div>
      </template>
      <el-table :data="list" border stripe>
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="username" label="账号" />
        <el-table-column prop="real_name" label="姓名" />
        <el-table-column prop="position" label="岗位" />
        <el-table-column prop="roles" label="角色">
          <template #default="{ row }">
            <el-tag v-for="r in row.roles" :key="r" size="small" style="margin-right:4px" type="primary">{{ r }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'danger'">{{ row.status === 1 ? '启用' : '禁用' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button size="small" @click="editRow(row)">分配角色</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新增用户弹窗 -->
    <el-dialog v-model="dialog" title="新增用户" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="账号">
          <el-input v-model="form.username" placeholder="登录账号" />
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="form.real_name" placeholder="真实姓名" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" placeholder="初始密码" />
        </el-form-item>
        <el-form-item label="岗位">
          <el-input v-model="form.position" placeholder="岗位名称" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialog = false">取消</el-button>
        <el-button type="primary" @click="createUser">创建</el-button>
      </template>
    </el-dialog>

    <!-- 分配角色弹窗 -->
    <el-dialog v-model="roleDialog" title="分配角色" width="450px">
      <p>为用户 <b>{{ currentUser?.username }}</b> 分配角色：</p>
      <el-checkbox-group v-model="selectedRoles">
        <el-checkbox v-for="r in allRoles" :key="r.role_code" :value="r.role_code" style="display:block;margin-bottom:8px">
          {{ r.role_name }}（{{ r.role_code }}）
        </el-checkbox>
      </el-checkbox-group>
      <template #footer>
        <el-button @click="roleDialog = false">取消</el-button>
        <el-button type="primary" @click="saveRoles">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import request from '../../api/request'
import { ElMessage } from 'element-plus'

const list = ref([])
const allRoles = ref([])
const dialog = ref(false)
const roleDialog = ref(false)
const currentUser = ref(null)
const selectedRoles = ref([])
const form = ref({ username: '', real_name: '', password: '', position: '' })

async function load() {
  const [userRes, roleRes] = await Promise.all([
    request.get('/api/system/users'),
    request.get('/api/system/roles'),
  ])
  list.value = userRes.data || []
  allRoles.value = roleRes.data || []
}

async function createUser() {
  await request.post('/api/system/users', form.value)
  ElMessage.success('用户创建成功')
  dialog.value = false
  form.value = { username: '', real_name: '', password: '', position: '' }
  load()
}

function editRow(row) {
  currentUser.value = row
  selectedRoles.value = [...(row.roles || [])]
  roleDialog.value = true
}

async function saveRoles() {
  ElMessage.success('角色已保存（示例）')
  roleDialog.value = false
}

onMounted(load)
</script>
