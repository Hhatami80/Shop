import '@/assets/fonts/fonts/iransans/fontiran.css'
import './assets/css/main.css'
import '@fortawesome/fontawesome-free/css/all.min.css'
// import '@fortawesome/fontawesome-free/css/all.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import VueCookies from 'vue-cookies'
import App from './App.vue'
import router from './router'

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

import Vue3Toastify from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'
import { Swiper, SwiperSlide } from 'swiper/vue'

import 'swiper/css'
import 'swiper/css/navigation'
import DatePicker from 'vue3-persian-datetime-picker'

import {
  faTachometerAlt,
  faFeatherAlt,
  faInfoCircle,
  faImage,
  faBoxOpen,
  faTags,
  faReceipt,
  faUsers,
  faComments,
  faCrown,
  faSignOutAlt,
  faHome,
  faUserCircle,
  faChevronUp,
  faChevronDown,
  faPlusCircle,
  faTrash,
  faEdit,
  faSpinner,
  faCheckCircle,
  faBalanceScale,
  faRulerCombined,
  faStar,
  faEye,
  faMinusCircle,
  faChevronLeft,
  faChevronRight,
  faWallet,
  faUser,
  faBox,
  faShoppingCart,
  faClipboardList,
  faColumns,
  faBars,
  faInbox,
  faPhoneSquareAlt

} from '@fortawesome/free-solid-svg-icons'

library.add(
  faTachometerAlt,
  faFeatherAlt,
  faInfoCircle,
  faImage,
  faBoxOpen,
  faTags,
  faReceipt,
  faUsers,
  faComments,
  faCrown,
  faSignOutAlt,
  faHome,
  faUserCircle,
  faChevronUp,
  faPlusCircle,
  faSpinner,
  faTrash,
  faEdit,
  faChevronDown,
  faCheckCircle,
  faBalanceScale,
  faRulerCombined,
  faStar,
  faEye,
  faMinusCircle,
  faChevronLeft,
  faChevronRight,
  faWallet,
  faUser,
  faBox,
  faShoppingCart,
  faClipboardList,
  faColumns,
  faBars,
  faInbox,
  faPhoneSquareAlt
  
)

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Vue3Toastify, {
  autoClose: 3000,
  position: 'top-right',
  theme: 'light',
})
app.component('fa-icon', FontAwesomeIcon)
app.component('DatePicker', DatePicker)
app.component('Swiper', Swiper)
app.component('SwiperSlide', SwiperSlide)

app.use(VueCookies)
app.mount('#app')
