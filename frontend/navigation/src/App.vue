<template>
  <div id="app">
    <div class="header-image"></div>
    <div class="main-container">
      <AppSidebar :categories="categories" />
      <AppContent :categories="categories" />
    </div>
  </div>
</template>

<script>
import AppSidebar from "./components/AppSidebar.vue";
import AppContent from "./components/AppContent.vue";
import { getWebsites, getCategories } from "./api/api";

export default {
  name: "App",
  components: {
    AppSidebar,
    AppContent,
  },
  data() {
    return {
      categories: [],
      websites: [],
    };
  },
  async created() {
    try {
      const [categoriesResponse, websitesResponse] = await Promise.all([
        getCategories(),
        getWebsites(),
      ]);

      const categories = categoriesResponse; // 从 getCategories 中直接获取数据
      const websites = websitesResponse.data; // 从 getWebsites 中提取 data 字段
      console.log(websites);

      if (!Array.isArray(websites)) {
        throw new Error("Websites data is not an array");
      }

      // 对分类和网址进行排序、过滤和组合
      this.categories = categories
        .map((category) => {
          const filteredWebsites = websites
            .filter((website) => website.category_id === category.id)
            .sort((a, b) => a.order - b.order); // 按网址 order 排序

          // 仅返回包含网址的分类
          return filteredWebsites.length > 0
            ? {
                ...category,
                websites: filteredWebsites,
              }
            : null;
        })
        .filter((category) => category !== null) // 过滤掉没有网址的分类
        .sort((a, b) => a.order - b.order); // 按分类 order 排序
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  },
};
</script>

<style>
html,
body,
#app {
  height: 100%; /* 确保整个页面高度被占用 */
  margin: 0;
  padding: 0;
  width: 100%;
}

html,
body {
  height: 100%;
  margin: 0;
  padding: 0;
}

#app {
  font-family: "moe", "Microsoft YaHei", Arimo, Arial, Helvetica, sans-serif;
}

/* 设置整体背景颜色 */
body {
  background-color: rgba(245, 245, 245, 1);
}

.main-container {
  display: flex;
  flex-direction: row; /* 水平排列Sidebar和Content */
  flex-grow: 1; /* 确保主容器占满空间 */
  margin: 20px; /* 外边距设定 */
}

html {
  scroll-behavior: smooth;
}

.header-image {
  width: calc(100% - 40px); /* 减去左右的间距总和 */
  height: 113px;
  margin-top: 16px;
  margin-left: auto;
  margin-right: auto;
  background-image: url("@/assets/header.png");
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  border-radius: 8px;
}

/* 为了响应式布局，可以添加媒体查询来调整样式 */
@media (max-width: 768px) {
  .header-image {
    width: calc(100% - 40px); /* 可以根据需要调整小屏幕上的宽度 */
    margin-top: 16px;
    margin-left: auto;
    margin-right: auto;
  }
}

/* 其他样式 */
</style>
