<template>
  <div class="website-card" @click="navigateToUrl(link.url)" @mouseover="checkTooltip" @mouseleave="hideTooltip">
    <div class="website-icon">
      <img :src="link.icon_url" alt="icon" />
    </div>
    <div class="website-info">
      <p class="website-name">{{ link.name }}</p>
      <p ref="descriptionRef" class="website-description">{{ link.description }}</p>
    </div>
    <div v-if="tooltipVisible" class="tooltip">
      {{ link.description }}
      <div class="tooltip-arrow"></div>
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
    checkTooltip() {
      const el = this.$refs.descriptionRef;
      this.tooltipVisible = el.scrollWidth > el.clientWidth || el.scrollHeight > el.clientHeight;
    },
    hideTooltip() {
      this.tooltipVisible = false;
    }
  }
};
</script>

<style scoped>
.website-card {
  width: 300px;
  height: 110px;
  opacity: 1;
  border-radius: 8px;
  background: rgba(255, 255, 255, 1);
  box-shadow: 0px 4px 4px rgba(240, 244, 249, 0.1);
  display: flex;
  cursor: pointer;
  position: relative;
}

.website-icon {
  padding: 20px;
}

.website-icon img {
  width: 40px;
  height: 40px;
  object-fit: contain;
}

.website-info {
  display: flex;
  flex-direction: column;
  padding-top: 20px;
  padding-bottom: 20px;
}

.website-name {
  margin: 0;
  font-size: 16px;
  padding-bottom: 6px;
}

.website-description {
  margin: 0;
  font-size: 12px;
  color: rgba(153, 153, 153, 1);
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
  text-overflow: ellipsis;
  max-height: 3em;
  padding-right: 44px;
}

.tooltip {
  position: absolute;
  top: 120%;
  /* 确保提示框在卡片下方 */
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.8);
  color: rgba(255, 255, 255, 0.9);
  padding: 8px;
  border-radius: 4px;
  width: 200px;
  max-width: 200px;
  white-space: normal;
  word-break: break-word;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
  font-size: 12px;
  opacity: 0;
  transition: opacity 0.3s;
  z-index: 1000;
}

.tooltip-arrow {
  position: absolute;
  bottom: 100%;
  /* 确保箭头在提示框上方 */
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-bottom: 5px solid rgba(0, 0, 0, 0.8);
  /* 箭头颜色与提示框一致 */
}

.website-card:hover .tooltip {
  opacity: 1;
}
</style>
