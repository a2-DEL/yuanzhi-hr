<template>
  <div>
    <!-- 欢迎卡片 -->
    <el-row :gutter="20" class="welcome-row">
      <el-col :span="24">
        <el-card>
          <h2 style="margin:0">欢迎使用源智HR</h2>
          <p style="color:#888;margin:8px 0 0">基于多Agent的开源智能人力运营系统 · 让HR工作更智能</p>
        </el-card>
      </el-col>
    </el-row>

    <!-- 核心指标卡片 -->
    <el-row :gutter="20" style="margin-top:20px">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background:#409eff"><el-icon><User /></el-icon></div>
            <div>
              <div class="stat-value">{{ empCount }}</div>
              <div class="stat-label">在职员工</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background:#67c23a"><el-icon><OfficeBuilding /></el-icon></div>
            <div>
              <div class="stat-value">{{ deptCount }}</div>
              <div class="stat-label">部门数量</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background:#e6a23c"><el-icon><MagicStick /></el-icon></div>
            <div>
              <div class="stat-value">{{ aiStats.total_calls || 0 }}</div>
              <div class="stat-label">AI调用次数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background:#f56c6c"><el-icon><Connection /></el-icon></div>
            <div>
              <div class="stat-value">{{ aiStats.total_cost || 0 }} ¥</div>
              <div class="stat-label">AI预估费用</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 快速入口 -->
    <el-row :gutter="20" style="margin-top:20px">
      <el-col :span="12">
        <el-card>
          <template #header><span>快速入口</span></template>
          <div class="quick-grid">
            <div class="quick-item" @click="$router.push('/employee')">
              <el-icon size="28"><User /></el-icon>
              <span>员工档案</span>
            </div>
            <div class="quick-item" @click="$router.push('/organization')">
              <el-icon size="28"><OfficeBuilding /></el-icon>
              <span>组织架构</span>
            </div>
            <div class="quick-item" @click="$router.push('/ai/assistant')">
              <el-icon size="28"><MagicStick /></el-icon>
              <span>AI助手</span>
            </div>
            <div class="quick-item" @click="$router.push('/ai/config')">
              <el-icon size="28"><Setting /></el-icon>
              <span>模型配置</span>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header><span>系统信息</span></template>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="系统名称">源智HR智能人力运营系统</el-descriptions-item>
            <el-descriptions-item label="版本号">v0.1.0 (MVP)</el-descriptions-item>
            <el-descriptions-item label="部署模式">私有化部署 · 数据本地存储</el-descriptions-item>
            <el-descriptions-item label="AI能力">多Agent团队 · 自托管API Key</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getEmpList, getDeptTree, getAiStats } from '../../api'

const empCount = ref(0)
const deptCount = ref(0)
const aiStats = ref({})

onMounted(async () => {
  try {
    const [empRes, deptRes, aiRes] = await Promise.all([
      getEmpList(), getDeptTree(), getAiStats()
    ])
    empCount.value = (empRes.data || []).length
    const countDepts = (list) => {
      let n = list.length
      list.forEach(d => { n += countDepts(d.children || []) })
      return n
    }
    deptCount.value = countDepts(deptRes.data || [])
    aiStats.value = aiRes.data || {}
  } catch (e) {}
})
</script>

<style scoped>
.stat-card { display: flex; align-items: center; gap: 16px; }
.stat-icon {
  width: 50px; height: 50px; border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 24px;
}
.stat-value { font-size: 24px; font-weight: bold; color: #333; }
.stat-label { color: #999; font-size: 13px; }
.quick-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
.quick-item {
  display: flex; flex-direction: column; align-items: center; gap: 8px;
  padding: 20px; background: #f5f7fa; border-radius: 8px; cursor: pointer;
  transition: all 0.3s;
}
.quick-item:hover { background: #ecf5ff; color: #409eff; }
</style>
