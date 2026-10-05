<template>
  <el-card>
    <template #header>AI智能助手</template>

    <el-row :gutter="20">
      <el-col :span="6">
        <h4 style="margin:0 0 12px">选择Agent</h4>
        <el-radio-group v-model="selectedAgent" direction="vertical">
          <el-radio v-for="a in agents" :key="a.code" :value="a.code" style="display:block;margin:8px 0">
            {{ a.name }}
            <div style="font-size:12px;color:#999;margin-left:25px">{{ a.description }}</div>
          </el-radio>
        </el-radio-group>
      </el-col>
      <el-col :span="18">
        <div class="chat-box">
          <div v-for="(m, i) in messages" :key="i" :class="['msg', m.role]">
            <div class="bubble">{{ m.content }}</div>
          </div>
          <div v-if="loading" class="msg assistant"><div class="bubble">思考中...</div></div>
        </div>
        <div style="display:flex;gap:10px;margin-top:12px">
          <el-input
            v-model="input"
            placeholder="输入您的问题，如：员工年假怎么计算？"
            @keyup.enter="send"
          />
          <el-button type="primary" @click="send" :loading="loading">发送</el-button>
        </div>
      </el-col>
    </el-row>
  </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getAgentList, callAgent } from '../../api'
import { ElMessage } from 'element-plus'

const agents = ref([])
const selectedAgent = ref('hr_assistant')
const messages = ref([
  { role: 'assistant', content: '您好！我是源智HR智能助手，请输入您的人事相关问题。' }
])
const input = ref('')
const loading = ref(false)

async function send() {
  if (!input.value.trim()) return
  const q = input.value
  messages.value.push({ role: 'user', content: q })
  input.value = ''
  loading.value = true
  try {
    const res = await callAgent({ agent_code: selectedAgent.value, input: q })
    messages.value.push({ role: 'assistant', content: res.data.content })
  } catch (e) {
    messages.value.push({ role: 'assistant', content: '抱歉，调用失败：' + (e.message || '请先配置AI模型') })
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  const res = await getAgentList()
  agents.value = res.data || []
})
</script>

<style scoped>
.chat-box {
  height: 400px; overflow-y: auto; padding: 16px;
  background: #f5f7fa; border-radius: 8px;
}
.msg { margin: 10px 0; display: flex; }
.msg.user { justify-content: flex-end; }
.bubble {
  max-width: 70%; padding: 10px 14px; border-radius: 8px;
  background: #fff; line-height: 1.5;
}
.msg.user .bubble { background: #409eff; color: #fff; }
</style>
