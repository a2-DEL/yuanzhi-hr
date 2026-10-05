import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/login', name: 'Login', component: () => import('../views/Login.vue') },
  {
    path: '/',
    component: () => import('../layouts/MainLayout.vue'),
    redirect: '/dashboard',
    children: [
      { path: 'dashboard', name: 'Dashboard', component: () => import('../views/dashboard/Index.vue'), meta: { title: '工作台' } },
      { path: 'dashboard/executive', name: 'ExecDashboard', component: () => import('../views/dashboard/Executive.vue'), meta: { title: '经营大屏' } },
      { path: 'employee', name: 'Employee', component: () => import('../views/employee/List.vue'), meta: { title: '员工档案' } },
      { path: 'organization', name: 'Organization', component: () => import('../views/organization/Dept.vue'), meta: { title: '组织架构' } },
      { path: 'attendance', name: 'Attendance', component: () => import('../views/attendance/Index.vue'), meta: { title: '考勤管理' } },
      { path: 'salary', name: 'Salary', component: () => import('../views/salary/Index.vue'), meta: { title: '薪酬核算' } },
      { path: 'planning', name: 'Planning', component: () => import('../views/planning/Index.vue'), meta: { title: '人力规划' } },
      { path: 'recruitment', name: 'Recruitment', component: () => import('../views/recruitment/Index.vue'), meta: { title: '招聘管理' } },
      { path: 'training', name: 'Training', component: () => import('../views/training/Index.vue'), meta: { title: '培训开发' } },
      { path: 'performance', name: 'Performance', component: () => import('../views/performance/Index.vue'), meta: { title: '绩效管理' } },
      { path: 'relation', name: 'Relation', component: () => import('../views/relation/Index.vue'), meta: { title: '员工关系' } },
      { path: 'self', name: 'Self', component: () => import('../views/self/Index.vue'), meta: { title: '员工自助' } },
      { path: 'plugin', name: 'Plugin', component: () => import('../views/plugin/Index.vue'), meta: { title: '插件中心' } },
      { path: 'ai/config', name: 'AiConfig', component: () => import('../views/ai/Config.vue'), meta: { title: 'AI模型配置' } },
      { path: 'ai/teams', name: 'AiTeams', component: () => import('../views/ai/Teams.vue'), meta: { title: 'Agent团队' } },
      { path: 'ai/assistant', name: 'AiAssistant', component: () => import('../views/ai/Assistant.vue'), meta: { title: 'AI智能助手' } },
      { path: 'system/users', name: 'SystemUsers', component: () => import('../views/system/Users.vue'), meta: { title: '用户管理' } },
      { path: 'system/roles', name: 'SystemRoles', component: () => import('../views/system/Roles.vue'), meta: { title: '角色管理' } },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.path === '/login') {
    next()
  } else if (!token) {
    next('/login')
  } else {
    next()
  }
})

export default router
