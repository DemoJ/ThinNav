<template>
  <div class="website-card" @click="navigateToUrl(link.url)" @mouseover="showTooltip" @mouseleave="hideTooltip">
    <div class="website-icon">
      <img :src="link.icon_url" alt="icon" />
    </div>
    <div class="website-info">
      <p class="website-name">{{ link.name }}</p>
      <p class="website-description">{{ link.description }}</p>
    </div>
    <div v-if="tooltipVisible" class="tooltip">
      {{ link.description }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'WebsiteCard',
  props: {
    link: Object
  },
  data() {
    return {
      tooltipVisible: false
    };
  },
  methods: {
    navigateToUrl(url) {
      window.open(url, '_blank');
    },
    showTooltip() {
      this.tooltipVisible = true;
    },
    hideTooltip() {
      this.tooltipVisible = false;
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
  box-shadow: 0px 4px 4px rgba(240, 244, 249, 0.1);
  display: flex;
  cursor: pointer; /* 当鼠标悬停时显示手指图标 */
  position: relative; /* 为了定位提示框 */
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

.website-description {
  margin: 0; /* 移除默认的外边距 */
  font-size: 12px; /* 描述文字大小 */
  color: rgba(153, 153, 153, 1);
  display: -webkit-box; /* 使用弹性盒布局 */
  -webkit-box-orient: vertical; /* 垂直方向布局 */
  -webkit-line-clamp: 2; /* 限制显示两行 */
  overflow: hidden; /* 超出部分隐藏 */
  text-overflow: ellipsis; /* 超出部分用省略号代替 */
  max-height: 3em; /* 两行文字的高度 */
  padding-right: 44px; /* 添加右侧内边距 */
}

.tooltip {
  position: absolute; /* 定位提示框 */
  bottom: -60px; /* 距离卡片底部 */
  left: 50%; /* 居中对齐 */
  transform: translateX(-50%); /* 居中对齐 */
  background-color: rgba(0, 0, 0, 0.8); /* 设置背景颜色为半透明黑色 */
  color: rgba(255, 255, 255, 0.9); /* 设置提示文字颜色 */
  padding: 8px;
  border-radius: 4px;
  width: 200px; /* 设置提示框的宽度 */
  max-width: 200px; /* 设置最大宽度 */
  white-space: normal; /* 允许自动换行 */
  word-break: break-word; /* 单词换行 */
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2); /* 添加阴影 */
  font-size: 12px; /* 调整提示文字大小 */
  opacity: 0; /* 初始状态下不可见 */
  transition: opacity 0.3s; /* 平滑过渡 */
  z-index: 1000; /* 确保提示框在最上层 */
}

.tooltip::after {
  content: "";
  position: absolute;
  bottom: 100%; /* 定位到提示框的顶部 */
  left: 50%;
  transform: translateX(-50%);
  border-width: 5px;
  border-style: solid;
  border-color: rgba(0, 0, 0, 0.8) transparent transparent transparent; /* 三角形的颜色 */
}
.website-card:hover .tooltip {
  opacity: 1; /* 鼠标悬停时显示提示框 */
}
</style>
