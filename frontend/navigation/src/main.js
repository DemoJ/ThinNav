import { createApp } from "vue";
import App from "./App.vue";
import "@/assets/css/main.css";
import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import axios from "axios";

// 创建 Axios 实例
const apiClient = axios.create({
  baseURL: "/api", // 设置后端的 baseURL
  headers: {
    "Content-Type": "application/json",
  },
});

// 动态加载图标
async function loadIcon(iconName) {
  try {
    const { [iconName]: icon } = await import(
      `@fortawesome/free-regular-svg-icons`
    );
    if (icon) {
      library.add(icon);
    } else {
      console.warn(`Icon ${iconName} not found`);
    }
  } catch (error) {
    console.error(`Failed to load icon ${iconName}:`, error);
  }
}

async function initializeApp() {
  try {
    const response = await apiClient.get("/categories/");
    const categories = response.data; // 获取 JSON 数据

    const iconNames = [
      ...new Set(
        categories.map((category) => category.icon_url).filter(Boolean)
      ),
    ];

    for (const iconName of iconNames) {
      await loadIcon(
        `fa${iconName.charAt(0).toUpperCase() + iconName.slice(1)}`
      );
    }

    const app = createApp(App);
    app.component("font-awesome-icon", FontAwesomeIcon);
    app.mount("#app");
  } catch (error) {
    console.error("Error initializing app:", error);
  }
}

// 初始化应用
initializeApp();
