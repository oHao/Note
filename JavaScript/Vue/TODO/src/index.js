import Vue from 'vue'
import App from './app.vue'
import './assets/images/bg.jpg'
import './assets/styles/test.css'
import './assets/styles/test.styl'
const root = document.createElement('div')
document.body.appendChild(root)
console.log("app.vue.....")
new Vue({
    render: (h) => h(App)
}).$mount(root);