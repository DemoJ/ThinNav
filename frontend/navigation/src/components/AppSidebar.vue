<template>
  <div class="AppSidebar" ref="sidebar">
    <ul>
      <li v-for="category in categories" :key="category.id" 
          class="nav-item"
          @click="navigateTo(category.name, $event)">
        <i :class="`fas fa-${category.icon_url}`" class="icon"></i>
        <span class="text-body-sm font-medium">{{ category.name }}</span>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'AppSidebar',
  props: {
    categories: Array
  },
  data() {
    return {
      bottomGap: 20, // 距离底部的固定距离
    }
  },
  mounted() {
    this.adjustSidebarHeight();
    window.addEventListener('resize', this.adjustSidebarHeight);
    window.addEventListener('scroll', this.adjustSidebarHeight);
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.adjustSidebarHeight);
    window.removeEventListener('scroll', this.adjustSidebarHeight);
  },
  methods: {
    adjustSidebarHeight() {
      const sidebar = this.$refs.sidebar;
      const windowHeight = window.innerHeight;
      const sidebarRect = sidebar.getBoundingClientRect();
      
      let newHeight = windowHeight - sidebarRect.top - this.bottomGap;

      // 确保 sidebar 高度不会小于最小值
      const minHeight = 100; // 设置一个最小高度值
      newHeight = Math.max(newHeight, minHeight);

      sidebar.style.height = `${newHeight}px`;
    },
    createRippleEffect(event) {
      // 创建波纹元素
      const ripple = document.createElement('span');
      ripple.classList.add('ripple');
      
      // 获取点击位置
      const rect = event.currentTarget.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;
      
      // 设置波纹位置和大小
      ripple.style.left = `${x}px`;
      ripple.style.top = `${y}px`;
      
      // 添加波纹到元素中
      event.currentTarget.appendChild(ripple);
      
      // 动画结束后移除波纹元素
      setTimeout(() => {
        ripple.remove();
      }, 600); // 与CSS动画时长匹配
    },
    navigateTo(categoryName, event) {
      // 创建波纹效果
      this.createRippleEffect(event);
      
      // 导航到对应的锚点
      window.location.hash = categoryName;
    }
  }
};
</script>

<!-- TODO sidebar始终居中显示 -->
<style scoped>
.AppSidebar {
  width: 100%;
  max-width: 200px;
  min-width: 125px;
  height: auto; /* 移除固定高度 */
  max-height: none; /* 移除最大高度限制，因为我们会动态计算 */
  background-color: white;
  border-radius: 8px;
  box-shadow: 0px 4px 4px rgba(240, 244, 249, 0.1);
  position: sticky;
  top: 20px; /* 设置当 sidebar 距离屏幕顶部 20px 时开始悬浮 */
  overflow-y: auto; /* 显示垂直滚动条 */
  overflow-x: hidden; /* 隐藏水平滚动条（如果不需要的话） */
  scrollbar-width: thin; /* Firefox */
  scrollbar-color: rgba(148, 148, 148, 0.1) transparent; /* Firefox 初始状态 */
  margin-bottom: 20px; /* 添加底部边距 */
}

/* 对 Webkit 浏览器（如 Chrome、Safari）的自定义滚动条 */
.AppSidebar::-webkit-scrollbar {
  width: 8px; /* 滚动条的宽度 */
}

.AppSidebar::-webkit-scrollbar-track {
  background: transparent; /* 轨道的背景色 */
}

.AppSidebar::-webkit-scrollbar-thumb {
  background: rgba(148, 148, 148, 0.1); /* 更透明的滚动条颜色 */
  border-radius: 8px; /* 滚动条的圆角 */
  transition: background 0.3s ease; /* 平滑过渡效果 */
}

.AppSidebar:hover::-webkit-scrollbar {
  opacity: 1; /* 鼠标悬停时显示滚动条 */
}

.AppSidebar:hover::-webkit-scrollbar-thumb {
  background: rgba(148, 148, 148, 0.1); /* 鼠标悬停时更明显的滚动条颜色 */
}

/* Firefox 滚动条颜色 */
.AppSidebar:hover {
  scrollbar-color: rgba(148, 148, 148, 0.1) transparent; /* 鼠标悬停时滚动条颜色 */
}

.AppSidebar {
  overflow: hidden; /* 初始隐藏滚动条 */
}

.AppSidebar:hover {
  overflow-y: auto; /* 鼠标悬停时显示滚动条 */
}

.AppSidebar ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.AppSidebar li {
  display: flex;
  align-items: center;
  height: 32px;
  line-height: 32px;
  padding: 4px 0 4px 16px;
  margin-top: 12px;
  position: relative;
  overflow: hidden; /* 为波纹效果添加溢出隐藏 */
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 100%; /* 确保整行都可点击 */
}

/* 导航项悬停效果 */
.AppSidebar li.nav-item:hover {
  background-color: rgba(0, 0, 0, 0.05);
  border-radius: 4px;
}

/* 波纹效果 */
.ripple {
  position: absolute;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  transform: scale(0);
  animation: ripple 0.6s linear;
  pointer-events: none; /* 确保波纹不会干扰点击事件 */
}

@keyframes ripple {
  to {
    transform: scale(4);
    opacity: 0;
  }
}

.AppSidebar .icon {
  font-size: 16px;
  width: 16px;
  height: 16px;
  margin-right: 12px;
  object-fit: contain;
}

.AppSidebar span {
  text-decoration: none;
  color: var(--text-color-primary);
  cursor: pointer;
  letter-spacing: var(--letter-spacing-normal);
  transition: color 0.2s ease;
}

.AppSidebar li:hover span {
  color: var(--text-color-secondary);
}
</style>
