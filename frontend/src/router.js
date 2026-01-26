import {createRouter, createWebHistory} from 'vue-router'
import Home from './pages/Home.vue'
import LaptopInfo from './pages/LaptopInfo.vue'
import Recommend from "./pages/RecommendRam.vue";

const routes = [
    {
        path: '/',
        name: 'home',
        component: Home
    },
    {
        path: '/laptopinfo',
        name: 'laptopinfo',
        component: LaptopInfo
    },
    {
        path: '/recommend',
        name: 'recommend',
        component: Recommend
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
