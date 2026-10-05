import request from './request'

// 认证
export const login = (data) => request.post('/api/auth/login', data)
export const getMe = () => request.get('/api/auth/me')

// 组织架构
export const getDeptTree = () => request.get('/api/org/departments/tree')
export const addDept = (data) => request.post('/api/org/departments', data)

// 员工
export const getEmpList = (params) => request.get('/api/employee/list', { params })
export const addEmp = (data) => request.post('/api/employee', data)

// AI
export const getAiPresets = () => request.get('/api/ai/providers/presets')
export const getModelList = () => request.get('/api/ai/models')
export const addModel = (data) => request.post('/api/ai/models', data)
export const delModel = (id) => request.delete(`/api/ai/models/${id}`)
export const detectModel = (data) => request.post('/api/ai/detect', data)
export const testModelConnection = (data) => request.post('/api/ai/test', data)

// 插件管理
export const getPluginList = () => request.get('/api/plugins/list')
export const enablePlugin = (data) => request.post('/api/plugins/enable', data)
export const disablePlugin = (data) => request.post('/api/plugins/disable', data)
export const runPlugin = (data) => request.post('/api/plugins/run', data)
export const getAgentList = () => request.get('/api/ai/agents')
export const callAgent = (data) => request.post('/api/ai/agents/call', data)
export const getAiStats = () => request.get('/api/ai/usage/stats')

// 系统
export const getUserList = () => request.get('/api/system/users')
export const getRoleList = () => request.get('/api/system/roles')

// 考勤
export const getLeaveList = () => request.get('/api/attendance/leave/list')
export const addLeave = (data) => request.post('/api/attendance/leave', data)
export const approveLeave = (id, action) => request.put(`/api/attendance/leave/${id}/approve?action=${action}`)
export const getAttendanceRecords = () => request.get('/api/attendance/records')
export const clockIn = (data) => request.post('/api/attendance/clock-in', data)

// 薪酬
export const getSalaryRecords = (params) => request.get('/api/salary/records', { params })
export const calculateSalary = (month) => request.post(`/api/salary/calculate?month=${month}`)
export const getSalaryStructures = () => request.get('/api/salary/structures')
export const setSalaryStructure = (data) => request.post('/api/salary/structures', data)

// 人力资源规划
export const getHeadcount = () => request.get('/api/planning/headcount')
export const setHeadcount = (data) => request.post('/api/planning/headcount', data)
export const getJobs = () => request.get('/api/planning/jobs')
export const addJob = (data) => request.post('/api/planning/jobs', data)
export const getPolicies = (params) => request.get('/api/planning/policies', { params })
export const addPolicy = (data) => request.post('/api/planning/policies', data)

// 招聘管理
export const getDemands = () => request.get('/api/recruitment/demands')
export const addDemand = (data) => request.post('/api/recruitment/demands', data)
export const getResumes = (params) => request.get('/api/recruitment/resumes', { params })
export const addResume = (data) => request.post('/api/recruitment/resumes', data)
export const updateResumeStatus = (id, status) => request.put(`/api/recruitment/resumes/${id}/status?status=${status}`)
export const getInterviews = () => request.get('/api/recruitment/interviews')
export const addInterview = (data) => request.post('/api/recruitment/interviews', data)
export const getFunnel = () => request.get('/api/recruitment/funnel')

// 培训与开发
export const getCourses = () => request.get('/api/training/courses')
export const addCourse = (data) => request.post('/api/training/courses', data)
export const getPlans = () => request.get('/api/training/plans')
export const addPlan = (data) => request.post('/api/training/plans', data)
export const getRecords = (params) => request.get('/api/training/records', { params })
export const addRecord = (data) => request.post('/api/training/records', data)
export const getPipeline = () => request.get('/api/training/pipeline')
export const addPipeline = (data) => request.post('/api/training/pipeline', data)

// 绩效管理
export const getIndicators = () => request.get('/api/performance/indicators')
export const addIndicator = (data) => request.post('/api/performance/indicators', data)
export const getCycles = () => request.get('/api/performance/cycles')
export const addCycle = (data) => request.post('/api/performance/cycles', data)
export const getScores = (params) => request.get('/api/performance/scores', { params })
export const addScore = (data) => request.post('/api/performance/scores', data)
export const getDistribution = (params) => request.get('/api/performance/distribution', { params })

// 员工关系
export const getContracts = () => request.get('/api/employee-relation/contracts')
export const addContract = (data) => request.post('/api/employee-relation/contracts', data)
export const getTransfers = () => request.get('/api/employee-relation/transfers')
export const addTransfer = (data) => request.post('/api/employee-relation/transfers', data)
export const getDisciplines = () => request.get('/api/employee-relation/disciplines')
export const addDiscipline = (data) => request.post('/api/employee-relation/disciplines', data)
export const getOffboardings = () => request.get('/api/employee-relation/offboardings')
export const addOffboarding = (data) => request.post('/api/employee-relation/offboardings', data)
export const getAttritionStats = () => request.get('/api/employee-relation/attrition-stats')

// AI Agent团队
export const getTeams = () => request.get('/api/ai/teams')
export const directorDispatch = (data) => request.post('/api/ai/teams/dispatch', data)

// 数据大屏
export const getExecutiveDashboard = () => request.get('/api/dashboard/executive')
