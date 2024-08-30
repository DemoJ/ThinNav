<script setup lang="ts">
defineOptions({
  name: "Welcome"
});
</script>

<template>
  <el-card shadow="always" class="welcome-card">
    <h2>欢迎使用 ThinNav</h2>
    <p>
      ThinNav
      是一个简洁轻便的网址导航工具，旨在帮助用户快速访问常用网站，项目代码托管在
      GitHub 上。
    </p>
    <p>
      项目地址：
      <a href="https://github.com/DemoJ/ThinNav" target="_blank"
        >https://github.com/DemoJ/ThinNav</a
      >
    </p>
    <p>如果你有任何问题或建议，请随时提交 Issue。</p>
  </el-card>
</template>

<style scoped>
.welcome-card {
  padding: 20px;
  text-align: left;
  line-height: 1.6;
}

h2 {
  margin-bottom: 10px;
}

a {
  color: #409eff;
}
</style>
