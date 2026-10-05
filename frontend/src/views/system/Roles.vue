<template>
  <el-card>
    <template #header>角色管理</template>
    <el-table :data="list" border stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="code" label="角色编码" />
      <el-table-column prop="name" label="角色名称" />
      <el-table-column prop="level" label="层级" />
      <el-table-column prop="data_scope" label="数据范围">
        <template #default="{ row }">
          <el-tag size="small">{{ row.data_scope }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.status === 1 ? 'success' : 'danger'">{{ row.status === 1 ? '启用' : '禁用' }}</el-tag>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getRoleList } from '../../api'

const list = ref([])
onMounted(async () => {
  const res = await getRoleList()
  list.value = res.data || []
})
</script>
