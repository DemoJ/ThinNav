<script setup lang="ts">
defineOptions({
  // name 作为一种规范最好必须写上并且和路由的name保持一致
  name: "Account"
});

import { reactive } from "vue";

const Infos = reactive({
  oldPassword: "",
  newPassword: "",
  confirmPassword: ""
});
</script>

<template>
  <el-card shadow="never">
    <h3 class="my-8">修改管理密码</h3>
    <el-form label-position="top" label-width="80px" :model="Infos">
      <el-form-item label="原密码" prop="oldPassword">
        <el-input
          v-model="Infos.oldPassword"
          placeholder="请输入原密码"
          clearable
          show-password
          maxlength="20"
        />
      </el-form-item>
      <el-form-item label="新密码" prop="newPassword">
        <el-input
          v-model="Infos.newPassword"
          placeholder="请输入新密码"
          clearable
          show-password
          maxlength="20"
        />
      </el-form-item>
      <el-form-item label="确认新密码" prop="confirmPassword">
        <el-input
          v-model="Infos.confirmPassword"
          placeholder="请再次输入新密码"
          clearable
          show-password
          maxlength="20"
        />
      </el-form-item>
      <el-button type="primary"> 更新信息 </el-button>
    </el-form>
  </el-card>
</template>

<style>
.el-form-item {
  width: 40%;
}
</style>
