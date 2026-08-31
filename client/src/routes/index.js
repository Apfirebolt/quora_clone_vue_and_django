import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import NotFound from '../views/NotFound.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('../views/Login.vue'),
        meta: { guestOnly: true },
    },
    {
        path: '/register',
        name: 'Register',
        component: () => import('../views/Register.vue'),
        meta: { guestOnly: true },
    },
    {
        path: '/profile',
        name: 'Profile',
        component: () => import('../views/Profile.vue'),
        meta: { requiresAuth: true },
    },
    {
        path: '/dashboard',
        name: 'Dashboard',
        component: () => import('../views/Dashboard.vue'),
        meta: { requiresAuth: true },
    },
    {
        path: '/my-questions',
        name: 'MyQuestions',
        component: () => import('../views/MyQuestions.vue'),
        meta: { requiresAuth: true },
    },
    {
        path: '/my-answers',
        name: 'MyAnswers',
        component: () => import('../views/MyAnswers.vue'),
        meta: { requiresAuth: true },
    },
    {
        path: '/questions/:slug',
        name: 'QuestionDetail',
        component: () => import('../views/QuestionDetail.vue'),
        meta: { requiresAuth: true },
    },
    {
        path: '/users',
        name: 'Users',
        component: () => import('../views/Users.vue'),
        meta: { requiresAuth: true },
    },
    {
        path: '/users/:username',
        name: 'UserDetail',
        component: () => import('../views/UserDetail.vue'),
        meta: { requiresAuth: true },
    },
    {
        path: '/server-error',
        name: 'ServerError',
        component: () => import('../views/ServerError.vue'),
    },
    {
        path: '/:catchAll(.*)*',
        name: 'NotFound',
        component: NotFound,
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior(to, from, savedPosition) {
        if (savedPosition) {
            return savedPosition
        }
        return { top: 0 }
    },
})

// Centralized Global Navigation Guard
router.beforeEach((to) => {
    const isAuthenticated = Boolean(localStorage.getItem('user'))

    // Protected routes: redirect unauthenticated users to login with redirect query
    if (to.meta.requiresAuth && !isAuthenticated) {
        return {
            name: 'Login',
            query: { redirect: to.fullPath },
        }
    }

    // Guest-only routes: redirect authenticated users to home/dashboard
    if (to.meta.guestOnly && isAuthenticated) {
        return { name: 'Dashboard' }
    }
})

export default router