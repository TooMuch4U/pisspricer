'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  API_URL: '"http://localhost:4941/api/v1"',
  VUE_APP_STATIC_URL: '"https://storage.googleapis.com/images.pisspricer.co.nz/"',
  VUE_APP_SCRAPER_API_URL: '"http://localhost:3000/scrapi/v1"'
})
