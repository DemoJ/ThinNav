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
import AppContent from './components/AppContent.vue';
import { getWebsites, getCategories } from './api/api';

export default {
  name: "App",
  components: {
    AppSidebar,
    AppContent
  },
  data() {
    return {
      categories: [],
      websites: []
    };
  },
  async created() {
    try {
      const [categoriesResponse, websitesResponse] = await Promise.all([
        getCategories(),
        getWebsites()
      ]);

      // 确保从响应数据中提取正确的数据
      const categories = categoriesResponse; // 从 getCategories 中直接获取数据
      const websites = websitesResponse.data; // 从 getWebsites 中提取 data 字段
      console.log(websites);


      // 确保 websites 是数组
      if (!Array.isArray(websites)) {
        throw new Error('Websites data is not an array');
      }

      // 对分类和网址进行排序并组合
      this.categories = categories.map(category => ({
        ...category,
        websites: websites
          .filter(website => website.category_id === category.id)
          .sort((a, b) => a.order - b.order) // 按网址 order 排序
      })).sort((a, b) => a.order - b.order); // 按分类 order 排序
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  }
};
</script>

<style>
html, body, #app {
  margin: 0;
  padding: 0;
}

html, body {
  max-width: 100%;
}

#app {
  font-family: 'moe','Microsoft YaHei',Arimo,Arial,Helvetica,sans-serif;
}

/* 设置整体背景颜色 */
body {
  background-color: rgba(245, 245, 245, 1);
}

.main-container {
  display: flex;
  margin-top: 20px; /* 距离上部图片20px */
  margin-left: 20px; /* 距离左部20px */
  margin-right: 20px;/* 距离右部20px */
  margin-bottom: 20px;/* 距离底部20px */
}

html {
  scroll-behavior: smooth;
}

.header-image {
  width: calc(100% - 40px); /* 减去左右的间距总和 */
  height: 113px; /* 图片高度 */
  margin-top: 16px; /* 上间距固定16px */
  margin-left: auto; /* 左间距，auto 会居中对齐 */
  margin-right: auto; /* 右间距，auto 会居中对齐 */
  background-image: url("@/assets/header.png"); /* 图片路径 */
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  border-radius:8px;
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
