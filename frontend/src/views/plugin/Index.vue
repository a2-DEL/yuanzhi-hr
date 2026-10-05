<template>
  <div>
    <el-alert type="info" :closable="false" style="margin-bottom:16px">
      插件化架构：微内核底座 + 可插拔扩展。官方内置插件开箱即用，社区开发者可按规范开发自定义插件。
    </el-alert>

    <el-row :gutter="16">
      <el-col :span="8" v-for="p in plugins" :key="p.plugin_id">
        <el-card shadow="hover" class="plugin-card">
          <div class="plugin-header">
            <span class="plugin-icon">{{ p.icon }}</span>
            <div class="plugin-info">
              <div class="plugin-name">{{ p.plugin_name }}</div>
              <div class="plugin-version">v{{ p.version }}</div>
            </div>
            <el-tag size="small" :type="p.enabled ? 'success' : 'info'">
              {{ p.enabled ? '已启用' : '已禁用' }}
            </el-tag>
          </div>
          <p class="plugin-desc">{{ p.description }}</p>
          <div class="plugin-actions">
            <el-button v-if="!p.enabled" size="small" type="primary" @click="toggle(p, true)">启用</el-button>
            <el-button v-else" size="small" @click="toggle(p, false)">禁用</el-button>
            <el-button size="small" text @click="run(p)">试运行</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 社区插件市场 -->
    <h3 style="margin:24px 0 12px">🌐 社区插件市场（即将上线）</h3>
    <el-row :gutter="16">
      <el-col :span="8" v-for="p in communityPlugins" :key="p.name">
        <el-card shadow="hover" class="plugin-card" style="opacity:0.7">
          <div class="plugin-header">
            <span class="plugin-icon">{{ p.icon }}</span>
            <div class="plugin-info">
              <div class="plugin-name">{{ p.name }}</div>
              <div class="plugin-version">{{ p.author }}</div>
            </div>
            <el-tag size="small" type="info">待上线</el-tag>
          </div>
          <p class="plugin-desc">{{ p.desc }}</p>
        </el-card>
      </el-col>
    </el-row>

    <!-- 试运行结果 -->
    <el-card v-if="runResult" style="margin-top:20px">
      <template #header><span>试运行结果</span></template>
      <pre style="white-space:pre-wrap;background:#f5f7fa;padding:16px;border-radius:8px">{{ runResult }}</pre>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getPluginList, enablePlugin, disablePlugin, runPlugin } from '../../api'
import { ElMessage } from 'element-plus'

const plugins = ref([])
const runResult = ref('')
const communityPlugins = ref([
  { icon: '💬', name: '企业微信通知', author: '@开源社区', desc: '审批结果自动推送到企业微信群' },
  { icon: '📊', name: '钉钉考勤同步', author: '@开源社区', desc: '自动同步钉钉打卡数据到源智HR' },
  { icon: '🎓', name: '在线考试系统', author: '@开源社区', desc: '培训后自动出题考试、自动阅卷' },
  { icon: '🏥', name: '体检管理', author: '@开源社区', desc: '员工年度体检预约、报告管理' },
  { icon: '🚌', name: '班车管理', author: '@开源社区', desc: '员工班车路线、座位预约' },
  { icon: '🍱', name: '订餐管理', author: '@开源社区', desc: '工作日午餐订餐、补贴计算' },
])

async function load() {
  const res = await getPluginList()
  plugins.value = res.data || []
}

async function toggle(p, enable) {
  if (enable) {
    await enablePlugin({ plugin_id: p.plugin_id })
    ElMessage.success(`${p.plugin_name} 已启用`)
  } else {
    await disablePlugin({ plugin_id: p.plugin_id })
    ElMessage.success(`${p.plugin_name} 已禁用`)
  }
  load()
}

async function run(p) {
  const action = p.plugin_id === 'notification' ? 'get_notifications' : 'export_employees'
  const res = await runPlugin({ plugin_id: p.plugin_id, action })
  runResult.value = JSON.stringify(res.data, null, 2)
}

onMounted(load)
</script>

<style scoped>
.plugin-card { margin-bottom: 16px; }
.plugin-header { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
.plugin-icon { font-size: 32px; }
.plugin-info { flex: 1; }
.plugin-name { font-weight: bold; }
.plugin-version { font-size: 11px; color: #999; }
.plugin-desc { color: #666; font-size: 13px; min-height: 40px; }
.plugin-actions { display: flex; gap: 8px; margin-top: 12px; }
</style>
