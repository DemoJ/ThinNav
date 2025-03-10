<template>
  <div class="app-content">
    <div class="content-wrapper">
      <div v-for="(category, index) in categories" 
           :key="category.id" 
           class="category fade-in" 
           :style="{ animationDelay: `${0.3 + index * 0.1}s` }">
        <p :id="category.name" class="category-name text-h3">{{ category.name }}</p>
        <div class="card-container staggered-container">
          <div
            v-for="website in category.websites"
            :key="website.id"
            class="card"
          >
            <WebsiteCard :link="website" />
          </div>
        </div>
      </div>
    </div>
    <div class="footer fade-in" style="animation-delay: 0.8s;">
      <a
        href="https://github.com/DemoJ/ThinNav"
        target="_blank"
        class="footer-link text-caption"
      >
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
  flex-direction: column;
  width: 100%; /* 确保容器占满宽度 */
  margin-left: 56px; /* 距离左部56px */
  min-height: calc(100vh - 213px); /* 计算最小高度，减去header-image的高度 */
}

.content-wrapper {
  flex-grow: 1; /* 占据剩余的垂直空间，确保footer在底部 */
}

.category {
  margin-bottom: 40px;
  opacity: 0; /* 初始状态为不可见 */
  animation-fill-mode: forwards; /* 保持动画结束后的状态 */
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
  margin-top: 0;
  margin-bottom: 16px;
  color: var(--text-color-primary);
}

/* 版权信息样式 */
.footer {
  text-align: center;
  margin-top: 20px;
  padding: 10px 0;
  width: 100%;
  flex-shrink: 0;
  /* 设置最小高度，确保 footer 在内容为空时仍然可见 */
  min-height: 40px;
  /* 可选：确保 footer 有垂直空间，即使内容为空 */
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0; /* 初始状态为不可见 */
  animation-fill-mode: forwards; /* 保持动画结束后的状态 */
}

.footer-link {
  color: var(--text-color-tertiary); /* 设置字体颜色 */
  text-decoration: none; /* 去除下划线 */
  display: flex;
  align-items: center; /* 垂直居中对齐图标和文本 */
  justify-content: center; /* 水平居中对齐图标和文本 */
  transition: color 0.2s ease;
}

.footer-link i {
  margin-right: 8px; /* 图标与文本之间的间距 */
  font-size: 16px; /* 图标大小 */
}

.footer-link:hover {
  color: var(--text-color-secondary); /* 鼠标悬停时的字体颜色 */
}
</style>
