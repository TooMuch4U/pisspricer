import { library } from '@fortawesome/fontawesome-svg-core'
import { faUser as faUserSolid, faWrench } from '@fortawesome/free-solid-svg-icons'
import { faUser as faUserReg } from '@fortawesome/free-regular-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import Vue from 'vue'

// Font awesome icons
library.add(faUserReg, faUserSolid, faWrench)
Vue.component('font-awesome-icon', FontAwesomeIcon)
