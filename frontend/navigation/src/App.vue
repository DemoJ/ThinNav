<template>
  <div id="app">
    <div class="header-image"></div>
    <div class="main-container">
      <!-- 创建一个新的容器包含AppSidebar和content -->
      <AppSidebar :categories="categories" />
      <AppContent :categories="categories" />
    </div>
  </div>
</template>

<script>
import AppSidebar from "./components/AppSidebar.vue";
import AppContent from './components/AppContent.vue';

export default {
  name: "App",
  components: {
    AppSidebar,
    AppContent
  },
  data() {
    return {
      categories: [
        {
          id: 1,
          name: "社交媒体",
          icon: "paper-plane",
          links: [
            { icon:"https://static.xx.fbcdn.net/rsrc.php/yb/r/hLRJ1GG_y0J.ico", name: "Facebook",description: "Facebook 社交平台", url: "https://www.facebook.com" },
            { icon:"https://static.xx.fbcdn.net/rsrc.php/yb/r/hLRJ1GG_y0J.ico", name: "Facebook",description: "Facebook 社交平台", url: "https://www.facebook.com" },
            { icon:"https://static.xx.fbcdn.net/rsrc.php/yb/r/hLRJ1GG_y0J.ico", name: "Facebook",description: "Facebook 社交平台", url: "https://www.facebook.com" },
            { icon:"https://static.xx.fbcdn.net/rsrc.php/yb/r/hLRJ1GG_y0J.ico", name: "Facebook",description: "Facebook 社交平台", url: "https://www.facebook.com" },
            { icon:"https://static.xx.fbcdn.net/rsrc.php/yb/r/hLRJ1GG_y0J.ico", name: "Facebook",description: "Facebook 社交平台", url: "https://www.facebook.com" },
            // 其他社交媒体网站...
          ],
        },
        {
          id: 2,
          name: "搜索引擎",
          icon: "sun",
          links: [
            { icon: "https://www.google.com/images/branding/googleg/1x/googleg_standard_color_128dp.png", name: "Google",description: "Google 搜索引擎", url: "https://www.google.com" },
            // 其他搜索引擎网站...
          ],
        },
        // 其他类别...
      ],
    };
  },
};
</script>

<style>
html, body, #app {
  margin: 0;
  padding: 0;
}

html, body {
  max-width: 100%;
  overflow-x: hidden;
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
