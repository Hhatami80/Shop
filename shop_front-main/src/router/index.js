import { createRouter, createWebHistory } from 'vue-router'
import VueCookies from 'vue-cookies'
import { useLoginStore } from '@/stores/useLoginStore'

import AdminPanel from '@/layouts/AdminPanel.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import ChangePass from '@/components/ChangePasswordModal.vue'
import MainPage from '@/views/MainPage.vue'
import ArticleForm from '@/components/ArticleForm.vue'
import ArticleList from '@/components/ArticleList.vue'
import FooterManager from '@/components/FooterManager.vue'
import HeaderManager from '@/components/HeaderManager.vue'
import ProductManager from '@/components/ProductManager.vue'
import AboutUsManager from '@/components/AboutUsManager.vue'
import FeatureSectionManager from '@/components/FeatureSectionManager.vue'
import CategoryManager from '@/components/CategoryManager.vue'
import UserList from '@/components/UserList.vue'
import ShoppingCart from '@/components/ShoppingCart.vue'
import ArticlesPage from '@/views/ArticlesPage.vue'
import AdminOrders from '@/components/AdminOrders.vue'
import CommetsManager from '@/components/CommetsManager.vue'
import ArticleView from '@/views/ArticleView.vue'
import Games from '@/views/Games.vue'
import UserPanel from '@/layouts/UserPanel.vue'
import ForgotPassword from '@/views/ForgotPassword.vue'
import CategoryPage from '@/views/CategoryPage.vue'
import ProductDetailPage from '@/views/ProductDetailPage.vue'
import ContactUs from '@/views/ContactUs.vue'
import AdminTransactions from '@/components/AdminTransactions.vue'
import ProductPage from '@/views/ProductPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'MainPage', component: MainPage },
    { path: '/login', name: 'Login', component: Login },
    { path: '/register', name: 'Register', component: Register },
    { path: '/shop-cart', name: 'shop-cart', component: ShoppingCart },
    { path: '/articles', name: 'articles', component: ArticlesPage },
    { path: '/articles/:id', name: 'ArticleView', component: ArticleView },
    { path: '/games', name: 'games', component: Games },
    { path: '/forgotPassword', name: 'forgotPassword', component: ForgotPassword },
    { path: '/categories', name: 'categoryPage', component: CategoryPage },
    {path: '/productpage' , name:'productpage' , component: ProductPage},
    {
      path: '/payment',
      name: 'payment',
      component: () => import('@/views/PaymentPage.vue'),
      meta: { title: 'پرداخت سفارش' },
    },
    {
      path: '/contactus',
      name: 'contactus',
      component: ContactUs,
    },
    {
      path: '/payment/verify',
      name: 'PaymentVerify',
      component: () => import('@/views/PaymentVerify.vue'),
      meta: { title: 'بررسی پرداخت' },
    },
    {
      path: '/categories/:id',
      name: 'CategoryDetail',
      component: () => import('@/views/CategoryDetail.vue'),
      props: true,
    },
    {
      path: '/checkout',
      name: 'checkout',
      component: () => import('@/views/CheckoutPage.vue'),
      meta: { title: 'تسویه حساب' },
    },
    {
      path: '/product/:id',
      name: 'ProductDetail',
      component: ProductDetailPage,
    },
    {
      path: '/payment/gateway',
      name: 'payment-gateway',
      component: () => import('@/views/PaymentGatewayPage.vue'),
      meta: { title: 'انتخاب درگاه پرداخت' },
    },
    {
      path: '/user/orders',
      name: 'UserOrders',
      component: () => import('@/components/UserOrders.vue'),
      meta: { requiresAuth: true },
    },

    {
      path: '/user',
      component: UserPanel,
      meta: { requiresAuth: true },
      children: [
        {
          path: 'wallet',
          name: 'Wallet',
          component: () => import('@/components/Wallet.vue'),
          meta: { title: 'کیف پول من' },
        },

        {
          path: 'wallet/verify',
          name: 'WalletVerify',
          component: () => import('@/views/WalletVerify.vue'),
          meta: { title: 'تأیید پرداخت کیف پول' },
        },
        {
          path: 'profile',
          name: 'UserProfile',
          component: () => import('@/components/UserProfile.vue'),
          meta: { title: 'پروفایل کاربری' },
        },

        {
          path: 'order-success',
          name: 'OrderSuccess',
          component: () => import('@/views/OrderSuccessPage.vue'),
          meta: { title: 'ثبت موفق سفارش' },
        },
      ],
    },
    {
      path: '/order-success',
      name: 'OrderSuccess',
      component: () => import('@/views/OrderSuccessPage.vue'),
      meta: { title: 'ثبت موفق سفارش' },
    },
    {
      path: '/wallet/payment',
      name: 'WalletPayment',
      component: () => import('@/views/WalletPaymentPage.vue'),
      meta: { title: 'شارژ کیف پول' },
    },
    {
      path: '/wallet/verify',
      name: 'WalletVerify',
      component: () => import('@/views/WalletVerify.vue'),
      meta: { title: 'تأیید پرداخت کیف پول' },
    },
    {
      path: '/admin',
      component: AdminPanel,
      children: [
        { path: 'header', name: 'header', component: HeaderManager },
        { path: 'footer', name: 'footer', component: FooterManager },
        { path: 'changepass', name: 'ChangePass', component: ChangePass },
        { path: 'articles', name: 'ArticleList', component: ArticleList },
        { path: 'articles/create', name: 'ArticleCreate', component: ArticleForm },
        { path: 'articles/edit/:id', name: 'ArticleEdit', component: ArticleForm, props: true },
        { path: 'productmanager', name: 'productmanager', component: ProductManager },
        { path: 'aboutusmanager', name: 'aboutusmanager', component: AboutUsManager },
        { path: 'bannermanager', name: 'bannermanager', component: FeatureSectionManager },
        { path: 'categorymanager', name: 'categorymanager', component: CategoryManager },
        { path: 'userslist', name: 'userslist', component: UserList },
        { path: 'orderList', name: 'orderList', component: AdminOrders },
        { path: 'comments', name: ' comments', component: CommetsManager },
        {
          path: '/admin/transactions',
          name: 'AdminTransactions',
          component: AdminTransactions,
          meta: { requiresAdmin: true },
        },
      ],
    },
  ],
})

// router.beforeEach((to) => {
//   const loginStore = useLoginStore()
//   if (!loginStore.token) {
//     loginStore.loadFromCookies()
//   }

//   const isAuthenticated = loginStore.isAuthenticated
//   const isAdmin = loginStore.isAdmin

//   if (to.path.startsWith('/admin') && !isAuthenticated) {
//     return { name: 'Login' }
//   }

//   if (to.path.startsWith('/user') && !isAuthenticated) {
//     return { name: 'Login' }
//   }

//   if (to.path.startsWith('/admin') && isAuthenticated && !isAdmin) {
//     return { name: 'MainPage' }
//   }

//   if (isAuthenticated && to.name === 'Login') {
//     return { name: 'MainPage' }
//   }
// })

export default router
