<template>
  <div class="AppSidebar">
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
  }
};
</script>

<style scoped>
.AppSidebar {
  width: 100%;
  max-width: 200px;
  min-width: 125px;
  height: calc(100vh - 169px);
  background-color: white;
  border-radius: 8px;
  box-shadow: 0px 4px 4px rgba(240, 244, 249, 0.1);
  position: sticky;
  top: 20px; /* 设置当 sidebar 距离屏幕顶部 20px 时开始悬浮 */
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
