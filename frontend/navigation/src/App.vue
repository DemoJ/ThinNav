<template>
  <div id="app">
    <LoadingIndicator 
      :is-loading="isLoading" 
      :progress="loadingProgress" 
      :loading-text="loadingText" 
    />
    <div v-show="!isLoading" class="content-fade-in">
      <div class="header-image fade-in-down"></div>
      <div class="main-container">
        <AppSidebar :categories="categories" class="fade-in-right delay-200" />
        <AppContent :categories="categories" class="fade-in delay-300" />
      </div>
    </div>
  </div>
</template>

<script>
import AppSidebar from "./components/AppSidebar.vue";
import AppContent from "./components/AppContent.vue";
import LoadingIndicator from "./components/LoadingIndicator.vue";
import { getWebsites, getCategories } from "./api/api";

export default {
  name: "App",
  components: {
    AppSidebar,
    AppContent,
    LoadingIndicator
  },
  data() {
    return {
      categories: [],
      websites: [],
      isLoading: true,
      loadingProgress: 0,
      loadingText: '加载中...'
    };
  },
  async created() {
    // 启动加载进度模拟
    this.startLoadingProgress();
    
    try {
      this.loadingText = '正在获取数据...';
      
      const [categoriesResponse, websitesResponse] = await Promise.all([
        getCategories(),
        getWebsites(),
      ]);

      this.loadingProgress = 70;
      this.loadingText = '正在处理数据...';

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
      
      this.loadingProgress = 90;
      this.loadingText = '准备完成...';
      
      // 完成加载
      setTimeout(() => {
        this.loadingProgress = 100;
        setTimeout(() => {
          this.isLoading = false;
        }, 500);
      }, 300);
      
    } catch (error) {
      console.error("Error fetching data:", error);
      this.loadingText = '加载失败，请刷新重试';
      this.loadingProgress = 100;
      setTimeout(() => {
        this.isLoading = false;
      }, 1500);
    }
  },
  methods: {
    startLoadingProgress() {
      let progress = 0;
      const interval = setInterval(() => {
        if (this.loadingProgress >= 90 || !this.isLoading) {
          clearInterval(interval);
          return;
        }
        
        // 模拟进度增加，但不超过70%（留给实际数据加载）
        if (progress < 70) {
          progress += Math.random() * 3;
          this.loadingProgress = Math.min(Math.round(progress), 70);
        }
      }, 200);
    }
  }
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
  font-family: var(--font-family-sans);
  color: var(--text-color-primary);
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

/* 内容淡入效果 */
.content-fade-in {
  opacity: 1;
  transition: opacity 0.5s ease-out;
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
