import axios from 'axios'
import cookies from 'vue-cookies'

const api = axios.create({
  baseURL: import.meta.env.VITE_LARAVEL_BASE_URL,
  timeout: 100000,
  // headers: {
  //   'Content-Type': 'application/json',
  // },
})

api.interceptors.request.use(
  (config) => {
    const token = cookies.get('token')
    if (token) {
      config.headers.Authorization = `Token ${token}`
    }

    return config
  },
  (error) => {
    console.error('Request error:', error)
    return Promise.reject(error)
  },
)

export default api
