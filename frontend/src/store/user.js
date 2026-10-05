import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as api from '../api'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(null)

  async function login(loginForm) {
    const res = await api.login(loginForm)
    token.value = res.data.token
    userInfo.value = res.data.user
    localStorage.setItem('token', res.data.token)
    return res
  }

  async function fetchMe() {
    const res = await api.getMe()
    userInfo.value = res.data
    return res.data
  }

  function logout() {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
  }

  return { token, userInfo, login, fetchMe, logout }
})
