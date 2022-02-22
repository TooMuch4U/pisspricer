import axios from 'axios'

const API_BASE_URL = process.env.VUE_APP_SCRAPER_API_URL

export default axios.create({
  baseURL: API_BASE_URL,
  timeout: 20000,
  withCredentials: true
})
