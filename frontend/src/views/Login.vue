<template>
  <div class="login-page">
    <!-- 动态粒子背景 -->
    <canvas ref="canvasRef" class="particle-canvas"></canvas>
    <div class="bg-decoration">
      <div class="glow glow-1"></div>
      <div class="glow glow-2"></div>
      <div class="grid-overlay"></div>
    </div>

    <div class="login-wrapper">
      <!-- 左侧品牌区 -->
      <div class="brand-panel">
        <div class="brand-logo">
          <div class="logo-icon">智</div>
          <span class="brand-name">源智 HR</span>
        </div>
        <h1 class="brand-title">
          基于多 Agent 的<br />
          <span class="gradient-text">智能人力运营操作系统</span>
        </h1>
        <p class="brand-desc">
          国内首个多Agent虚拟HR团队 · 数据私有化部署 · 全模型自由适配
        </p>

        <!-- 数据动画卡片 -->
        <div class="stats-row">
          <div class="stat-box">
            <div class="stat-num">6</div>
            <div class="stat-label">专业HR团队</div>
          </div>
          <div class="stat-box">
            <div class="stat-num">21</div>
            <div class="stat-label">执行Agent</div>
          </div>
          <div class="stat-box">
            <div class="stat-num">6+</div>
            <div class="stat-label">大模型适配</div>
          </div>
        </div>

        <div class="feature-list">
          <div class="feature-item">
            <div class="feature-dot"></div>
            <span>多Agent团队自动完成HR事务，效率提升80%</span>
          </div>
          <div class="feature-item">
            <div class="feature-dot"></div>
            <span>API Key自托管，数据不出企业，零官方成本</span>
          </div>
          <div class="feature-item">
            <div class="feature-dot"></div>
            <span>兼容豆包 / DeepSeek / GPT / 通义千问 / 智谱</span>
          </div>
        </div>

        <!-- 角色体系 -->
        <div class="role-tags">
          <span class="role-tag">HR总监</span>
          <span class="role-tag">部门经理</span>
          <span class="role-tag">HR专员</span>
          <span class="role-tag">普通员工</span>
          <span class="role-tag">系统管理员</span>
        </div>
      </div>

      <!-- 右侧登录表单 -->
      <div class="form-panel">
        <div class="form-card">
          <h2 class="form-title">欢迎登录</h2>
          <p class="form-subtitle">源智HR智能人力运营系统</p>

          <el-form :model="form" @submit.prevent="handleLogin" size="large">
            <el-form-item>
              <el-input v-model="form.username" placeholder="请输入账号" :prefix-icon="User" />
            </el-form-item>
            <el-form-item>
              <el-input v-model="form.password" type="password" placeholder="请输入密码"
                :prefix-icon="Lock" @keyup.enter="handleLogin" show-password />
            </el-form-item>
            <el-button type="primary" class="login-btn" :loading="loading" @click="handleLogin">
              登 录
            </el-button>
          </el-form>

          <div class="login-tip">
            <el-icon><InfoFilled /></el-icon>
            管理员账号 admin · 密码 admin123
          </div>
        </div>
        <div class="copyright">© 2026 源智HR · 开源 MIT License</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { User, Lock, InfoFilled } from '@element-plus/icons-vue'
import { useUserStore } from '../store/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const form = ref({ username: 'admin', password: 'admin123' })
const loading = ref(false)

async function handleLogin() {
  if (!form.value.username || !form.value.password) {
    ElMessage.warning('请输入账号和密码')
    return
  }
  loading.value = true
  try {
    await userStore.login(form.value)
    ElMessage.success('登录成功，欢迎回来')
    router.push('/')
  } catch (e) {
    // 错误已拦截
  } finally {
    loading.value = false
  }
}

// 粒子动画
const canvasRef = ref(null)
let animationId = null
let particles = []

function initParticles() {
  const canvas = canvasRef.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  canvas.width = window.innerWidth
  canvas.height = window.innerHeight

  particles = Array.from({ length: 60 }, () => ({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    r: Math.random() * 2 + 1,
    dx: (Math.random() - 0.5) * 0.5,
    dy: (Math.random() - 0.5) * 0.5,
    opacity: Math.random() * 0.5 + 0.2,
  }))

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    particles.forEach(p => {
      p.x += p.dx
      p.y += p.dy
      if (p.x < 0 || p.x > canvas.width) p.dx *= -1
      if (p.y < 0 || p.y > canvas.height) p.dy *= -1
      ctx.beginPath()
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2)
      ctx.fillStyle = `rgba(107, 140, 255, ${p.opacity})`
      ctx.fill()
    })
    animationId = requestAnimationFrame(animate)
  }
  animate()
}

