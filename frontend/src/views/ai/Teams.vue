<template>
  <div>
    <!-- HR总监调度大厅 -->
    <el-card class="lobby-card">
      <div class="lobby-header">
        <span class="lobby-icon">🎯</span>
        <div>
          <div class="lobby-title">HR总监 · 全局调度大厅</div>
          <div class="lobby-sub">输入需求，HR总监自动拆解任务、跨部门派单、汇总交付</div>
        </div>
      </div>
      <el-input
        v-model="userInput"
        placeholder="例如：下周一研发部张三入职，高级后端工程师，薪资18k"
        size="large"
        @keyup.enter="doDispatch"
      >
        <template #append>
          <el-button type="primary" @click="doDispatch" :loading="dispatching">
            {{ dispatching ? '派单中...' : '派单' }}
          </el-button>
        </template>
      </el-input>

      <!-- 任务识别提示 -->
      <div v-if="dispatchResult" class="task-hint">
        <el-alert type="success" :closable="false" style="margin-bottom:10px">
          <b>已识别任务</b> → 派发至 {{ teamName(dispatchResult.routed_team) }} · {{ dispatchResult.execution?.agent_name }}
          <span style="color:#999;margin-left:12px">{{ dispatchResult.route_reason }}</span>
        </el-alert>
        <div v-if="dispatchResult.execution" class="exec-box">
          <pre>{{ dispatchResult.execution.content }}</pre>
        </div>
      </div>
    </el-card>

    <!-- 6大团队办公区 -->
    <h3 style="margin:24px 0 16px">🏢 各部门办公区（点击进入部门空间）</h3>
    <el-row :gutter="16">
      <el-col :span="8" v-for="(team, key) in teams" :key="key">
        <el-card shadow="hover" class="team-card" :style="{ borderTop: `4px solid ${team.color}` }" @click="enterTeam(key)">
          <div class="team-head">
            <span class="team-icon" :style="{ background: team.color }">{{ team.icon }}</span>
            <div class="team-info">
              <div class="team-name">{{ team.name }}</div>
              <div class="team-lead">主管：{{ team.lead?.name || '待任命' }}</div>
            </div>
          </div>
          <p class="team-desc">{{ team.lead?.desc }}</p>
          <div class="team-stats">
            <el-tag size="small" :style="{ background: team.color, color: '#fff' }">{{ team.agent_count }}人在岗</el-tag>
            <el-tag size="small" type="info">待办 0</el-tag>
            <el-button size="small" type="primary" text>进入部门 →</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 部门独立办公空间弹窗 -->
    <el-dialog v-model="teamDialog" :title="`${currentTeam?.name} · 部门办公空间`" width="800px" top="5vh">
      <!-- 主管对话区 -->
      <div class="dept-lead-box">
        <div class="dept-lead-head">
          <span class="lead-avatar">{{ currentTeam?.lead?.icon }}</span>
          <div>
            <b>{{ currentTeam?.lead?.name }}</b>
            <span style="color:#999;font-size:12px;margin-left:8px">{{ currentTeam?.lead?.title }}</span>
          </div>
        </div>
        <el-input
          v-model="deptInput"
          :placeholder="`向${currentTeam?.lead?.name}提出需求...`"
          @keyup.enter="talkToLead"
        >
          <template #append><el-button @click="talkToLead">发送</el-button></template>
        </el-input>
      </div>

      <!-- 专员矩阵 -->
      <div class="dept-agents-title">📋 部门执行专员</div>
      <el-row :gutter="12">
        <el-col :span="12" v-for="a in currentTeam?.agents || []" :key="a.code">
          <div class="agent-row">
            <span class="agent-dot"></span>
            <div>
              <div class="agent-name">{{ a.name }}</div>
              <div class="agent-desc">{{ a.desc }}</div>
            </div>
            <el-tag size="small" type="success">空闲</el-tag>
          </div>
        </el-col>
      </el-row>

      <!-- 对话结果 -->
      <div v-if="deptResult" class="exec-box" style="margin-top:16px">
        <pre>{{ deptResult }}</pre>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import request from '../../api/request'
import { ElMessage } from 'element-plus'

const teams = ref({})
const userInput = ref('')
const dispatching = ref(false)
const dispatchResult = ref(null)
const teamDialog = ref(false)
const currentTeam = ref(null)
const deptInput = ref('')
const deptResult = ref('')

async function loadTeams() {
  const res = await request.get('/api/ai/teams')
  teams.value = res.data || {}
}

async function doDispatch() {
  if (!userInput.value) return
  dispatching.value = true
  try {
    const res = await request.post('/api/ai/teams/dispatch', { user_input: userInput.value })
    dispatchResult.value = res.data
  } catch (e) {
    ElMessage.error('派单失败')
  } finally {
    dispatching.value = false
  }
}

function teamName(key) {
  return teams.value[key]?.name || key
}

function enterTeam(key) {
  currentTeam.value = teams.value[key]
  deptResult.value = ''
  deptInput.value = ''
  teamDialog.value = true
}

async function talkToLead() {
  if (!deptInput.value) return
  deptResult.value = '（主管Agent处理中...）'
  // 简化：直接调用dispatch
  try {
    const res = await request.post('/api/ai/teams/dispatch', { user_input: deptInput.value })
    deptResult.value = res.data.execution?.content || '处理完成'
  } catch (e) {
    deptResult.value = 'AI服务暂不可用，请检查模型配置'
  }
  deptInput.value = ''
}

onMounted(loadTeams)
</script>

<style scoped>
.lobby-card { background: linear-gradient(135deg, #667eea, #764ba2); border: none; }
.lobby-card :deep(.el-card__body) { padding: 24px; }
.lobby-header { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; color: #fff; }
.lobby-icon { font-size: 36px; }
.lobby-title { font-size: 20px; font-weight: bold; }
.lobby-sub { font-size: 13px; opacity: 0.9; }
.dispatch-result { margin-top: 16px; }
.exec-box { background: #f5f7fa; border-radius: 8px; padding: 16px; margin-top: 10px; max-height: 300px; overflow-y: auto; }
.exec-box pre { white-space: pre-wrap; margin: 0; font-size: 13px; }

.team-card { margin-bottom: 16px; cursor: pointer; transition: transform 0.2s; }
.team-card:hover { transform: translateY(-2px); }
.team-head { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
.team-icon { width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 22px; color: #fff; }
.team-name { font-weight: bold; font-size: 15px; }
.team-lead { font-size: 12px; color: #999; }
.team-desc { font-size: 13px; color: #666; min-height: 36px; }
.team-stats { display: flex; align-items: center; gap: 8px; margin-top: 12px; }

.dept-lead-box { background: #f0f5ff; border-radius: 8px; padding: 16px; margin-bottom: 16px; }
.dept-lead-head { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
.lead-avatar { width: 40px; height: 40px; border-radius: 50%; background: #409eff; color: #fff; display: flex; align-items: center; justify-content: center; font-size: 20px; }
.dept-agents-title { font-weight: bold; margin: 16px 0 12px; }
.agent-row { display: flex; align-items: center; gap: 10px; padding: 10px; background: #f9fafc; border-radius: 6px; margin-bottom: 8px; }
.agent-dot { width: 8px; height: 8px; border-radius: 50%; background: #67c23a; }
.agent-name { font-size: 13px; font-weight: 600; }
.agent-desc { font-size: 11px; color: #999; }
</style>
