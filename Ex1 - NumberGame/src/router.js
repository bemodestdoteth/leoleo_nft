import Vue from 'vue'
import Router from 'vue-router'
import GameBapp from '@/components/game-bapp'
Vue.use(Router)

export default new Router({
 routes: [
  {
   path: '/',
   name: 'game-bapp',
   component: GameBapp
  }
 ]
})
