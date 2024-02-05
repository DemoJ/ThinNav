<template>
  <div class="website-card" @click="navigateToUrl(link.url)">
    <div class="website-icon">
      <img :src="link.icon" alt="icon" />
    </div>
    <div class="website-info">
      <p class="website-name">{{ link.name }}</p>
      <p class="website-description">{{ link.description }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'WebsiteCard',
  props: {
    link: Object
  },
  methods: {
    navigateToUrl(url) {
      window.open(url, '_blank');
    }
  }
};
</script>

<style scoped>
.website-card {
  width: 300px; /* 卡片宽度 */
  height: 110px; /* 卡片高度 */
  opacity: 1;
  border-radius: 8px;
  background: rgba(255, 255, 255, 1);
  box-shadow: 0px 4px 4px  rgba(240, 244, 249, 0.1);
  display: flex;
  cursor: pointer; /* 当鼠标悬停时显示手指图标 */
}

.website-icon {
  padding: 20px; /* 内边距 */
}

.website-icon img {
  width: 40px; /* 图标宽度 */
  height: 40px; /* 图标高度 */
  object-fit: contain; /* 保持图标的比例 */
}

.website-info {
  display: flex;
  flex-direction: column; /* 使名称和描述垂直排列 */
  padding-top: 20px;
  padding-bottom: 20px;
}

.website-name {
  margin: 0; /* 移除默认的外边距 */
  font-size: 16px; /* 名称文字大小 */
  padding-bottom: 6px;
}

.website-description{
  margin: 0; /* 移除默认的外边距 */
  font-size: 12px; /* 描述文字大小 */
  color: rgba(153, 153, 153, 1);
}
</style>
