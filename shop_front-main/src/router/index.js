import { createRouter, createWebHistory } from 'vue-router'
import { useLoginStore } from '@/stores/useLoginStore'

import AdminPanel from '@/layouts/AdminPanel.vue'
import UserPanel from '@/layouts/UserPanel.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import MainPage from '@/views/MainPage.vue'
import ArticlesPage from '@/views/ArticlesPage.vue'
import ArticleView from '@/views/ArticleView.vue'
import Games from '@/views/Games.vue'
import ForgotPassword from '@/views/ForgotPassword.vue'
import CategoryPage from '@/views/CategoryPage.vue'
import ProductPage from '@/views/ProductPage.vue'
import ProductDetailPage from '@/views/ProductDetailPage.vue'
import ContactUs from '@/views/ContactUs.vue'
import AdminTransactions from '@/components/AdminTransactions.vue'
import ChangePass from '@/components/ChangePasswordModal.vue'
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
import AdminOrders from '@/components/AdminOrders.vue'
import CommetsManager from '@/components/CommetsManager.vue'
import CategoryDetail from '@/views/CategoryDetail.vue'
import Dashboard from '@/components/Dashboard.vue'
import AdminDashboard from '@/components/AdminDashboard.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'MainPage', component: MainPage },
    { path: '/login', name: 'Login', component: Login },
    { path: '/register', name: 'Register', component: Register },
    { path: '/articles', name: 'articles', component: ArticlesPage },
    { path: '/articles/:id', name: 'ArticleView', component: ArticleView },
    { path: '/games', name: 'games', component: Games },
    { path: '/forgotPassword', name: 'forgotPassword', component: ForgotPassword },
    { path: '/categories', name: 'categoryPage', component: CategoryPage },
    { path: '/categories/:id', name: 'categorydetail', component: CategoryDetail },
    { path: '/productpage', name: 'productpage', component: ProductPage },
    { path: '/product/:id', name: 'ProductDetail', component: ProductDetailPage },
    { path: '/contactus', name: 'contactus', component: ContactUs },
    {
      path: '/payment',
      name: 'payment',
      component: () => import('@/views/PaymentPage.vue'),
      meta: { title: 'پرداخت سفارش' },
    },
    {
      path: '/payment/verify',
      name: 'PaymentVerify',
      component: () => import('@/views/PaymentVerify.vue'),
      meta: { title: 'بررسی پرداخت' },
    },
    {
      path: '/checkout',
      name: 'checkout',
      component: () => import('@/views/CheckoutPage.vue'),
      meta: { title: 'تسویه حساب' },
    },
    {
      path: '/payment/gateway',
      name: 'payment-gateway',
      component: () => import('@/views/PaymentGatewayPage.vue'),
      meta: { title: 'انتخاب درگاه پرداخت' },
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
      path: '/user',
      component: UserPanel,
      meta: { requiresAuth: true },
      children: [
        {
          path: 'profile',
          component: () => import('@/components/UserProfile.vue'),
          children: [
            { path: 'info', component: () => import('@/components/ProfileInfo.vue') },
            { path: 'addresses', component: () => import('@/components/ProfileAddresses.vue') },
            { path: 'bank', component: () => import('@/components/BankAccounts.vue') },
            { path: '', redirect: 'info' },
          ],
        },
        { path: 'wallet', component: () => import('@/components/Wallet.vue') },
        { path: 'shop-cart', component: ShoppingCart },
        { path: 'dashboard' , component:Dashboard},
        { path: 'orders', component: () => import('@/components/UserOrders.vue') },
        { path: 'wallet/verify', component: () => import('@/views/WalletVerify.vue') },
        { path: 'order-success', component: () => import('@/views/OrderSuccessPage.vue') },
      ],
    },

    {
      path: '/admin',
      component: AdminPanel,
      children: [
        { path: 'header', component: HeaderManager },
        { path: 'footer', component: FooterManager },
        { path: 'changepass', component: ChangePass },
        { path: 'articles', component: ArticleList },
        {
          path: 'articles/create',
          component: ArticleForm,
        },
        { path: 'articles/edit/:id', component: ArticleForm, props: true },
        { path: 'productmanager', component: ProductManager },
        { path: 'aboutusmanager', component: AboutUsManager },
        { path: 'bannermanager', component: FeatureSectionManager },
        { path: 'categorymanager', component: CategoryManager },
        { path: 'userslist', component: UserList },
        { path: 'orderList', component: AdminOrders },
        { path: 'comments', component: CommetsManager },
        { path: 'transactions', component: AdminTransactions, meta: { requiresAdmin: true } },
        { path: 'dashboard', component: AdminDashboard},
      ],
    },
  ],
})

router.beforeEach((to) => {
  const loginStore = useLoginStore()
  if (!loginStore.token) {
    loginStore.loadFromCookies()
  }

  const isAuthenticated = loginStore.isAuthenticated
  const isAdmin = loginStore.isAdmin

  if (to.path.startsWith('/admin') && !isAuthenticated) {
    return { name: 'Login' }
  }

  if (to.path.startsWith('/user') && !isAuthenticated) {
    return { name: 'Login' }
  }

  if (to.path.startsWith('/admin') && isAuthenticated && !isAdmin) {
    return { name: 'MainPage' }
  }

  if (isAuthenticated && to.name === 'Login') {
    return { name: 'MainPage' }
  }
})

export default router
