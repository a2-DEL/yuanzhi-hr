<template>
  <el-container class="layout-container">
    <!-- 侧边栏 -->
    <el-aside :width="isCollapse ? '64px' : '220px'" class="sidebar">
      <div class="logo">
        <span v-if="!isCollapse" class="logo-text">源智HR</span>
        <span v-else class="logo-text-sm">智</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        :collapse="isCollapse"
        router
        class="sidebar-menu"
      >
        <el-menu-item index="/dashboard">
          <el-icon><Odometer /></el-icon>
          <template #title>工作台</template>
        </el-menu-item>

        <el-menu-item index="/dashboard/executive">
          <el-icon><DataAnalysis /></el-icon>
          <template #title>经营大屏</template>
        </el-menu-item>

        <el-menu-item index="/self">
          <el-icon><User /></el-icon>
          <template #title>员工自助</template>
        </el-menu-item>

        <el-sub-menu index="org">
          <template #title>
            <el-icon><OfficeBuilding /></el-icon>
            <span>人事管理</span>
          </template>
          <el-menu-item index="/organization">组织架构</el-menu-item>
          <el-menu-item index="/employee">员工档案</el-menu-item>
          <el-menu-item index="/attendance">考勤管理</el-menu-item>
          <el-menu-item index="/salary">薪酬核算</el-menu-item>
          <el-menu-item index="/planning">人力规划</el-menu-item>
          <el-menu-item index="/recruitment">招聘管理</el-menu-item>
          <el-menu-item index="/training">培训开发</el-menu-item>
          <el-menu-item index="/performance">绩效管理</el-menu-item>
          <el-menu-item index="/relation">员工关系</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="ai">
          <template #title>
            <el-icon><MagicStick /></el-icon>
            <span>AI能力</span>
          </template>
          <el-menu-item index="/ai/assistant">智能助手</el-menu-item>
          <el-menu-item index="/ai/teams">Agent团队</el-menu-item>
          <el-menu-item index="/ai/config">模型配置</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="system">
          <template #title>
            <el-icon><Setting /></el-icon>
            <span>系统管理</span>
          </template>
          <el-menu-item index="/system/users">用户管理</el-menu-item>
          <el-menu-item index="/system/roles">角色管理</el-menu-item>
          <el-menu-item index="/plugin">插件中心</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>

    <!-- 主内容区 -->
    <el-container>
      <el-header class="header">
        <div class="header-left">
          <el-icon class="collapse-btn" @click="isCollapse = !isCollapse">
            <Expand v-if="isCollapse" />
            <Fold v-else />
          </el-icon>
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="'/'">首页</el-breadcrumb-item>
            <el-breadcrumb-item>{{ route.meta.title }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-right">
          <el-badge :value="unreadCount" :hidden="unreadCount === 0" style="margin-right:20px;cursor:pointer" @click="openMessages">
            <el-icon size="20"><Bell /></el-icon>
          </el-badge>
          <el-dropdown @command="handleCommand">
            <span class="user-info">
              <el-icon><UserFilled /></el-icon>
              {{ userStore.userInfo?.real_name || '管理员' }}
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>

    <!-- 消息抽屉 -->
    <el-drawer v-model="showMessages" title="消息中心" size="400px">
      <div v-for="m in messages" :key="m.id" class="msg-item" :class="{unread: !m.is_read}" @click="readMsg(m)">
        <div class="msg-title">
          <el-tag size="small" :type="msgTypeColor(m.type)">{{ m.type }}</el-tag>
          <b>{{ m.title }}</b>
        </div>
        <div class="msg-content">{{ m.content }}</div>
        <div class="msg-time">{{ m.time }}</div>
      </div>
      <el-empty v-if="messages.length === 0" description="暂无消息" />
    </el-drawer>
  </el-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../store/user'
import request from '../api/request'
import { Bell } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const isCollapse = ref(false)
const unreadCount = ref(0)
const messages = ref([])
const showMessages = ref(false)

const activeMenu = computed(() => route.path)

async function loadUnread() {
  try {
    const res = await request.get('/api/message/unread')
    unreadCount.value = res.data.count
  } catch (e) {}
}

async function openMessages() {
  showMessages.value = true
  try {
    const res = await request.get('/api/message/list')
    messages.value = res.data || []
  } catch (e) {}
}

async function readMsg(m) {
  if (!m.is_read) {
    await request.post(`/api/message/read/${m.id}`)
    m.is_read = true
    unreadCount.value = Math.max(0, unreadCount.value - 1)
  }
}

function msgTypeColor(t) {
  return { system: 'info', approval: 'warning', warning: 'danger', birthday: 'success' }[t] || 'info'
}

onMounted(() => {
  if (!userStore.userInfo) {
    userStore.fetchMe().catch(() => {})
  }
  loadUnread()
})

function handleCommand(cmd) {
  if (cmd === 'logout') {
    userStore.logout()
    router.push('/login')
  }
}
</script>

<style scoped>
.layout-container { height: 100vh; }
.sidebar {
  background: #ffffff;
  border-right: 1px solid #e8e8e8;
  transition: width 0.3s;
  overflow: hidden;
  box-shadow: 2px 0 8px rgba(0,0,0,0.03);
}
.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: bold;
  background: linear-gradient(135deg, #4f6ef7, #6b5cf7);
  color: #fff;
  letter-spacing: 1px;
}
.logo-text-sm { font-size: 22px; }
.sidebar-menu { border-right: none; background: #fff; }
.sidebar-menu .el-menu-item,
.sidebar-menu .el-sub-menu__title {
  color: #333 !important;
}
.sidebar-menu .el-menu-item:hover,
.sidebar-menu .el-sub-menu__title:hover {
  background: #f0f4ff !important;
  color: #4f6ef7 !important;
}
.sidebar-menu .el-menu-item.is-active {
  background: #ecf0ff !important;
  color: #4f6ef7 !important;
  font-weight: 600;
  border-right: 3px solid #4f6ef7;
}
.header {
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 1px 4px rgba(0,21,41,0.08);
  padding: 0 20px;
}
.header-left { display: flex; align-items: center; gap: 16px; }
.collapse-btn { font-size: 20px; cursor: pointer; }
.user-info { cursor: pointer; display: flex; align-items: center; gap: 6px; }
.main-content { background: #f0f2f5; padding: 20px; }
.msg-item { padding: 12px; border-bottom: 1px solid #f0f0f0; cursor: pointer; }
.msg-item:hover { background: #f5f7fa; }
.msg-item.unread { background: #ecf5ff; }
.msg-title { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
.msg-content { color: #666; font-size: 13px; margin-bottom: 4px; }
.msg-time { color: #999; font-size: 11px; }

/* 移动端响应式 */
@media (max-width: 768px) {
  .sidebar { width: 60px !important; }
  .main-content { padding: 10px; }
  .header { padding: 0 10px; }
  .user-info span { display: none; }
}
</style>
