<template>
  <div class="website-card zoom-in" @click="navigateToUrl(link.url)" @mouseover="showTooltip" @mouseleave="hideTooltip" ref="card">
    <div class="website-icon">
      <img :src="link.icon_url" alt="icon" />
    </div>
    <div class="website-info">
      <p class="website-name text-body">{{ link.name }}</p>
      <p class="website-description text-body-sm">{{ link.description }}</p>
    </div>
    <teleport to="body">
      <div v-if="tooltipVisible" class="tooltip text-body-sm" :style="tooltipStyle">
        {{ link.description }}
        <div class="tooltip-arrow" :style="tooltipArrowStyle"></div>
      </div>
    </teleport>
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
      tooltipVisible: false,
      tooltipStyle: {},
      tooltipArrowStyle: {}
    };
  },
  methods: {
    navigateToUrl(url) {
      window.open(url, '_blank');
    },
    showTooltip() {
      this.tooltipVisible = true;
      this.$nextTick(() => {
        this.updateTooltipPosition();
      });
    },
    hideTooltip() {
      this.tooltipVisible = false;
    },
    updateTooltipPosition() {
      const cardRect = this.$refs.card.getBoundingClientRect();
      const tooltipHeight = 60; // 提示框的高度，您可以根据实际高度调整
      const spaceBelow = window.innerHeight - cardRect.bottom;
      
      // 计算绝对位置（相对于视口）
      const absoluteLeft = cardRect.left + cardRect.width / 2;
      
      if (spaceBelow < tooltipHeight) {
        // 当底部空间不足时，将提示框放在卡片上方
        this.tooltipStyle = {
          position: 'fixed',
          top: `${cardRect.top - tooltipHeight - 10}px`,
          left: `${absoluteLeft}px`,
          transform: 'translateX(-50%)',
          zIndex: '9999'
        };
        this.tooltipArrowStyle = {
          position: 'absolute',
          top: '100%',
          left: '50%',
          transform: 'translateX(-50%)',
          borderWidth: '5px 5px 0 5px',
          borderColor: 'rgba(0, 0, 0, 0.8) transparent transparent transparent',
        };
      } else {
        // 当底部空间足够时，将提示框放在卡片下方
        this.tooltipStyle = {
          position: 'fixed',
          top: `${cardRect.bottom + 10}px`,
          left: `${absoluteLeft}px`,
          transform: 'translateX(-50%)',
          zIndex: '9999'
        };
        this.tooltipArrowStyle = {
          position: 'absolute',
          bottom: '100%',
          left: '50%',
          transform: 'translateX(-50%)',
          borderWidth: '0 5px 5px 5px',
          borderColor: 'transparent transparent rgba(0, 0, 0, 0.8) transparent',
        };
      }
    }
  }
};
</script>

<style scoped>
.website-card {
  width: 300px; /* 卡片宽度 */
  height: 110px; /* 卡片高度 */
  opacity: 0; /* 初始状态为不可见 */
  border-radius: 8px;
  background: rgba(255, 255, 255, 1);
  box-shadow: 0px 4px 4px rgba(240, 244, 249, 0.1);
  display: flex;
  cursor: pointer; /* 当鼠标悬停时显示手指图标 */
  position: relative; /* 为了定位提示框 */
  animation-fill-mode: forwards; /* 保持动画结束后的状态 */
  transition: transform 0.3s ease, box-shadow 0.3s ease; /* 添加过渡效果 */
}

.website-card:hover {
  transform: translateY(-3px); /* 悬停时轻微上浮 */
  box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.1); /* 增强阴影效果 */
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
  padding-right: 20px;
}

.website-name {
  margin: 0 0 6px 0; /* 移除默认的外边距，保留底部间距 */
  color: var(--text-color-primary);
}

.website-description {
  margin: 0; /* 移除默认的外边距 */
  color: var(--text-color-secondary);
  display: -webkit-box; /* 使用弹性盒布局 */
  -webkit-box-orient: vertical; /* 垂直方向布局 */
  -webkit-line-clamp: 2; /* 限制显示两行 */
  overflow: hidden; /* 超出部分隐藏 */
  text-overflow: ellipsis; /* 超出部分用省略号代替 */
  max-height: 3em; /* 两行文字的高度 */
  line-height: var(--line-height-normal);
}
</style>

<style>
/* 全局样式，确保tooltip在任何地方都能正确显示 */
.tooltip {
  position: fixed;
  background-color: rgba(0, 0, 0, 0.8);
  color: rgba(255, 255, 255, 0.9);
  padding: 8px 12px;
  border-radius: 4px;
  width: 200px;
  max-width: 200px;
  white-space: normal;
  word-break: break-word;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
  opacity: 1;
  z-index: 9999;
  pointer-events: none;
  line-height: var(--line-height-normal);
}

.tooltip-arrow {
  width: 0;
  height: 0;
  border-style: solid;
}
</style>
