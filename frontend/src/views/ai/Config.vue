<template>
  <el-card>
    <template #header>
      <div style="display:flex;justify-content:space-between;align-items:center">
        <span>AI模型配置</span>
        <el-button type="primary" @click="openDialog">添加模型</el-button>
      </div>
    </template>

    <el-alert type="info" :closable="false" style="margin-bottom:16px">
      只需粘贴您自己的API Key，系统自动识别厂商并配置好。支持OpenAI、豆包、DeepSeek、通义千问、智谱、Kimi等主流模型，数据不出本地。
    </el-alert>

    <el-table :data="list" border stripe>
      <el-table-column prop="provider_name" label="厂商" width="180" />
      <el-table-column prop="base_url" label="API地址" />
      <el-table-column prop="default_model" label="默认模型" width="180" />
      <el-table-column prop="route_level" label="路由等级" width="100">
        <template #default="{ row }">
          <el-tag :type="row.route_level === 'high' ? 'danger' : row.route_level === 'low' ? 'info' : 'primary'">
            {{ row.route_level === 'high' ? '高精度' : row.route_level === 'low' ? '低成本' : '常规' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="is_enabled" label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.is_enabled ? 'success' : 'info'">{{ row.is_enabled ? '启用' : '禁用' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="100">
        <template #default="{ row }">
          <el-button type="danger" size="small" @click="remove(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加模型弹窗 -->
    <el-dialog v-model="dialogVisible" title="添加AI模型" width="600px">
      <!-- 步骤1：粘贴Key -->
      <el-form label-width="100px">
        <el-form-item label="API Key" required>
          <el-input
            v-model="form.api_key"
            type="password"
            placeholder="粘贴您的API Key（以 sk- 开头）"
            show-password
            size="large"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="doDetect" :loading="detecting" size="large" style="width:100%">
            ✨ 智能识别厂商
          </el-button>
        </el-form-item>
      </el-form>

      <!-- 识别结果 -->
      <div v-if="detected" style="background:#f0f9eb;padding:16px;border-radius:8px;margin-bottom:16px">
        <div style="font-weight:bold;color:#67c23a;margin-bottom:8px">✅ 已识别为：{{ detected.provider_name }}</div>
        <div style="font-size:13px;color:#666">API地址：{{ detected.base_url }}</div>
        <div style="font-size:13px;color:#666">默认模型：{{ detected.default_model }}</div>

        <!-- 候选厂商（如果识别不确定） -->
        <div v-if="candidates.length > 1" style="margin-top:12px">
          <div style="font-size:12px;color:#999;margin-bottom:6px">不确定？点选其他厂商：</div>
          <el-radio-group v-model="form.provider" @change="onCandidateSelect" size="small">
            <el-radio v-for="c in candidates" :key="c.provider" :value="c.provider">
              {{ c.provider_name }}
            </el-radio>
          </el-radio-group>
        </div>
      </div>

      <!-- 高级设置（折叠） -->
      <el-collapse v-if="detected">
        <el-collapse-item title="高级设置（一般无需修改）" name="adv">
          <el-form label-width="100px">
            <el-form-item label="API地址">
              <el-input v-model="form.base_url" />
            </el-form-item>
            <el-form-item label="默认模型">
              <el-input v-model="form.default_model" />
            </el-form-item>
            <el-form-item label="路由等级">
              <el-radio-group v-model="form.route_level">
                <el-radio value="high">高精度（复杂任务）</el-radio>
                <el-radio value="normal">常规</el-radio>
                <el-radio value="low">低成本（简单问答）</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-form>
        </el-collapse-item>
      </el-collapse>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button v-if="form.provider" @click="doTest" :loading="testing">测试连接</el-button>
        <el-button type="primary" @click="save" :disabled="!form.provider">保存配置</el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getModelList, addModel, delModel, detectModel, testModelConnection } from '../../api'
import { ElMessage } from 'element-plus'

const list = ref([])
const dialogVisible = ref(false)
const detecting = ref(false)
const testing = ref(false)
const detected = ref(null)
const candidates = ref([])
const form = ref({
  provider: '', base_url: '', api_key: '',
  default_model: '', route_level: 'normal'
})

function openDialog() {
  form.value = { provider: '', base_url: '', api_key: '', default_model: '', route_level: 'normal' }
  detected.value = null
  candidates.value = []
  dialogVisible.value = true
}

async function doDetect() {
  if (!form.value.api_key.trim()) {
    ElMessage.warning('请先粘贴API Key')
    return
  }
  detecting.value = true
  try {
    const res = await detectModel({
      api_key: form.value.api_key,
      base_url: form.value.base_url || ''
    })
    detected.value = res.data.detected
    candidates.value = res.data.candidates || []
    if (detected.value) {
      form.value.provider = detected.value.provider
      form.value.base_url = detected.value.base_url
      form.value.default_model = detected.value.default_model
      ElMessage.success('识别成功！')
    }
  } catch (e) {
    ElMessage.error('识别失败，请手动选择厂商')
  } finally {
    detecting.value = false
  }
}

function onCandidateSelect(provider) {
  const c = candidates.value.find(x => x.provider === provider)
  if (c) {
    form.value.base_url = c.base_url
    form.value.default_model = c.default_model
    detected.value = c
  }
}

async function loadData() {
  const res = await getModelList()
  list.value = res.data || []
}

async function save() {
  await addModel(form.value)
  ElMessage.success('模型配置已保存，整个Agent团队现在都能用了')
  dialogVisible.value = false
  loadData()
}

async function doTest() {
  testing.value = true
  try {
    const res = await testModelConnection({
      base_url: form.value.base_url,
      api_key: form.value.api_key,
      default_model: form.value.default_model,
    })
    if (res.data.success) {
      ElMessage.success(`连接成功！模型回复：${res.data.reply}`)
    } else {
      ElMessage.error(`连接失败：${res.data.error}`)
    }
  } catch (e) {
    ElMessage.error('连接失败，请检查API Key和地址')
  } finally {
    testing.value = false
  }
}

async function remove(id) {
  await delModel(id)
  ElMessage.success('已删除')
  loadData()
}

onMounted(loadData)
</script>
