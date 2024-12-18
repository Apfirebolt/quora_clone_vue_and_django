import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import NotFound from '../views/NotFound.vue'

const authGuard = (to, from, next) => {
    if (localStorage.getItem('user')) {
        next()
    } else {
        next('/login')
    }
}

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('../views/Login.vue')
    },
    {
        path: '/register',
        name: 'Register',
        component: () => import('../views/Register.vue')
    },
    {
        path: '/profile',
        name: 'Profile',
        beforeEnter: authGuard,
        component: () => import('../views/Profile.vue')
    },
    {
        path: '/dashboard',
        name: 'Dashboard',
        beforeEnter: authGuard,
        component: () => import('../views/Dashboard.vue')
    },
    {
        path: '/my-questions',
        name: 'MyQuestions',
        beforeEnter: authGuard,
        component: () => import('../views/MyQuestions.vue')
    },
    {
        path: '/questions/:slug',
        name: 'QuestionDetail',
        beforeEnter: authGuard,
        component: () => import('../views/QuestionDetail.vue')
    },
    {
        path: '/users',
        name: 'Users',
        beforeEnter: authGuard,
        component: () => import('../views/Users.vue')
    },
    {
        path: '/server-error',
        name: 'ServerError',
        component: () => import('../views/ServerError.vue')
    },
    {
        path: '/:catchAll(.*)',
        name: 'NotFound',
        component: NotFound
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})


export default router