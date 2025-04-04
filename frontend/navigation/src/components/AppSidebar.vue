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
    <!-- 添加底部填充元素，确保有20px的空间 -->
    <div class="sidebar-bottom-spacer"></div>
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
    // 立即设置初始高度
    this.adjustSidebarHeight();
    
    // 确保在DOM更新后调整高度
    this.$nextTick(this.adjustSidebarHeight);
    
    // 保留一个短延迟，确保样式已完全应用
    setTimeout(this.adjustSidebarHeight, 0);
    
    // 监听window事件
    window.addEventListener('resize', this.adjustSidebarHeight);
    window.addEventListener('scroll', this.adjustSidebarHeight);
    window.addEventListener('load', this.adjustSidebarHeight);
    
    // 创建MutationObserver监听DOM变化
    if (window.MutationObserver) {
      this.observer = new MutationObserver(this.adjustSidebarHeight);
      this.observer.observe(document.body, { 
        childList: true, 
        subtree: true 
      });
    }
    
    // 强制在加载完成延迟后再次调整（确保所有资源加载完成）
    window.setTimeout(this.adjustSidebarHeight, 1000);
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.adjustSidebarHeight);
    window.removeEventListener('scroll', this.adjustSidebarHeight);
    window.removeEventListener('load', this.adjustSidebarHeight);
    
    // 清理MutationObserver
    if (this.observer) {
      this.observer.disconnect();
    }
  },
  watch: {
    categories: {
      handler() {
        // 当分类数据变化时，重新计算sidebar高度
        this.$nextTick(() => {
          this.adjustSidebarHeight();
        });
      },
      deep: true
    }
  },
  methods: {
    adjustSidebarHeight() {
      const sidebar = this.$refs.sidebar;
      if (!sidebar) return;
      
      // 计算可用窗口高度
      const windowHeight = window.innerHeight;
      
      // 获取sidebar当前的顶部位置
      const sidebarTop = sidebar.getBoundingClientRect().top;
      
      // 计算sidebar的最大高度：窗口高度 - 顶部位置 - 底部间距
      const maxHeight = windowHeight - sidebarTop - this.bottomGap;
      
      // 设置最大高度（不再动态设置height属性）
      sidebar.style.maxHeight = `${Math.max(maxHeight, 100)}px`;
      
      // 移除不必要的样式设置，依赖CSS中的margin-bottom
      if (sidebar.style.marginBottom !== `${this.bottomGap}px`) {
        sidebar.style.marginBottom = `${this.bottomGap}px`;
      }
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
      
      // 查找目标元素
      const targetElement = document.getElementById(categoryName);
      if (targetElement) {
        // 使用 scrollIntoView 进行平滑滚动
        targetElement.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
        
        // 更新 URL，但不触发默认的滚动行为
        history.pushState(null, '', `#${categoryName}`);
      }
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
  background-color: white;
  border-radius: 8px;
  box-shadow: 0px 4px 4px rgba(240, 244, 249, 0.1);
  position: sticky;
  top: 20px; /* 顶部固定距离 */
  margin-bottom: 20px; /* 保持底部边距 */
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: thin;
  scrollbar-color: rgba(148, 148, 148, 0.1) transparent;
  display: flex;
  flex-direction: column;
  
  /* 高度调整 */
  height: auto;
  max-height: calc(100vh - 40px); /* 视口高度减去顶部和底部边距 */
}

/* 添加底部填充元素样式 */
.sidebar-bottom-spacer {
  height: 20px;
  min-height: 20px;
  width: 100%;
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
