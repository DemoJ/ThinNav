<template>
  <div class="AppSidebar">
    <ul>
      <li v-for="category in categories" :key="category.id">
        <font-awesome-icon :icon="['far', category.icon]" class="icon" /> <!-- 图标 -->
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
  }
};
</script>

<style scoped>
.AppSidebar {
  width: 200px;
  min-width: 125px; /* 或其他适当的最小宽度 */
  height: calc(100vh - 169px); /* 高度占满屏幕 */
  background-color: white; /* 背景颜色 */
  border-radius: 8px;
  box-shadow: 0px 4px 4px  rgba(240, 244, 249, 0.1);
  /* 其他样式 */
}

.AppSidebar ul {
  list-style-type: none; /* 移除默认的列表样式 */
  padding: 0; /* 移除默认的padding */
  margin: 0; /* 移除默认的margin */
}

.AppSidebar li {
  display: flex; /* 使图标和文本在一行显示 */
  align-items: center; /* 垂直居中 */
  height: 32px; /* 每一行的高度设置为32px */
  line-height: 32px;
  padding: 4px 0 4px 16px;
  margin-top: 12px;
  /* 可以添加 hover 效果等 */
}

.AppSidebar .icon {
  font-size: 16px;
  width: 16px;
  height: 16px;
  margin-right: 12px; /* 右侧文本的间距为10px */
  object-fit: contain;
}

.AppSidebar a {
  font-size: 14px; /* 文本大小设置为14px */
  text-decoration: none; /* 移除下划线 */
  color: rgba(0, 0, 0, 1); /* 继承父元素的文本颜色 */
  cursor: pointer; /* 鼠标悬停时显示手指图标 */
  /* 可以添加其他文本样式，如颜色、字体等 */
}

.AppSidebar a:visited {
  color: inherit; /* 保持访问过的链接颜色不变 */
}

/* 其他样式 */
</style>
