<script setup lang="ts">
import axios from 'axios';
import { reactive } from "vue";

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
    alert('新密码和确认新密码不匹配');
    return;
  }

  // 假设的 getCookie 函数，添加了返回类型注解
  const getCookie = (name: string): string | null => {
    let cookieArray = document.cookie.split('; ');
    for (let cookie of cookieArray) {
      let [cookieName, cookieValue] = cookie.split('=');
      if (cookieName === name) {
        return cookieValue;
      }
    }
    return null;
  };

  let token: string | undefined; // 声明 token 变量可能为 undefined

  try {
    const encodedJson = getCookie('authorized-token'); // 从 cookie 中获取编码的 JSON
    if (encodedJson) {
      const decodedJson = decodeURIComponent(encodedJson); // 解码 URL 编码的字符串
      const tokenData = JSON.parse(decodedJson); // 解析 JSON 字符串
      token = tokenData.accessToken; // 从解析的 JSON 对象中获取 accessToken
    }
  } catch (error) {
    console.error("Error parsing token data:", error);
  }

  if (!token) {
    alert('无法获取访问令牌，请重新登录');
    return;
  }

  try {
    const response = await axios.post('http://localhost:8000/admin/change-password', {
      old_password: Infos.oldPassword,
      new_password: Infos.newPassword,
    }, {
      headers: {
        'Authorization': `Bearer ${token}` // 使用 Bearer 方案添加令牌
      }
    });
    alert("密码更新成功");
  } catch (error) {
    console.error('密码更新失败', error);
    alert('密码更新失败，请重试');
  }
};

</script>

<template>
  <el-card shadow="never">
    <h3 class="my-8">修改管理密码</h3>
    <el-form label-position="top" label-width="80px" :model="Infos">
      <el-form-item label="原密码" prop="oldPassword">
        <el-input v-model="Infos.oldPassword" placeholder="请输入原密码" clearable show-password maxlength="20" />
      </el-form-item>
      <el-form-item label="新密码" prop="newPassword">
        <el-input v-model="Infos.newPassword" placeholder="请输入新密码" clearable show-password maxlength="20" />
      </el-form-item>
      <el-form-item label="确认新密码" prop="confirmPassword">
        <el-input v-model="Infos.confirmPassword" placeholder="请再次输入新密码" clearable show-password maxlength="20" />
      </el-form-item>
      <el-button type="primary" @click="submitPasswordChange"> 更新信息 </el-button>
    </el-form>
  </el-card>
</template>

<style>
.el-form-item {
  width: 40%;
}
</style>
