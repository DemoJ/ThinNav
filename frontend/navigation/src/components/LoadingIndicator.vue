<template>
  <div class="loading-container" :class="{ 'fade-out': !isLoading }">
    <div class="loading-bar">
      <div class="loading-progress" :style="{ width: `${progress}%` }"></div>
    </div>
    <div class="loading-text text-body">{{ loadingText }}</div>
  </div>
</template>

<script>
export default {
  name: 'LoadingIndicator',
  props: {
    isLoading: {
      type: Boolean,
      default: true
    },
    progress: {
      type: Number,
      default: 0
    },
    loadingText: {
      type: String,
      default: '加载中...'
    }
  }
};
</script>

<style scoped>
.loading-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(245, 245, 245, 1);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  transition: opacity 0.5s ease-out;
}

.loading-bar {
  width: 300px;
  height: 4px;
  background-color: rgba(220, 220, 220, 0.8);
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 16px;
}

.loading-progress {
  height: 100%;
  background-color: #4285f4;
  border-radius: 2px;
  transition: width 0.3s ease-in-out;
}

.loading-text {
  color: var(--text-color-secondary);
  letter-spacing: var(--letter-spacing-normal);
}

.fade-out {
  opacity: 0;
  pointer-events: none;
}
</style> 