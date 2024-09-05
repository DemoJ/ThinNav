<template>
  <div class="app-content">
    <div class="content-wrapper">
      <div v-for="category in categories" :key="category.id" class="category">
        <p :id="category.name" class="category-name">{{ category.name }}</p>
        <div class="card-container">
          <div v-for="website in category.websites" :key="website.id" class="card">
            <WebsiteCard :link="website" />
          </div>
        </div>
      </div>
    </div>
    <div class="footer">
      <a href="https://github.com/DemoJ/ThinNav" target="_blank" class="footer-link">
        <i class="fab fa-github"></i> Created by Diyun and ChatGPT
      </a>
    </div>
  </div>
</template>

<script>
import WebsiteCard from "./WebsiteCard.vue";

export default {
  name: "AppContent",
  components: {
    WebsiteCard,
  },
  props: {
    categories: Array,
  },
};
</script>

<style scoped>
.app-content {
  display: flex;
  flex-direction: column; /* 垂直排列内容和版权信息 */
  min-height: calc(100vh - 169px); /* 确保内容区域至少占据视口高度 */
  margin-left: 56px; /* 距离左部56px */
  padding-bottom: 40px; /* 确保底部的版权信息不被内容覆盖 */
}

.content-wrapper {
  flex-grow: 1;
}

.category {
  margin-bottom: 40px;
}

.card-container {
  display: flex; /* 启用flex布局 */
  flex-wrap: wrap; /* 允许卡片换行 */
  justify-content: flex-start; /* 卡片从左侧开始排列 */
  align-items: flex-start; /* 卡片从顶部开始对齐 */
}

.card {
  margin: 10px 20px 10px 0px; /* 卡片之间的间距 */
}

.category-name {
  font-size: 16px;
  font-weight: 400;
  letter-spacing: 0px;
  line-height: 21.95px;
  color: rgba(0, 0, 0, 1);
  text-align: left;
  vertical-align: top;
}

/* 版权信息样式 */
.footer {
  text-align: center; /* 居中显示文本 */
}

.footer-link {
  color: rgba(0, 0, 0, 0.5); /* 设置字体颜色 */
  text-decoration: none; /* 去除下划线 */
  display: flex;
  align-items: center; /* 垂直居中对齐图标和文本 */
  justify-content: center; /* 水平居中对齐图标和文本 */
}

.footer-link i {
  margin-right: 8px; /* 图标与文本之间的间距 */
  font-size: 16px; /* 图标大小 */
}

.footer-link:hover {
  color: rgba(0, 0, 0, 0.8); /* 鼠标悬停时的字体颜色 */
}
</style>
