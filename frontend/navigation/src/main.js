import { createApp } from 'vue';
import App from './App.vue';
import '@/assets/css/main.css';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faPaperPlane, faSun } from '@fortawesome/free-regular-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';


library.add(faSun, faPaperPlane); // 添加图标到库

const app = createApp(App);

// 注册Font Awesome组件
app.component('font-awesome-icon', FontAwesomeIcon);

// 在Vue 3中，config.productionTip在控制台中不再禁止显示生产模式提示
// 如果你需要控制提示信息，你需要使用其他方式来配置

app.mount('#app');