onMounted(initParticles)
onUnmounted(() => { if (animationId) cancelAnimationFrame(animationId) })
</script>

<style scoped>
.login-page {
  position: relative;
  height: 100vh;
  background: #0a0e1a;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.particle-canvas {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.bg-decoration { position: absolute; inset: 0; pointer-events: none; }
.glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.5;
}
.glow-1 {
  width: 600px; height: 600px;
  background: #4f6ef7;
  top: -200px; left: -150px;
}
.glow-2 {
  width: 500px; height: 500px;
  background: #9b5cf7;
  bottom: -180px; right: -100px;
}
.grid-overlay {
  position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
  background-size: 50px 50px;
}

.login-wrapper {
  position: relative;
  z-index: 1;
  width: 960px;
  height: 580px;
  display: flex;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 20px;
  backdrop-filter: blur(20px);
  overflow: hidden;
  box-shadow: 0 30px 80px rgba(0,0,0,0.5);
}

.brand-panel {
  flex: 1.2;
  padding: 45px 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background: linear-gradient(135deg, rgba(79,110,247,0.15), rgba(155,92,247,0.1));
}
.brand-logo { display: flex; align-items: center; gap: 12px; margin-bottom: 30px; }
.logo-icon {
  width: 40px; height: 40px;
  background: linear-gradient(135deg, #4f6ef7, #9b5cf7);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 20px; font-weight: bold;
}
.brand-name { color: #fff; font-size: 20px; font-weight: 600; letter-spacing: 1px; }
.brand-title {
  color: #fff;
  font-size: 26px;
  line-height: 1.4;
  margin: 0 0 12px;
  font-weight: 600;
}
.gradient-text {
  background: linear-gradient(90deg, #6b8cff, #b78cff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.brand-desc {
  color: rgba(255,255,255,0.55);
  font-size: 13px;
  line-height: 1.6;
  margin: 0 0 24px;
}

.stats-row { display: flex; gap: 12px; margin-bottom: 24px; }
.stat-box {
  flex: 1;
  background: rgba(255,255,255,0.06);
  border-radius: 10px;
  padding: 12px;
  text-align: center;
}
.stat-num { font-size: 24px; font-weight: bold; color: #6b8cff; }
.stat-label { font-size: 11px; color: rgba(255,255,255,0.5); margin-top: 4px; }

.feature-list { display: flex; flex-direction: column; gap: 10px; margin-bottom: 20px; }
.feature-item { display: flex; align-items: center; gap: 10px; color: rgba(255,255,255,0.75); font-size: 12px; }
.feature-dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: #6b8cff;
  box-shadow: 0 0 10px #6b8cff;
}

.role-tags { display: flex; flex-wrap: wrap; gap: 6px; }
.role-tag {
  font-size: 11px;
  padding: 3px 10px;
  border-radius: 20px;
  background: rgba(107,140,255,0.15);
  color: #8ba8ff;
  border: 1px solid rgba(107,140,255,0.3);
}

.form-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 45px 45px;
  background: rgba(10,14,26,0.6);
}
.form-card { width: 100%; }
.form-title { color: #fff; font-size: 26px; margin: 0 0 8px; font-weight: 600; }
.form-subtitle { color: rgba(255,255,255,0.4); font-size: 13px; margin: 0 0 32px; }

.login-btn {
  width: 100%;
  height: 44px;
  background: linear-gradient(135deg, #4f6ef7, #6b5cf7);
  border: none;
  font-size: 15px;
  letter-spacing: 4px;
  margin-top: 8px;
}
.login-btn:hover {
  background: linear-gradient(135deg, #5d7cf7, #7a6cf7);
  opacity: 0.9;
}

.login-tip {
  margin-top: 24px;
  text-align: center;
  color: rgba(255,255,255,0.35);
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
}
.copyright {
  margin-top: 30px;
  text-align: center;
  color: rgba(255,255,255,0.25);
  font-size: 12px;
}

:deep(.el-input__wrapper) {
  background: rgba(255,255,255,0.06) !important;
  box-shadow: 0 0 0 1px rgba(255,255,255,0.1) inset !important;
  border-radius: 8px;
}
:deep(.el-input__inner) { color: #fff !important; }
:deep(.el-input__inner::placeholder) { color: rgba(255,255,255,0.35) !important; }
:deep(.el-input__prefix-inner) { color: rgba(255,255,255,0.45) !important; }
:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px #6b8cff inset !important;
}
</style>
