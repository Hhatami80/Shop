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
    {
      path: '/categories/:id',
      name: 'CategoryDetail',
      component: () => import('@/views/CategoryDetail.vue'),
      props: true,
    },
    {
      path: '/product/:id',
      name: 'ProductDetail',
      component:ProductDetailPage,
    },

    { path: '/user', name: 'user', component: UserPanel },

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

//   if (to.path.startsWith('/admin') && isAuthenticated && !isAdmin) {
//     return { name: 'MainPage' }
//   }

//   if (isAuthenticated && to.name === 'Login') {
//     return { name: 'MainPage' }
//   }
// })

export default router
