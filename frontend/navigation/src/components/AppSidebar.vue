<template>
  <div class="AppSidebar" ref="sidebar">
    <ul>
      <li v-for="category in categories" :key="category.id">
        <i :class="`fas fa-${category.icon_url}`" class="icon"></i>
        <a :href="'#' + category.name">{{ category.name }}</a>
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
}

.AppSidebar .icon {
  font-size: 16px;
  width: 16px;
  height: 16px;
  margin-right: 12px;
  object-fit: contain;
}

.AppSidebar a {
  font-size: 14px;
  text-decoration: none;
  color: rgba(0, 0, 0, 1);
  cursor: pointer;
}

.AppSidebar a:visited {
  color: inherit;
}
</style>
