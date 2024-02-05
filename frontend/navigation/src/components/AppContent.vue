<template>
  <div class="app-content">
    <div v-for="category in categories" :key="category.id" class="category">
      <p :id="category.name" class="category-name">{{ category.name }}</p>
      <div class="card-container">
        <div v-for="link in category.links" :key="link.url" class="card">
          <WebsiteCard :link="link" />
        </div>
      </div>
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
  flex-grow: 1;
  margin-left: 56px; /* 距离左部56px */
  /* 其他样式 */
}

.category {
  margin-bottom:40px ;
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
  /** 文本1 */
  font-size: 16px;
  font-weight: 400;
  letter-spacing: 0px;
  line-height: 21.95px;
  color: rgba(0, 0, 0, 1);
  text-align: left;
  vertical-align: top;
}
</style>
