<script setup lang="ts">
import { reactive } from "vue";
import { changeUserPassword } from "@/api/user";
import { message } from "@/utils/message";

defineOptions({
  // name 作为一种规范最好必须写上并且和路由的name保持一致
  name: "Account"
});

const Infos = reactive({
  oldPassword: "",
  newPassword: "",
  confirmPassword: ""
});

const submitPasswordChange = async () => {
  if (Infos.newPassword !== Infos.confirmPassword) {
    message("新密码和确认新密码不匹配", { type: "error" });
    return;
  }

  const data = {
    old_password: Infos.oldPassword,
    new_password: Infos.newPassword
  };

  try {
    const response = await changeUserPassword(data);
    message("密码更新成功", { type: "success" });
    console.log(response);
  } catch (error) {
    console.error("密码更新失败", error);
    message("密码更新失败，请重试", { type: "error" });
  }
};
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
      <el-button type="primary" @click="submitPasswordChange">
        更新信息
      </el-button>
    </el-form>
  </el-card>
</template>

<style scoped>
.el-form-item {
  width: 40%;
}
</style>
