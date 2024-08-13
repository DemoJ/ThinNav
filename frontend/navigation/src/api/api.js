import axios from "axios";

// 创建 Axios 实例
const apiClient = axios.create({
  baseURL: "/api", // 使用代理的路径前缀
  headers: {
    "Content-Type": "application/json",
  },
});

// 获取所有网址信息
export const getWebsites = async () => {
  try {
    const response = await apiClient.get("/websites/?all_data=true");
    // 确保响应格式符合预期
    if (response.data && response.data.data) {
      return response.data; // 返回完整的响应数据
    } else {
      throw new Error('Invalid data format from /websites/ endpoint');
    }
  } catch (error) {
    console.error("Failed to fetch websites:", error);
    throw error; // 抛出错误以便在调用处处理
  }
};

// 获取分类信息
export const getCategories = async () => {
  try {
    const response = await apiClient.get("/categories/");
    // 确保响应格式符合预期
    if (Array.isArray(response.data)) {
      return response.data; // 返回分类数据数组
    } else {
      throw new Error('Invalid data format from /categories/ endpoint');
    }
  } catch (error) {
    console.error("Failed to fetch categories:", error);
    throw error; // 抛出错误以便在调用处处理
  }
};
