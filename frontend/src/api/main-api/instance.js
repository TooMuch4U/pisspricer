import axios from 'axios'

const API_BASE_URL = process.env.API_URL

export default axios.create({
  baseURL: API_BASE_URL,
  timeout: 2000
})
